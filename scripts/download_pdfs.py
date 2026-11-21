#!/usr/bin/env python3
"""Fetch public research PDFs for an ephemeral Actions artifact and validate format.

No paywall bypasses, credentials, cookie copying, or file redistribution to git.
The download_results.csv log reflects THIS RUN only, not Sider availability.
Requires pypdf (installed by the GitHub Actions PDF collection workflow).
"""
import csv
import hashlib
import io
import json
import pathlib
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "pdfs"
PDF_DIR.mkdir(exist_ok=True)
MAX_BYTES = 40_000_000

papers = json.loads((ROOT / "metadata/papers.json").read_text(encoding="utf-8"))


def check_pdf(data):
    if len(data) < 256 or not data.lstrip(b"\xef\xbb\xbf\t\n\r ").startswith(b"%PDF-"):
        raise ValueError("Response does not start with a PDF header")
    if b"%%EOF" not in data[-2048:]:
        raise ValueError("PDF end-of-file marker missing or incomplete")
    reader = PdfReader(io.BytesIO(data), strict=False)
    if reader.is_encrypted:
        raise ValueError("Encrypted PDF, cannot validate")
    pages = len(reader.pages)
    if pages < 1:
        raise ValueError("PDF has zero readable pages")
    return pages


def source_is_pdf_candidate(paper):
    if paper.get("pdf_available_at_source") is False or paper.get("pdf_status") == "not available":
        return False
    u = urlparse(paper["source_url"])
    path = u.path.lower()
    # Source metadata may explicitly identify a direct PDF even at an unusual endpoint.
    return (
        paper.get("pdf_available_at_source") is True
        or path.endswith(".pdf")
        or "/_pdf" in path
        or path.endswith("/download")
        or "/article/download/" in path
        or "/download/file/" in path
    )


with (ROOT / "metadata/download_results.csv").open("w", newline="", encoding="utf-8") as f:
    columns = ["id", "status", "http_status", "bytes", "pages", "sha256", "source_url", "details"]
    writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for paper in papers:
        result = {"id": paper["id"], "source_url": paper["source_url"]}
        destination = PDF_DIR / (paper["id"] + ".pdf")
        try:
            if paper.get("pdf_available_at_source") is False or paper.get("pdf_status") == "not available":
                result.update(status="skipped_no_pdf", details="No public PDF listed at original source")
            elif not source_is_pdf_candidate(paper):
                result.update(status="skipped_unverified_url", details="Link is not a verified direct-PDF endpoint")
            else:
                if destination.exists():
                    data = destination.read_bytes()
                    result["status"] = "already_downloaded_this_run"
                else:
                    req = urllib.request.Request(
                        paper["source_url"],
                        headers={"User-Agent": "AcademicLiteratureIndex/1.0"},
                    )
                    with urllib.request.urlopen(req, timeout=25) as response:
                        result["http_status"] = response.status
                        length = response.headers.get("Content-Length")
                        if length and int(length) > MAX_BYTES:
                            raise ValueError("Source declares file larger than the 40 MB cap")
                        data = response.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    raise ValueError("PDF exceeds 40 MB size cap")
                result["bytes"] = len(data)
                pages = check_pdf(data)
                result["pages"] = pages
                result["sha256"] = hashlib.sha256(data).hexdigest()
                if not destination.exists():
                    destination.write_bytes(data)
                    result["status"] = "downloaded_validated"
                else:
                    result["status"] = "already_downloaded_validated"
                result["details"] = "PDF structure and page count validated; article identity not reviewed"
        except Exception as exc:
            destination.unlink(missing_ok=True)
            result["status"] = "failed"
            result["details"] = f"{type(exc).__name__}: {str(exc)[:200]}"
            if isinstance(exc, urllib.error.HTTPError):
                result["http_status"] = exc.code
        writer.writerow(result)
        f.flush()
        # Respect servers; no circumvention or burst retries after access failures.
        time.sleep(0.25)
print("See metadata/download_results.csv. Downloaded PDF bytes remain in the ephemeral pdfs/ folder.")
