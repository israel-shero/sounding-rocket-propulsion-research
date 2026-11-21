#!/usr/bin/env python3
"""Deterministically regenerate public research metadata from source records.

Authoritative inputs:
  metadata/papers.json
  metadata/sider_import_events.jsonl (append-only observations)

Generated outputs:
  metadata/papers.csv
  metadata/sider_imports.csv
  metadata/quality_report.md

Sider is not queried by this script. A record is only as verified as its
source observation; file-list presence must not imply full-text readability.
"""
import csv
import io
import json
from pathlib import Path
from urllib.parse import urlparse
from check_catalog import check_catalog
from audit_bibliography import audit, write_report

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "metadata"
PAPER_COLS = [
    "id", "category", "title", "source_url", "pdf_status", "access_status",
    "year", "publication_date", "authors", "document_type", "doi",
    "citation_url", "metadata_status", "research_utility",
    "pdf_available_at_source", "notes",
]
SIDER_COLS = [
    "filename", "source_url", "title", "status", "verification",
    "observed_at", "notes",
]
STATUSES = {"processed", "submitted", "process_failed", "not_found"}
VERIFICATIONS = {"file_list", "viewer", "unverified"}


def output_csv(path, columns, records):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore",
                            lineterminator="\n")
    writer.writeheader()
    for record in records:
        writer.writerow({key: record.get(key, "") for key in columns})
    expected = stream.getvalue()
    if not path.exists() or path.read_text(encoding="utf-8") != expected:
        path.write_text(expected, encoding="utf-8")
        print(f"Updated {path.relative_to(ROOT)} ({len(records)} records)")
    else:
        print(f"Unchanged {path.relative_to(ROOT)} ({len(records)} records)")


def main():
    papers = json.loads((META / "papers.json").read_text(encoding="utf-8"))
    if not isinstance(papers, list):
        raise ValueError("papers.json must contain an array")
    ids = set()
    urls = set()
    for paper in papers:
        if not all(paper.get(key) for key in ("id", "title", "source_url")):
            raise ValueError(f"Paper lacks id, title or source_url: {paper}")
        if paper["id"] in ids:
            raise ValueError(f"Duplicate paper ID: {paper['id']}")
        ids.add(paper["id"])
        source = paper["source_url"]
        if source in urls:
            raise ValueError(f"Duplicate source URL: {source}")
        urls.add(source)
        if urlparse(source).scheme not in {"http", "https"}:
            raise ValueError(f"Unexpected URL scheme: {source}")
    metrics, hard, review = audit(papers)
    write_report(metrics, hard, review)
    if hard:
        raise ValueError("Bibliography structural audit failed: " + "; ".join(hard))
    report = check_catalog(papers)
    if report["errors"]:
        raise ValueError("Catalog audit failed: " +
                         json.dumps(report["errors"], ensure_ascii=False))
    report_file = META / "catalog_quality.json"
    expected_report = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if not report_file.exists() or report_file.read_text(encoding="utf-8") != expected_report:
        report_file.write_text(expected_report, encoding="utf-8")
        print("Updated metadata/catalog_quality.json")
    output_csv(META / "papers.csv", PAPER_COLS, papers)

    events_path = META / "sider_import_events.jsonl"
    latest = {}
    if events_path.exists():
        for line_no, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at line {line_no}") from exc
            filename = event.get("filename", "").strip()
            if not filename:
                raise ValueError(f"Missing Sider filename at line {line_no}")
            if event.get("status") not in STATUSES:
                raise ValueError(f"Invalid Sider status on line {line_no}")
            if event.get("verification") not in VERIFICATIONS:
                raise ValueError(f"Invalid verification level on line {line_no}")
            source = event.get("source_url", "")
            if source and urlparse(source).scheme not in {"http", "https"}:
                raise ValueError(f"Invalid source URL on line {line_no}")
            if not event.get("observed_at"):
                raise ValueError(f"Missing observation date on line {line_no}")
            latest[filename] = event
    output_csv(META / "sider_imports.csv", SIDER_COLS,
               [latest[k] for k in sorted(latest, key=str.casefold)])


if __name__ == "__main__":
    main()
