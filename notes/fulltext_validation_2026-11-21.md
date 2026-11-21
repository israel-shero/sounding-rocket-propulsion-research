# Complete source-PDF structural audit — 2026-11-21

**Run:** [GitHub Actions full-library PDF audit](https://github.com/israel-shero/sounding-rocket-propulsion-research/actions/runs/44874212474)

The audit tested **all 159 source-listed PDF URLs** in the 190-record catalog. The six independent validation shards completed, and the reconciler checked every expected paper ID before publishing. **140 PDFs passed structure validation** (PDF header and EOF marker, readable page tree/first page, SHA-256), about **88.1%** of the 159 tested links.

**These checks do NOT prove that the PDF's cover matches the catalog title, that all pages are legible, or that the research is peer-reviewed.** No PDFs were copied into the public GitHub repository. The source listed a PDF in the other 31 citation-only records only if marked; those entries were not downloaded.

## Final results

| Status | Count |
|---|---:|
| `encrypted_pdf` | 2 |
| `http_error` | 10 |
| `network_error` | 2 |
| `no_source_pdf` | 31 |
| `not_pdf` | 1 |
| `pdf_structure_valid` | 140 |
| `too_large` | 4 |

**Audit timestamp:** 2026-11-21T06:30:11+00:00. **Audited catalog commit:** `ec70458e2e46e62286db15d66bee1f91550145d6`. Results were recorded in [metadata/fulltext_validation.csv](../metadata/fulltext_validation.csv) and [metadata/fulltext_summary.json](../metadata/fulltext_summary.json).

## 19 records requiring follow-up

| ID | Original source citation | Result | Details |
|---|---|---|---|
| RSP-001 | [Development of Main Propulsion System for Reusable Sounding Rocket: Design Considerations and Technology Demonstration](https://www.jstage.jst.go.jp/article/tastj/12/ists29/12_Tm_1/_article) | encrypted pdf | Cannot validate encrypted document |
| RSP-003 | [Parameters Affecting the Erosive Burning of Solid Rocket Motor](https://www.matec-conferences.org/articles/matecconf/abs/2018/12/matecconf_icmme2018_03001/matecconf_icmme2018_03001.html) | HTTP 403 | HTTP 403: Forbidden |
| RSP-004 | [Erosive Burning Modeling for Solid Propellant Rocket Motor](https://iccee.journals.ekb.eg/article_35124.html) | network error | URLError: <urlopen error timed out> |
| RSP-007 | [Pressure oscillations and instability of working processes in the combustion chambers of solid rocket motors](https://www.sciencedirect.com/science/article/abs/pii/S0094576516308153) | network error | URLError: <urlopen error [Errno -3] Temporary failure in name resolution> |
| RSP-010 | [Two-Dimensional Modeling of Ablation and Pyrolysis with Application to Rocket Nozzles](https://deepblue.lib.umich.edu/handle/2027.42/143121) | not pdf | Response does not begin with a PDF header |
| RSP-016 | [Sounding rockets](https://ntrs.nasa.gov/citations/19650006344) | too large | Declared Content-Length exceeds 40 MB |
| RSP-023 | [Solid Rocket Motor Internal Ballistics Simulation Using Three-Dimensional Grain Burnback](https://www.ideals.illinois.edu/items/14484) | HTTP 403 | HTTP 403: Forbidden |
| RSP-025 | [Advanced Computer Science on Internal Ballistics of Solid Rocket Motors](https://www.jstage.jst.go.jp/article/tastj/8/ists27/8_ists27_Pa_29/_article) | encrypted pdf | Cannot validate encrypted document |
| RSP-027 | [Time-resolved burning of solid fuels for hybrid rocket propulsion](https://www.eucass-proceedings.eu/articles/eucass/abs/2012/01/eucass2p405/eucass2p405.html) | HTTP 403 | HTTP 403: Forbidden |
| RSP-028 | [Approaches to Low Fuel Regression Rate in Hybrid Rocket Engines](https://doi.org/10.1155/2012/649753) | HTTP 403 | HTTP 403: Forbidden |
| RSP-047 | [Development, modeling and testing of thermal protection systems in small, slow-burning solid rocket motors](https://dspace.mit.edu/entities/publication/3532ac0e-4b63-4ec7-9cc3-f550f7ff0444) | HTTP 429 | HTTP 429: Too Many Requests |
| RSP-083 | [Solid rocket booster performance evaluation model. Volume 1: Engineering description](https://ntrs.nasa.gov/citations/19770020237) | too large | Declared Content-Length exceeds 40 MB |
| RSP-086 | [Solid rocket booster performance evaluation model. Volume 4: Program listing](https://ntrs.nasa.gov/citations/19770020240) | too large | Declared Content-Length exceeds 40 MB |
| RSP-105 | [Experimental Modeling of Alumina Particulate in Solid Booster: Final Report](https://elib.dlr.de/136755/) | too large | Declared Content-Length exceeds 40 MB |
| RSP-154 | [Integrated Navigation using MEMS-based Inertial, GPS and Sun Vector Measurements aboard the Spin-Stabilized PMWE-1 Sounding Rocket](https://elib.dlr.de/128022/) | HTTP 401 | HTTP 401: Unauthorized |
| RSP-176 | [Unsupervised Anomaly Detection for Ground Tests of Rocket Propulsion Systems](https://elib.dlr.de/218718/) | HTTP 401 | HTTP 401: Unauthorized |
| RSP-184 | [DLR Global Launch Emission Inventory 2024: Overview and Initial Results](https://elib.dlr.de/222025/) | HTTP 401 | HTTP 401: Unauthorized |
| RSP-185 | [Simulation and Evaluation of Throttleable LOX/LCH4 Rocket Propulsion System Architectures for In-Space Applications](https://elib.dlr.de/219927/) | HTTP 401 | HTTP 401: Unauthorized |
| RSP-187 | [Combustion Dynamics of a Liquid Rocket Engine in subcritical Injection Conditions](https://elib.dlr.de/218742/) | HTTP 401 | HTTP 401: Unauthorized |

## Recommended follow-up order

1. **Correct non-PDF link**: RSP-010 returned an HTML or other non-PDF response even with HTTP 200. Locate an official archive PDF link.
2. **Review source restrictions**: RSP-154, 176, 184, 185, 187 returned HTTP 401. RSP-003, 023, 027, 028 returned HTTP 403; RSP-047 returned HTTP 429. Keep these catalogued without treating them as successful downloaded documents.
3. **Review size-cap exceptions**: RSP-016, 083, 086, 105 were too large for the default 40 MB cap. Their status does not imply the PDFs are invalid. Use separate large-file auditing if research value justifies the bandwidth and time.
4. **Review encrypted PDFs**: RSP-001 and RSP-025 were not readable by the automated PDF parser. Do not bypass publisher restrictions.
5. **Retest transient source errors**: RSP-004 (timeout) and RSP-007 (DNS) need a later source check. Do not infer they have been withdrawn.
6. **Verify identity and full text**: Open a sample of structurally valid PDFs, compare first-page paper titles/authors to the bibliography, and check internal pages before marking `content_verified`.

## Sider reconciliation (separate platform)

A read-only Wisebase audit found **86 file entries** (previously 79). Six requested research PDF filenames were visibly processed:
`19740011276.pdf`, `20040085893.pdf`, `19770020238.pdf`, `19770020239.pdf`, `19770020240.pdf`, and `IAC-18.A2.5.4x44337.pdf`.

Three requested PDFs were not found: `19770020237.pdf`, `20110007984.pdf`, and `EUCASS2019-0241.pdf`. The last link created a separate **HTML authorization-error page entry**, not a valid research PDF. No files were deleted.

**Different evidence levels:** Sider file-list processing and GitHub PDF parsing are independent; neither by itself proves scholarly document identity. See [Sider import history](../metadata/sider_imports.csv) for source-level evidence.

## Automation

[fulltext-audit.yml](../.github/workflows/fulltext-audit.yml) validates all source-listed URLs in six shards, reconciles duplicate/missing IDs, and commits only a result ledger, not PDF bytes. The separate [scheduled rotating downloader](../.github/workflows/collect-pdfs.yml) checks a subset of up to 30 sources per run and retains downloaded PDFs as temporary workflow artifacts.

**Re-run policy:** run the full audit deliberately after significant new catalog additions or source changes; avoid unnecessarily hammering publishers that return rate limits.
