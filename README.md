# Sounding Rocket & Propulsion Research

Public, version-controlled bibliography for sounding rockets, solid rocket motors, propulsion research, instrumentation, thermal protection, and internal ballistics.

## Current status

- **28 candidate publications** indexed from scholarly discovery on November 20, 2026.
- **0 PDFs verified or uploaded**. URLs are discovery leads, not confirmed downloadable files.
- Citation metadata and redistribution permissions need further verification.

## Contents

- [Paper catalog (CSV)](metadata/papers.csv) — spreadsheet-friendly, stable paper IDs.
- [Paper catalog (JSON)](metadata/papers.json) — machine-readable bibliography.
- [PDF downloader](scripts/download_pdfs.py) — tries publicly available links, checks PDF signatures, and logs failures.
- [Reading notes template](notes/READING_TEMPLATE.md).
- [Sider Wisebase integration](SIDER_SETUP.md).

## Get started

Clone this repository and run:

```bash
python scripts/download_pdfs.py
```

Downloaded PDFs are saved under `pdfs/` and excluded from Git. Inspect `metadata/download_results.csv` for results. The script does not bypass access restrictions.

## Scope

Sounding rocket systems and flight testing; telemetry and instrumentation; solid propulsion and erosive burning; combustion instability; grain burnback and internal ballistics; nozzle ablation; hybrid propulsion. Planned: liquid propulsion, experimental methods, recovery, flight dynamics, and validated computational tools.

## Research integrity

Do not equate a PDF URL with open access or a redistribution license. Validate title, authors, year, DOI, source, and license before citing or sharing. Keep GitHub as the bibliographic source of truth and use Sider Wisebase as a separately maintained full-text library.
