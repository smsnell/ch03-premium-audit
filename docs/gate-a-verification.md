Owner subsequently accepted Gate A and authorized Gate B. The verification below records the accepted Gate A result.

# Gate A — completeness, allowances and owner uncertainty

2026-11-04 (America/New_York). Owner authorized Gate A after the independent audit, explicitly prioritizing missing individual records as well as missing collections. Implementation and targeted verification were completed at this gate; **the owner has since accepted Gate A and authorized Gate B**. No business confirmation, audit sign-off, commit or push was made.

## Changes

- The helper requires seven explicit record arrays and completeness declarations. Complete collections reconcile identifiers and substantive values against the fingerprint-verified source CSVs, including duplicate multiplicity. Counts copied from normalized data are not the control. Source schemas/allowed exclusions are documented in the input contract. Independent route-log matching and whole-source receipts totals cover lost rides and omitted receipt rows as well.
- Missing mandatory inputs stop publication. A supported empty/not-applicable declaration is explicit. Documented unavailable certificates remain an open coverage problem and do not exempt payment additions.
- Dated allowances share one $47 cap per employee/day. Positive-day aggregates require documented uniform daily rates and exact multiplication; multiple aggregates or aggregate/daily mixtures require dated evidence. Original payments remain in ledger input controls and grouped payment reasons. Reimbursements and zero-day P5 treatment retain their prior behavior.
- Owners explicitly distinguish `unverified`, `included` and `excluded`. Missing election documentation establishes neither inclusion nor exclusion. Evidence-backed inclusion can use the flat field-owner basis without inventing an unknown draw. Unknown non-field remuneration or unresolved treatment of known register pay blocks calculation. The five existing owner omissions retain their provisional open issues and null amounts.
- Ledgers add `input_controls` for completeness declarations, owner evidence/state and original allowance inputs. Existing financial fields, issues, notes, decisions and source fingerprints remain unchanged.

Astra lead owned policy/state code, input-contract migration and integration; bounded Sol 6.1 Medium work updated the existing fixtures and targeted tests. No separate review pipeline was introduced.

## Verification

`PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v`: **59 passed** (45 previous checks with migrated fixtures, 14 Gate A checks).

The negative completeness tests first establish a valid captured-source baseline, then mutate only normalized inputs; they do not regenerate the comparator after deleting a record. Focused checks cover missing arrays/declarations, single employee/invoice/sign-in/roofing/allowance/certificate omissions, same-count invoice identity/amount substitutions, missing route rides, receipts omissions with and without threshold changes, and no partial CLI publication. Synthetic construction helpers used by the other arithmetic tests are not live-source capture utilities.

Additional concrete CLI checks removed each of **all eight Severn invoices individually**, keeping its real captured payment file and fingerprints unchanged. Every case exited 2 with a named `Source reconciliation failed for sub_invoices` diagnostic and created no output. This includes all three insured Tenbury invoices, whose omission would not change a payroll total. Saved results: `.runs/gate-a/verification.json`.

Allowance checks establish $70 + $24 on separate dates adds $23; on one date it adds $47. Duplicate IDs, out-of-period dates, inconsistent same-day classes, unsupported aggregate rates and potentially overlapping inputs fail. Owner tests cover unsupported inclusion/exclusion, preserved unknowns, included off-register field owners with null actual draw, and missing non-field remuneration.

## Six-case preservation and replay

This is a **calculation replay of Gate 3 captures**, not a new live audit. `.runs/gate-a/prepare_replay.py` records the reviewed migration into `.runs/gate-a/six-cases.json`. It adds source-column reconciliation, marks the five uncertain owners unverified, supports Raymond's existing inclusion with business-description evidence, and adds Patuxent's uniform-rate evidence from the existing field notes. It does not alter captured records, wages, duties, existing open issues or confirmations. The original Gate 3 bundle is preserved and intentionally fails the stricter input contract.

From the repository root, with retained local run artifacts:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B skills/class-code-assistant/scripts/audit.py \
  --bundle .runs/gate-a/six-cases.json \
  --output-dir .runs/gate-a/new-replay-six
```

Choose a new destination. A fresh checkout must retrieve and normalize through the Skill as README describes; ignored replay files are not shipped as reusable employer answers.

Compared with the accepted baseline:

- **Six CSVs byte-identical**, including exact references and amounts.
- **Three Markdown deliverables byte-identical**; question-quality changes belong to Gate B.
- Six ledgers differ only by the added `input_controls` field. All previously present fields compare equal. Regenerated ledgers were copied into `deliverables/` only after this check passed.
- **16 issues remain open, five owner amounts remain null, zero confirmations**, and all 131 case notes remain unchanged. No unexpected financial/business difference occurred.

| Employer | Unchanged code allocations (USD) |
| --- | --- |
| Harbor Point Legal | C-110 425148.16 |
| Bay Crest Exteriors | C-110 44812.35; R-310 450480.60; R-320 46205.10 |
| Severn Homebuilders | C-110 117368.70; H-420 369204.39; R-310 27567.39 |
| Patuxent Electric | C-110 43905.60; E-510 372274.85 |
| Annapolis Courier | C-110 107820.45; T-610 176694.95 |
| Larkspur Lane Bistro | F-710 340725.35 |

Harbor remains provisionally accepted on legal-support evidence; Bay, Severn, Patuxent and Courier remain rejected on their recorded duties/logs/payments; Larkspur remains provisionally rejected using the disclosed receipts proxy. These decisions are unchanged and grant no sign-off.

Skill metadata validation passes. Local pinned skill scanner 2.0.13 exited 0; sole finding INFO `MANIFEST_MISSING_LICENSE` at `SKILL.md`, accepted because no redistribution license has been selected. Report: `.runs/gate-a/skill-scan.md`. The telemetry warning used an in-memory identifier. The scan is not a security guarantee; manual inspection found no new network calls, source-content execution or external writes in the helper. `git diff --check` passes. Existing Entire hooks provide real session capture; no manual checkpoint was created and this uncommitted revision has no new commit-linked checkpoint yet.

## Limits and next boundary

Completeness is checked against the supplied captures and reviewed mappings. A source already missing an invoice cannot be proven complete from itself: independent payment registers/control totals and employer confirmation are still needed. Folder inventory, prose interpretation, applicability declarations, inclusion/exclusion evidence and uniform-rate assertions remain agent/auditor-reviewed facts. The helper neither infers those facts nor grants approval.

Unsupported source layouts require verified extraction. New schema fields require reviewed migration; do not manufacture a capture from normalized rows or refresh hashes simply to suppress a discrepancy. Rates, premiums, certificate-renewal policy, governing eligibility, CG-07 support and question redesign are outside Gate A. Gate A stopped for owner review; that acceptance is now recorded in PROJECT-TRACKER.md.
