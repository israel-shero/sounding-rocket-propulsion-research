# Research collection cleanup audit — 2026-11-20

## Outcome

The bibliography retains **190 records and stable IDs**. No records were deleted. The metadata sync, downloader, and collection workflows have been tightened to distinguish original-source PDF listings from actual file validation. The Sider Wisebase has not been modified.

### Data quality after the cleanup

| Metric | Count |
|---|---:|
| Indexed records | 190 |
| Publication years present | 189 |
| Author fields present | 114 |
| DOI fields present | 21 |
| Citation pages present | 190 |
| Source explicitly lists a PDF | 90 |
| Source explicitly has no verified open PDF | 30 |
| PDF source availability not yet verified | 70 |

The final remaining missing year is **RSP-164**; the NASA source did not provide a reliable publication-date field. We did not infer a date from its report identifier.

### Confirmed repairs

- **RSP-001**: Restored the full JAXA reusable sounding-rocket propulsion paper title, author list, year, DOI, and original J-STAGE PDF link.
- **RSP-002–003, RSP-008, RSP-010–014, RSP-023–028**: Recovered independently supported citation dates, original citation links, authors and/or DOIs where available.
- **RSP-015–017**: Replaced landing-page or legacy-archive download URLs with PDF paths explicitly listed by the NASA NTRS source record.
- **RSP-006, RSP-012, RSP-014**: Downgraded misleading publisher/DOI links to citation-only status where an unrestricted direct PDF could not be verified.
- **RSP-004 and RSP-007**: Repaired previously uncertain original-source metadata using publisher and journal references, including title, date, DOI, and correct institutional or conference download information.
- **RSP-057–060**: Removed four invented/constructed NASA PDF download links. The NTRS API lists **zero PDF downloads** for these reports, so the genuine bibliographic pages are retained and the downloader will skip them.
- **PDF collection script**: Prevents HTML/DOI landing-page responses from being counted as PDFs; requires readable PDF structure and page count, and records byte size, SHA-256, final status and failure reasons. Third-party PDFs stay in temporary GitHub Actions artifacts; not the public GitHub repository.
- **Scheduled metadata sync**: Runs source consistency checks and generates `metadata/quality_report.md`. Structural defects fail the sync; incomplete citation fields remain flagged for review.

### What these checks do not establish

- The repository has not yet completed a full run of **190 PDF downloads with structure validation**. Until it does, the absence of a committed `metadata/download_results.csv` is not proof that those downloads failed.
- PDF signature and page-count validation are **not** evidence that the PDF contains the expected article or that its scholarly claims are valid.
- Some bibliography records are abstracts, presentations, posters, theses, and technical reports rather than peer-reviewed journal papers.
- The Sider import history includes a NATO 404 page and a previously failed processing record; neither was deleted, and the current status was not rechecked during this cleanup.
- The **70 PDF availability-unknown records** require source-specific access checks. A failed HTTP response from a publisher is not proof the paper has no legitimate open-access copy.

## Source of truth and automated checks

- [Bibliography JSON](../metadata/papers.json)
- [Bibliography CSV](../metadata/papers.csv)
- [Bibliography quality report](../metadata/quality_report.md)
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
