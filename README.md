# Sounding Rocket & Propulsion Research

Public, version-controlled bibliography for sounding rockets, rocket propulsion, instrumentation, thermal protection, and internal ballistics. **GitHub is the bibliographic source of truth; Sider Wisebase is a separate full-text reading library.**

## Status

- The `metadata/papers.json` now contains **51 research records** (original 28 discovery leads plus 23 additional source-checked entries). The original leads still need individual validation; later entries were checked against NASA, DLR, MIT, or NATO records.
- On November 20, 2026, Sider displayed **54 file records** after the latest expansion, compared with 36 at the start of this round. That includes 17 additional PDF-named entries and one NATO link import that produced an HTML error page rather than a research PDF. The import observation log identifies **52 filenames/records** from the 54 total; two earlier records lack reliable identifiers. Earlier checks also noted a failed-to-process file, `19970004933.pdf`, whose current status has not been re-verified exhaustively. The CSV distinguishes viewer-verified files from file-list-only entries.
- Open the [Sider research Wisebase](https://sider.ai/wisebase/6b00ca26d3e350873fe60644).

## Metadata and automation

- [Bibliography source (JSON)](metadata/papers.json) — authoritative records with stable paper IDs.
- [Bibliography (CSV)](metadata/papers.csv) — auto-generated from JSON.
- [Sider import observations (JSONL)](metadata/sider_import_events.jsonl) — append-only evidence log (one JSON object per line, latest observation for each filename takes precedence).
- [Sider import inventory (CSV)](metadata/sider_imports.csv) — auto-generated from the observation log.
- [Download results (CSV)](metadata/download_results.csv) — updated by the scheduled PDF download workflow when it runs.
- [PDF retrieval script](scripts/download_pdfs.py) — attempts public PDFs, checks signatures, reports failures, and saves files as workflow artifacts (not in git).
- [Metadata sync script](scripts/sync_metadata.py) — validates input records and deterministically refreshes CSV outputs.
- [Metadata sync GitHub Action](.github/workflows/sync-metadata.yml) — runs on source-data pushes, daily, and manually; commits generated CSV changes when necessary.
- [PDF collection GitHub Action](.github/workflows/collect-pdfs.yml) — runs every other day and on demand; saves downloadable PDF artifacts and commits download logs and metadata updates.
- [Reading template](notes/READING_TEMPLATE.md) and [Sider setup](SIDER_SETUP.md).

GitHub Actions uses a repository-scoped `GITHUB_TOKEN` with `contents: write` to commit changed CSV files. It does not need a personal access token. Actions must be enabled and write permissions allowed for workflows; protected branch rules may also affect pushes.

**Important:** The workflow does not log into Sider or independently poll its file list. Sider observations must first be appended to `metadata/sider_import_events.jsonl` by a verified importer or other authorized integration. Once source records are committed, GitHub Actions automatically regenerates and commits the public import CSV. A document listed as `processed` with verification `file_list` has not necessarily been opened or verified as full-text readable. For stronger verification, use `verification: viewer` only when the document was opened.

## Running locally

```bash
python3 scripts/sync_metadata.py
python3 scripts/download_pdfs.py
```

The PDF retrieval script writes local PDFs to `pdfs/`, excluded from git. The metadata sync script uses the Python standard library. No paywall, authentication, or publisher access controls are bypassed.

## Scope

Sounding rocket systems and flight testing; telemetry and instrumentation; solid propulsion and erosive burning; combustion instability; internal ballistics; nozzle ablation; hybrid propulsion; flight dynamics; computational tools.

## Research integrity

Do not equate a PDF URL with open access or permission to redistribute it. Validate author, year, DOI, source, document title, and license before citing. Import status, downloader status, and bibliographic correctness are separate fields of evidence.
