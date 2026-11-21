# Bibliography quality report

Generated deterministically from the current bibliography. This report checks **metadata consistency only**; it does not test network links, access rights, PDF readability, paper identity, Sider presence, or peer-review status.

| Check | Value |
|---|---:|
| Records | 190 |
| Publication years present | 190 |
| Author fields present | 159 |
| DOIs present | 21 |
| Citation pages present | 190 |
| Explicit source-listed PDFs | 159 |
| Explicit no-PDF sources | 31 |
| PDF availability unknown | 0 |
| PDFs verified as readable in this audit | 0 |
| Structural errors | 0 |
| Review flags | 0 |

## Blocking structural issues

None.

## Items needing further source verification

None.

## Reading status vocabulary

- `pdf_available_at_source = true`: a publisher/archive lists a PDF. **Not proof of download.**
- `pdf_status = not downloaded`: PDF is not stored in this repository; it is only a candidate for collection.
- `pdf_status = not available`: no openly listed direct PDF at the source; preserve the bibliographic lead.
- `downloaded_validated` in the download log (when present): a fetched PDF passed format checks; not necessarily reviewed for article-title or content matching.
- Sider `verification = file_list`: file name was seen; full PDF contents not checked.
- Sider `verification = viewer`: file was opened, but matching the full article title still requires care.

## Scope and next actions

Review original discovery records with missing authors, DOIs, or citation links. Review publisher-blocked links manually. Do not infer that a DOI landing page is a PDF. Never rehost third-party PDFs without permission.
