#!/usr/bin/env python3
"""Check bibliography integrity and write an inspectable, non-destructive quality report.

No network calls. Source-level metadata is not evidence that a full PDF is readable.
Only structural defects fail the check; incomplete legacy entries remain flagged.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "metadata/papers.json"
REPORT = ROOT / "metadata/quality_report.md"


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", str(text or "").casefold()).strip()


def normalize_doi(value):
    s = str(value or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s


def audit(papers):
    hard, review = [], []
    seen_ids, seen_urls, seen_dois = {}, {}, {}
    for row, paper in enumerate(papers, 1):
        ident = paper.get("id", "")
        title = paper.get("title", "")
        source = paper.get("source_url", "")
        if not re.fullmatch(r"RSP-\d{3,}", ident):
            hard.append(f"Row {row}: missing or invalid paper ID")
        if not title or not source:
            hard.append(f"{ident or row}: missing title or source_url")
        if ident in seen_ids:
            hard.append(f"{ident}: duplicated ID (rows {seen_ids[ident]}, {row})")
        seen_ids[ident] = row
        if source in seen_urls:
            hard.append(f"{ident}: duplicated source URL (also {seen_urls[source]})")
        seen_urls[source] = ident
        u = urlparse(source)
        if u.scheme not in {"https", "http"} or not u.netloc:
            hard.append(f"{ident}: invalid source URL")
        doi = normalize_doi(paper.get("doi"))
        if doi:
            if doi in seen_dois:
                hard.append(f"{ident}: duplicate DOI (also {seen_dois[doi]})")
            seen_dois[doi] = ident
            if not doi.startswith("10.") or "/" not in doi:
                review.append(f"{ident}: DOI format needs review")
        year = paper.get("year")
        if year is not None and (not isinstance(year, int) or year < 1900 or year > datetime.now(timezone.utc).year + 1):
            review.append(f"{ident}: implausible publication year {year}")
        if paper.get("year") is None:
            review.append(f"{ident}: publication year not yet verified")
        if paper.get("pdf_available_at_source") is None:
            review.append(f"{ident}: source PDF availability not yet verified")
        if paper.get("metadata_status") == "needs_source_verification":
            review.append(f"{ident}: bibliographic source still requires checking")
        if paper.get("pdf_available_at_source") is False and paper.get("pdf_status") == "not downloaded":
            hard.append(f"{ident}: no source PDF, yet pdf_status is 'not downloaded'")
        if paper.get("pdf_status") == "not available" and paper.get("pdf_available_at_source") is True:
            hard.append(f"{ident}: PDF available but pdf_status claims unavailable")
        if paper.get("pdf_available_at_source") is False and ".pdf" in urlparse(source).path.lower():
            review.append(f"{ident}: no downloadable PDF listed, but source URL still resembles a PDF")
        if paper.get("citation_url"):
            c = urlparse(paper["citation_url"])
            if c.scheme not in {"https", "http"} or not c.netloc:
                review.append(f"{ident}: invalid citation page URL")
        if not paper.get("metadata_status"):
            review.append(f"{ident}: original-source metadata not yet independently verified")

    titles = defaultdict(list)
    for p in papers:
        titles[norm(p.get("title"))].append(p.get("id"))
    for title, ids in titles.items():
        if len(ids) > 1:
            review.append("Same normalized title: " + ", ".join(ids))

    metrics = {
        "Records": len(papers),
        "Publication years present": sum(p.get("year") is not None for p in papers),
        "Author fields present": sum(bool(p.get("authors")) for p in papers),
        "DOIs present": sum(bool(p.get("doi")) for p in papers),
        "Citation pages present": sum(bool(p.get("citation_url")) for p in papers),
        "Explicit source-listed PDFs": sum(p.get("pdf_available_at_source") is True for p in papers),
        "Explicit no-PDF sources": sum(p.get("pdf_available_at_source") is False for p in papers),
        "PDF availability unknown": sum(p.get("pdf_available_at_source") is None for p in papers),
        "PDFs verified as readable in this audit": 0,
        "Structural errors": len(hard),
        "Review flags": len(review),
    }
    return metrics, hard, review


def write_report(metrics, hard, review):
    lines = [
        "# Bibliography quality report", "",
        "Generated deterministically from the current bibliography. This report checks "
        "**metadata consistency only**; it does not test network links, access rights, "
        "PDF readability, paper identity, Sider presence, or peer-review status.", "",
        "| Check | Value |", "|---|---:|",
    ]
    lines += [f"| {k} | {v} |" for k, v in metrics.items()]
    lines += ["", "## Blocking structural issues", ""]
    lines += [f"- {x}" for x in hard] if hard else ["None."]
    lines += ["", "## Items needing further source verification", ""]
    lines += [f"- {x}" for x in review] if review else ["None."]
    lines += [
        "", "## Reading status vocabulary", "",
        "- `pdf_available_at_source = true`: a publisher/archive lists a PDF. **Not proof of download.**",
        "- `pdf_status = not downloaded`: PDF is not stored in this repository; it is only a candidate for collection.",
        "- `pdf_status = not available`: no openly listed direct PDF at the source; preserve the bibliographic lead.",
        "- `downloaded_validated` in the download log (when present): a fetched PDF passed format checks; "
        "not necessarily reviewed for article-title or content matching.",
        "- Sider `verification = file_list`: file name was seen; full PDF contents not checked.",
        "- Sider `verification = viewer`: file was opened, but matching the full article title still requires care.",
        "", "## Scope and next actions", "",
        "Review original discovery records with missing authors, DOIs, or citation links. "
        "Review publisher-blocked links manually. Do not infer that a DOI landing page is a PDF. "
        "Never rehost third-party PDFs without permission.",
    ]
    content = "\n".join(lines) + "\n"
    if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != content:
        REPORT.write_text(content, encoding="utf-8")
        print(f"Updated {REPORT.relative_to(ROOT)}")
    else:
        print(f"Unchanged {REPORT.relative_to(ROOT)}")


def main():
    papers = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(papers, list):
        raise SystemExit("Bibliography must be a JSON array")
    metrics, hard, review = audit(papers)
    write_report(metrics, hard, review)
    print(f"Validated {len(papers)} records; {len(hard)} structural errors, {len(review)} review flags")
    if hard:
        for issue in hard:
            print("ERROR:", issue, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
