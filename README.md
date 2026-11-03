# Class Code and Premium Audit Assistant

Reusable, agent-guided payroll classification for Linden Shore Mutual. Uses the company's guide and auditor decisions; does not set rates or quote premiums. Current scope: Gate 3 draft deliverables and verification; Gate 4 integrated completion review requires owner acceptance.

## Setup

Use Python 3 (tested with 3.14.4), standard library only, and an agent with connected Google Drive read tools. The Skill is at `skills/class-code-assistant/SKILL.md`; read it directly when the host does not automatically discover repository skills. Source captures and generated verification drafts live in ignored `.runs/` directories. Do not commit credentials.

## Live Skill runs

In the agent, invoke one employer with:

```text
Use skills/class-code-assistant/SKILL.md for <employer folder URL> with <classification guide URL>; retrieve sources afresh and write drafts to <new output directory>.
```

For all six:

```text
Use skills/class-code-assistant/SKILL.md for every employer in https://drive.google.com/drive/folders/1pt8gzX8HDuaAq6g8ZFeQ66zbVIYdlN_n with guide https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view; retrieve all sources afresh and prepare the six-employer draft package.
```

For a new employer, supply its folder URL and audit period, use the same Skill invocation, and build new source-backed duty mappings. Do not copy another employer's answers. Unsupported duties or missing documents stay explicit open items; additional policy requires auditor confirmation. The agent prepares normalized case JSON using the Skill's input contract, then executes the helper. Prose interpretation and live retrieval are agent tasks; the helper is not an autonomous Drive client.

## Calculation replay

Given reviewed case files and their captured sources, from the repository root:

```bash
python3 skills/class-code-assistant/scripts/audit.py --case path/to/employer.json --output-dir .runs/replay-one
python3 skills/class-code-assistant/scripts/audit.py --bundle path/to/all-six.json --output-dir .runs/replay-six
```

The bundle is a JSON list of normalized cases or an object with a `cases` list. `--case` may also be repeated. Use a new output directory. The helper verifies source fingerprints and input contracts before generating `codes/<slug>.csv`, `audit-report.md`, `audit-questions.md`, and `ledgers/<slug>.json`. Replaying saved cases verifies arithmetic; it does not satisfy fresh retrieval for a new audit run.

All CSVs must travel with the draft report/questions. Owner approval to implement provisional P1–P7 treatments is not employer confirmation. Missing owner remuneration remains unknown, never zero; calculations cannot grant final audit approval.

## Verification

```bash
python3 -m unittest discover -s tests -v
```

Source checks and the requirements map are in `docs/gate1-verification.md`; Gate 2 results are in `docs/gate2-verification.md`. Gate 3 source/run results are in `docs/gate3-source-run.md`; new-employer and changed-source CLI checks are in `docs/gate3-reuse-checks.md`. Tests cover policy boundaries, evidence gaps, money reconciliation, draft status and case-specific evidence.

The six-case draft package is in `deliverables/`. After the fresh agent retrieval and normalization, its calculation command is:

```bash
python3 skills/class-code-assistant/scripts/audit.py --bundle .runs/gate3/six-cases.json --output-dir .runs/gate3/replay-six
```

That local bundle and its fresh captures are ignored run artifacts. To rerun in a new checkout, use the live Skill invocation above to retrieve and normalize sources again; do not expect `.runs/` to be checked in. See `docs/gate3-verification.md` for exact result checks and limitations.

## Interview rule and source handling

**Interview rule.** You conduct the stakeholder interview yourself, and the questions are yours. Do not connect a coding
agent or any other AI to the interview to run, script, or automate it. The interview transcript is assessed together
with the code; a project whose interview was run by an agent is not scored.

- This is a real-case Challenge, closer to client work. The course rule is to plan for at most 3 conversations with the stakeholder, so prepare before each conversation and ask completely.
- The employer files and the company's classification rules are not in this repository. Ask Nadia Brennan, the
  premium auditor you interview, where they are, and read them from there during each run.
- Runtime: Python 3 standard library plus the connected Drive read tools described above.
- Export your interview as the original Markdown, save one final complete file per session under `interviews/`, and
  commit it with your code. Do not rewrite the export.
