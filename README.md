# Sounding Rocket & Propulsion Research

Public research bibliography for sounding rockets, solid propulsion, internal ballistics, erosive burning, combustion instability, nozzle thermal protection, instrumentation, and hybrid propulsion.

## Current status
- 28 candidate records in [metadata/papers.json](metadata/papers.json), assembled from scholarly discovery on 2026-11-20.
- Source URLs and bibliographic details have **not** been independently verified in bulk.
- PDFs have **not** been downloaded or uploaded to Sider.
- CSV export is pending; JSON is the canonical index until it is committed.

## Contents
- `metadata/papers.json`: indexed candidates with IDs RSP-001 through RSP-028
- `scripts/download_pdfs.py`: download publicly accessible PDFs and log failures (requires `metadata/papers.csv`)
- `notes/READING_TEMPLATE.md`: reading and analysis template
- `SIDER_SETUP.md`: steps to ingest PDFs into Sider Wisebase
- `.gitignore`: excludes PDFs and local download logs

## Next steps
1. Add `metadata/papers.csv` with matching IDs and fields.
2. Verify citations, DOIs, licenses, and PDF availability.
3. Run the downloader locally and import eligible PDFs into Sider.
4. Expand categories and add reproducible paper-level notes.

PDF URLs do not establish permission to redistribute their content.