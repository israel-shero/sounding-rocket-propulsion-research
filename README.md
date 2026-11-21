# Sounding Rocket & Propulsion Research

Public, version-controlled bibliography for sounding rockets, rocket propulsion, instrumentation, thermal protection, and internal ballistics. **GitHub is the bibliographic source of truth; Sider Wisebase is a separate full-text reading library.**

## Status

- The `metadata/papers.json` contains **190 indexed research records** (28 original discovery leads and 162 later source-checked additions). The latest 34 NASA/DLR references (RSP-157–190) strengthen coverage in solid-motor slag behavior, propellant aging, testing, flight reconstruction, hybrid regression measurement, alternative propellants and liquid-engine combustion. Of the 34 new records, **28 have source-listed public PDF links** and **6 are citation-only or otherwise lack verified open full text**. None of these newly listed PDFs have been downloaded or imported into Sider as part of the current expansion.
- On November 20, 2026, Sider displayed **79 total file records**, up from 62 at the start of the latest expansion. All 17 new NASA PDF filenames were individually confirmed present after two targeted retry imports; 2 were opened in the full-text viewer, while the other 15 have file-list-level processing confirmation. Total file count is not a count of fully verified academic papers: older errors, an imported NATO 404 page, and records still awaiting content validation remain. The import observation log is historical, including failures, so its row count does not have to match Sider's current file count.
- Open the [Sider research Wisebase](https://sider.ai/wisebase/6b00ca26d3e350873fe60644).

## Metadata and automation

- [Bibliography source (JSON)](metadata/papers.json) — authoritative records with stable paper IDs.
- [Bibliography (CSV)](metadata/papers.csv) — auto-generated from JSON, including authors, publication date, paper type, DOI, citation link, research utility, and PDF availability when available.
- [Sider import observations (JSONL)](metadata/sider_import_events.jsonl) — append-only evidence log (one JSON object per line, latest observation for each filename takes precedence).
- [Sider import inventory (CSV)](metadata/sider_imports.csv) — auto-generated from the observation log.
- [Download results (CSV)](metadata/download_results.csv) — updated by the scheduled PDF download workflow when it runs.
- [PDF retrieval script](scripts/download_pdfs.py) — attempts public PDFs, checks signatures, reports failures, and saves files as workflow artifacts (not in git).
- [Metadata sync script](scripts/sync_metadata.py) — validates input records and deterministically refreshes CSV outputs.
- [Metadata sync GitHub Action](.github/workflows/sync-metadata.yml) — runs on source-data pushes, daily, and manually; commits generated CSV changes when necessary.
- [PDF collection GitHub Action](.github/workflows/collect-pdfs.yml) — runs every other day and on demand; saves downloadable PDF artifacts and commits download logs and metadata updates.
- [Coverage-gap expansion guide](notes/coverage_gap_expansion_2026-11-20.md) — 46 NASA/DLR sources grouped by previously underrepresented research area, with public PDF availability and validation caveats.
- [Continued 190-record research expansion](notes/research_expansion_190_2026-11-20.md) — all 34 new NASA/DLR references with citation links, topic summaries, and access status.
- [November 20 research expansion reading guide](notes/research_expansion_2026-11-20.md) — 28 newly indexed NASA and DLR publications with topic-by-topic reading priorities.
- [Reading template](notes/READING_TEMPLATE.md) and [Sider setup](SIDER_SETUP.md).

GitHub Actions uses a repository-scoped `GITHUB_TOKEN` with `contents: write` to commit changed CSV files. It does not need a personal access token. Actions must be enabled and write permissions allowed for workflows; protected branch rules may also affect pushes.

**Important:** The workflow does not log into Sider or independently poll its file list. Sider observations must first be appended to `metadata/sider_import_events.jsonl` by a verified importer or other authorized integration. Once source records are committed, GitHub Actions automatically regenerates and commits the public import CSV. A document listed as `processed` with verification `file_list` has not necessarily been opened or verified as full-text readable. For stronger verification, use `verification: viewer` only when the document was opened.

## Running locally

```bash
python3 scripts/sync_metadata.py
python3 scripts/download_pdfs.py
```

The PDF retrieval script skips bibliography-only records whose sources do not list a public PDF, and writes local PDFs to `pdfs/`, excluded from git. The metadata sync script uses the Python standard library. No paywall, authentication, or publisher access controls are bypassed.

## Scope

Sounding rocket systems and flight testing; telemetry and instrumentation; solid propulsion and erosive burning; combustion instability; internal ballistics; nozzle ablation; hybrid propulsion; flight dynamics; computational tools.

## Research integrity

Do not equate a PDF URL with open access or permission to redistribute it. Validate author, year, DOI, source, document title, and license before citing. Import status, downloader status, and bibliographic correctness are separate fields of evidence.
