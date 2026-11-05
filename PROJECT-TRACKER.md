# Project tracker

Keep this file concise: current state, next gate, material blockers, and one cumulative usage summary. Detailed decisions belong in `IMPLEMENTATION-PLAN.md` and source interviews.

## Current context

- **Owner accepted Gate B and all completed reporting/judgment work on November 5, 2026.** Gate A was already accepted. The owner authorized final checks, commit/push, then a separate token-accounting tracker update and push. **Software acceptance is not audit sign-off.**
- Accepted scope: individual-record completeness; daily allowance caps; explicit owner uncertainty; supported governing field eligibility; actual time/pay CG-07 splits; priority-ordered employer questions with visible individual outcomes and linked traceability; readable currency; the evidence brief and owner judgment record. See [Gate A](docs/gate-a-verification.md), [Gate B](docs/gate-b-verification.md) and [final acceptance](docs/final-acceptance.md).
- [JUDGMENTS.md](JUDGMENTS.md) now says the owner is judging **allocations supplied by the employers**, without independently recalculating every record. Six provisional employer decisions and the Severn-first/Larkspur-second call ranking remain separate. The owner-confirmed Severn addition is **$52,260.78**; recording checks are [separate](docs/judgments-verification.md).
- Business state unchanged: six payroll allocations preserved, **16 issues open**, **five unknown owner amounts**, **131 original evidence notes**, **zero case confirmations**. Missing evidence and P1–P7 limitations remain visible; follow-up evidence and scoped auditor decisions are still required.
- Lead owns integration/final review; Sol 6.1 supplied bounded implementation, tests and recording checks. Final checks passed: **86 tests**, exact reproduction of all 15 generated files, Skill validation and local scan (license INFO only). Publication is next; actual commit/checkpoint details and the refreshed accounting cutoff will be recorded after the first push.

## Cumulative usage — prior snapshot; refresh after publication

| Metric | Project estimate | Reported cumulative actual |
| --- | ---: | ---: |
| Total work time | 4 hours | **Approximately 8 hours, a user-supplied estimate—not measured elapsed or active time** |
| Tokens | 50,000,000 | **28,653,026**, partial coverage; includes cache reads and reported workers |

- G4 Complete: `575f253`, successfully pushed to origin/main on 2026-11-03. Entire checkpoint `01M6G3ZFXW7A7R4EYEKQTZWS25` synced and transcript verified. This follow-up records the post-push evidence and usage cutoff.
- Measurement: Entire caller-session `01a19fc2-7e8e-7312-982c-a399477e4d95`, post-push session reading **23,227,476** = 786,248 input + 22,384,384 cache-read + 56,844 output. The pre-push reading separately reported **5,425,550 worker tokens**, yielding **28,653,026** combined; no repeated cumulative reading is added twice. Post-push output dropped the worker subtotal, so the latest reported subtotal is retained separately.
- Coverage: setup/other sessions and in-flight lead/worker usage may be missing. The current checkpoint's 5,692,297 tokens overlap session usage and are **not added**. These are final available measurements, not a claimed complete billed total; do not substitute estimates for unavailable active time.
- Measurement recorded: 2026-11-03T07:13:09.646268+00:00. Refresh at any later push if a newer cumulative reading is available; retain this cutoff rather than claiming bookkeeping calls are included.
