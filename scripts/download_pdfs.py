#!/usr/bin/env python3
"""Download candidate PDFs without bypassing access controls."""
import csv
import pathlib
import time
import urllib.request

root = pathlib.Path(__file__).resolve().parents[1]
(root / "pdfs").mkdir(exist_ok=True)
with (root / "metadata/papers.csv").open(newline="", encoding="utf-8") as f:
    papers = list(csv.DictReader(f))
with (root / "metadata/download_results.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "status", "details"])
    for paper in papers:
        dest = root / "pdfs" / (paper["id"] + ".pdf")
        if dest.exists():
            writer.writerow([paper["id"], "exists", str(dest)])
            continue
        try:
            request = urllib.request.Request(paper["source_url"], headers={"User-Agent": "AcademicLiteratureIndex/1.0"})
            with urllib.request.urlopen(request, timeout=25) as response:
                data = response.read(40_000_001)
            if len(data) > 40_000_000 or not data.startswith(b"%PDF-"):
                raise ValueError("Not a PDF or file exceeds 40 MB")
            dest.write_bytes(data)
            writer.writerow([paper["id"], "downloaded", len(data)])
        except Exception as exc:
            writer.writerow([paper["id"], "failed", str(exc)[:240]])
        time.sleep(0.5)
print("See metadata/download_results.csv")
