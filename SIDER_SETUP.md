# Sider Wisebase setup

GitHub stores the master paper catalog, scripts, and notes. PDFs remain outside Git unless redistribution is permitted.

1. Run `python scripts/download_pdfs.py` locally with internet access.
2. Review `metadata/download_results.csv` for successes and failures.
3. Import successfully downloaded PDFs into Sider Wisebase through its supported upload workflow.
4. Keep each PDF's `RSP-###` identifier in its filename so it maps back to `metadata/papers.csv`.
5. Confirm import completion and full-text search in Sider before marking a paper as indexed there.

The Sider connector did not provide a verified inventory or working bulk PDF import in this session. No import is claimed.
