# Gate 3 verification

Completed 2026-11-03; awaiting owner review before Gate 4. Gate 4 integrated review has not been performed. All business outputs remain drafts with unresolved items preserved.

## Outputs and fresh run

`deliverables/` contains all six exact-name code CSVs, `audit-report.md`, `audit-questions.md`, and six supporting JSON ledgers. A new Drive retrieval captured the guide plus all 34 employer files, with 35 independently verified byte counts and SHA-256 hashes. Source locations/timestamps and file/row context are recorded in the manifest and case evidence. See `gate3-source-run.md` for the source checks.

The agent interpreted the fresh raw records into `.runs/gate3/six-cases.json`, then the helper ran end to end first into `.runs/gate3/initial-output` and again into the new `deliverables/` directory. The second calculation uses the same fresh capture set; it is not represented as a second remote retrieval. No old Gate 1 captures supplied the Gate 3 calculation.

```bash
python3 -B skills/class-code-assistant/scripts/audit.py --bundle .runs/gate3/six-cases.json --output-dir deliverables
```

The command requires a new destination; use another directory to replay. For a new live audit, invoke the Skill to retrieve/normalize sources afresh, as documented in README. The helper validates explicit normalized mappings and source hashes; it does not independently interpret arbitrary source prose or establish freshness from timestamps alone.

## Verified allocations

| Employer | Code allocations (USD) | Decision basis |
| --- | --- | --- |
| Harbor Point Legal | C-110 425148.16 | Provisionally accept employee split under P1: legal-support duties clarified in interview; six visits retained as evidence. |
| Bay Crest Exteriors | C-110 44812.35; R-310 450480.60; R-320 46205.10 | Reject application: roof-day threshold, Rafael exactly 15, Jamal nine, Teresa's nine site days and governing payroll comparison. |
| Severn Homebuilders | C-110 117368.70; H-420 369204.39; R-310 27567.39 | Reject: Dana's 11 site days plus 60% of Tidewater and all Kent payments without verified full-period coverage. |
| Patuxent Electric | C-110 43905.60; E-510 372274.85 | Reject: Raymond's field duties/fixed owner basis, three allowance excesses, and proposed Kyle $390 inclusion. |
| Annapolis Courier | C-110 107820.45; T-610 176694.95 | Reject: Lena's 25 qualifying pay weeks transfer $22808.75; one-day weeks remain clerical. |
| Larkspur Lane Bistro | F-710 340725.35 | Provisionally reject: supplied receipts show approximately 22.00395% catering; calendar-period proxy remains open. |

Lead checks passed: six exact filenames; exact three-column headers; positive amounts with two decimals; description paragraph IDs read from the current guide; known register plus net adjustments equals allocated totals; expected code totals; six report/question sections; a confirmation question for every allocation adjustment and relied-on source; all 131 numbered case-evidence notes linked to questions; five owner issues retain null amounts; every issue remains open with no fabricated confirmations.

Case notes add specific employee IDs, dates/weeks, invoice IDs, raw source row references, amounts and interview timestamps. The renderer validates registered evidence references and requires a specific confirmation question for each note. Application aggregates are not converted into invented named employee classifications. Notes remain agent-reviewed interpretation and must agree with calculation ledgers.

## Reuse and verification

`python3 -m unittest discover -s tests -v`: **32 tests passed** (28 existing plus four CLI checks). See `gate3-reuse-checks.md` for concrete synthetic inputs, commands, and results:

- New employer produces the expected C-110/E-510 split with unique names, IDs and amounts.
- Changed source bytes reject stale hashes. After reviewed normalization and updated fingerprints, a fifth site day transfers the affected employee's whole pay and changes output totals; previous output remains intact.
- Missing case/source/mandatory data refuses publication, including a partially valid bundle; preexisting destinations are preserved.
- Null owner amounts and unresolved status survive both runs; numbered case evidence/questions retain their links and reject invalid fields/references.

Skill metadata validation passed. Local scanner 2.0.13 exited 0, with only INFO `MANIFEST_MISSING_LICENSE` at `SKILL.md`, accepted because no redistribution license has been selected. No LOW/MEDIUM/HIGH/CRITICAL findings. Report: `.runs/gate3-checks/skill-scan.md`. The scanner's telemetry persistence warning used an in-memory identifier; its incidental local runtime file was moved into the ignored run directory. No cloud analyzers were enabled; a pass is not security certification.

## Open items and handoff

Harbor's office-wording exception, governing-order application, Kent's identity and full-period coverage, five missing owner elections/unknown additional amounts, Kyle's zero-day allowance, and Larkspur's receipts alignment remain open. The report preserves alternatives and uncertainty; software acceptance grants no audit sign-off. Severn and Larkspur remain the two recommended calls for the evidence that could change $52260.78 of subcontractor additions and $114293.80 of catering classification respectively.

`G2 Complete` was pushed to main as `115ab0b`, with Entire checkpoint `01M6G16M45PXZVT2QQXZZCJ9YV`. Post-push usage reading: 9,989,631 session tokens including cache reads, recorded in the tracker as partial project coverage; active agent time is unknown. Gate 3 files and the post-push tracker update remain local for review. Real Entire session records, not these verification notes, supply coding-session capture evidence; Gate 4 will check final revision linkage.
