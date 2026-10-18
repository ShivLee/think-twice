# Progress

The task record for building think-twice. **Read it at the start of every session and update it at the end.** What
the product does is defined in [REQUIREMENTS.md](REQUIREMENTS.md); this file says where the work stands.

This repository is public: no personal reasoning, journal content or real-use transcripts go here.

## Current outcome

**Slice 1: test feasibility probe, validation script and test-level gaps.** Serves 5.1 (P-1–P-7), RC-06 and
section 9. Done when the P-1–P-7 results are in `docs/evaluation.md`, the "How" column of section 5 is set from
them, the validation script runs RC-06, and the test-level gaps below are settled before any test is frozen.

## Last verified state

- 2026-10-18: requirements reviewed by Codex in five passes, v0.4 → v0.7.1 (gpt-6-astra, high; thread
  `01a14e42-3bc6-7750-bd9b-be610089efce`). The last pass met the closing condition: no High-severity consistency
  or ambiguity issue. Decisions D30–D42 record what changed.
- 2026-10-18: owner approved REQUIREMENTS as **v1.0** (D43), tagged `requirements-v1.0`. Freeze small: tests and
  real use drive later changes.
- Nothing is built yet. No test has been written or run.

## Tasks

| Task | Serves | Status | Done when |
| --- | --- | --- | --- |
| Run probes P-1–P-7 with a throwaway skill | 5.1 | **Next** | Results recorded in `docs/evaluation.md`, with CLI and model versions |
| Set the "How" column of section 5 from the probe results | 5.1 | Waiting | Every test has Auto or Manual set from evidence |
| Validation script with RC-06 (traceability and goal map) | RC-06, section 9 rule 8 | Waiting | Script fails on a missing ID or an unmapped requirement |
| Settle the test-level gaps below | Section 5 | Waiting | Each is written into its test or grader before freezing |
| Write and freeze the acceptance prompts and graders | Section 9 rule 2 | Waiting | Frozen; changes need a decision entry |

## Test-level gaps to settle in slice 1 (Codex review)

Settle these while writing the tests, before freezing them. Numbers refer to the Codex review.

- #7 Behavioural coverage: QR-2's four conditions; FR-1.3's "examined and accepted" group; the before phase not
  reading anything on its own initiative; affected people and other fields (Perspectives lens).
- #12 Probe records CLI and model versions, and checks that the baseline gets an equivalent task.
- #13 An SC-1 gate that computes "≥2 of 3 runs, no critical failure" from per-run results, even when P-6 passes;
  how manual tests are re-run.
- #18 Counting rules for QR-6 and QR-13 (tokenizer, mixed languages, tolerance) and which cards load first when more
  than 3 apply.
- #10 is decided by probe P-5.

**Later (no blocker for freezing):**

- #9 Procedure for changing method cards and tests (CONTRIBUTING.md covers situations only).
- #14 Keep eval results private (`--no-publish`, results out of git).
- #19 What "one pass" means alongside the correction loop.
- #21 Paired self-review cases: the same reasoning attributed to Claude, to me and to a third party.

## Waiting on the owner

- Whether to push to `https://github.com/ShivLee/think-twice.git`.

## Next action

Start slice 1 with probe P-1: can `claude plugin eval` invoke a manual-only skill through `/think-twice:pause`?
