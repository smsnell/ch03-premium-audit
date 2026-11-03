# Gate 3 fresh source run

Gate 3 used the connected Google Drive plugin to list the supplied employer root, enumerate all six employer folders, read guide metadata, and fetch the original raw bytes of the guide and every employer file. The Google Drive skill was read before retrieval. No previous run's source bytes or normalized cases were used as fresh evidence.

The run manifest is `.runs/gate3/manifest.json`. It retains the root and folder listings, Drive IDs/URLs, modification and retrieval timestamps, byte counts, SHA-256 values, and CSV column/row counts. There are 35 captures totaling 152,717 bytes: the guide plus 34 employer files (Harbor 5, Bay Crest 6, Severn 7, Patuxent 5, Annapolis 6, Larkspur 5). Each listing contained fewer than the requested 100 items, with no continuation/truncation indication. Every materialized byte count matched the listed Drive file size. CSVs decode as UTF-8 and all rows match their header width. The largest file, Bay Crest's crew timesheets, was captured as 88,107 raw bytes with 1,726 data rows. Annapolis has 936 route rows and 312 weekly-payroll rows.

Raw fetching returned authenticated temporary file references. Materialization initially encountered sandbox DNS restrictions; the scoped download escalation was approved and downloaded the source files successfully. Temporary bearer download URLs were removed from the local retrieval metadata after use. The durable manifest contains ordinary source URLs only. Captures live under `.runs/gate3/sources/`; the guide is `sources/guide.md`. This Markdown records the source/verification result; it does not substitute for real coding-session capture records.

The original `interviews/interview-2.md` is referenced by absolute path and SHA-256 in every normalized case. Its earlier discussion repeats interview 1 and is not counted as an independent second confirmation. The new 12:26–12:37 AM discussion supplies the clarified house practice. No employer confirmation was received or fabricated. P1–P7 implementation approval remains separate from case confirmation.

## Reviewed case inputs

The six-case bundle is `.runs/gate3/six-cases.json`; individual files are `.runs/gate3/<employer-slug>.json`. Source paths are absolute so the lead can run the bundle from the repository. `.runs/gate3/prepare_cases.py` records this run's explicit source-to-duty mappings and normalization; it is case preparation data/code, not part of the reusable Skill. None of these six employers' answers are hardcoded in the reusable helper.

Each register person is represented once, each application total reconciles to the known register, and the five omitted owners are separately represented with unknown pay/code/field duties as JSON null. The bundle includes 131 specific evidence notes and associated confirmation questions, covering employee wages/duties, site dates, crew day counts, route/week joins, invoices/certificates, allowances, receipt-period boundaries and the original application decision. Blank-ID county inspectors are excluded explicitly. July 2026 field visits after audit end supply context and are not counted as additional in-period work days.

Harbor's Tomas/Thomas and Bay Crest's employer/estimator transcription variants are disclosed as contextual identity mappings while preserving the original interview. Larkspur's 40% threshold is attributed to interview 2, not fabricated as a guide paragraph; the fresh guide contains the code definitions but no threshold.

## Targeted calculation checks

The current helper successfully generated `.runs/gate3/initial-output` with:

```sh
python3 skills/class-code-assistant/scripts/audit.py \
  --bundle .runs/gate3/six-cases.json \
  --output-dir .runs/gate3/initial-output
```

The output directory must be new on replay. Replaying the bundle is a calculation check, not a fresh retrieval run.

| Employer | Decision on reported employee split | Calculated code payroll | Known basis change |
| --- | --- | --- | --- |
| Harbor Point Legal | Provisionally accept, based on legal duties, six real log entries and Nadia's explanation; CG-04 wording exception remains open | C-110 425148.16 | 0.00 |
| Bay Crest Exteriors | Reject, based on actual crew roof-day records and Teresa's nine sign-ins | R-310 450480.60; R-320 46205.10; C-110 44812.35 | 0.00 |
| Severn Homebuilders | Reject, based on Dana's eleven days, Marissa's four days and full-period subcontractor evidence gaps | H-420 369204.39; R-310 27567.39; C-110 117368.70 | +52260.78 |
| Patuxent Electric | Reject, based on Raymond's field duties and the allowance/day columns | E-510 372274.85; C-110 43905.60 | -51750.00 |
| Annapolis Courier | Reject, based on complete Monday–Sunday weekly wages joined to route days | T-610 176694.95; C-110 107820.45 | 0.00 |
| Larkspur Lane Bistro | Provisionally reject, using the disclosed full-month receipts proxy | F-710 340725.35 | 0.00 |

All six generated totals match the planning sanity checks. Verification independently recomputed every normalized source fingerprint, checked the helper's register-plus-net-adjustment conservation, confirmed evidence notes survive into ledgers, asserted all confirmation lists remain empty and all issues remain open, and asserted exactly five unknown off-register owners retain null amounts. No zero-pay F-720 row is emitted.

## Items still requiring substantive resolution

P1 retains Tomas's 64212.48 legal-support pay under C-110 while disclosing all six visits and the office-wording exception. P2 retains distinct positive roofing-date counts and corrected field payroll before office transfers. P3 does not alias Kent's names; all three Kent payments add 60% because even the proposed alias certificate ends before audit end. Tenbury's exact-name full-period certificate is relied on and specifically questioned; Tidewater coverage is missing. P4 retains five unquantified owner gaps and proposed election-first precedence without claiming verified exclusions. P5 includes Kyle's 390.00 provisionally, with a 415790.45 employer-total alternative if sufficient excluded-reimbursement evidence arrives. P6 retains the nonmatching receipts period and requests exact audit-period evidence; catering-crew pay is 114293.80, and unknown boundary receipts prevent proving the exact-period ratio. P7 keeps half-up per-payment rounding and scoped confirmations as disclosed practices; there are no received confirmation records.

The proposed first two calls are Severn, where documentation can change 52260.78 of subcontractor additions and resolve entity/coverage gaps, and Larkspur, where exact-period receipts/proxy resolution controls the 114293.80 catering-crew code decision. Both suggestions and reasons appear in case evidence notes with confirmation questions. No stakeholder was contacted; no rates or premium were calculated. These are provisional allocations for owner review, with final sign-off blocked by unresolved evidence and treatments.
