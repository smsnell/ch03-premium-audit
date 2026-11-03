# Draft audit report

Provisional allocations. CSVs must accompany this report and audit-questions.md. Final audit sign-off is not established. Retrieval timestamps are provenance, not proof of a fresh live run.

Case evidence appears once below; full notes, decisions, source paths and SHA-256 fingerprints remain in each linked ledger. Rule provenance and proposal approvals are in [internal-decisions.md](internal-decisions.md).

## Harbor Point Legal

Provisionally accept the reported payroll split; draft; final sign-off not established.

Audit period: 2025-07-07 through 2026-07-05. [Full ledger](ledgers/harbor-point-legal.json).

| Code | Reported | Allocated | Difference |
| --- | --- | --- | --- |
| C-110 | 425148.16 | 425148.16 | 0.00 |

Known register 425148.16 + net adjustments 0.00 = allocated 425148.16. Unknown owner amounts are excluded from this reconciliation and remain completeness gaps.

Allocations and adjustments (application person-level code may be unspecified):

| ID | Employee/payment | Before | Allocated | Net | Reason | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| adjustment-1 | Marcus Adeyemi | code not specified in application 128400.00 | C-110 128400.00 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-2 | Julia Fenwick | code not specified in application 121750.00 | C-110 121750.00 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-3 | Tomas Reyes | code not specified in application 64212.48 | C-110 64212.48 | 0.00 | Explicit evidence-backed work mapping; provisional exception P1-tomas-legal-visits | payroll-register.csv, business-description.md, field-notes.md, guide, site-signin-log.csv, interview-2 |
| adjustment-4 | Ellen Short | code not specified in application 51880.16 | C-110 51880.16 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-5 | Gwen Talbot | code not specified in application 58905.52 | C-110 58905.52 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |

Case-specific evidence (note IDs are stable by input order):

| Note | Subject | Evidence and limits | Sources |
| --- | --- | --- | --- |
| harbor-point-legal-evidence-1 | Source timing and confirmation status | Audit period is July 7, 2025 through July 5, 2026. The field-note visit is after audit end and supplies duty/context evidence; it is not an additional in-period site or ride day. Application code figures are aggregate only; individual application classifications are unspecified. No employer confirmation has been received; source statements and implementation approval are not case confirmation. | business-description.md, application.md, field-notes.md, interview-2 |
| harbor-point-legal-evidence-2 | Marcus Adeyemi / HP-E01 | payroll-register.csv line 2: wages 128400.00; Legal professional duties in the described law office; field notes state court appearances/closings are not job sites and no staff perform physical field work. C-110 under CG-04, subject to confirming off-office professional duties. | payroll-register.csv, business-description.md, field-notes.md, guide |
| harbor-point-legal-evidence-3 | Julia Fenwick / HP-E02 | payroll-register.csv line 3: wages 121750.00; Legal professional duties in the described law office; field notes distinguish courts/closings from jobs and establish no physical field work. C-110 under CG-04, subject to confirming off-office professional duties. | payroll-register.csv, business-description.md, field-notes.md, guide |
| harbor-point-legal-evidence-4 | Tomas Reyes / HP-E03 | payroll-register.csv line 4: wages 64212.48; Legal support, supplemented by the six log entries and Nadia’s 12:26 AM testimony: observed an expert inspection and took litigation notes/photos, not construction. P1 retains C-110 despite office-confined wording; no field trade has been established. | payroll-register.csv, business-description.md, field-notes.md, guide |
| harbor-point-legal-evidence-5 | Ellen Short / HP-E04 | payroll-register.csv line 5: wages 51880.16; Secretarial/correspondence work in the described law office, with field notes establishing no physical field work and no employee sign-ins; CG-04 provisional mapping requires duty confirmation. | payroll-register.csv, business-description.md, field-notes.md, guide |
| harbor-point-legal-evidence-6 | Gwen Talbot / HP-E05 | payroll-register.csv line 6: wages 58905.52; Management/administration of the described law office, with field notes establishing no physical field work and no employee sign-ins; CG-04 provisional mapping requires duty confirmation. | payroll-register.csv, business-description.md, field-notes.md, guide |
| harbor-point-legal-evidence-7 | Tomas Reyes / six visits and identity mapping | site-signin-log.csv lines 2–7 list HP-E03 on 2025-09-16, 2025-10-22, 2025-12-09, 2026-01-28, 2026-03-04, 2026-04-15 at Sallowmere Court Condominiums. Nadia at 12:26 AM identifies inspection observation and litigation notes/photos. The transcript says “Thomas” and a phonetic site variant; context maps these to the unique HP-E03 case, without editing the original transcript. This is not roofing/construction work. Provisionally accept the application’s 425148.16 C-110 employee split; the owner exclusion and professional office exception remain open. | site-signin-log.csv, interview-2, application.md, payroll-register.csv, guide |
| harbor-point-legal-evidence-8 | Catherine Harbor / reported owner exclusion | business-description.md reports an election and omission from the register, but no election form/effective dates are among the freshly listed files. Retain the reported omission only as P4 provisional completeness gap. Pay, duties, field-work status and any additional exposure remain unknown, not zero; 63700.00 is not automatically assigned to an owner of unknown duties. CG-05-first precedence against the working-owner rule is proposed, not confirmed. | business-description.md, guide, interview-2 |

Issues and confirmation status:

| Issue | Subject | Proposed treatment / missing evidence | Amount | Alternative | Status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| P1-tomas-legal-visits | Tomas Reyes | Retain 64212.48 C-110 as a proposed professional-duty exception. Six real visits remain counted; contractor office transfer has no defined field destination for this law office. Confirm legal-support work and acceptance despite CG-04 office wording. | 64212.48 | unknown | open | site-signin-log.csv, field-notes.md, interview-2, guide |
| HP-owner-owner-election | Catherine Harbor | P4: retain reported omission provisionally; obtain election, effective dates, duties and remuneration. Unknown amount is not verified zero. | unknown (not zero) | unknown | open | business-description.md, guide, interview-2 |

Sources (fingerprints and full local paths are in the ledger):

| ID / record | Audience | Retrieved |
| --- | --- | --- |
| [site-signin-log.csv](https://drive.google.com/file/d/1XYS_ajsSQMqxqgKLGtI8t9yZE3d4BSAp/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [payroll-register.csv](https://drive.google.com/file/d/13UaL8k95JkOjoi18ySAZoU5T5qaGb6sF/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [field-notes.md](https://drive.google.com/file/d/13LHYTQQPRLHv41732VtJ_wlPP-_d9sPM/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [business-description.md](https://drive.google.com/file/d/1mjpCGvogGUDfL-Jbo1bQhZZ1R6qtV4p7/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [application.md](https://drive.google.com/file/d/1CpRtyJghao9DSkFNbhLVaRHIwFiuI_ai/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [guide](https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view?usp=drivesdk) | internal | 2026-11-03T06:24:18.728Z |
| [interview-2](local:interviews/interview-2.md) | internal | 2026-11-03T06:28:07.754231+00:00 |

## Bay Crest Exteriors

Provisionally reject the reported payroll split; draft; final sign-off not established.

Audit period: 2025-07-07 through 2026-07-05. [Full ledger](ledgers/bay-crest-exteriors.json).

| Code | Reported | Allocated | Difference |
| --- | --- | --- | --- |
| C-110 | 363970.45 | 44812.35 | -319158.10 |
| R-310 | 177527.60 | 450480.60 | 272953.00 |
| R-320 | 0.00 | 46205.10 | 46205.10 |

Known register 541498.05 + net adjustments 0.00 = allocated 541498.05. Unknown owner amounts are excluded from this reconciliation and remain completeness gaps.

Allocations and adjustments (application person-level code may be unspecified):

| ID | Employee/payment | Before | Allocated | Net | Reason | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| adjustment-1 | Darnell Price | code not specified in application 61240.55 | R-310 61240.55 | 0.00 | 188 unique in-period positive roof days; whole-person allocation | payroll-register.csv, business-description.md, field-notes.md, guide, crew-timesheets.csv, interview-2 |
| adjustment-2 | Kevin Moraes | code not specified in application 58976.20 | R-310 58976.20 | 0.00 | 176 unique in-period positive roof days; whole-person allocation | payroll-register.csv, business-description.md, field-notes.md, guide, crew-timesheets.csv, interview-2 |
| adjustment-3 | Sam Okonjo | code not specified in application 57310.85 | R-310 57310.85 | 0.00 | 201 unique in-period positive roof days; whole-person allocation | payroll-register.csv, business-description.md, field-notes.md, guide, crew-timesheets.csv, interview-2 |
| adjustment-4 | Luis Carrillo | code not specified in application 54880.40 | R-310 54880.40 | 0.00 | 164 unique in-period positive roof days; whole-person allocation | payroll-register.csv, business-description.md, field-notes.md, guide, crew-timesheets.csv, interview-2 |
| adjustment-5 | Brian Tull | code not specified in application 52115.75 | R-310 52115.75 | 0.00 | 152 unique in-period positive roof days; whole-person allocation | payroll-register.csv, business-description.md, field-notes.md, guide, crew-timesheets.csv, interview-2 |
| adjustment-6 | Owen Petrakis | code not specified in application 49607.30 | R-310 49607.30 | 0.00 | 97 unique in-period positive roof days; whole-person allocation | payroll-register.csv, business-description.md, field-notes.md, guide, crew-timesheets.csv, interview-2 |
| adjustment-7 | Rafael Duarte | code not specified in application 47918.65 | R-310 47918.65 | 0.00 | 15 unique in-period positive roof days; whole-person allocation | payroll-register.csv, business-description.md, field-notes.md, guide, crew-timesheets.csv, interview-2 |
| adjustment-8 | Jamal Whitfield | code not specified in application 46205.10 | R-320 46205.10 | 0.00 | 9 unique in-period positive roof days; whole-person allocation | payroll-register.csv, business-description.md, field-notes.md, guide, crew-timesheets.csv, interview-2 |
| adjustment-9 | Teresa Lindqvist | code not specified in application 68430.90 | R-310 68430.90 | 0.00 | 9 unique in-period site days; entire pay to governing field code before office transfers (P2) | payroll-register.csv, business-description.md, field-notes.md, guide, interview-2, site-signin-log.csv |
| adjustment-10 | Nora Beckett | code not specified in application 44812.35 | C-110 44812.35 | 0.00 | 0 unique in-period site days | payroll-register.csv, business-description.md, field-notes.md, guide, interview-2 |

Case-specific evidence (note IDs are stable by input order):

| Note | Subject | Evidence and limits | Sources |
| --- | --- | --- | --- |
| bay-crest-exteriors-evidence-1 | Source timing and confirmation status | Audit period is July 7, 2025 through July 5, 2026. The field-note visit is after audit end and supplies duty/context evidence; it is not an additional in-period site or ride day. Application code figures are aggregate only; individual application classifications are unspecified. No employer confirmation has been received; source statements and implementation approval are not case confirmation. | business-description.md, application.md, field-notes.md, interview-2 |
| bay-crest-exteriors-evidence-2 | Darnell Price / BC-E01 | payroll-register.csv line 2: wages 61240.55; Crew time records show actual roofing, siding and/or gutter installation at the jobs; apply the specific whole-worker roof-day rule, not title or hour proportions. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-3 | Kevin Moraes / BC-E02 | payroll-register.csv line 3: wages 58976.20; Crew time records show actual roofing, siding and/or gutter installation at the jobs; apply the specific whole-worker roof-day rule, not title or hour proportions. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-4 | Sam Okonjo / BC-E03 | payroll-register.csv line 4: wages 57310.85; Crew time records show actual roofing, siding and/or gutter installation at the jobs; apply the specific whole-worker roof-day rule, not title or hour proportions. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-5 | Luis Carrillo / BC-E04 | payroll-register.csv line 5: wages 54880.40; Crew time records show actual roofing, siding and/or gutter installation at the jobs; apply the specific whole-worker roof-day rule, not title or hour proportions. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-6 | Brian Tull / BC-E05 | payroll-register.csv line 6: wages 52115.75; Crew time records show actual roofing, siding and/or gutter installation at the jobs; apply the specific whole-worker roof-day rule, not title or hour proportions. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-7 | Owen Petrakis / BC-E06 | payroll-register.csv line 7: wages 49607.30; Crew time records show actual roofing, siding and/or gutter installation at the jobs; apply the specific whole-worker roof-day rule, not title or hour proportions. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-8 | Rafael Duarte / BC-E07 | payroll-register.csv line 8: wages 47918.65; Crew time records show actual roofing, siding and/or gutter installation at the jobs; apply the specific whole-worker roof-day rule, not title or hour proportions. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-9 | Jamal Whitfield / BC-E08 | payroll-register.csv line 9: wages 46205.10; Crew time records show actual roofing, siding and/or gutter installation at the jobs; apply the specific whole-worker roof-day rule, not title or hour proportions. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-10 | Teresa Lindqvist / BC-E09 | payroll-register.csv line 10: wages 68430.90; Field notes identify estimator measuring houses; sign-in log establishes visits. Contractor office rule sends entire wages to the largest corrected field code at five days. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-11 | Nora Beckett / BC-E10 | payroll-register.csv line 11: wages 44812.35; Field notes explicitly place the bookkeeper in the office; no sign-in entries. Retain clerical under CG-04, subject to completeness confirmation. | payroll-register.csv, business-description.md, field-notes.md, guide |
| bay-crest-exteriors-evidence-12 | Nonemployee visitor | Blank employee-ID sign-in excluded from employee day counts: 2025-10-09 County inspector at Arnold re-roof. | site-signin-log.csv |
| bay-crest-exteriors-evidence-13 | Darnell Price / actual crew work | crew-timesheets.csv filtered employee_id=BC-E01: 222 work rows, lines 2–1721, 188 distinct positive-time roofing dates; all 61240.55 goes to R-310 under Nadia’s 12:27 AM rule. Roofing dates range 2025-07-07–2026-07-01. | crew-timesheets.csv, payroll-register.csv, interview-2 |
| bay-crest-exteriors-evidence-14 | Kevin Moraes / actual crew work | crew-timesheets.csv filtered employee_id=BC-E02: 217 work rows, lines 3–1714, 176 distinct positive-time roofing dates; all 58976.20 goes to R-310 under Nadia’s 12:27 AM rule. Roofing dates range 2025-07-07–2026-06-26. | crew-timesheets.csv, payroll-register.csv, interview-2 |
| bay-crest-exteriors-evidence-15 | Sam Okonjo / actual crew work | crew-timesheets.csv filtered employee_id=BC-E03: 219 work rows, lines 4–1722, 201 distinct positive-time roofing dates; all 57310.85 goes to R-310 under Nadia’s 12:27 AM rule. Roofing dates range 2025-07-07–2026-07-03. | crew-timesheets.csv, payroll-register.csv, interview-2 |
| bay-crest-exteriors-evidence-16 | Luis Carrillo / actual crew work | crew-timesheets.csv filtered employee_id=BC-E04: 216 work rows, lines 5–1723, 164 distinct positive-time roofing dates; all 54880.40 goes to R-310 under Nadia’s 12:27 AM rule. Roofing dates range 2025-07-07–2026-07-03. | crew-timesheets.csv, payroll-register.csv, interview-2 |
| bay-crest-exteriors-evidence-17 | Brian Tull / actual crew work | crew-timesheets.csv filtered employee_id=BC-E05: 212 work rows, lines 6–1724, 152 distinct positive-time roofing dates; all 52115.75 goes to R-310 under Nadia’s 12:27 AM rule. Roofing dates range 2025-07-07–2026-07-02. | crew-timesheets.csv, payroll-register.csv, interview-2 |
| bay-crest-exteriors-evidence-18 | Owen Petrakis / actual crew work | crew-timesheets.csv filtered employee_id=BC-E06: 215 work rows, lines 7–1725, 97 distinct positive-time roofing dates; all 49607.30 goes to R-310 under Nadia’s 12:27 AM rule. Roofing dates range 2025-07-07–2026-07-03. | crew-timesheets.csv, payroll-register.csv, interview-2 |
| bay-crest-exteriors-evidence-19 | Rafael Duarte / actual crew work | crew-timesheets.csv filtered employee_id=BC-E07: 211 work rows, lines 8–1726, 15 distinct positive-time roofing dates; all 47918.65 goes to R-310 under Nadia’s 12:27 AM rule. Roofing dates range 2025-08-18–2026-05-27. Exact roofing dates: 2025-08-18, 2025-09-19, 2025-09-29, 2025-09-30, 2025-10-01, 2025-10-10, 2025-11-04, 2025-12-18, 2025-12-22, 2025-12-30, 2026-01-19, 2026-04-10, 2026-05-06, 2026-05-12, 2026-05-27. | crew-timesheets.csv, payroll-register.csv, interview-2 |
| bay-crest-exteriors-evidence-20 | Jamal Whitfield / actual crew work | crew-timesheets.csv filtered employee_id=BC-E08: 214 work rows, lines 9–1727, 9 distinct positive-time roofing dates; all 46205.10 goes to R-320 under Nadia’s 12:27 AM rule. Roofing dates range 2025-07-10–2026-04-21. Exact roofing dates: 2025-07-10, 2025-08-27, 2025-09-01, 2025-09-08, 2025-12-25, 2026-01-05, 2026-01-30, 2026-02-06, 2026-04-21. | crew-timesheets.csv, payroll-register.csv, interview-2 |
| bay-crest-exteriors-evidence-21 | Teresa Lindqvist / governing-code transfer | BC-E09 has nine sign-ins on 2025-07-24, 2025-09-02, 2025-11-17, 2025-11-26, 2025-12-25, 2026-03-04, 2026-05-26, 2026-06-03, 2026-07-01. Corrected direct crew payroll is 382049.70 R-310 versus 46205.10 R-320 before office transfer, so all 68430.90 moves to R-310; Nora Beckett’s 44812.35 remains C-110 with zero sign-ins. Reject APP-BCE-0217: job work and day counts contradict the claimed seven clerical people. Interview “Baycrest Interiors”/“Therese” are contextual mappings to Bay Crest Exteriors/BC-E09; original wording is preserved. | site-signin-log.csv, crew-timesheets.csv, payroll-register.csv, application.md, field-notes.md, interview-2 |
| bay-crest-exteriors-evidence-22 | Philip Crestwood / reported owner exclusion | business-description.md reports an election and omission from the register, but no election form/effective dates are among the freshly listed files. Retain the reported omission only as P4 provisional completeness gap. Pay, duties, field-work status and any additional exposure remain unknown, not zero; 63700.00 is not automatically assigned to an owner of unknown duties. CG-05-first precedence against the working-owner rule is proposed, not confirmed. | business-description.md, guide, interview-2 |

Issues and confirmation status:

| Issue | Subject | Proposed treatment / missing evidence | Amount | Alternative | Status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| P2-count-order | Bay Crest crew and office transfer | Distinct positive roofing dates and corrected field totals before office transfers are proposed P2 conventions; roofing is governing on current records. | 68430.90 | unknown | open | crew-timesheets.csv, site-signin-log.csv, interview-2 |
| BC-owner-owner-election | Philip Crestwood | P4: retain reported omission provisionally; obtain election, effective dates, duties and remuneration. Unknown amount is not verified zero. | unknown (not zero) | unknown | open | business-description.md, guide, interview-2 |

Sources (fingerprints and full local paths are in the ledger):

| ID / record | Audience | Retrieved |
| --- | --- | --- |
| [crew-timesheets.csv](https://drive.google.com/file/d/1JmQFTWBYEeGW0nqiVHn8VqVUaDqym2MG/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [site-signin-log.csv](https://drive.google.com/file/d/1MATgZl09ZeMk91mLBl8Y9TfDLEsGZxYE/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [payroll-register.csv](https://drive.google.com/file/d/1LNA3cclH6SaZDCWRljlZYnpFTnsPdkox/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [field-notes.md](https://drive.google.com/file/d/10VpsaBvK25j7W8CuwW5jVOR0BCQG5pqB/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [business-description.md](https://drive.google.com/file/d/1SHcro76JYUSRvD3OocHDwJh8DbsDEU29/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [application.md](https://drive.google.com/file/d/1vNdqk0QSSVsSBTJY2aAVJSWkh6XTw8-M/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [guide](https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view?usp=drivesdk) | internal | 2026-11-03T06:24:18.728Z |
| [interview-2](local:interviews/interview-2.md) | internal | 2026-11-03T06:28:07.754231+00:00 |

## Severn Homebuilders

Provisionally reject the reported payroll split; draft; final sign-off not established.

Audit period: 2025-07-07 through 2026-07-05. [Full ledger](ledgers/severn-homebuilders.json).

| Code | Reported | Allocated | Difference |
| --- | --- | --- | --- |
| C-110 | 177209.40 | 117368.70 | -59840.70 |
| H-420 | 284670.30 | 369204.39 | 84534.09 |
| R-310 | 0.00 | 27567.39 | 27567.39 |

Known register 461879.70 + net adjustments 52260.78 = allocated 514140.48. Unknown owner amounts are excluded from this reconciliation and remain completeness gaps.

Allocations and adjustments (application person-level code may be unspecified):

| ID | Employee/payment | Before | Allocated | Net | Reason | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| adjustment-1 | Garrett Holm | code not specified in application 66315.40 | H-420 66315.40 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-2 | Victor Amadi | code not specified in application 62780.15 | H-420 62780.15 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-3 | Peter Kowal | code not specified in application 58442.60 | H-420 58442.60 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-4 | Andre Sutton | code not specified in application 49905.85 | H-420 49905.85 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-5 | Colin Rusk | code not specified in application 47226.30 | H-420 47226.30 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-6 | Kent Island Roofing invoice SV-KEN-01 | — | R-310 8580.00 | 8580.00 | No verified matching full-period certificate: 60% per invoice, half-up cents (P3/P7) | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| adjustment-7 | Tidewater Drywall invoice SV-TID-01 | — | H-420 10944.33 | 10944.33 | No verified matching full-period certificate: 60% per invoice, half-up cents (P3/P7) | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| adjustment-8 | Tidewater Drywall invoice SV-TID-02 | — | H-420 13749.06 | 13749.06 | No verified matching full-period certificate: 60% per invoice, half-up cents (P3/P7) | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| adjustment-9 | Kent Island Roofing invoice SV-KEN-02 | — | R-310 11928.27 | 11928.27 | No verified matching full-period certificate: 60% per invoice, half-up cents (P3/P7) | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| adjustment-10 | Kent Island Roofing invoice SV-KEN-03 | — | R-310 7059.12 | 7059.12 | No verified matching full-period certificate: 60% per invoice, half-up cents (P3/P7) | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| adjustment-11 | Marissa Gale | code not specified in application 71250.45 | C-110 71250.45 | 0.00 | 4 unique in-period site days | payroll-register.csv, business-description.md, field-notes.md, guide, interview-2, site-signin-log.csv |
| adjustment-12 | Dana Whitcomb | code not specified in application 59840.70 | H-420 59840.70 | 0.00 | 11 unique in-period site days; entire pay to governing field code before office transfers (P2) | payroll-register.csv, business-description.md, field-notes.md, guide, interview-2, site-signin-log.csv |
| adjustment-13 | Helen Ostrow | code not specified in application 46118.25 | C-110 46118.25 | 0.00 | 0 unique in-period site days | payroll-register.csv, business-description.md, field-notes.md, guide, interview-2 |

Case-specific evidence (note IDs are stable by input order):

| Note | Subject | Evidence and limits | Sources |
| --- | --- | --- | --- |
| severn-homebuilders-evidence-1 | Source timing and confirmation status | Audit period is July 7, 2025 through July 5, 2026. The field-note visit is after audit end and supplies duty/context evidence; it is not an additional in-period site or ride day. Application code figures are aggregate only; individual application classifications are unspecified. No employer confirmation has been received; source statements and implementation approval are not case confirmation. | business-description.md, application.md, field-notes.md, interview-2 |
| severn-homebuilders-evidence-2 | Garrett Holm / SH-E01 | payroll-register.csv line 2: wages 66315.40; Own crew performs residential framing, drywall, finish carpentry and site labor per business description; consistent with field notes describing houses under construction and no evidence of separate employee roofing/electrical trades. CG-15 mapping remains subject to employee-duty confirmation. | payroll-register.csv, business-description.md, field-notes.md, guide |
| severn-homebuilders-evidence-3 | Victor Amadi / SH-E02 | payroll-register.csv line 3: wages 62780.15; Own crew performs residential framing, drywall, finish carpentry and site labor per business description; consistent with field notes describing houses under construction and no evidence of separate employee roofing/electrical trades. CG-15 mapping remains subject to employee-duty confirmation. | payroll-register.csv, business-description.md, field-notes.md, guide |
| severn-homebuilders-evidence-4 | Peter Kowal / SH-E03 | payroll-register.csv line 4: wages 58442.60; Own crew performs residential framing, drywall, finish carpentry and site labor per business description; consistent with field notes describing houses under construction and no evidence of separate employee roofing/electrical trades. CG-15 mapping remains subject to employee-duty confirmation. | payroll-register.csv, business-description.md, field-notes.md, guide |
| severn-homebuilders-evidence-5 | Andre Sutton / SH-E04 | payroll-register.csv line 5: wages 49905.85; Own crew performs residential framing, drywall, finish carpentry and site labor per business description; consistent with field notes describing houses under construction and no evidence of separate employee roofing/electrical trades. CG-15 mapping remains subject to employee-duty confirmation. | payroll-register.csv, business-description.md, field-notes.md, guide |
| severn-homebuilders-evidence-6 | Colin Rusk / SH-E05 | payroll-register.csv line 6: wages 47226.30; Own crew performs residential framing, drywall, finish carpentry and site labor per business description; consistent with field notes describing houses under construction and no evidence of separate employee roofing/electrical trades. CG-15 mapping remains subject to employee-duty confirmation. | payroll-register.csv, business-description.md, field-notes.md, guide |
| severn-homebuilders-evidence-7 | Marissa Gale / SH-E06 | payroll-register.csv line 7: wages 71250.45; Field notes identify estimator’s occasional measuring visits; four logged days permit whole-pay C-110 under contractor office rule. | payroll-register.csv, business-description.md, field-notes.md, guide |
| severn-homebuilders-evidence-8 | Dana Whitcomb / SH-E07 | payroll-register.csv line 8: wages 59840.70; Field notes identify material/paperwork deliveries and inspector meetings at sites; eleven logged days move whole pay to governing H-420, despite “errands” description. | payroll-register.csv, business-description.md, field-notes.md, guide |
| severn-homebuilders-evidence-9 | Helen Ostrow / SH-E08 | payroll-register.csv line 9: wages 46118.25; Field notes explicitly state bookkeeper stays in office; no employee sign-ins, so CG-04 clerical. | payroll-register.csv, business-description.md, field-notes.md, guide |
| severn-homebuilders-evidence-10 | Nonemployee visitor | Blank employee-ID sign-in excluded from employee day counts: 2025-12-02 County inspector at Lot 7 Mill Pond Rd. | site-signin-log.csv |
| severn-homebuilders-evidence-11 | Marissa Gale / office day count | site-signin-log.csv employee_id=SH-E06: 4 distinct dates: 2025-07-24, 2026-01-16, 2026-03-24, 2026-04-21. Whole pay 71250.45 remains C-110. | site-signin-log.csv, payroll-register.csv, field-notes.md, interview-2 |
| severn-homebuilders-evidence-12 | Dana Whitcomb / office day count | site-signin-log.csv employee_id=SH-E07: 11 distinct dates: 2025-09-17, 2025-09-19, 2025-10-02, 2025-10-17, 2025-11-14, 2026-01-08, 2026-01-14, 2026-01-16, 2026-03-04, 2026-06-16, 2026-06-23. Whole pay 59840.70 moves to H-420. | site-signin-log.csv, payroll-register.csv, field-notes.md, interview-2 |
| severn-homebuilders-evidence-13 | Helen Ostrow / office day count | site-signin-log.csv employee_id=SH-E08: 0 distinct dates: none. Whole pay 46118.25 remains C-110. | site-signin-log.csv, payroll-register.csv, field-notes.md, interview-2 |
| severn-homebuilders-evidence-14 | Tenbury Ridge Framing Co. / SV-TRF-01 | subcontractor-payments.csv line 2: 2025-08-22, framing, payment 21480.00; Exact-name MD-WC-448201 covers 2025-06-01–2026-12-31, including the full audit period; no addition. Provisional payroll addition 0.00 to H-420; round 60% per payment half-up to cents (P7). | subcontractor-payments.csv, insurance-certificates.csv, interview-2, guide |
| severn-homebuilders-evidence-15 | Kent Island Roofing / SV-KEN-01 | subcontractor-payments.csv line 3: 2025-09-12, roofing, payment 14300.00; Payment names Kent Island Roofing, certificate names Kent Island Roofing & Siding LLC; identity is unconfirmed and certificate MD-WC-517736 ends 2026-01-31, short of audit end even if identity were proved. Full-period coverage rule applies even to September payment. Provisional payroll addition 8580.00 to R-310; round 60% per payment half-up to cents (P7). | subcontractor-payments.csv, insurance-certificates.csv, interview-2, guide |
| severn-homebuilders-evidence-16 | Tidewater Drywall / SV-TID-01 | subcontractor-payments.csv line 4: 2025-10-03, drywall, payment 18240.55; No Tidewater certificate appears in the complete insurance-certificates.csv. Provisional payroll addition 10944.33 to H-420; round 60% per payment half-up to cents (P7). | subcontractor-payments.csv, insurance-certificates.csv, interview-2, guide |
| severn-homebuilders-evidence-17 | Tenbury Ridge Framing Co. / SV-TRF-02 | subcontractor-payments.csv line 5: 2025-11-14, framing, payment 18925.50; Exact-name MD-WC-448201 covers 2025-06-01–2026-12-31, including the full audit period; no addition. Provisional payroll addition 0.00 to H-420; round 60% per payment half-up to cents (P7). | subcontractor-payments.csv, insurance-certificates.csv, interview-2, guide |
| severn-homebuilders-evidence-18 | Tidewater Drywall / SV-TID-02 | subcontractor-payments.csv line 6: 2026-02-27, drywall, payment 22915.10; No Tidewater certificate appears in the complete insurance-certificates.csv. Provisional payroll addition 13749.06 to H-420; round 60% per payment half-up to cents (P7). | subcontractor-payments.csv, insurance-certificates.csv, interview-2, guide |
| severn-homebuilders-evidence-19 | Kent Island Roofing / SV-KEN-02 | subcontractor-payments.csv line 7: 2026-03-20, roofing, payment 19880.45; Payment names Kent Island Roofing, certificate names Kent Island Roofing & Siding LLC; identity is unconfirmed and certificate MD-WC-517736 ends 2026-01-31, short of audit end even if identity were proved. Full-period coverage rule applies even to September payment. Provisional payroll addition 11928.27 to R-310; round 60% per payment half-up to cents (P7). | subcontractor-payments.csv, insurance-certificates.csv, interview-2, guide |
| severn-homebuilders-evidence-20 | Tenbury Ridge Framing Co. / SV-TRF-03 | subcontractor-payments.csv line 8: 2026-04-03, framing, payment 24610.25; Exact-name MD-WC-448201 covers 2025-06-01–2026-12-31, including the full audit period; no addition. Provisional payroll addition 0.00 to H-420; round 60% per payment half-up to cents (P7). | subcontractor-payments.csv, insurance-certificates.csv, interview-2, guide |
| severn-homebuilders-evidence-21 | Kent Island Roofing / SV-KEN-03 | subcontractor-payments.csv line 9: 2026-05-08, roofing, payment 11765.20; Payment names Kent Island Roofing, certificate names Kent Island Roofing & Siding LLC; identity is unconfirmed and certificate MD-WC-517736 ends 2026-01-31, short of audit end even if identity were proved. Full-period coverage rule applies even to September payment. Provisional payroll addition 7059.12 to R-310; round 60% per payment half-up to cents (P7). | subcontractor-payments.csv, insurance-certificates.csv, interview-2, guide |
| severn-homebuilders-evidence-23 | Martin Severn / reported owner exclusion | business-description.md reports an election and omission from the register, but no election form/effective dates are among the freshly listed files. Retain the reported omission only as P4 provisional completeness gap. Pay, duties, field-work status and any additional exposure remain unknown, not zero; 63700.00 is not automatically assigned to an owner of unknown duties. CG-05-first precedence against the working-owner rule is proposed, not confirmed. | business-description.md, guide, interview-2 |

Issues and confirmation status:

| Issue | Subject | Proposed treatment / missing evidence | Amount | Alternative | Status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| P3-kent-identity | Kent Island Roofing | No automatic alias to Kent Island Roofing & Siding LLC. Include 60% of all three payments; listed certificate would still fail full-period test even if names match. Obtain legal-identity and whole-period coverage evidence. | 27567.39 | 0.00 | open | insurance-certificates.csv, subcontractor-payments.csv, interview-2 |
| P2-governing-order | Dana Whitcomb | Compare corrected field payroll including supported trade additions before office transfers; H-420 governs, so transfer all 59840.70. | 59840.70 | unknown | open | payroll-register.csv, subcontractor-payments.csv, site-signin-log.csv, interview-2 |
| SH-owner-owner-election | Martin Severn | P4: retain reported omission provisionally; obtain election, effective dates, duties and remuneration. Unknown amount is not verified zero. | unknown (not zero) | unknown | open | business-description.md, guide, interview-2 |
| SV-KEN-01-coverage | Kent Island Roofing invoice SV-KEN-01 | Confirm legal identity, trade and full-period coverage; reverse only on sufficient evidence. | 8580.00 | 0.00 | open | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| SV-TID-01-coverage | Tidewater Drywall invoice SV-TID-01 | Confirm legal identity, trade and full-period coverage; reverse only on sufficient evidence. | 10944.33 | 0.00 | open | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| SV-TID-02-coverage | Tidewater Drywall invoice SV-TID-02 | Confirm legal identity, trade and full-period coverage; reverse only on sufficient evidence. | 13749.06 | 0.00 | open | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| SV-KEN-02-coverage | Kent Island Roofing invoice SV-KEN-02 | Confirm legal identity, trade and full-period coverage; reverse only on sufficient evidence. | 11928.27 | 0.00 | open | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |
| SV-KEN-03-coverage | Kent Island Roofing invoice SV-KEN-03 | Confirm legal identity, trade and full-period coverage; reverse only on sufficient evidence. | 7059.12 | 0.00 | open | subcontractor-payments.csv, insurance-certificates.csv, guide, interview-2 |

Sources (fingerprints and full local paths are in the ledger):

| ID / record | Audience | Retrieved |
| --- | --- | --- |
| [subcontractor-payments.csv](https://drive.google.com/file/d/1aGYgGe_OuDtWqNxLrkwuPSFCnsiVN3zw/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [site-signin-log.csv](https://drive.google.com/file/d/1kKrXNEVrrbAhcXcZltxfiagYqN-5g8WE/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [payroll-register.csv](https://drive.google.com/file/d/1aSBzZCWLFZJUTvLkz0hDPqk-flSWwOpU/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [insurance-certificates.csv](https://drive.google.com/file/d/1_oolMVpZAkbDIGqkMDxreysfcQR-nlJN/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [field-notes.md](https://drive.google.com/file/d/1t04ez9kiXyK7cCaGIBAMi-DVUvML8OID/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [business-description.md](https://drive.google.com/file/d/1roIR4kXhtGFaas5i2dmIdLY62LxF0tVy/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [application.md](https://drive.google.com/file/d/1xgtCvPL9ke2MMfS3Q3_WnKQCi50Q0PJD/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [guide](https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view?usp=drivesdk) | internal | 2026-11-03T06:24:18.728Z |
| [interview-2](local:interviews/interview-2.md) | internal | 2026-11-03T06:28:07.754231+00:00 |

## Patuxent Electric

Provisionally reject the reported payroll split; draft; final sign-off not established.

Audit period: 2025-07-07 through 2026-07-05. [Full ledger](ledgers/patuxent-electric.json).

| Code | Reported | Allocated | Difference |
| --- | --- | --- | --- |
| C-110 | 161905.60 | 43905.60 | -118000.00 |
| E-510 | 306024.85 | 372274.85 | 66250.00 |

Known register 467930.45 + net adjustments -51750.00 = allocated 416180.45. Unknown owner amounts are excluded from this reconciliation and remain completeness gaps.

Allocations and adjustments (application person-level code may be unspecified):

| ID | Employee/payment | Before | Allocated | Net | Reason | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| adjustment-1 | Raymond Dunmore | code not specified in application 118000.00 | E-510 63700.00 | -54300.00 | Included working owner with field duties: fixed period basis | payroll-register.csv, business-description.md, field-notes.md, guide, site-signin-log.csv, interview-2 |
| adjustment-2 | Curtis Bell | code not specified in application 72410.35 | E-510 72410.35 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-3 | Hector Ruiz | code not specified in application 69855.90 | E-510 69855.90 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-4 | Aaron Weiss | code not specified in application 64120.65 | E-510 64120.65 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-5 | Tyrone Banks | code not specified in application 58377.20 | E-510 58377.20 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-6 | Kyle Brandt | code not specified in application 41260.75 | E-510 41260.75 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-7 | Linda Marsh | code not specified in application 43905.60 | C-110 43905.60 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-8 | Curtis Bell payment PE-E02-travel | — | E-510 720.00 | 720.00 | $47 per recorded out-of-town day; only excess included | payroll-register.csv, field-notes.md, business-description.md, guide, interview-2 |
| adjustment-9 | Hector Ruiz payment PE-E03-travel | — | E-510 720.00 | 720.00 | $47 per recorded out-of-town day; only excess included | payroll-register.csv, field-notes.md, business-description.md, guide, interview-2 |
| adjustment-10 | Aaron Weiss payment PE-E04-travel | — | E-510 720.00 | 720.00 | $47 per recorded out-of-town day; only excess included | payroll-register.csv, field-notes.md, business-description.md, guide, interview-2 |
| adjustment-11 | Kyle Brandt payment PE-E06-travel | — | E-510 390.00 | 390.00 | P5: zero-day payment provisionally included absent documented expense basis | payroll-register.csv, field-notes.md, business-description.md, guide, interview-2 |

Case-specific evidence (note IDs are stable by input order):

| Note | Subject | Evidence and limits | Sources |
| --- | --- | --- | --- |
| patuxent-electric-evidence-1 | Source timing and confirmation status | Audit period is July 7, 2025 through July 5, 2026. The field-note visit is after audit end and supplies duty/context evidence; it is not an additional in-period site or ride day. Application code figures are aggregate only; individual application classifications are unspecified. No employer confirmation has been received; source statements and implementation approval are not case confirmation. | business-description.md, application.md, field-notes.md, interview-2 |
| patuxent-electric-evidence-2 | Raymond Dunmore / PE-E01 | payroll-register.csv line 2: wages 118000.00; Business description says included owner with no election; field notes establish leading crews and personally pulling wire. In-period sign-ins corroborate field presence; replace actual 118000.00 with fixed 63700.00 E-510 under Nadia’s 11:28 PM rule. | payroll-register.csv, business-description.md, field-notes.md, guide |
| patuxent-electric-evidence-3 | Curtis Bell / PE-E02 | payroll-register.csv line 3: wages 72410.35; Business description establishes residential/light-commercial wiring; field notes describe electricians on wiring crews and out-of-town electrical jobs. CG-21 actual-trade mapping, subject to confirming individual work and period. | payroll-register.csv, business-description.md, field-notes.md, guide |
| patuxent-electric-evidence-4 | Hector Ruiz / PE-E03 | payroll-register.csv line 4: wages 69855.90; Business description establishes residential/light-commercial wiring; field notes describe electricians on wiring crews and out-of-town electrical jobs. CG-21 actual-trade mapping, subject to confirming individual work and period. | payroll-register.csv, business-description.md, field-notes.md, guide |
| patuxent-electric-evidence-5 | Aaron Weiss / PE-E04 | payroll-register.csv line 5: wages 64120.65; Business description establishes residential/light-commercial wiring; field notes describe electricians on wiring crews and out-of-town electrical jobs. CG-21 actual-trade mapping, subject to confirming individual work and period. | payroll-register.csv, business-description.md, field-notes.md, guide |
| patuxent-electric-evidence-6 | Tyrone Banks / PE-E05 | payroll-register.csv line 6: wages 58377.20; Business description establishes residential/light-commercial wiring; field notes describe electricians on wiring crews and out-of-town electrical jobs. CG-21 actual-trade mapping, subject to confirming individual work and period. | payroll-register.csv, business-description.md, field-notes.md, guide |
| patuxent-electric-evidence-7 | Kyle Brandt / PE-E06 | payroll-register.csv line 7: wages 41260.75; Business description establishes residential/light-commercial wiring; field notes describe electricians on wiring crews and out-of-town electrical jobs. CG-21 actual-trade mapping, subject to confirming individual work and period. | payroll-register.csv, business-description.md, field-notes.md, guide |
| patuxent-electric-evidence-8 | Linda Marsh / PE-E07 | payroll-register.csv line 8: wages 43905.60; Field notes explicitly state Linda runs the office and never goes to jobs; C-110 under CG-04. | payroll-register.csv, business-description.md, field-notes.md, guide |
| patuxent-electric-evidence-9 | Raymond Dunmore / owner basis | payroll-register.csv line 2 pays 118000.00; business-description.md says no election; field-notes.md says he personally pulls wire. site-signin-log.csv lines 2–215 contain 214 distinct PE-E01 dates, 2025-07-07 through 2026-07-03. Fixed working-owner basis replaces his wages with 63700.00 E-510, reducing known payroll 54300.00. No election precedence exception is needed on these facts; source duty continuity and no-election statement need confirmation. | payroll-register.csv, business-description.md, field-notes.md, site-signin-log.csv, interview-2, guide |
| patuxent-electric-evidence-10 | Curtis Bell / allowance PE-E02-travel | payroll-register.csv line 3: allowance 2600.00, recorded out-of-town days 40; 47.00 × 40 = 1880.00 cap, included excess 720.00 E-510. No separate expense log/documented reimbursement is in the complete employer folder. Flat allowance above the day cap is remuneration under the house practice. | payroll-register.csv, field-notes.md, interview-2, guide |
| patuxent-electric-evidence-11 | Hector Ruiz / allowance PE-E03-travel | payroll-register.csv line 4: allowance 2600.00, recorded out-of-town days 40; 47.00 × 40 = 1880.00 cap, included excess 720.00 E-510. No separate expense log/documented reimbursement is in the complete employer folder. Flat allowance above the day cap is remuneration under the house practice. | payroll-register.csv, field-notes.md, interview-2, guide |
| patuxent-electric-evidence-12 | Aaron Weiss / allowance PE-E04-travel | payroll-register.csv line 5: allowance 2600.00, recorded out-of-town days 40; 47.00 × 40 = 1880.00 cap, included excess 720.00 E-510. No separate expense log/documented reimbursement is in the complete employer folder. Flat allowance above the day cap is remuneration under the house practice. | payroll-register.csv, field-notes.md, interview-2, guide |
| patuxent-electric-evidence-13 | Tyrone Banks / allowance PE-E05-travel | payroll-register.csv line 6: allowance 1034.00, recorded out-of-town days 22; 47.00 × 22 = 1034.00 cap, included excess 0.00 E-510. At the cap, so all 1034.00 is excluded. | payroll-register.csv, field-notes.md, interview-2, guide |
| patuxent-electric-evidence-14 | Kyle Brandt / allowance PE-E06-travel | payroll-register.csv line 7: allowance 390.00, recorded out-of-town days 0; 47.00 × 0 = 0.00 cap, included excess 390.00 E-510. No separate expense log/documented reimbursement is in the complete employer folder. Zero days do not support an allowance exclusion; P5 provisionally includes 390.00 under CG-03 and awaits purpose/expense/corrected travel evidence. | payroll-register.csv, field-notes.md, interview-2, guide |

Issues and confirmation status:

| Issue | Subject | Proposed treatment / missing evidence | Amount | Alternative | Status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| PE-E06-travel-zero-days | Kyle Brandt payment PE-E06-travel | Obtain purpose, expense log and corrected travel days; zero-day treatment is proposed. | 390.00 | 0.00 | open | payroll-register.csv, field-notes.md, business-description.md, guide, interview-2 |

Sources (fingerprints and full local paths are in the ledger):

| ID / record | Audience | Retrieved |
| --- | --- | --- |
| [site-signin-log.csv](https://drive.google.com/file/d/1zzZY5CVt3pokymdMxhrY-h3KoW2ccvar/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [payroll-register.csv](https://drive.google.com/file/d/1rpnsNOubZb5fCpElBk8wPAU5lf8LqT6S/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [field-notes.md](https://drive.google.com/file/d/1ffTc3p664aUqgxSYHxAHXLHj0wGkemBh/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [business-description.md](https://drive.google.com/file/d/1rlhBvA_oIrQZx4W0yUpHC5Fhp39dSZYA/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.140Z |
| [application.md](https://drive.google.com/file/d/1PeZVBAsMdsAHNreQLoFBrhJ3L2f3ro9O/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [guide](https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view?usp=drivesdk) | internal | 2026-11-03T06:24:18.728Z |
| [interview-2](local:interviews/interview-2.md) | internal | 2026-11-03T06:28:07.754231+00:00 |

## Annapolis Courier

Provisionally reject the reported payroll split; draft; final sign-off not established.

Audit period: 2025-07-07 through 2026-07-05. [Full ledger](ledgers/annapolis-courier.json).

| Code | Reported | Allocated | Difference |
| --- | --- | --- | --- |
| C-110 | 130629.20 | 107820.45 | -22808.75 |
| T-610 | 153886.20 | 176694.95 | 22808.75 |

Known register 284515.40 + net adjustments 0.00 = allocated 284515.40. Unknown owner amounts are excluded from this reconciliation and remain completeness gaps.

Allocations and adjustments (application person-level code may be unspecified):

| ID | Employee/payment | Before | Allocated | Net | Reason | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| adjustment-1 | Derek Nolan | code not specified in application 52956.80 | T-610 52956.80 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide, weekly-payroll.csv, route-log.csv |
| adjustment-2 | Maria Santos | code not specified in application 51311.00 | T-610 51311.00 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide, weekly-payroll.csv, route-log.csv |
| adjustment-3 | Felix Grant | code not specified in application 49618.40 | T-610 49618.40 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide, weekly-payroll.csv, route-log.csv |
| adjustment-4 | Lena Ortiz | code not specified in application 47442.20 | T-610 22808.75; C-110 24633.45 | 0.00 | Whole-week route-day rule | payroll-register.csv, business-description.md, field-notes.md, guide, weekly-payroll.csv, route-log.csv, interview-2 |
| adjustment-5 | Paul Haskins | code not specified in application 46675.20 | C-110 46675.20 | 0.00 | Whole-week route-day rule | payroll-register.csv, business-description.md, field-notes.md, guide, weekly-payroll.csv, route-log.csv, interview-2 |
| adjustment-6 | Irene Voss | code not specified in application 36511.80 | C-110 36511.80 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide, weekly-payroll.csv, route-log.csv |

Case-specific evidence (note IDs are stable by input order):

| Note | Subject | Evidence and limits | Sources |
| --- | --- | --- | --- |
| annapolis-courier-evidence-1 | Source timing and confirmation status | Audit period is July 7, 2025 through July 5, 2026. The field-note visit is after audit end and supplies duty/context evidence; it is not an additional in-period site or ride day. Application code figures are aggregate only; individual application classifications are unspecified. No employer confirmation has been received; source statements and implementation approval are not case confirmation. | business-description.md, application.md, field-notes.md, interview-2 |
| annapolis-courier-evidence-2 | Derek Nolan / AC-E01 | payroll-register.csv line 2: wages 52956.80; Route-log driver_id AC-E01 operates AR-1 delivering documents/parcels, supported by business description of van routes. CG-31 actual driving duties. | payroll-register.csv, business-description.md, field-notes.md, guide |
| annapolis-courier-evidence-3 | Maria Santos / AC-E02 | payroll-register.csv line 3: wages 51311.00; Route-log driver_id AC-E02 operates AR-2 delivering documents/parcels, supported by business description of van routes. CG-31 actual driving duties. | payroll-register.csv, business-description.md, field-notes.md, guide |
| annapolis-courier-evidence-4 | Felix Grant / AC-E03 | payroll-register.csv line 4: wages 49618.40; Route-log driver_id AC-E03 operates AR-3 delivering documents/parcels, supported by business description of van routes. CG-31 actual driving duties. | payroll-register.csv, business-description.md, field-notes.md, guide |
| annapolis-courier-evidence-5 | Lena Ortiz / AC-E04 | payroll-register.csv line 5: wages 47442.20; Application describes dispatch/route training; field notes observe Lena riding, while in-period route-log and Monday–Sunday payroll decide whole-week treatment, not annual proportion. | payroll-register.csv, business-description.md, field-notes.md, guide |
| annapolis-courier-evidence-6 | Paul Haskins / AC-E05 | payroll-register.csv line 6: wages 46675.20; Field notes place Paul on dispatch radio; route log records occasional rides, requiring weekly 0/1/2-day test rather than site sign-in rule. | payroll-register.csv, business-description.md, field-notes.md, guide |
| annapolis-courier-evidence-7 | Irene Voss / AC-E06 | payroll-register.csv line 7: wages 36511.80; Bookkeeping in the described dispatch office; complete route log has no driver or rider entry for Irene. CG-04 office duty mapping requires confirmation beyond title. | payroll-register.csv, business-description.md, field-notes.md, guide |
| annapolis-courier-evidence-8 | Derek Nolan / annual weekly reconciliation | weekly-payroll.csv employee_id=AC-E01 has 52 complete Monday–Sunday weeks, 2025-07-07–2026-07-05, totaling 52956.80 exactly equal to payroll-register.csv. route-log.csv contains 312 driver rows, all identifying AC-E01, supporting direct T-610. | weekly-payroll.csv, route-log.csv, payroll-register.csv, business-description.md |
| annapolis-courier-evidence-9 | Maria Santos / annual weekly reconciliation | weekly-payroll.csv employee_id=AC-E02 has 52 complete Monday–Sunday weeks, 2025-07-07–2026-07-05, totaling 51311.00 exactly equal to payroll-register.csv. route-log.csv contains 312 driver rows, all identifying AC-E02, supporting direct T-610. | weekly-payroll.csv, route-log.csv, payroll-register.csv, business-description.md |
| annapolis-courier-evidence-10 | Felix Grant / annual weekly reconciliation | weekly-payroll.csv employee_id=AC-E03 has 52 complete Monday–Sunday weeks, 2025-07-07–2026-07-05, totaling 49618.40 exactly equal to payroll-register.csv. route-log.csv contains 312 driver rows, all identifying AC-E03, supporting direct T-610. | weekly-payroll.csv, route-log.csv, payroll-register.csv, business-description.md |
| annapolis-courier-evidence-11 | Lena Ortiz / week 2025-07-07 | weekly-payroll.csv line 5, Monday–Sunday 2025-07-07–2025-07-13, gross 912.35; route-log.csv line 11 2025-07-10 AR-1; line 14 2025-07-11 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-12 | Lena Ortiz / week 2025-07-21 | weekly-payroll.csv line 17, Monday–Sunday 2025-07-21–2025-07-27, gross 912.35; route-log.csv line 45 2025-07-23 AR-2. 1 distinct ride days sends the entire 912.35 to C-110. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-13 | Lena Ortiz / week 2025-07-28 | weekly-payroll.csv line 23, Monday–Sunday 2025-07-28–2025-08-03, gross 912.35; route-log.csv line 57 2025-07-28 AR-2; line 64 2025-07-30 AR-3. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-14 | Lena Ortiz / week 2025-08-18 | weekly-payroll.csv line 41, Monday–Sunday 2025-08-18–2025-08-24, gross 912.35; route-log.csv line 114 2025-08-19 AR-2; line 118 2025-08-20 AR-3; line 120 2025-08-21 AR-2. 3 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-15 | Lena Ortiz / week 2025-08-25 | weekly-payroll.csv line 47, Monday–Sunday 2025-08-25–2025-08-31, gross 912.35; route-log.csv line 128 2025-08-25 AR-1; line 137 2025-08-28 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-16 | Lena Ortiz / week 2025-09-01 | weekly-payroll.csv line 53, Monday–Sunday 2025-09-01–2025-09-07, gross 912.35; route-log.csv line 149 2025-09-02 AR-1; line 162 2025-09-06 AR-2. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-17 | Lena Ortiz / week 2025-09-08 | weekly-payroll.csv line 59, Monday–Sunday 2025-09-08–2025-09-14, gross 912.35; route-log.csv line 165 2025-09-08 AR-2; line 179 2025-09-13 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-18 | Lena Ortiz / week 2025-09-15 | weekly-payroll.csv line 65, Monday–Sunday 2025-09-15–2025-09-21, gross 912.35; route-log.csv line 184 2025-09-15 AR-3; line 189 2025-09-17 AR-2. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-19 | Lena Ortiz / week 2025-09-29 | weekly-payroll.csv line 77, Monday–Sunday 2025-09-29–2025-10-05, gross 912.35; route-log.csv line 219 2025-09-29 AR-2; line 228 2025-10-02 AR-2; line 232 2025-10-03 AR-3. 3 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-20 | Lena Ortiz / week 2025-10-06 | weekly-payroll.csv line 83, Monday–Sunday 2025-10-06–2025-10-12, gross 912.35; route-log.csv line 245 2025-10-09 AR-1; line 251 2025-10-11 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-21 | Lena Ortiz / week 2025-10-13 | weekly-payroll.csv line 89, Monday–Sunday 2025-10-13–2025-10-19, gross 912.35; route-log.csv line 256 2025-10-13 AR-3; line 271 2025-10-18 AR-3. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-22 | Lena Ortiz / week 2025-10-27 | weekly-payroll.csv line 101, Monday–Sunday 2025-10-27–2025-11-02, gross 912.35; route-log.csv line 290 2025-10-27 AR-1; line 307 2025-11-01 AR-3. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-23 | Lena Ortiz / week 2025-11-03 | weekly-payroll.csv line 107, Monday–Sunday 2025-11-03–2025-11-09, gross 912.35; route-log.csv line 310 2025-11-03 AR-3; line 313 2025-11-04 AR-3. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-24 | Lena Ortiz / week 2025-11-10 | weekly-payroll.csv line 113, Monday–Sunday 2025-11-10–2025-11-16, gross 912.35; route-log.csv line 329 2025-11-11 AR-1; line 338 2025-11-14 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-25 | Lena Ortiz / week 2025-11-17 | weekly-payroll.csv line 119, Monday–Sunday 2025-11-17–2025-11-23, gross 912.35; route-log.csv line 344 2025-11-17 AR-1; line 353 2025-11-20 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-26 | Lena Ortiz / week 2025-11-24 | weekly-payroll.csv line 125, Monday–Sunday 2025-11-24–2025-11-30, gross 912.35; route-log.csv line 365 2025-11-25 AR-1; line 369 2025-11-26 AR-2; line 377 2025-11-29 AR-1. 3 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-27 | Lena Ortiz / week 2025-12-15 | weekly-payroll.csv line 143, Monday–Sunday 2025-12-15–2025-12-21, gross 912.35; route-log.csv line 416 2025-12-15 AR-1. 1 distinct ride days sends the entire 912.35 to C-110. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-28 | Lena Ortiz / week 2025-12-22 | weekly-payroll.csv line 149, Monday–Sunday 2025-12-22–2025-12-28, gross 912.35; route-log.csv line 442 2025-12-24 AR-3; line 443 2025-12-25 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-29 | Lena Ortiz / week 2025-12-29 | weekly-payroll.csv line 155, Monday–Sunday 2025-12-29–2026-01-04, gross 912.35; route-log.csv line 452 2025-12-29 AR-1; line 463 2026-01-01 AR-3. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-30 | Lena Ortiz / week 2026-01-05 | weekly-payroll.csv line 161, Monday–Sunday 2026-01-05–2026-01-11, gross 912.35; route-log.csv line 480 2026-01-08 AR-2. 1 distinct ride days sends the entire 912.35 to C-110. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-31 | Lena Ortiz / week 2026-01-19 | weekly-payroll.csv line 173, Monday–Sunday 2026-01-19–2026-01-25, gross 912.35; route-log.csv line 509 2026-01-20 AR-1; line 514 2026-01-21 AR-3. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-32 | Lena Ortiz / week 2026-02-02 | weekly-payroll.csv line 185, Monday–Sunday 2026-02-02–2026-02-08, gross 912.35; route-log.csv line 544 2026-02-02 AR-3; line 547 2026-02-03 AR-3; line 548 2026-02-04 AR-1. 3 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-33 | Lena Ortiz / week 2026-02-16 | weekly-payroll.csv line 197, Monday–Sunday 2026-02-16–2026-02-22, gross 912.35; route-log.csv line 578 2026-02-16 AR-1; line 585 2026-02-18 AR-2. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-34 | Lena Ortiz / week 2026-03-02 | weekly-payroll.csv line 209, Monday–Sunday 2026-03-02–2026-03-08, gross 912.35; route-log.csv line 624 2026-03-05 AR-2; line 629 2026-03-07 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-35 | Lena Ortiz / week 2026-04-06 | weekly-payroll.csv line 239, Monday–Sunday 2026-04-06–2026-04-12, gross 912.35; route-log.csv line 715 2026-04-09 AR-3. 1 distinct ride days sends the entire 912.35 to C-110. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-36 | Lena Ortiz / week 2026-04-13 | weekly-payroll.csv line 245, Monday–Sunday 2026-04-13–2026-04-19, gross 912.35; route-log.csv line 733 2026-04-16 AR-3. 1 distinct ride days sends the entire 912.35 to C-110. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-37 | Lena Ortiz / week 2026-04-20 | weekly-payroll.csv line 251, Monday–Sunday 2026-04-20–2026-04-26, gross 912.35; route-log.csv line 746 2026-04-22 AR-1; line 755 2026-04-25 AR-1. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-38 | Lena Ortiz / week 2026-04-27 | weekly-payroll.csv line 257, Monday–Sunday 2026-04-27–2026-05-03, gross 912.35; route-log.csv line 771 2026-05-01 AR-2; line 774 2026-05-02 AR-2. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-39 | Lena Ortiz / week 2026-05-04 | weekly-payroll.csv line 263, Monday–Sunday 2026-05-04–2026-05-10, gross 912.35; route-log.csv line 780 2026-05-05 AR-2. 1 distinct ride days sends the entire 912.35 to C-110. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-40 | Lena Ortiz / week 2026-06-01 | weekly-payroll.csv line 287, Monday–Sunday 2026-06-01–2026-06-07, gross 912.35; route-log.csv line 854 2026-06-03 AR-1; line 865 2026-06-06 AR-3. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-41 | Lena Ortiz / week 2026-06-08 | weekly-payroll.csv line 293, Monday–Sunday 2026-06-08–2026-06-14, gross 912.35; route-log.csv line 871 2026-06-09 AR-3; line 880 2026-06-12 AR-3. 2 distinct ride days sends the entire 912.35 to T-610. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-42 | Lena Ortiz / annual weekly reconciliation | weekly-payroll.csv employee_id=AC-E04 has 52 complete Monday–Sunday weeks, 2025-07-07–2026-07-05, totaling 47442.20 exactly equal to payroll-register.csv. Route evidence, including no-ride weeks, controls the inside employee treatment. | weekly-payroll.csv, route-log.csv, payroll-register.csv, business-description.md |
| annapolis-courier-evidence-43 | Paul Haskins / week 2025-12-01 | weekly-payroll.csv line 132, Monday–Sunday 2025-12-01–2025-12-07, gross 897.60; route-log.csv line 387 2025-12-03 AR-2. 1 distinct ride days sends the entire 897.60 to C-110. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-44 | Paul Haskins / week 2026-03-23 | weekly-payroll.csv line 228, Monday–Sunday 2026-03-23–2026-03-29, gross 897.60; route-log.csv line 677 2026-03-26 AR-1. 1 distinct ride days sends the entire 897.60 to C-110. | weekly-payroll.csv, route-log.csv, interview-2 |
| annapolis-courier-evidence-45 | Paul Haskins / annual weekly reconciliation | weekly-payroll.csv employee_id=AC-E05 has 52 complete Monday–Sunday weeks, 2025-07-07–2026-07-05, totaling 46675.20 exactly equal to payroll-register.csv. Route evidence, including no-ride weeks, controls the inside employee treatment. | weekly-payroll.csv, route-log.csv, payroll-register.csv, business-description.md |
| annapolis-courier-evidence-46 | Irene Voss / annual weekly reconciliation | weekly-payroll.csv employee_id=AC-E06 has 52 complete Monday–Sunday weeks, 2025-07-07–2026-07-05, totaling 36511.80 exactly equal to payroll-register.csv. Route evidence, including no-ride weeks, controls the inside employee treatment. | weekly-payroll.csv, route-log.csv, payroll-register.csv, business-description.md |
| annapolis-courier-evidence-47 | Lena Ortiz / weekly conclusion | {0: 21, 1: 6, 2: 21, 3: 4} maps ride-day count to number of weeks. T-610 22808.75, C-110 24633.45. One-day weeks stay entirely C-110; no fraction-of-days or annual five-day rule is used. The 2026-07-20 field observation is outside the audit and is not counted. | weekly-payroll.csv, route-log.csv, field-notes.md, interview-2 |
| annapolis-courier-evidence-48 | Paul Haskins / weekly conclusion | {0: 50, 1: 2} maps ride-day count to number of weeks. T-610 0.00, C-110 46675.20. One-day weeks stay entirely C-110; no fraction-of-days or annual five-day rule is used. The 2026-07-20 field observation is outside the audit and is not counted. | weekly-payroll.csv, route-log.csv, field-notes.md, interview-2 |
| annapolis-courier-evidence-50 | Gloria Rhee / reported owner exclusion | business-description.md reports an election and omission from the register, but no election form/effective dates are among the freshly listed files. Retain the reported omission only as P4 provisional completeness gap. Pay, duties, field-work status and any additional exposure remain unknown, not zero; 63700.00 is not automatically assigned to an owner of unknown duties. CG-05-first precedence against the working-owner rule is proposed, not confirmed. | business-description.md, guide, interview-2 |

Issues and confirmation status:

| Issue | Subject | Proposed treatment / missing evidence | Amount | Alternative | Status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| AC-owner-owner-election | Gloria Rhee | P4: retain reported omission provisionally; obtain election, effective dates, duties and remuneration. Unknown amount is not verified zero. | unknown (not zero) | unknown | open | business-description.md, guide, interview-2 |

Sources (fingerprints and full local paths are in the ledger):

| ID / record | Audience | Retrieved |
| --- | --- | --- |
| [route-log.csv](https://drive.google.com/file/d/19UX2yawPRLp6wr2PLCK1-PqviXtI4Btu/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.143Z |
| [weekly-payroll.csv](https://drive.google.com/file/d/1CGWUkMjRyosKXQguk9Wb6F1ngaGtlKpi/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.143Z |
| [payroll-register.csv](https://drive.google.com/file/d/1eJgq7W9-XcwBIaIddXIHwKg1yNd-3dFD/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.143Z |
| [field-notes.md](https://drive.google.com/file/d/1eSt_14PU6n8daKBY6dXqzmGW7Ny1mozi/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.143Z |
| [business-description.md](https://drive.google.com/file/d/1O_EdWsI1LkifqGFAmB227iFlfXjSHu0T/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.143Z |
| [application.md](https://drive.google.com/file/d/1_QqnLoaf3ceKMMJMT2jw5ABHV3kgSIBJ/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.143Z |
| [guide](https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view?usp=drivesdk) | internal | 2026-11-03T06:24:18.728Z |
| [interview-2](local:interviews/interview-2.md) | internal | 2026-11-03T06:28:07.754231+00:00 |

## Larkspur Lane Bistro

Provisionally reject the reported payroll split; draft; final sign-off not established.

Audit period: 2025-07-07 through 2026-07-05. [Full ledger](ledgers/larkspur-lane-bistro.json).

| Code | Reported | Allocated | Difference |
| --- | --- | --- | --- |
| F-710 | 226431.55 | 340725.35 | 114293.80 |
| F-720 | 114293.80 | 0.00 | -114293.80 |

Known register 340725.35 + net adjustments 0.00 = allocated 340725.35. Unknown owner amounts are excluded from this reconciliation and remain completeness gaps.

Allocations and adjustments (application person-level code may be unspecified):

| ID | Employee/payment | Before | Allocated | Net | Reason | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| adjustment-1 | Anton Varga | code not specified in application 52310.45 | F-710 52310.45 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-2 | Bea Lindell | code not specified in application 41872.30 | F-710 41872.30 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-3 | Omar Haddad | code not specified in application 39640.15 | F-710 39640.15 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-4 | Sophie Tran | code not specified in application 33215.80 | F-710 33215.80 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-5 | Will Garner | code not specified in application 31904.65 | F-710 31904.65 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-6 | Jose Melendez | code not specified in application 27488.20 | F-710 27488.20 | 0.00 | Explicit evidence-backed work mapping | payroll-register.csv, business-description.md, field-notes.md, guide |
| adjustment-7 | Hannah Pryor | code not specified in application 46725.55 | F-710 46725.55 | 0.00 | Catering receipts 362410.85 / 1647026.05 below 40%; threshold applies to catering crew, no proportional wage split | payroll-register.csv, business-description.md, field-notes.md, guide, gross-receipts.csv, interview-2 |
| adjustment-8 | Ivan Petrov | code not specified in application 38190.40 | F-710 38190.40 | 0.00 | Catering receipts 362410.85 / 1647026.05 below 40%; threshold applies to catering crew, no proportional wage split | payroll-register.csv, business-description.md, field-notes.md, guide, gross-receipts.csv, interview-2 |
| adjustment-9 | Clara Bose | code not specified in application 29377.85 | F-710 29377.85 | 0.00 | Catering receipts 362410.85 / 1647026.05 below 40%; threshold applies to catering crew, no proportional wage split | payroll-register.csv, business-description.md, field-notes.md, guide, gross-receipts.csv, interview-2 |

Case-specific evidence (note IDs are stable by input order):

| Note | Subject | Evidence and limits | Sources |
| --- | --- | --- | --- |
| larkspur-lane-bistro-evidence-1 | Source timing and confirmation status | Audit period is July 7, 2025 through July 5, 2026. The field-note visit is after audit end and supplies duty/context evidence; it is not an additional in-period site or ride day. Application code figures are aggregate only; individual application classifications are unspecified. No employer confirmation has been received; source statements and implementation approval are not case confirmation. | business-description.md, application.md, field-notes.md, interview-2 |
| larkspur-lane-bistro-evidence-2 | Anton Varga / LL-E01 | payroll-register.csv line 2: wages 52310.45; Restaurant meal preparation/service or dishwashing in the 70-seat restaurant, consistent with business description and field notes describing kitchen/dining operations; CG-41 mapping requires individual duty confirmation beyond the register label. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-3 | Bea Lindell / LL-E02 | payroll-register.csv line 3: wages 41872.30; Restaurant meal preparation/service or dishwashing in the 70-seat restaurant, consistent with business description and field notes describing kitchen/dining operations; CG-41 mapping requires individual duty confirmation beyond the register label. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-4 | Omar Haddad / LL-E03 | payroll-register.csv line 4: wages 39640.15; Restaurant meal preparation/service or dishwashing in the 70-seat restaurant, consistent with business description and field notes describing kitchen/dining operations; CG-41 mapping requires individual duty confirmation beyond the register label. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-5 | Sophie Tran / LL-E04 | payroll-register.csv line 5: wages 33215.80; Restaurant meal preparation/service or dishwashing in the 70-seat restaurant, consistent with business description and field notes describing kitchen/dining operations; CG-41 mapping requires individual duty confirmation beyond the register label. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-6 | Will Garner / LL-E05 | payroll-register.csv line 6: wages 31904.65; Restaurant meal preparation/service or dishwashing in the 70-seat restaurant, consistent with business description and field notes describing kitchen/dining operations; CG-41 mapping requires individual duty confirmation beyond the register label. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-7 | Jose Melendez / LL-E06 | payroll-register.csv line 7: wages 27488.20; Restaurant meal preparation/service or dishwashing in the 70-seat restaurant, consistent with business description and field notes describing kitchen/dining operations; CG-41 mapping requires individual duty confirmation beyond the register label. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-8 | Hannah Pryor / LL-E07 | payroll-register.csv line 8: wages 46725.55; Part of the three-person event crew: field notes establish preparing event food in restaurant kitchen and serving at venues, with restaurant shifts on quiet weeks. The interview’s receipts threshold decides the crew code; no unsupported time/pay percentage split. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-9 | Ivan Petrov / LL-E08 | payroll-register.csv line 9: wages 38190.40; Part of the three-person event crew: field notes establish preparing event food in restaurant kitchen and serving at venues, with restaurant shifts on quiet weeks. The interview’s receipts threshold decides the crew code; no unsupported time/pay percentage split. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-10 | Clara Bose / LL-E09 | payroll-register.csv line 10: wages 29377.85; Part of the three-person event crew: field notes establish preparing event food in restaurant kitchen and serving at venues, with restaurant shifts on quiet weeks. The interview’s receipts threshold decides the crew code; no unsupported time/pay percentage split. | payroll-register.csv, business-description.md, field-notes.md, guide |
| larkspur-lane-bistro-evidence-11 | Monthly receipts / period mismatch | gross-receipts.csv lines 2–13 cover July 2025–June 2026: dine-in 1284615.20, off-site 362410.85, gross 1647026.05, catering share approximately 22.00395373%, below the interview’s 40% threshold. These months include July 1–6, 2025 outside the audit and omit July 1–5, 2026 inside it. P6 uses only an explicitly provisional full-month proxy; no invented daily proration. Unknown boundary receipts prevent proving the exact-period result. Nadia’s 12:35 AM attribution to the guide is contradicted by the freshly read guide: CG-41/CG-42 give definitions, no 40% threshold. | gross-receipts.csv, business-description.md, field-notes.md, interview-2, guide |
| larkspur-lane-bistro-evidence-13 | Rosa Delacroix / reported owner exclusion | business-description.md reports an election and omission from the register, but no election form/effective dates are among the freshly listed files. Retain the reported omission only as P4 provisional completeness gap. Pay, duties, field-work status and any additional exposure remain unknown, not zero; 63700.00 is not automatically assigned to an owner of unknown duties. CG-05-first precedence against the working-owner rule is proposed, not confirmed. | business-description.md, guide, interview-2 |

Issues and confirmation status:

| Issue | Subject | Proposed treatment / missing evidence | Amount | Alternative | Status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| receipts-period | Gross receipts 2025-07-01 to 2026-06-30 | P6: supplied-period proxy only. Obtain audit-period summary or boundary transactions; no daily proration. | unknown (not zero) | unknown | open | gross-receipts.csv, field-notes.md, guide, interview-2 |
| LL-owner-owner-election | Rosa Delacroix | P4: retain reported omission provisionally; obtain election, effective dates, duties and remuneration. Unknown amount is not verified zero. | unknown (not zero) | unknown | open | business-description.md, guide, interview-2 |

Sources (fingerprints and full local paths are in the ledger):

| ID / record | Audience | Retrieved |
| --- | --- | --- |
| [payroll-register.csv](https://drive.google.com/file/d/1RweuVXBFLbhY1-d6ztTbrBBI3hsbg2AL/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [gross-receipts.csv](https://drive.google.com/file/d/1XvNTJ1snLoBgwjNLFAKsW4m8ZeNbL4oV/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [field-notes.md](https://drive.google.com/file/d/1gryH8fMXpdLz7m3wfIqt3rP4TBna-10B/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [business-description.md](https://drive.google.com/file/d/1soA8l52GMsdnLnxg9a0vbZi3OGw83soJ/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [application.md](https://drive.google.com/file/d/1Q1tKM5Hx3KvkZOyP-clxI0vpmB5_cFP_/view?usp=drivesdk) | employer | 2026-11-03T06:24:16.141Z |
| [guide](https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view?usp=drivesdk) | internal | 2026-11-03T06:24:18.728Z |
| [interview-2](local:interviews/interview-2.md) | internal | 2026-11-03T06:28:07.754231+00:00 |

