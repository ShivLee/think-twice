# Progress

The task record for building think-twice. **Read it at the start of every session and update it at the end.** What
the product does is defined in [REQUIREMENTS.md](REQUIREMENTS.md); the slices and tasks are in [plan.md](plan.md);
this file says where the work stands.

This repository is public: no personal reasoning, journal content or real-use transcripts go here.

## Current outcome

**Slice 1: test feasibility probe, validation script, tests written and frozen.** Serves 5.1 (P-1–P-7), RC-06 and
section 9. Done when tasks T1.1–T1.12 in [plan.md](plan.md) are done, including the owner test review (D44).

## Last verified state

- 2026-10-18: requirements reviewed by Codex in five passes, v0.4 → v0.7.1 (gpt-6-astra, high; thread
  `01a14e42-3bc6-7750-bd9b-be610089efce`). The last pass met the closing condition: no High-severity consistency
  or ambiguity issue. Decisions D30–D42 record what changed.
- 2026-10-18: owner approved REQUIREMENTS as **v1.0** (D43), tagged `requirements-v1.0`. Freeze small: tests and
  real use drive later changes.
- 2026-10-18: Codex reviewed a streamlining proposal (gpt-6-astra, high; thread
  `01a15259-f481-73d2-8658-a609e2c89b01`): NEEDS REVISION. The owner kept the original plan (7 slices, all tests,
  freeze before skill text). Owner approved D44 (slice 1 ends with an owner test review) and D45 (SC-3 counting
  starts after slice 6, with six counting rules).
- 2026-10-18: `docs/plan.md` created (section 9 rule 9). `evals/results/` added to `.gitignore` (T1.1, #14).
- 2026-10-18: Codex rule 9 review of plan.md (gpt-6-astra, high; thread `01a15293-dbca-75b0-b297-9ea90c69f2e3`):
  NEEDS REVISION, 1 High and 5 Medium findings. All six fixed: every test assigned to a slice gate, the omission
  pass placed in slice 6, D45 checkpoints in slices 6 and 7, IDs on every task, stronger done-when for T1.6–T1.8,
  and a plan review before each later slice. Owner chose no re-check.
- 2026-10-18: committed `f7795fa` (D44, D45) and `c6e4471` (plan.md, progress.md, `.gitignore`, HANDOFF.md);
  pushed `main` to `origin`. HANDOFF.md rewritten for this session.
- 2026-10-19: **probe P-1 passed** (T1.2; FR-0.1, QR-11). `claude plugin eval` invokes a manual-only skill
  through `/think-twice:pause <text>` in the case prompt, and passes the text as its argument: 3/3 runs, plus a control
  showing the model cannot invoke it on its own. Claude Code 2.1.303, `claude-opus-5-5`. No fallback needed. Details
  and side findings for T1.3 in [evaluation.md](evaluation.md). Runs used a throwaway plugin outside the repository,
  with `--no-publish`.
- 2026-10-19: **probes P-2–P-7 done** (T1.3; FR-2.1, FR-2.2, QR-12, QR-13, RC-05, SC-1). All pass: pasted and
  real-session conversations behave alike (P-2); fixtures work through `scaffold_script` (P-3); card loads can be
  counted (P-4); scope is reported truthfully after a real compaction (P-5); `--json` has per-run, per-grader results,
  and a small script will compute SC-1 (P-6); the P-7 list is written. Five constraints for the test writing are
  recorded in [evaluation.md](evaluation.md), one of them for the owner (below).
- 2026-10-19: **T1.4 done.** Owner approved D46 (each SC-2 test gets its own plain-wording baseline case) and D47
  (test methods from the probe; every Auto test stays Auto, every Manual test stays Manual for now, revisited after
  slice 2). REQUIREMENTS updated to cite them; `git diff requirements-v1.0` shows only lines citing D44–D47.
- 2026-10-19: **T1.5 done.** `scripts/validate-plugin.sh` implements RC-06 and passes on the current docs (58 FR/QR
  units, 48 tests). `--self-test` passes 14/14 scenarios, including the four required failures: a missing ID, an
  unmapped requirement, a test citing an unknown ID, an undefined subcase. Eval cases declare their IDs in `tags`.
- 2026-10-19: **T1.6 done.** The 5.2 tests are written: 34 auto cases in `evals/`, 10 SC-2 baseline cases in
  `evals-baseline/` (D46), and 9 manual scripts in `evals/manual/`. Every case declares its IDs, dialogue state and
  graded reply; every PASS and FAIL condition in its row has a grader; every case checks the critical failures, AT-12
  and RC-05. Dialogues are frozen as `dialogue.md` and built by `scripts/build-histories.py` (D47). Gaps #7, #10 and
  #18 settled ([plan.md](plan.md)). A smoke run confirmed the mechanics, and a judge calibration led to a tighter
  critical-failure wording ([evaluation.md](evaluation.md)). Not frozen yet (T1.10).
- 2026-10-19: **T1.7 done.** The 5.3 situation tests are written: 10 auto cases (AT-S1–AT-S7, with AT-S2 and AT-S3
  as two prompts each, and AT-S7 as no-cue and two-cue cases) and 4 SC-2 baseline cases (AT-S1, AT-S2a, AT-S2b,
  AT-S5). Same conventions as T1.6. A smoke run checked the multi-line pause argument in AT-S3b. Not frozen yet.
- 2026-10-19: AT-31 and AT-41 test pages published in the public repository `ShivLee/think-twice-fixtures` and
  pinned by commit (`0787d68`), on the owner's choice after a Codex consultation (thread
  `01a15293-dbca-75b0-b297-9ea90c69f2e3`). AT-31's preflight passes: 200 with the expected SHA-256, and a real 404.
  AT-31's page is now the owner's own conclusion (fixing a conflict with S3); every manual script now says a critical
  failure in any run fails the test; FR-0.8's redirect rule is recorded as a known gap.
- 2026-10-19: **T1.8 done.** The 5.4 tests are written: AT-26 (auto case, plus a manual follow-up), AT-28 (the
  Chinese versions of AT-04, AT-08, AT-02 and AT-S1, with the same graders), AT-29 (an instruction injected into the
  owner's notes), and manual scripts for AT-27 (journal, protecting any real journal) and AT-41 (commit-pinned page;
  preflight passes). `scripts/sc1-gate.py` computes SC-1; its self-test passes 15/15 (including the three required
  examples) and it reads real eval output. The Chinese length rule was simplified to CJK characters. All tests in
  section 5 are now written; none is frozen yet.
- No product skill text has been written yet.

## Slice 1 status

| Task | Status |
| --- | --- |
| T1.1 Eval privacy | `.gitignore` done; `--no-publish` applies from the first run |
| T1.2 Probe P-1 | Done 2026-10-19: pass ([evaluation.md](evaluation.md)) |
| T1.3 Probes P-2–P-7 | Done 2026-10-19: all pass ([evaluation.md](evaluation.md)) |
| T1.4 Set the "How" column | Done 2026-10-19 (D46, D47) |
| T1.5 Validation script (RC-06) | Done 2026-10-19 |
| T1.6 Tests in 5.2 | Done 2026-10-19 (not frozen until T1.10) |
| T1.7 Tests in 5.3 (situations) | Done 2026-10-19 (not frozen until T1.10) |
| T1.8 Tests in 5.4 and the SC-1 gate | Done 2026-10-19 |
| T1.9 Owner test review (D44) | **Next** |
| T1.10–T1.12 | Waiting |

The test-level gaps to settle before the freeze (Codex #7, #10, #12, #13, #18) are listed in
[plan.md](plan.md#test-level-gaps-to-settle-in-t16t18-codex-review).

## Next action

T1.9: the owner test review (D44). Read a sample chosen in advance, covering the three phases and the four failure
modes (QR-1 substitution, QR-2 manufactured objections, QR-3 overstated facts, QR-4 agreement, and QR-5), and check
each case: is it a situation the owner actually meets, and would its PASS behaviour really help? Fix unrealistic
cases before the freeze (T1.10).

## Waiting on the owner

- Nothing at the moment.
