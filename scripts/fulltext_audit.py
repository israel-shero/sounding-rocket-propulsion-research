#!/usr/bin/env python3
"""Audit all source-listed PDFs without publishing copyrighted PDF bytes.

Run on separate GitHub Actions shards, then merge only after EVERY shard reports.
A successful validation proves the fetched response parses as a PDF, not that
its first-page scholarly identity or licensing was manually verified.
"""
import argparse
import collections
import csv
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "metadata" / "papers.json"
OUT = ROOT / "audit-output"
FIELDS = [
    "id", "status", "http_status", "bytes", "pages", "sha256",
    "pdf_internal_title", "source_url", "details",
]
MAX_BYTES = 40_000_000
USER_AGENT = "SoundingRocketResearchBibliography/1.0 (public academic PDF validator)"


def records():
    papers = json.loads(RECORDS.read_text(encoding="utf-8"))
    if not isinstance(papers, list):
        raise ValueError("Expected array in metadata/papers.json")
    return papers


def pdf_candidates(papers):
    return [p for p in papers if p.get("pdf_available_at_source") is True]


def inspect(paper):
    from pypdf import PdfReader

    result = {k: "" for k in FIELDS}
    result.update(id=paper["id"], source_url=paper["source_url"])
    try:
        request = urllib.request.Request(
            paper["source_url"],
            headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*;q=0.8"}
        )
        with urllib.request.urlopen(request, timeout=24) as response:
            result["http_status"] = response.status
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > MAX_BYTES:
                result["status"] = "too_large"
                result["details"] = "Declared Content-Length exceeds 40 MB"
                return result
            data = response.read(MAX_BYTES + 1)
        result["bytes"] = len(data)
        if len(data) > MAX_BYTES:
            result["status"] = "too_large"
            result["details"] = "Response exceeded 40 MB safety limit"
            return result
        if len(data) < 256 or not data.lstrip(b"\xef\xbb\xbf\t\n\r ").startswith(b"%PDF-"):
            result["status"] = "not_pdf"
            result["details"] = "Response does not begin with a PDF header"
            return result
        if b"%%EOF" not in data[-2048:]:
            result["status"] = "truncated_pdf"
            result["details"] = "PDF end-of-file marker not found"
            return result
        try:
            reader = PdfReader(io.BytesIO(data), strict=False)
            if reader.is_encrypted:
                result["status"] = "encrypted_pdf"
                result["details"] = "Cannot validate encrypted document"
                return result
            pages = len(reader.pages)
            if pages < 1:
                raise ValueError("PDF has zero pages")
            reader.pages[0].get_contents()
            title = (reader.metadata.title if reader.metadata else "") or ""
            result["pdf_internal_title"] = " ".join(str(title).split())[:220]
            result["pages"] = pages
        except Exception as exc:
            result["status"] = "parse_failed"
            result["details"] = f"{type(exc).__name__}: {str(exc)[:180]}"
            return result
        result["status"] = "pdf_structure_valid"
        result["sha256"] = hashlib.sha256(data).hexdigest()
        result["details"] = "PDF header/trailer, page tree and first-page contents parsed; source identity not manually checked"
    except urllib.error.HTTPError as exc:
        result["http_status"] = exc.code
        result["status"] = "http_error"
        result["details"] = f"HTTP {exc.code}: {str(exc.reason)[:180]}"
    except (urllib.error.URLError, socket.timeout, TimeoutError) as exc:
        result["status"] = "network_error"
        result["details"] = f"{type(exc).__name__}: {str(exc)[:180]}"
    except Exception as exc:
        result["status"] = "unexpected_error"
        result["details"] = f"{type(exc).__name__}: {str(exc)[:180]}"
    return result


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        w = csv.DictWriter(file, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def shard(index, count):
    if count < 1 or index < 0 or index >= count:
        raise ValueError("Shard index must be within shard count")
    candidates = pdf_candidates(records())
    selected = [paper for i, paper in enumerate(candidates) if i % count == index]
    print(f"Shard {index}/{count}: {len(selected)} source PDFs", flush=True)
    results = []
    for paper in selected:
        outcome = inspect(paper)
        results.append(outcome)
        print(f"{paper['id']}: {outcome['status']} pages={outcome['pages']} http={outcome['http_status']}", flush=True)
        time.sleep(0.5)
    write_csv(OUT / f"shard-{index}.csv", results)


def merge(shard_count):
    papers = records()
    by_id = {p["id"]: p for p in papers}
    expected = {p["id"] for p in pdf_candidates(papers)}
    all_results = {}
    for index in range(shard_count):
        file = OUT / f"shard-{index}.csv"
        if not file.exists():
            raise ValueError(f"Missing shard: {file.name}; NOT publishing partial audit")
        with file.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        for row in rows:
            paper_id = row["id"]
            if paper_id not in expected or paper_id in all_results:
                raise ValueError(f"Unexpected or duplicate audit ID: {paper_id}")
            if row["source_url"] != by_id[paper_id]["source_url"]:
                raise ValueError(f"PDF source changed while auditing: {paper_id}")
            all_results[paper_id] = row
    if set(all_results) != expected:
        missing = sorted(expected - set(all_results))
        raise ValueError(f"Incomplete audit: {len(missing)} missing sources: {missing}")
    final = []
    for paper in papers:
        row = all_results.get(paper["id"])
        if row is None:
            if paper.get("pdf_available_at_source") is not False:
                raise ValueError(f"Unresolved source availability: {paper['id']}")
            row = {key: "" for key in FIELDS}
            row.update(id=paper["id"], status="no_source_pdf",
                       source_url=paper["source_url"],
                       details="Original repository does not list an accessible source PDF")
        final.append(row)
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    counts = dict(sorted(collections.Counter(x["status"] for x in final).items()))
    summary = {
        "audited_at_utc": stamp,
        "catalog_git_sha": os.environ.get("GITHUB_SHA", ""),
        "catalog_records": len(papers),
        "source_listed_pdfs": len(expected),
        "source_tested_in_this_run": len(all_results),
        "source_pdfs_with_valid_structure": counts.get("pdf_structure_valid", 0),
        "citation_only_records": counts.get("no_source_pdf", 0),
        "results_by_status": counts,
        "limits": "40 MB per source; no paywall bypass; no PDF bytes committed",
        "validation_scope": "Downloaded PDF structure/page tree/checksum only; scholarly title/identity and reading quality not independently checked",
    }
    write_csv(ROOT / "metadata" / "fulltext_validation.csv", final)
    path = ROOT / "metadata" / "fulltext_summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    a = sub.add_parser("shard")
    a.add_argument("--index", type=int, required=True)
    a.add_argument("--count", type=int, default=6)
    b = sub.add_parser("merge")
    b.add_argument("--count", type=int, default=6)
    args = parser.parse_args()
    if args.action == "shard":
        shard(args.index, args.count)
    else:
        merge(args.count)


if __name__ == "__main__":
    main()
