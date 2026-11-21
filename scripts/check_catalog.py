#!/usr/bin/env python3
"""Offline, deterministic integrity audit for the research bibliography.

Use this in GitHub Actions or locally. Never infers open access from a URL's
appearance and never marks PDFs as downloaded by inspecting metadata alone.
"""
import argparse
import collections
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "metadata/papers.json"
REPORT = ROOT / "metadata/catalog_quality.json"


def normalized_title(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).casefold()).strip()


def normalized_url(value):
    url = urlsplit(value.strip())
    # Ignore presentation-only download switches, not meaningful version IDs.
    query = urlencode(sorted((k, v) for k, v in parse_qsl(url.query)
                             if k.lower() not in {"attachment", "download"}))
    return urlunsplit((url.scheme.lower(), url.netloc.lower(),
                       url.path.rstrip("/"), query, ""))


def check_catalog(papers):
    errors, warnings = [], []
    ids, titles, sources, dois = {}, {}, {}, {}
    count = collections.Counter()
    for index, p in enumerate(papers):
        ident = str(p.get("id") or "").strip()
        title = str(p.get("title") or "").strip()
        url = str(p.get("source_url") or "").strip()
        if not re.fullmatch(r"RSP-\d{3,}", ident):
            errors.append({"code": "bad_id", "id": ident, "index": index})
        if not title or not p.get("category") or not url:
            errors.append({"code": "missing_required", "id": ident})
        else:
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append({"code": "invalid_url", "id": ident})
        for mapping, key, label in (
            (ids, ident, "duplicate_id"),
            (titles, normalized_title(title), "duplicate_title"),
            (sources, normalized_url(url), "duplicate_source"),
        ):
            if key and key in mapping:
                errors.append({"code": label, "id": ident,
                               "other_id": mapping[key]})
            elif key:
                mapping[key] = ident
        doi = str(p.get("doi") or "").strip().casefold()
        if doi:
            if doi in dois:
                errors.append({"code": "duplicate_doi", "id": ident,
                               "other_id": dois[doi]})
            elif not doi.startswith("10.") or "/" not in doi:
                errors.append({"code": "invalid_doi", "id": ident})
            else:
                dois[doi] = ident
        status = p.get("pdf_status")
        available = p.get("pdf_available_at_source")
        if status not in {"not downloaded", "not available", "downloaded"}:
            errors.append({"code": "invalid_pdf_status", "id": ident})
        if available is False and status != "not available":
            errors.append({"code": "pdf_availability_conflict", "id": ident})
        if available is True and status == "not available":
            errors.append({"code": "pdf_availability_conflict", "id": ident})
        if available is True and re.search(r"ntrs\.nasa\.gov/citations/\d+/?$", url):
            errors.append({"code": "citation_page_marked_as_pdf", "id": ident})
        if status == "downloaded" and not p.get("pdf_checksum"):
            warnings.append({"code": "download_unproven", "id": ident})
        year = p.get("year")
        if year is not None and (isinstance(year, bool) or
                                 not isinstance(year, int) or
                                 year < 1900 or year > 2100):
            errors.append({"code": "invalid_publication_year", "id": ident})
        if not year:
            count["missing_year"] += 1
        if not p.get("authors"):
            count["missing_authors"] += 1
        if not doi:
            count["missing_doi"] += 1
        if not p.get("document_type"):
            count["missing_type"] += 1
        if available is None:
            count["unconfirmed_pdf_availability"] += 1
        elif available is True:
            count["source_listed_pdf"] += 1
        else:
            count["citation_only"] += 1
        if url.lower().startswith("http://"):
            count["http_source_links"] += 1
        if status == "downloaded":
            count["declared_downloaded"] += 1
        if "abstract" in str(p.get("document_type", "")).lower():
            count["abstract_records"] += 1
        if re.search(r"\b(poster|presentation)\b",
                     str(p.get("document_type", "")), re.I):
            count["presentation_or_poster_records"] += 1
    summary = {"records": len(papers), **dict(sorted(count.items()))}
    return {"summary": summary, "errors": errors, "warnings": warnings,
            "scope": "metadata integrity only; not an online PDF audit"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    records = json.loads(DATA.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise SystemExit("Expected a JSON list of bibliography records")
    report = check_catalog(records)
    if args.write_report:
        output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != output:
            REPORT.write_text(output, encoding="utf-8")
            print(f"Updated {REPORT.relative_to(ROOT)}")
    print(json.dumps(report["summary"], sort_keys=True))
    if report["errors"]:
        print(json.dumps(report["errors"], indent=2))
        raise SystemExit(1)
    print("Catalog metadata integrity checks passed.")


if __name__ == "__main__":
    main()
