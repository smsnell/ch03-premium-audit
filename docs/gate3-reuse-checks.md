# Gate 3 reuse and incomplete-input checks

Checked 2026-11-03. These are synthetic software checks, separate from the six-employer evidence run. Juniper Spark Services, its employees, records, policy, and amounts are invented; they supply no business evidence. The helper receives explicit agent-normalized duty mappings and inputs. It does not fetch or interpret raw employer records itself.

## Results

`python3 -m unittest discover -s tests -v` passes **32 tests**: the existing 28 Gate 2 checks and four new CLI checks in `tests/test_gate3.py`. The new checks run `audit.py` as a Python subprocess against files on disk, and inspect the resulting CSV, JSON ledger, report, and questions.

- New employer: JS-E17 Mira Calder has $72,819.43 in electrical installation; JS-E29 Owen Vale has $18,234.56 office payroll and four site dates. Output is C-110 $18,234.56 / E-510 $72,819.43, total $91,053.99, provisionally accepting the reported split. Exact output paths, three CSV columns, positive two-decimal amounts, code-description references, register reconciliation, source fingerprints, and source questions are checked.
- Changed source: the register changes Owen's pay to $19,456.78 and the site log adds a fifth date. The saved case with stale fingerprints exits 2 with `Source fingerprint mismatch: register`, creating no output directory. After updating source fingerprints **and reviewing/updating the normalized pay, reported amount, and site records**, the CLI emits E-510 $92,276.21 only. The ledger preserves the $19,456.78 C-110 → E-510 reclassification, zero net monetary adjustment, new register total, and provisional rejection. The previous output bytes remain intact. A fingerprint update alone is not a source interpretation step.
- Unknown owner: JS-O03 Elena Sato has unknown duties/pay and no election. Both runs preserve an `open` election issue with JSON `amount: null` and `alternative_amount: null`. The report states `unknown (not zero)`, and questions name the issue. No zero wage or $63,700 amount is invented.
- Missing input/atomic publication: a valid first case followed by a missing case file, missing source file, missing `people` field, or null employee pay exits 2 with an explicit incomplete diagnostic. No partial output or staging directory remains. An existing destination is refused and its sentinel contents remain intact.
- Case evidence: a note's subject, detail, evidence, and confirmation question survive into the ledger. Report and questions share `juniper-spark-services-evidence-1`, with source references. Empty subject/detail/question and an unregistered source reference each fail before publication.

## Saved CLI evidence

`.runs/gate3-checks/cli-results.json` records argv, working directory, return code, stdout/stderr, and destination existence for five additional concrete invocations: new employer, stale fingerprint, updated normalized case, missing second case, and existing-output refusal. `.runs/gate3-checks/unittest-results.txt` contains the 32-test result. Input snapshots stay separate so both successful outputs retain locally verifiable source fingerprints:

- `.runs/gate3-checks/initial-input/case.json` and `initial-output/`
- `.runs/gate3-checks/changed-input/case.json` (stale) and `updated.json` (reviewed changes), plus `changed-output/`

From the repository root, replay successful cases into new destinations:

```sh
python3 skills/class-code-assistant/scripts/audit.py --case .runs/gate3-checks/initial-input/case.json --output-dir /tmp/juniper-initial-replay
python3 skills/class-code-assistant/scripts/audit.py --case .runs/gate3-checks/changed-input/updated.json --output-dir /tmp/juniper-changed-replay
```

Choose destinations that do not already exist. The stale `changed-input/case.json` intentionally fails fingerprint validation. These checks establish bounded CLI reuse and failure behavior; they do not validate an agent's interpretation of unseen source prose or grant audit approval. No defects or blockers were found in this bounded check. Gate 4 completion review remains separate.
