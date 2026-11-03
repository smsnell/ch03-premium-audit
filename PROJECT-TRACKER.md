# Project tracker

Keep this file concise: current state, next gate, material blockers, and one cumulative usage summary. Detailed decisions belong in `IMPLEMENTATION-PLAN.md` and source interviews.

## Current context

- Gates 1–4 software/package accepted; final question corrections verified and **G4 Complete pushed as 575f253**. See [Gate 4 verification](docs/gate4-verification.md). Software acceptance is not audit sign-off.
- Verified: **45 tests pass**, Skill validation passes, final local scan exit 0 (license INFO only). Regenerated six CSVs and six ledgers byte-identical; 131 notes retained. Human review files 34.55% shorter than Gate 3.
- Fixed: employer/issue-scoped confirmations, calculated allowance classes, field-owner destination, and factual/internal question separation. Final corrections ask Dana about duties/site days, Raymond about reported absence of an election, and each employer about actual audit-period applicability.
- Open: all 16 audit issues unchanged: Harbor exception, governing ordering/application, Kent identity/coverage, **five unknown owner amounts**, Kyle's $390 and receipts proxy. No case confirmations added. P1–P7 provisional; priority calls Severn and Larkspur.
- Completion: checkpoint 01M6G3ZFXW7A7R4EYEKQTZWS25 synced; stored transcript contains final request, 45-test result and regeneration. Next: business evidence review. Business evidence and scoped auditor decisions remain future work; no audit signed off. Astra High integration and bounded Sol 6.1 reporting work complete.

## Cumulative usage — final available snapshot

| Metric | Project estimate | Reported cumulative actual |
| --- | ---: | ---: |
| Agent time | 4 hours | Unknown — no verified cumulative measurement |
| Tokens | 50,000,000 | **28,653,026**, partial coverage; includes cache reads and reported workers |

- G4 Complete: `575f253`, successfully pushed to origin/main on 2026-11-03. Entire checkpoint `01M6G3ZFXW7A7R4EYEKQTZWS25` synced and transcript verified. This follow-up records the post-push evidence and usage cutoff.
- Measurement: Entire caller-session `01a19fc2-7e8e-7312-982c-a399477e4d95`, post-push session reading **23,227,476** = 786,248 input + 22,384,384 cache-read + 56,844 output. The pre-push reading separately reported **5,425,550 worker tokens**, yielding **28,653,026** combined; no repeated cumulative reading is added twice. Post-push output dropped the worker subtotal, so the latest reported subtotal is retained separately.
- Coverage: setup/other sessions and in-flight lead/worker usage may be missing. The current checkpoint's 5,692,297 tokens overlap session usage and are **not added**. These are final available measurements, not a claimed complete billed total; do not substitute estimates for unavailable active time.
- Measurement recorded: 2026-11-03T07:13:09.646268+00:00. Refresh at any later push if a newer cumulative reading is available; retain this cutoff rather than claiming bookkeeping calls are included.
