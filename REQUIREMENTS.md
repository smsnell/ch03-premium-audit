# Class Code and Premium Audit Assistant

## Scenario

Linden Shore Mutual writes workers' compensation insurance in Maryland. Underwriting is quoting six new employers, and before a quote goes out the premium audit team checks that each employer's payroll sits under the right class code. Employers fill in their own payroll split on the application, and the audit team confirms or corrects it from the employer's records. Nadia Brennan, Senior Premium Auditor, wants a reusable Agent Skill that does the first pass on any employer file: suggest the class codes, allocate the payroll to them, and list the questions she should put to the employer. The company, people, employers and records are fictional.

## Your task

Build the Skill and run it on all six employers: Harbor Point Legal, Bay Crest Exteriors, Severn Homebuilders, Patuxent Electric, Annapolis Courier and Larkspur Lane Bistro.

The employer files and the classification rules are not in the starter repository. Read them from the locations the auditor gives you, during each run. This company uses its own class codes; public classification manuals do not apply and will give wrong answers. Where the written rules leave a case open, or an employer's records disagree with what the employer reported, find out from the auditor how her team handles it rather than guessing, and say in the report which records decided each case. The Skill classifies and allocates payroll only; it does not set rates or quote premium.

## Deliverables

Paths are relative to your repository.

| Path | Required content |
| --- | --- |
| `skills/class-code-assistant/SKILL.md` | Reusable Skill instructions with name and description metadata, inputs, invocation, outputs, error behavior and references to its supporting files. |
| Supporting Skill files | Your code and focused references under the Skill or documented project paths; no answers hardcoded for these six employers. |
| `README.md` | Setup, the command that runs the Skill on one employer and on all six, how you verified the results, **and how to rerun the Skill on a new employer file**. |
| `deliverables/codes/<employer>.csv` | One file per employer, named `harbor-point-legal.csv`, `bay-crest-exteriors.csv`, `severn-homebuilders.csv`, `patuxent-electric.csv`, `annapolis-courier.csv` and `larkspur-lane-bistro.csv`. Columns exactly `class_code,payroll_allocated,rationale_ref`: one row per class code that carries payroll at that employer for the audit period, no rows with zero payroll. `payroll_allocated` is US dollars to the cent without thousands separators. `rationale_ref` is the identifier, exactly as printed in the company's classification rules, of the paragraph that describes the code. |
| `deliverables/audit-questions.md` | One section per employer with the questions the auditor should put to the employer before signing off. Each question names the employee, subcontractor or record it is about. Every adjustment you make, and every record your decision relies on, has at least one question asking the employer to confirm it. |
| `deliverables/audit-report.md` | One section per employer: the codes and payroll you allocated; where and why your allocation differs from the employer's own split; every adjustment, naming the employee or payment it concerns and its amount to the cent; and the records that support it. |
| Coding-session evidence | The capture tool's real session records for the submitted code revision; self-written logs do not substitute for them. |

In your coding session, decide and state in your own words whether you accept each employer's own payroll split, and what record that decision rests on.
