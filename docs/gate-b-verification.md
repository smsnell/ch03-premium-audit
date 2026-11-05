# Gate B — field eligibility, actual time/pay splits and factual questions

Gate A was accepted by the owner, who authorized this bounded Gate B implementation. This note records the checks completed at the original Gate B review stop. The owner subsequently accepted Gate B and the completed reporting/judgment work on November 5, 2026, and authorized final checks, commit and push; see [final-acceptance.md](final-acceptance.md). No employer confirmation or audit sign-off is implied.

## Changes

- Governing contractor field codes require an explicit reviewed eligibility mapping, supported by the current guide and employer business evidence. Shop payroll cannot win merely because it is larger. Every allocated supported field trade must be represented; missing eligibility fails. Corrected eligible payroll and supported additions still precede office transfers; ties/no destination retain the existing explicit open fallback.
- Ordinary CG-07 splits keep one employee ID and reconcile captured actual time/pay rows to every declared code allocation and the employee's full register wages. Missing records, unsupported allocations, duplicate IDs, invalid hours/dates and mismatched amounts fail. Different wage rates are supported without inventing proportional-pay or rounding rules. Whole-person/whole-week and other specific house rules retain precedence.
- Reviewed `factual_question` fields preserve precise employer questions while retaining original notes and policy requests. The six-case package adds **22 factual prompts**, including Rafael's 15 roof dates, Tomas's six visits/identity, office site counts, owner uncertainty, allowance payments, dispatcher weeks, Kent coverage and both receipts boundaries. Grouped requests retain adjustment/note/source traceability; policy decisions remain internal.

The lead owned policy/state integration, source mapping, contract documentation and replay. Two bounded Sol 6.1 Medium tasks owned reporting/question preparation and focused regressions respectively.

## Checks

| Check | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p 'test_gate_b.py' -v` | **15 passed** |
| `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v` | **76 passed**, including Gate A and reporting checks |
| Standalone CLI: new synthetic field/shop employer | E-510 **300.00**, M-830 **1000.00**; office pay follows E-510 despite larger shop pay |
| Standalone CLI: new synthetic mixed-duty employer | E-510 **100.01**, H-420 **23.44**; total **123.45**, matching actual time/pay records despite unequal rates |
| Incomplete split CLI regression | Exit 2, no new package; existing output preserved |
| Skill `quick_validate.py` | Passed |
| Local pinned scanner 2.0.13 | Exit 0; one INFO, missing license in `skills/class-code-assistant/SKILL.md` |
| `git diff --check` | Passed |

The first full run exposed one older changed-source fixture missing the newly required governing eligibility. Its synthetic evidence declaration was updated; the expected payroll outcome stayed unchanged. The full suite then passed. No unexpected employer allocation difference occurred.

The scanner ran through the [scan-agent-skill instructions](/home/mike/.codex/plugins/cache/fellowship-apprentice-workspace/apprentice-workspace/local/library/skills/scan-agent-skill/SKILL.md), with local analyzers only. The license INFO is accepted because project licensing has not been specified; no license was invented. Manual inspection covered the changed instructions, scripts, resources and file operations: no credential access, network execution, new external writes or destructive operations were added. This check is not certification of business correctness.

## Six-case preservation

This is a calculation replay of the already captured Gate 3 evidence, not a fresh live retrieval. `.runs/gate-b/prepare_replay.py` composes the factual prompts from `prepare_questions.py` with reviewed field mappings for Bay Crest (R-310/R-320) and Severn (H-420/R-310). It reads the accepted Gate A case bundle and preserves original source files and fingerprints. Field eligibility is supported by the captured guide, business descriptions and Severn subcontractor records/field notes.

Run:

```bash
python3 -B skills/class-code-assistant/scripts/audit.py --bundle .runs/gate-b/six-cases.json --output-dir .runs/gate-b/review-output
```

Use a new output directory for a later replay. Run artifacts are ignored; a new checkout/live audit must retrieve and normalize evidence afresh as described in README.

Compared against the accepted Gate A package saved before changes:

- All **six CSVs are byte-identical**. Totals, register baselines, net adjustments, governing comparisons, decisions and allocation amounts/reasons are unchanged.
- All **16 issues**, their amounts/alternatives/statuses and **zero confirmations** are unchanged. All **five unknown owner amounts** remain null.
- All **131 original case notes** and their original questions/details/evidence remain intact; 22 notes gain a separate factual prompt.
- Ledgers add eligibility/time/split control metadata. Severn's Dana transfer gains the reviewed business-description evidence reference; no existing evidence is removed.
- Employer questions intentionally change. The report changes only to display the additional Severn transfer source; internal decisions remain byte-identical.
- The 15 generated files match the reviewed package copied to `deliverables/`.

Evidence: `.runs/gate-b/verification.json`, `focused-tests.txt`, `full-tests.txt`, `skill-scan.md`, `review-output/`, and the standalone CLI inputs/outputs under `new-employer/`. Durable regression tests are in `tests/test_gate_b.py` and `tests/test_reporting.py`; none relies on ignored replay scripts.

## Boundaries for owner review

Eligibility is bounded to the current guide's supported contractor field trades; new codes or changed definitions require compatibility review. The agent still reviews business meaning—source references and fingerprints cannot prove prose claims or discover records missing from every supplied source.

CG-07 currently requires attributable pay alongside actual time. Hours-only records, unallocated bonuses and mixed cases involving the special-rule code families stop for reviewed handling instead of receiving an invented split. This is a deliberate implementation boundary, not an additional stakeholder classification rule. No current six-case employee uses this new generic split path.

P1–P7 and all employer-specific unknowns remain open as before. Software acceptance does not resolve those business questions. The original next action was owner review of Gate B. Subsequent software acceptance and publication authorization are recorded in PROJECT-TRACKER.md and final-acceptance.md.
