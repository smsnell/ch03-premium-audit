# Gate 4 — completion review

2026-11-03. Gate 3 was accepted by the owner and pushed to `origin/main` as **3a39077 — G3 Complete**. One integrated Astra High requirements review found and fixed the bounded issues below, with Sol 6.1 implementing reporting and focused regression checks. Gate 4 software/package checks pass; owner accepted the package with final question corrections and authorized G4 Complete publication. No employer audit has been approved.

## Findings and fixes

| Finding | Final behavior / evidence |
| --- | --- |
| Confirmation IDs could repeat across employers; factual confirmation and policy approval were indistinguishable. | Each confirmation requires `case_slug`, `issue_id`, `kind` (`employer_fact` or `internal_decision`), who, when, evidence and scope. A mismatched employer or missing/invalid kind fails before publishing outputs. Only the addressed issue becomes `confirmation_recorded`; payroll, other issues and other employers stay unchanged. The whole case remains a draft. |
| Allowances could use an employee's initial class after a roofing or other rule changed it. | Default allocation uses that person's calculated class by employee ID. Multiple calculated classes require an explicit code and allocation evidence. Regression examples: under-15-day roof worker's allowance goes to siding; multi-code dispatcher fails without allocation evidence; employees sharing a name remain distinct. |
| An included field-working owner could retain clerical as the normalized destination. | Reject C-110 for that owner instead of emitting a contradictory fixed-basis allocation. Existing owner-election uncertainty remains open. |
| Reports repeated case narratives, decisions, weekly detail and questions, and asked employers to approve policy. | Compact allocation/adjustment tables, one full case-note narrative, grouped factual employer requests, and separate `internal-decisions.md`. Adjustment, note and source IDs preserve traceability. Full weekly entries, source paths/hashes, original note questions and confirmation records remain in the ledgers. Same-name extra allocations are not hidden by consolidation. Explicit internal audience metadata survives normalization. |

## Requirements review

| Requirement | Result and practical limit |
| --- | --- |
| Reusable Skill, metadata, inputs, invocation, outputs, errors and references | Pass. Skill validation succeeds. Python standard library helper; live retrieval and duty interpretation remain agent tasks. No six-employer results embedded in the calculation engine. |
| Read company rules and employer records during each live run | Gate 3 fresh retrieval evidence remains in `gate3-source-run.md`. Gate 4 deliberately replays those verified captures to isolate software/report changes; this is not a new live audit. A new audit must retrieve again. |
| Company rules and auditor decisions, no unsupported public manuals | Pass. Guide code-description references remain separate from interview-only thresholds and P1–P7 provisional applications. Employer facts and internal decisions have separate review channels. |
| One/all/new employer instructions | Pass. README documents live Skill requests and one-case/bundle calculation commands; new-employer and changed-source CLI tests pass. Ignored `.runs/` captures are not available in a fresh checkout; retrieve and normalize anew there. |
| Six exact CSV filenames/columns, positive cent amounts and guide paragraph IDs | Pass. Every CSV is byte-identical to the accepted Gate 3 output. Code-description reference checks and money-conservation tests pass. |
| Report every allocation difference and adjustment, amount, subject and supporting record | Pass. Report tables preserve before/after/net and evidence IDs. All 131 case notes survive in the report/internal file and unchanged ledgers. Full detailed weekly records remain linked rather than repeated. |
| Questions cover every adjustment and relied-on record | Pass. Each adjustment maps to a named factual request; every employer source is in the case's record-confirmation list. Guide/interview provenance and rule approval route to the auditor, consistent with the owner's requested separation. They are not employer factual confirmations. |
| State acceptance/rejection and decisive evidence | Pass; case decisions below are unchanged. All retain provisional draft status where unresolved issues apply. |
| Missing evidence and unknown owner amounts visible | Pass. All 16 open issues are unchanged; five owner amounts remain null/unknown, never zero or an invented fixed amount. No case confirmations were added to real employer data. |
| Real coding-session evidence for submitted revision | G3 commit includes Entire checkpoint `01M6G29RXZ14YG1QDSFMG0VN3P`; push synchronized checkpoint refs. Caller-resolved session `01a19fc2-7e8e-7312-982c-a399477e4d95` reports active. G4 Complete was pushed as `575f253`; Entire checkpoint `01M6G3ZFXW7A7R4EYEKQTZWS25` synced. Its stored transcript contains the final owner request, 45-test result and complete-output regeneration, verifying actual capture for the submitted code revision. The status display reports a stale exited process ID although caller-session records have captured this task and its changed files; verify stored checkpoint content rather than relying on the active label alone. This document is not a substitute for the real session records. |

## Verification results

- `python3 -B -m unittest discover -s tests -v`: **45 passed**. Includes the prior rule boundaries, new-employer and changed-source checks, atomic/incomplete failures, two-employer CLI isolation, factual/internal confirmation kinds, allocation fixes and reporting traceability.
- Skill metadata validator: **valid**. Final local security scan: exit 0; only the existing missing-license INFO remains. No license is invented on the owner's behalf. Generated bytecode from worker checks was moved outside the Skill and the scan rerun. Scanner output is in `.runs/gate4/skill-scan-complete.md`; it is a local static check, not a guarantee against every threat.
- Full six-employer CLI replay: `python3 -B skills/class-code-assistant/scripts/audit.py --bundle .runs/gate3/six-cases.json --output-dir .runs/gate4/complete-output`. Source fingerprints checked; generated files copied into `deliverables/` and byte-verified against the run output.
- Compared with accepted Gate 3: **six CSVs and six full ledgers byte-identical**, 16 open issues, five unknown owner amounts, 131 full case notes. Local comparison evidence: `.runs/gate4/package-verification.json`.
- Report/questions previously totaled **199,351 bytes**. New report **81,884**, employer questions **32,124**, internal decisions **16,469**: **130,477 bytes combined, 34.55% less**, including the additional internal file. All adjustment IDs and employer records remain covered; all detailed notes remain available once in the human review files and in full in the ledgers.
- `git diff --check`: pass. No source transcript rewritten and no external employer contact made.

## Case decisions and remaining review

| Employer | Decision and deciding records |
| --- | --- |
| Harbor Point Legal | Provisionally accept C-110 employee split. Legal duties, six logged visits and Nadia's clarification support the professional-duty proposal; CG-04 wording exception remains open. |
| Bay Crest Exteriors | Reject. Crew timesheets establish whole-person roofing/siding thresholds, including Rafael's 15 and Jamal's nine days; Teresa's site log establishes her transfer. Governing ordering and owner's election remain open. |
| Severn Homebuilders | Reject. Site log transfers Dana; certificate and payment records support $52,260.78 of provisional subcontractor additions. Kent identity/full-period coverage, governing ordering and owner's election remain open. |
| Patuxent Electric | Reject. Field duties replace Raymond's draw with the fixed field-owner basis; payroll/allowance records add excess and provisional Kyle $390. Zero-day payment support remains open. |
| Annapolis Courier | Reject. Route logs joined to weekly payroll move Lena's 25 qualifying weeks, $22,808.75. Owner's election remains open. |
| Larkspur Lane Bistro | Provisionally reject. Supplied receipts show 22.00395% off-site catering and support the provisional F-710 allocation, but the receipts period is a proxy. Audit-period receipts and owner's election remain open. |

Priority employer calls remain **Severn** (coverage/identity/payment facts) and **Larkspur** (exact-period receipts). The owner conducts any calls; internal treatment approval belongs to the auditor. One suitable scoped confirmation may support a later reviewed decision, but recording it does not itself resolve the audit. Do not infer new facts or owner remuneration from software acceptance.

Final owner corrections: Dana now receives duties/site-day questions from her own allocation context, without certificate questions triggered by shared governing evidence. Raymond is asked to confirm the reported absence of an election and supply a filed election if that report is wrong. All six timing requests name the audit dates and ask whether later observations describe that period. The added regression preserves decisive facts and note/adjustment/source IDs. Full regeneration confirms six CSVs and six ledgers byte-identical, all 16 issues open and five owner amounts unknown; comparison saved in `.runs/gate4/completion-verification.json`. Software acceptance is not audit sign-off.

Reuse limits: a deferred contractor-office allowance also needs explicit `code` and `allocation_evidence`, because its governing destination is decided after the allowance pass. Missing allocation support fails visibly. For new rule records with IDs other than `guide`/`interview…`, set source `audience: internal` during reviewed normalization. These agent-reviewed mappings are not inferred from source prose by the arithmetic helper.

Completion: G4 Complete pushed successfully on 2026-11-03. Final available combined usage is 28,653,026 tokens with partial coverage; see PROJECT-TRACKER.md for lead/worker accounting and cutoff. Software acceptance is not audit sign-off.
