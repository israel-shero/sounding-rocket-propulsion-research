# Bibliography quality report

Generated deterministically from the current bibliography. This report checks **metadata consistency only**; it does not test network links, access rights, PDF readability, paper identity, Sider presence, or peer-review status.

| Check | Value |
|---|---:|
| Records | 190 |
| Publication years present | 189 |
| Author fields present | 158 |
| DOIs present | 21 |
| Citation pages present | 190 |
| Explicit source-listed PDFs | 138 |
| Explicit no-PDF sources | 31 |
| PDF availability unknown | 21 |
| PDFs verified as readable in this audit | 0 |
| Structural errors | 0 |
| Review flags | 22 |

## Blocking structural issues

None.

## Items needing further source verification

- RSP-029: source PDF availability not yet verified
- RSP-030: source PDF availability not yet verified
- RSP-031: source PDF availability not yet verified
- RSP-032: source PDF availability not yet verified
- RSP-033: source PDF availability not yet verified
- RSP-047: source PDF availability not yet verified
- RSP-065: source PDF availability not yet verified
- RSP-097: source PDF availability not yet verified
- RSP-098: source PDF availability not yet verified
- RSP-099: source PDF availability not yet verified
- RSP-100: source PDF availability not yet verified
- RSP-101: source PDF availability not yet verified
- RSP-102: source PDF availability not yet verified
- RSP-103: source PDF availability not yet verified
- RSP-104: source PDF availability not yet verified
- RSP-105: source PDF availability not yet verified
- RSP-106: source PDF availability not yet verified
- RSP-107: source PDF availability not yet verified
- RSP-108: source PDF availability not yet verified
- RSP-109: source PDF availability not yet verified
- RSP-110: source PDF availability not yet verified
- RSP-164: publication year not yet verified

## Reading status vocabulary

- `pdf_available_at_source = true`: a publisher/archive lists a PDF. **Not proof of download.**
- `pdf_status = not downloaded`: PDF is not stored in this repository; it is only a candidate for collection.
- `pdf_status = not available`: no openly listed direct PDF at the source; preserve the bibliographic lead.
- `downloaded_validated` in the download log (when present): a fetched PDF passed format checks; not necessarily reviewed for article-title or content matching.
- Sider `verification = file_list`: file name was seen; full PDF contents not checked.
- Sider `verification = viewer`: file was opened, but matching the full article title still requires care.

## Scope and next actions

Review original discovery records with missing authors, DOIs, or citation links. Review publisher-blocked links manually. Do not infer that a DOI landing page is a PDF. Never rehost third-party PDFs without permission.
