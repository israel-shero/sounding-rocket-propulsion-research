# Research collection cleanup audit — 2026-11-20

## Outcome

The bibliography retains **190 records and stable IDs**. No records were deleted. The metadata sync, downloader, and collection workflows have been tightened to distinguish original-source PDF listings from actual file validation. The Sider Wisebase has not been modified.

### Data quality after the cleanup

| Metric | Count |
|---|---:|
| Indexed records | 190 |
| Publication years present | 190 |
| Author fields present | 179 |
| DOI fields present | 24 |
| Citation pages present | 190 |
| Source explicitly lists a PDF | 159 |
| Citation-only/no source PDF | 31 |
| PDF source availability not yet verified | 0 |

**RSP-164** is dated **2022** on the basis of the AIAA SciTech Forum meeting dates (January 3–7, 2022) in its official NASA NTRS record. Its conference year is verified, but NTRS supplies no separate paper publication date.

### Confirmed repairs

- **RSP-013**: Corrected the IIETA article DOI to `10.18280/ijht.360338`, verified its open PDF link and populated its author list and journal-article type.
- **RSP-164**: Confirmed the 2022 conference year from NASA-listed SciTech Forum dates and recovered the full author list.
- **DLR papers RSP-029–033, 065, 097–110**: Confirmed original PDF links and filled 20 author fields, plus additional DOIs where supported.
- **RSP-001**: Restored the full JAXA reusable sounding-rocket propulsion paper title, author list, year, DOI, and original J-STAGE PDF link.
- **RSP-002–003, RSP-008, RSP-010–014, RSP-023–028**: Recovered independently supported citation dates, original citation links, authors and/or DOIs where available.
- **RSP-015–017**: Replaced landing-page or legacy-archive download URLs with PDF paths explicitly listed by the NASA NTRS source record.
- **RSP-006, RSP-012, RSP-014**: Downgraded misleading publisher/DOI links to citation-only status where an unrestricted direct PDF could not be verified.
- **RSP-004 and RSP-007**: Repaired previously uncertain original-source metadata using publisher and journal references, including title, date, DOI, and correct institutional or conference download information.
- **RSP-057–060**: Removed four invented/constructed NASA PDF download links. The NTRS API lists **zero PDF downloads** for these reports, so the genuine bibliographic pages are retained and the downloader will skip them.
- **PDF collection script**: Prevents HTML/DOI landing-page responses from being counted as PDFs; requires readable PDF structure and page count, and records byte size, SHA-256, final status and failure reasons. Third-party PDFs stay in temporary GitHub Actions artifacts; not the public GitHub repository.
- **Scheduled metadata sync**: Runs source consistency checks and unit tests, generating `metadata/quality_report.md` and `metadata/catalog_quality.json`. Structural defects fail the sync; incomplete citation fields remain flagged for review.

### What these checks do not establish

- The repository has not completed **full-text retrieval validation**. The downloader now selects rotating batches of at most **30 eligible PDF links per run**, rather than trying all sources within the 40-minute GitHub Actions timeout. Its log describes the **most recent run only**, including records marked `not_checked_this_run`. Absence of a committed `metadata/download_results.csv` does not establish download failure.
- PDF signature and page-count validation are **not** evidence that the PDF contains the expected article or that its scholarly claims are valid.
- Some bibliography records are abstracts, presentations, posters, theses, and technical reports rather than peer-reviewed journal papers.
- The Sider import history includes a NATO 404 page and a previously failed processing record; neither was deleted, and the current status was not rechecked during this cleanup.
- The former **69 unknown PDF-availability records**, plus the subsequently corrected citation-only AGARD proceedings, have now been reconciled against original NASA, DLR, and MIT repository listings. This verifies link listings, not successful file retrieval. MIT's thesis PDF, for example, returned HTTP 429 during a direct fetch even though the archive lists the file.

## Source of truth and automated checks

- [Bibliography JSON](../metadata/papers.json)
- [Bibliography CSV](../metadata/papers.csv)
- [Bibliography quality report](../metadata/quality_report.md)
- [Machine-readable audit](../metadata/catalog_quality.json)
- [Regression tests](../tests/test_catalog_quality.py)
- [Downloader](../scripts/download_pdfs.py)
- [Metadata audit](../scripts/audit_bibliography.py)
- [Sider import observations](../metadata/sider_import_events.jsonl)

## Remaining recommended work

1. Run and verify the PDF collection workflow to generate a **fresh download-results CSV**; the workflow may encounter source blocking, PDF parsing failures, and the existing 40 MB file cap.
2. Resolve the 70 unknown source-PDF statuses by checking publishers and repositories for legally available PDF downloads.
3. Improve the 76 missing author fields and 169 missing DOI fields as appropriate; many NASA reports legitimately do not have DOIs.
4. Conduct a document-by-document content identity audit of any PDF successfully retrieved, and reconcile incorrect or unverified Sider filenames without inferring metadata from numeric filenames alone.
5. Review licenses before distributing any third-party PDF files.

The conservative rule is to retain uncertain references as review leads, not remove them or falsely count them as verified full text.
