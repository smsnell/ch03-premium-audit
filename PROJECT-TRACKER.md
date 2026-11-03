# Project tracker

Keep this file concise: current state, next gate, material blockers, and one cumulative usage summary. Detailed decisions belong in `IMPLEMENTATION-PLAN.md` and source interviews.

## Current context

- Phase: planning approved on 2026-11-03; implementation not started. Owner authorized Gate 1 and conditional progression through Gate 2, then review. P1–P7 and draft-output contract approved as provisional only.
- Confirmed: 15 roof-day threshold; governing field code by payroll; 60% subcontractor inclusion without full-period coverage; one-day route weeks clerical/site rule inapplicable; 40% catering threshold (interview-only, absent from guide); one suitable confirmation suffices.
- Next: push Planning Complete, finish Gate 1 source/runtime checks, then Gate 2. Entire caller-env session is active; planning capture is pending. At most one further stakeholder conversation reserved.
- Open: Harbor/no field code; governing calculation order; Kent identity; five missing owner elections/precedence; Kyle's $390; receipt-period mismatch; draft CSV handling. Proposed calls: Severn and Larkspur.
- Ownership: Astra High lead; bounded Sol 6.1 tasks assigned within each approved stage. No implementation tasks assigned yet.

## Cumulative usage — update at each push

| Metric | Project estimate | Cumulative actual through last push |
| --- | ---: | ---: |
| Agent time | 4 hours | Unknown — no verified cumulative measurement yet |
| Tokens | 50,000,000 | 1,790,977 reported session tokens at pre-push cutoff; partial project coverage |

- Push preparation: Planning Complete on main; success pending. Measurement cutoff: Entire last_active 2026-11-03T00:59:03-05:00, session 01a19fc2-7e8e-7312-982c-a399477e4d95 (caller-env, active). These estimates are planning estimates, not automatic execution or spending authorization.
- At each push, update this file with cumulative usage through the measurement cutoff, cutoff timestamp, source of measurements, and the revision being pushed. Record successful push status afterward; do not report success before it occurs.
- Measured tokens: 153,387 input + 1,621,248 cache-read + 16,342 output = 1,790,977; Entire counts cache reads separately. Earlier setup-session usage and this in-flight turn are not fully covered. Active time is unavailable; session wall time includes waits and is not substituted.
- Count agent-active elapsed time across lead and workers (sum concurrent agents; exclude idle stakeholder waits). Count reported input and output tokens across those sessions, without double counting repeated cumulative readings. State any different provider accounting explicitly.
- Use actual session/tool usage records where available. If a measure is unavailable or coverage is partial, say so and identify the gap; never substitute an estimate as actual or reset an unknown baseline to zero.
- Refresh current context at the same time; retain only outstanding decisions and the next acceptance gate here.
