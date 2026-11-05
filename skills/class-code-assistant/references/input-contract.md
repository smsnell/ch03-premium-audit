# Case preparation and calculation contract

The case JSON is an agent-normalized interpretation of freshly read sources. Source files remain evidence; the case is not an alternate source of business facts. Prepare a new case after each live retrieval, review its mappings, and retain all source citations. The helper validates bytes and calculations, not whether an agent interpreted prose correctly or actually contacted Drive today.

## Capture and normalize

Use connected Drive `list_folder` and `fetch` for the user-supplied folder and guide. Capture every listed file, check truncation/shape, and record IDs, URLs, retrieval times, modification times where available, byte counts and SHA-256. Retain folder listings to demonstrate completeness. Save plain Markdown and CSV bytes locally; spreadsheet/PDF formats require a separately verified extraction before normalization. A malformed/unreadable mandatory record blocks the case rather than authorizing an empty substitute.

Map employee IDs to duties using business description, notes, and logs; never select a rule from an employer name or a title alone. The `people` array must reconcile to all register people. Explicitly add reported off-register owners as unresolved records with unknown pay. Convert CSV money to decimal strings, dates to ISO dates, and preserve source identifiers for every normalized event. Blank-ID visitors such as inspectors are not employees; document their exclusion. Separate post-period notes from in-period events.

## Top-level shape

Each case has `slug`, `employer`, inclusive `audit_start`/`audit_end`, `guide_source` (ID of the captured guide), `sources`, `rule_refs`, `reported`, and `completeness`. All seven arrays are required: `people`, `signin`, `roofing`, `route_weeks`, `allowances`, `sub_invoices`, `certificates`. Supply an empty array only with the supported declaration below. Older cases must be reviewed and migrated; omitted collections never mean zero activity.

- `sources`: entries with `id`, local `path`, `sha256`, `url`, and `retrieved_at`. Include the fresh guide and the original interview as cited sources. Evidence arrays reference these IDs. Use exact saved bytes to compute the hash.
- `rule_refs`: rule keys mapped to `{sources: [source IDs], citation: "paragraph or interview timestamp"}`. The guide supplies code-description references; house thresholds cite the interview. Supported keys are `roofing`, `office`, `governing`, `owner`, `allowance`, `subcontractors`, `dispatcher`, `catering`, and `division` (CG-07); keys are required when their policy is used.
- `reported`: application code totals as dollar strings, not inferred employee-level assignments. The report compares aggregate code totals; employee-level reported allocations must not be invented where the application only supplies totals.
- `people`: `{id, name, pay, role, code, evidence}` plus applicable owner/exception fields. `evidence` contains source IDs. Roles: `direct`, `roofing`, `office`, `dispatcher`, `owner`, `catering`, `split`. `code` identifies a direct/trade code where applicable; role-specific house rules determine the final code. Unknown owner pay and unknown work code are JSON null, never invented zero wages or duties. Contractor office staff require `contractor: true`; noncontractor office staff with at least five visits need `exception_issue` linked to an explicit open treatment. `reported_code` is optional and requires `reported_code_evidence`; omit it when the application provides only aggregate totals. The helper labels those person-level baseline codes unspecified.
- `signin`: `{person, date, evidence}`. Count unique in-period employee dates.
- `roofing`: `{person, date, hours, evidence}`. Normalize only roofing entries from the crew file; other work does not add roof days. Retain positive-time dates and let period/deduplication checks apply. A worker with no roofing rows needs `roofing_evidence: [source IDs]` attesting that the full record supports zero roofing days.
- `route_weeks`: `{person, start, pay, ride_dates, evidence}`. Include all weeks for each dispatcher, not just qualifying weeks. Join rides by employee and dates to Monday–Sunday weeks; reconcile total weekly gross to register wages. Direct drivers use their work code independently.
- `allowances`: `{id, person, amount, days, documented_reimbursement, evidence}`. Dated daily payments add `date` and use `days: 1`; all payments for the same worker/date share one $47 cap and must have one reviewed allocation class. Undated positive-day aggregates require `basis: "uniform_daily"`, a cent-exact `daily_rate` satisfying `amount = daily_rate × days`, and `basis_evidence` supporting a uniform rate over the audit-period travel days. Permit only one non-reimbursement aggregate per worker and no mix with dated daily payments; use dated records otherwise. A numerical average alone is not evidence of a uniform rate. Zero-day payments retain the open P5 treatment. Documented reimbursement requires actual supporting evidence, not an application assertion. A zero-day payment stays an explicit proposed inclusion. Allowances follow the employee ID’s unique calculated class. If classification is ambiguous or a different allocation is supported, provide explicit `code` and `allocation_evidence: [source IDs]`; missing allocation evidence blocks output.
- `sub_invoices`: `{id, name, date, amount, code, evidence}`; `certificates`: `{name, start, end, evidence}`. Associate amounts with invoice IDs. Preserve certificate entity names; do not fuzzy-match. A certificate alias requires `alias_for`, `alias_approved: true`, and `alias_evidence: [IDs]`; never rewrite source text to force a match. Out-of-period invoices are rejected for explicit resolution.
- `receipts`: `{start, end, gross, catering, evidence}`. Gross includes dine-in plus off-site receipts. Preserve actual covered dates; nonmatching periods require a visible open proxy issue. The 40% rule selects a code; it never distributes wages by the receipts percentage.
- `case_notes`: optional entries `{subject, detail, evidence, question}` for clear case-specific evidence. Name employees/invoices and quote source row numbers, dates, amounts, duties and applicable interview timestamps in `detail`; supply the corresponding precise confirmation question. Add a reviewed `factual_question` for case-specific facts that must appear in employer questions (counts, dates, amounts, duties or identities). Keep policy choices in the original `question` and internal decision notes; never copy a mixed fact/policy question into this field. The renderer retains both original note fields and groups the factual prompts with adjustment/source traceability. Optional `audience: internal` routes a policy/priority note to the internal decision file; factual notes stay in the report and grouped employer requests. Application-decision and call-priority subjects are internal by default. Notes are reviewed narrative, not calculation inputs, and must agree with the ledger. The helper validates references and preserves numbered evidence links across report/questions/internal decisions and the full ledger. Employer-record sources are factual; guide and interview source IDs are internal by default, with optional source `audience` overriding routing.
- `open_issues`: `{id, subject, treatment, amount, alternative_amount, evidence}`. Use null for unknown amounts and identify missing documents. Add an exception issue reference for any person retained in C-110 despite a no-field-code situation. Each owner omission must be visible independently.
- Owner fields: `off_register`, explicit `election_status` (`unverified`, `included`, `excluded`), and `field_work` (boolean when included, null when unknown). `unverified` preserves the existing off-register omission as an open completeness gap with `pay: null`; unknown duties/code stay null. Known register pay with uncertain inclusion requires reviewed resolution before calculation. `included` requires `inclusion_evidence`; field work plus a supported trade code yields $63,700 even when an off-register owner’s actual draw is unknown. A non-field included owner requires evidenced remuneration. `excluded` requires `election_evidence`, `election_start`, and `election_end` covering the audit; P4 precedence remains provisional. Missing election evidence alone establishes neither inclusion nor exclusion. Retire `election_valid` during reviewed migration; conflicting legacy values fail. Input controls retain unknown actual draw as null, separately from known register reconciliation.
- `confirmations`: `{case_slug, issue_id, kind, by, at, evidence, scope}`. Require `case_slug` to match this employer and `kind` to be `employer_fact` or `internal_decision`. Only include real received confirmations, with a precise scope. An issue ID alone is insufficient because IDs can repeat across employers. Records set only `confirmation_recorded` for the addressed issue, never automatic resolution or audit approval. Owner approval of P1–P7 is approval to propose these treatments, not a case confirmation. Confirmation cannot change payroll facts by itself; updated evidence/mappings require a new reviewed case.

## Output review

Run the helper into a new directory and inspect its ledger, report, questions, and CSV together. Check every normalized amount/date/role against the source, every adjustment against the ledger, and all relied-on records against the questions. Semantic issues not captured by a source-level question require a specific additional question before handoff. Report original payroll, adjustments, code totals/differences, and acceptance decision; distinguish reclassification from changes in payroll basis.

Approval status is separate from mathematical reconciliation. In particular, an off-register owner omitted under a provisional exclusion remains an unknown additional exposure even if the known payroll balances perfectly. A successful run produces draft artifacts and cannot certify final audit approval.

## Source-row completeness

For each required collection, `completeness` must contain one of:

- `{"status":"complete","checks":[{"source":"source-id","columns":{"normalized_field":"csv_header"}}]}`. Read the fingerprint-verified captured CSV and reconcile the full multiset of mapped row values to the normalized collection. Missing, duplicated, substituted, or changed rows fail even if counts or totals agree. Each source can occur once per collection; multiple source files may supply one collection with the same mapped fields.
- `{"status":"not_applicable","evidence":["source-id"]}` with an empty array and source evidence establishing no applicable activity. This cannot replace payroll or required dispatcher records.
- For **certificates only**, `{"status":"unavailable","evidence":["source-id"]}` with an empty array documents an unsuccessful coverage search. It does not exempt subcontractor payments. Unavailable mandatory records block publication.

Required mapped fields:

| Collection | Normalized field names |
| --- | --- |
| people | id, name, pay |
| signin | person, date |
| roofing | person, date, hours |
| route_weeks | person, start, pay |
| allowances | person, amount, days; date required for dated payments; id optional |
| sub_invoices | id, name, date, amount |
| certificates | name, start, end |

For example, reconcile invoices directly to the original payment capture:

```json
"sub_invoices": {
  "status": "complete",
  "checks": [{
    "source": "subcontractor-payments.csv",
    "columns": {"id":"invoice", "name":"subcontractor", "date":"date", "amount":"amount_paid"}
  }]
}
```

Preserve source field representations in normalization (dates, monetary strings, hours); the comparison is exact. CSV headers must be unique and rows rectangular. Captured `data_rows`, if present, must match the source. All checks use existing registered source IDs. Retain provider byte counts and complete folder listings during retrieval.

Only these source-row exclusions are supported: blank-ID sign-in visitors; zero-amount allowance rows; off-register owners with blank register pay; weekly rows for known non-dispatchers; and non-roofing work selected by a roofing check’s `work_column` and optional `roof_value` (default `roofing`). Invoice and certificate checks have no row exclusions. Record the reason for nonemployee/other-work exclusions in case notes. Unsupported source layouts need a separately verified extraction and reviewed mappings; never generate the comparison source from the normalized rows in a live run.

When dispatchers exist, the `route_weeks` declaration also requires `route_log: {"source":"route-log.csv","columns":{"person":"ride_along_id","date":"date"}}`. Ride dates reconcile independently to each pay week; unknown riders or rides without a matching week fail.

When catering or receipts are present, `completeness.receipts` requires `status: "complete"` and CSV checks mapping either `gross`/`catering` or `dine_in`/`catering`. The helper sums every captured row and reconciles both totals to `receipts`. Period alignment still requires source review and the existing open proxy treatment where appropriate.

These checks establish consistency with captured records. They cannot discover an invoice already absent from everything the employer supplied, prove a prose assertion, or verify that the source inventory itself is complete. Compare independent payment registers/control totals and obtain employer completeness confirmation when available; unexplained gaps remain open or block normalization. A source fingerprint proves byte consistency, not completeness of the business records.

The ledger’s `input_controls` retains completeness declarations, owner states and original allowance inputs. For grouped daily payments, the calculation identifies each original payment and amount before applying one daily cap. Existing business issues are not resolved by passing these controls.

## Governing field eligibility (Gate B)

When a contractor office employee reaches five site days, supply `governing_eligibility`, a mapping of eligible code to `{reason, evidence}`. Each entry must cite the captured guide and employer business evidence, explaining why the actual work is a field trade. Review all corrected field allocations, including supported additions. An omitted allocated field trade fails. An explicitly empty mapping is allowed only when no field trade is allocated; the existing open no-destination exception is still required.

Supported contractor field trades are R-310, R-320, L-620, H-420 and E-510, as described in the current company guide. M-830 is shop work and cannot win merely because its payroll is larger; clerical, restaurant and other non-contractor codes are also ineligible here. A new field code or changed guide needs compatibility review. The helper verifies the supported set and references; the agent must verify the business meaning of the evidence. It cannot prove prose claims.

Compare eligible corrected payroll and supported additions before office transfers. Ties or no positive destination require the existing explicit open fallback; never invent a tie-breaker. Eligibility and its supporting sources remain in the ledger's input controls and transfer provenance. Cases without a qualifying transfer keep their existing informational pre-office totals.

## CG-07 actual time/pay splits (Gate B)

For an ordinary mixed-duty employee, use one register ID with `role: "split"`, `code: null`, full register `pay`, and `allocations: {"E-510": "60.00", "M-830": "40.00"}`. Cite `division` in `rule_refs` to CG-07 of the captured current guide. Do not duplicate the employee into separate people records.

Supply `time_records: {"checks": [{"source": "actual-time-pay", "columns": {"id": "record_id", "person": "employee_id", "date": "work_date", "code": "class_code", "hours": "actual_hours", "pay": "attributable_pay"}}]}`. The helper reads every row directly from fingerprint-verified CSV captures; there is no normalized subset to drop individual records from. If a verified extraction joins time and payroll sources, retain and review both originals and the extraction. Do not manufacture time/pay rows from desired allocation amounts.

Every time record needs a globally unique nonblank ID, the split employee's register ID, an in-period date, a supported code, finite positive actual hours and attributable pay in exact cents. Code-level source pay must equal each declared allocation, and allocations must sum to the full register pay. At least two codes must have positive pay. Missing hours/pay, omitted code allocations, duplicate records, unknown employees, unmatched totals or altered fingerprints block output. Unequal wage rates are allowed because attributable pay, not an invented hourly average, controls the division. No new rounding convention is introduced.

This bounded helper does not infer payroll shares from hours alone. Where records contain only hours, or bonuses/other wages cannot be attributed, obtain an evidence-backed reconciliation and reviewed method before calculation. Whole-person roofing/office, owner, whole-week dispatcher and catering rules retain precedence. Allocations on another role fail. Generic splits involving C-110, R-310, R-320, T-610, F-710 or F-720 fail for scenario review instead of bypassing a house rule; an unrelated mixed-duty case involving one of these codes needs an explicitly reviewed extension. Multicode allowances still require a supported explicit allocation class.

The ledger retains split inputs and time-source mappings. Review factual employer questions about the worker's duties, time/pay records and full-wage reconciliation separately from the auditor's CG-07 policy decision.
