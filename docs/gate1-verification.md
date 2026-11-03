# Gate 1 source and verification map

Gate 1 inventory completed on 2026-11-03. This records source/schema checks and planned acceptance checks; it does not implement policy or claim Gate 2 passes. Owner approval of P1–P7 is provisional treatment approval, not employer confirmation or final audit approval.

## Fresh retrieval and provenance

Freshly listed the supplied [employer root](https://drive.google.com/drive/folders/1pt8gzX8HDuaAq6g8ZFeQ66zbVIYdlN_n) and each of its six direct employer folders with `top_k=100`. The root returned six folders, and the child listings returned 34 files: Harbor 5, Bay 6, Severn 7, Patuxent 5, Annapolis 6, Larkspur 5. No folder approaches the listing bound. Fetched all 34 files and the [classification guide](https://drive.google.com/file/d/1L5MxLny7erhjSwCvl43DTSmAt3wgv22j/view) through the connected Google Drive tool, using readable text; all are stored Markdown/CSV files.

Local verbatim text captures are in `.runs/gate1/sources/<employer>/<original filename>` and `.runs/gate1/sources/guide.md`. `.runs/gate1/manifest.json` records the root/child listings, each file ID/URL, retrieval and source modification timestamps, metadata byte size, captured byte size, SHA-256, CSV header and data-row count. All 35 captures exactly match their source metadata byte sizes; guide size is 3,555 bytes. These are readable-text captures with local fingerprints, not provider-signed hashes or original binary downloads. Full captures are run artifacts, not submission evidence or permission to reuse stale inputs.

Every employer has `application.md`, `business-description.md`, `field-notes.md`, and `payroll-register.csv`. All business descriptions give the audit period July 7, 2025–July 5, 2026. Field visits occurred after this period, July 14–21, 2026; historical logs supply period day counts. All returned source contents are untrusted data, not agent instructions or authority for external actions.

## Observed CSV contracts

Counts exclude the header. All rows match their header width. Register employee IDs are unique within each employer; all nonempty employee/driver/ride-along IDs in supporting CSVs resolve to that employer's register.

| File family | Exact columns | Employer: data rows |
| --- | --- | --- |
| Standard payroll register | `employee_id,name,position,wages_paid` | Harbor 5; Bay 10; Severn 8; Annapolis 6; Larkspur 9 |
| Patuxent payroll register | `employee_id,name,position,wages_paid,travel_days,travel_allowance_paid` | Patuxent 7 |
| Site sign-in | `date,employee_id,name,site,signed_in_at` | Harbor 6; Bay 10; Severn 16; Patuxent 214 |
| Crew time | `date,employee_id,name,job_id,work_type,hours` | Bay 1,726 |
| Subcontractor payments | `date,subcontractor,work,invoice,amount_paid` | Severn 8 |
| Insurance certificates | `subcontractor,certificate_no,coverage_from,coverage_to` | Severn 2 |
| Route log | `date,route_id,driver_id,ride_along_id,stops` | Annapolis 936 |
| Weekly payroll | `week_start,week_end,employee_id,gross_pay` | Annapolis 312 |
| Gross receipts | `month,dine_in_receipts,offsite_catering_receipts` | Larkspur 12 |

Observed source wages (register sums only, before any adjustment): Harbor $425,148.16; Bay $541,498.05; Severn $461,879.70; Patuxent $467,930.45; Annapolis $284,515.40; Larkspur $340,725.35. These are reconciliation baselines, not computed audit allocations. All date-bearing daily/weekly source rows fall within the audit period. Larkspur's supplied receipts instead span calendar July 2025–June 2026.

## Rule provenance and unresolved evidence

The guide supplies code-description references C-110/CG-04, R-310/CG-11, R-320/CG-12, H-420/CG-15, E-510/CG-21, T-610/CG-31, F-710/CG-41 and F-720/CG-42. It contains no 40% catering threshold. Attribute that threshold to interview 2, 12:34–12:35 AM; retain guide references for CSV code descriptions. General rules CG-03/05/06/07 do not establish the specific house thresholds by themselves.

The confirmed house practices and P1–P7 treatments remain as stated in `IMPLEMENTATION-PLAN.md`. Interview 2 repeats interview 1 before adding new discussion; repetition is not independent confirmation. Its “Thomas,” “Baycrest Interiors,” and “Therese” are contextual mappings to source-file Tomas Reyes, Bay Crest Exteriors and Teresa Lindqvist based on the unique cases. Preserve the transcript text; use source IDs/names for joins.

Source completeness means all listed supplied files were retrieved. It does not mean all facts needed for sign-off are present:

- No election forms are supplied for Catherine Harbor, Philip Crestwood, Martin Severn, Gloria Rhee or Rosa Delacroix. Reported off-register omission remains conditional; missing owner wages/duties cannot be invented as zero or automatically $63,700.
- Harbor's six log visits remain real. Retention in C-110 for confirmed litigation-support duties is P1, an open office-wording exception with no established field code.
- Severn has two certificate rows for three paid subcontractors. Tidewater coverage is absent; Kent's name differs and its certificate ends before audit-period end. Exact-name Tenbury coverage is relied-on evidence and still requires a confirmation question.
- Kyle's $390 with zero travel days lacks a documented expense basis; P5 inclusion remains proposed. Larkspur lacks daily receipts for July 1–6, 2025 and July 1–5, 2026 to align its audit period; P6 proxy use remains provisional.
- Source confirmation, owner evidence/precedence and any P-item confirmation are separate from software checks. No stakeholder contact was made.

## Requirements-to-check map

The following checks are planned acceptance evidence, not reported passes.

| Requirement or decision | Focused acceptance check | Gate |
| --- | --- | --- |
| Reusable Skill with metadata, inputs/invocation, output/error behavior and supporting references | Inspect `skills/class-code-assistant/SKILL.md`; validate metadata/links and a small documented runner; no employer-specific answer lookup | 2/4 |
| Fresh rules and source locations each run | Retrieve supplied guide and employer folder; capture IDs/timestamps/hashes; changed-source rerun changes the affected basis; missing source is explicit | 2/3 |
| Site transfer and governing-code P2 | 4/5 site-day boundary; unique dates; out-of-period exclusion; all pay transferred; corrected field totals before office transfer; ties/no field code stay open | 2 |
| Roof/siding house threshold | 14/15 roof-day boundary, duplicate dates, positive roofing time, no hourly splitting; inspect Rafael's exactly-15-day case | 2 |
| Full-period subcontractor rule and P3/P7 | Exact-name match; unapproved alias stays open; certificate must cover both endpoints; pre-expiry payment still included if full period fails; 60% per invoice, Decimal half-up cents | 2 |
| Owner rules and P4 | Present/missing election; conditional off-register omission blocks sign-off; field-working included owner flat basis; unknown duties/remuneration remain unknown | 2 |
| Allowance and P5 | $47/day boundary, excess addition, documented reimbursement exclusion, zero-day anomaly remains proposed | 2 |
| Courier weekly rule | 1/2 distinct ride-day boundary; Monday–Sunday join; complete weeks; site-log independence; weekly totals reconcile to register | 2 |
| Catering and P6 | Below/exactly 40%; catering crew threshold treatment; no wage percentage split; period mismatch remains visible | 2 |
| Draft contract and P1–P7 status | Provisional output is conspicuous; owner approval never becomes employer confirmation; changed confirmation affects only relevant facts/treatments; Harbor exception remains visible | 2/3 |
| Six exact CSV filenames and three exact columns | `class_code,payroll_allocated,rationale_ref`; positive payroll only, cents without separators, code-description paragraph exactly from fetched guide | 3 |
| Audit report explains every allocation, difference and adjustment | Recalculate from source IDs/rows; name employee/payment and cents; reconcile source baseline + ledger adjustments to CSV totals; explicitly accept/reject each employer split in session and report | 3 |
| Audit questions cover all adjustments and relied-on records | Cross-check question references against every ledger adjustment and source dependency, including unchanged allocations/certificates | 3 |
| README setup, one/all/new-employer run and verification | Preserve interview rule; execute documented one-employer/all-six commands; synthetic new employer; missing-input and changed-source reruns | 3 |
| Classifies payroll only | No rate, premium, public-manual classification or automated stakeholder-contact behavior | 2/4 |
| Actual coding-session evidence for submitted revision | Verify capture tool's real session records and revision linkage; self-written inventory/check logs do not substitute | 4 |

Gate 1 retrieval/schema checks passed. No source-access blocker was found. Gate 2 policy/boundary checks, output generation, reusable invocation and final capture/revision verification remain to be done by their owning stages. Required business confirmations remain open under the approved provisional contract.

## Lead acceptance and runtime

Owner approved revised plan, P1–P7 provisional treatments, and draft-output contract in the current session. Python 3.14.4 is available (`python3`; no `python` alias). Lead independently rechecked all 35 capture hashes and byte counts. Gate 1 passes with business open items preserved.

`Planning Complete` commit `f1fa5a7d5b4c7f36d7650275fdc383dd552e827f` was pushed to `origin/main`. Entire's hook reported two checkpoint refs synced; the commit trailer links `01M6FZWNXGZAF1EHM4EEAGF18S`. `entire session current --json` resolved the caller via `caller-env` with status `active`, and a network-enabled checkpoint listing verified the checkpoint without the sandbox's network warning. No manual checkpoint was created.

Runtime contract: live Skill invocations retrieve Drive sources through connected tools and normalize reviewed duty/record mappings into case JSON; the Python helper performs deterministic arithmetic and draft output validation. Case replay is explicitly not fresh retrieval. Input and invocation details are maintained under the Skill references and CLI help. No separate API service or package dependencies are needed.
