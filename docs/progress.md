# Progress

The task record for building think-twice. **Read it at the start of every session and update it at the end.** What
the product does is defined in [REQUIREMENTS.md](REQUIREMENTS.md); this file says where the work stands.

This repository is public: no personal reasoning, journal content or real-use transcripts go here.

## Current outcome

**Approve the requirements as v1.0.** The feature discussion closed on 2026-10-18 (Codex: closing condition MET
on v0.7.1). Done when the owner approves, and the file is committed and tagged `requirements-v1.0`.

## Last verified state

- 2026-10-18: Codex reviewed REQUIREMENTS v0.4 (gpt-6-astra, high). Verdict: **NEEDS REVISION**, 23 findings.
  Codex thread `01a14e42-3bc6-7750-bd9b-be610089efce`.
- 2026-10-18: owner approved D30–D35. REQUIREMENTS v0.5 applies them.
- 2026-10-18: Codex verified v0.5 (same thread). 7 findings fixed, 7 partial, 9 deferred; 5 new issues (N1–N5).
  **Closing condition NOT MET.** Blockers: N1, #16, #17, and the evaluation-contract part of #22.
- 2026-10-18: owner approved D36–D41 (after a drift check against the goal). REQUIREMENTS v0.6 applies them,
  with N2–N5.
- 2026-10-18: Codex verified v0.6. Fixed: N2–N5, #16, #22. Partial: N1 (now Medium, V3), #17 (V1, V2).
  Drift check: no drift in D36, D37, D40, D41; a risk in D38 (V1) and D39 (what SC-2 claims). **Closing condition
  NOT MET.** Blockers: V1, V2.
- 2026-10-18: owner approved D42. REQUIREMENTS v0.7 applies it, with V3, V4 and an SC-2 scope line. Applied,
  not yet verified.
- 2026-10-18: Codex verified v0.7. Fixed: V2, V3, V4. **NOT MET**: W1 (High), the verdict order made "Sound if
  narrowed" unreachable; W2 (Medium), AT-34 didn't enforce the wait. v0.7.1 swaps the order (D42 corrected) and
  fixes AT-34.
- 2026-10-18: Codex verified v0.7.1. W1, W2 fixed; no new issues; D42 drift check clean. **Closing condition
  MET.** Feature discussion closed.

## Tasks

| Task | Serves | Status | Done when |
| --- | --- | --- | --- |
| Apply D30–D35 to REQUIREMENTS v0.5 | D30–D35 | Done | Codex check passes |
| Codex checks the v0.5 changes | Section 9 | Done: NOT MET | No High-severity consistency or ambiguity finding |
| Owner decides on the four blockers (N1, #16, #17, #22 evaluation contract) | FR-0.2, FR-0.6, FR-1.2–1.7, FR-2.3, SC-2 | Done: D36–D39 | Decision entries approved |
| Fix N2–N5 (AT-31 split, FR-5.7 headline, AT-29b vs subcase rule, lesson timing) | FR-0.8, FR-5.7, RC-06, FR-2.4 | Done: D41 | Applied in v0.6 |
| Codex checks v0.6, including a drift check of D36–D41 (D40) | Section 9 | Done: NOT MET | Closing condition met; no drift |
| Owner decides on V1 (verdict precedence) and V2 (AT-06 vs AT-40); fix V3, V4 | FR-2.7, FR-1.3, FR-1.7, AT-06, AT-35 | Applied (D42), not verified | Applied as v0.7 |
| Codex checks v0.7 | Section 9 | Done: NOT MET (W1) | Closing condition met |
| Codex checks v0.7.1 (W1, W2) | Section 9 | Done: MET | Closing condition met |
| Resolve the open review findings below that block freezing the tests | Section 5 | Waiting | Each is fixed, or deferred by the owner |
| Owner approves v1.0; commit and tag `requirements-v1.0` | Section 9, rule 7 | **Next** | Tag exists |
| Slice 1: feasibility probe P-1–P-7, validation script with RC-06 | 5.1, RC-06 | Waiting | Results in `docs/evaluation.md`; RC-06 passes |

## Open review findings (Codex, 2026-10-18)

Not addressed by D30–D41. Codex verified #16 and #22 as fixed; N1 and #17 are partly fixed (V1–V3). Numbers refer to the Codex review.

**Before the tests are frozen:**

- #7 Behavioural coverage: QR-2's four conditions; FR-1.3's "examined and accepted" group; the before phase not
  reading anything on its own initiative; affected people and other fields (Perspectives lens).
- #18 Counting rules for QR-6 and QR-13 (tokenizer, mixed languages, tolerance) and which cards to load first when
  more than 3 apply.
- Partial fixes still to finish: #5 (redirects, oversized input), #6 (retry, partial write), #10, #12, #13 (an SC-1
  aggregation gate even when P-6 passes).

**Later (no blocker for freezing):**

- #9 Procedure for changing method cards and tests (CONTRIBUTING.md covers situations only).
- #14 Keep eval results private (`--no-publish`, results out of git).
- #19 What "one pass" means alongside the correction loop.
- #21 Paired self-review cases: the same reasoning attributed to Claude, to me and to a third party.

## Waiting on the owner

- Approval of v1.0, and whether to settle the requirement-level items below first.

## Next action

Owner decides on v1.0 approval. Codex thread for later checks: `01a14e42-3bc6-7750-bd9b-be610089efce`.
