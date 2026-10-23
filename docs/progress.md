# Progress

The task record for building think-twice. **Read it at the start of every session and update it at the end.** What
the product does is defined in [REQUIREMENTS.md](REQUIREMENTS.md); the slices and tasks are in [plan.md](plan.md);
this file says where the work stands.

This repository is public (D3; made public on 2026-10-19): no personal reasoning, journal content or real-use
transcripts go here.

## Current outcome

**Slice 1 is done** (2026-10-21; D44): test feasibility probe, validation script, tests written and frozen, slice
review read by the owner. **Next: plan slice 2** (recognition, core and the quick after review; IDs in the
[plan.md](plan.md) slice table): its tasks with IDs and done-when, then the Codex rule 9 review, before any skill text.

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
- 2026-10-20: **T1.9 done** (D44; QR-1–QR-5). The owner reviewed the advance sample on one page: all 18 cases are
  situations they meet, and every PASS behaviour would help; the Chinese prompts (AT-28a–d) and AT-26's chapter 1
  anchor are right. Fixes from the review: 9 SC-2 baselines (AT-04, AT-07, AT-08, AT-09, AT-10, AT-14, AT-19a,
  AT-19b, AT-S1) now use the owner's own wording, which is the plugin text with nothing added (D39); AT-06 keeps one
  question, because its plugin turn is only the slash command; AT-18's `pass-notices-shift` now requires the reply
  to set the standard fixed before the favourite against the one applied after (in both arms, word for word). The
  owner's answers are kept privately in `.local/`.
- 2026-10-20: **T1.10 done: prompts, dialogues and graders frozen**, tag `tests-v1.0` (section 9 rule 2; all AT).
  RC-06 passes; 18/18 dialogues parse; the shared graders (`critical-`, `at12-`, `rc05-`) are identical in every
  case, apart from the per-phase and Chinese length limits; each baseline has the same PASS and FAIL graders as its
  plugin case. From now on a change to a test needs a decision entry.
- 2026-10-20: **judge pinned: `claude-opus-5-5`** (SC-1, SC-2; D39, D47 item 7). A probe showed the judge sees only
  the final reply. A calibration set of 33 fixed replies (101 labelled verdicts) was graded with the frozen graders
  by three judges, under a selection rule fixed beforehand: Haiku gave 2 false critical failures, Sonnet missed a
  critical failure 3 times, Opus made no error. Details, cost and limits in [evaluation.md](evaluation.md);
  `evals-calibration/` and `scripts/judge-calibration.py` re-run it.
- 2026-10-20: owner approved **D48** (protected: success criteria): runs use the latest Opus through the `opus` alias,
  for the model and the judge, instead of a fixed ID (`claude-opus` is not a valid CLI name). The resolved ID is
  recorded per run session; one comparison never mixes versions; a judge change re-runs the calibration.
  REQUIREMENTS section 5 cites it.
- 2026-10-21: **T1.11 done** (SC-2; D39, D46, D48). Plain Claude (`opus` = `claude-opus-5-5`) passes at most 1 of
  3 runs on 8 of the 10 SC-2 tests; it already passes AT-09 (3/3) and AT-06 (2/3). SC-2's "at least 7 of 10" is
  reachable with a margin of one. Much of the margin comes from `critical-reply` (plain Claude hands over
  conclusions). Details in [evaluation.md](evaluation.md); raw results private in `.local/t111/`.
  `evals-baseline/results/` added to `.gitignore`.
- 2026-10-21: **T1.12 review run** (section 9 rule 11; all slice 1 IDs). Start-up checks pass; `opus` resolves to
  `claude-opus-5-5` (CLI 2.1.307). Codex (gpt-6-astra, high; thread `01a161b1-9ae3-78b2-a37f-75d80937f314`) reviewed
  `git diff 96748d6..HEAD`: NEEDS REVISION, 4 High, 4 Medium, 1 Low; each finding checked against the files and
  confirmed. Tooling fixed without a decision: `scripts/sc1-gate.py` (incomplete evidence passed; a manual pass hid
  an auto critical failure; RC-05 reported for cases without its grader; self-test 21/21) and
  `scripts/judge-calibration.py` (whole-reply echo check, complete coverage, pooled re-runs; self-test 14/14). Owner
  approved **D49** (protected: success criteria) for the test fixes: requested views in three baselines, *Beyond
  Feelings* citations as critical, `Grep`/`Glob` journal and card checks, leading questions, AT-06's sources, and a
  safe AT-27 setup. Commit `3bc95ff` names no requirement ID (finding 9): it records handoff and status for T1.6–T1.8.
- 2026-10-21: **re-calibration accepted** (339 verdicts, 0 wrong) and **baseline re-run** under D49
  ([evaluation.md](evaluation.md)): plain Claude passes ≤1 of 3 on exactly 7 of the 10 SC-2 tests (AT-S5 now passes
  3/3 once its requested view is not counted as a conclusion). SC-2 is still reachable, with **no margin**.
- 2026-10-21: owner read the T1.12 review: **slice 1 done** (D44).
- 2026-10-21: committed `6ddfa0a` (scripts) and `d4e3729` (D49 tests and docs), tagged **`tests-v1.1`**, pushed `main`
  and the tag to `origin`. Raw T1.12 results and the review are private in `.local/t112/`.
- 2026-10-22: start-up checks pass: RC-06, 18/18 dialogues parsed, `sc1-gate.py` self-test 21/21,
  `judge-calibration.py` self-test passes, `git diff tests-v1.1 --stat -- evals evals-baseline` empty. `opus`
  resolves to `claude-opus-5-5`, unchanged; the CLI is now **2.1.308** (was 2.1.307 at the last calibration). No
  graded run this session, so nothing re-run; T2.5 re-runs the calibration if the CLI or judge differs at the gate.
- 2026-10-22: **slice 2 planned** in [plan.md](plan.md) (T2.1–T2.10, each with IDs and done-when; section 9 rule 9).
  The Codex rule 9 review brief is drafted privately in `.local/t2-plan/`, for the owner to read before it is sent.
- 2026-10-22: **Codex rule 9 review of the slice 2 plan** (gpt-6-astra, high; fresh thread
  `01a1668c-f769-7e60-8f52-38161738a006`): NEEDS REVISION, 3 High, 4 Medium; each finding checked against the files
  and confirmed (for example, `scripts/sc1-gate.py` drops subcase letters and does not require every frozen grader).
  Plan revised to T2.1–T2.15: gate tooling and the D49 chapter check (empty card set) first, calibration before any
  graded run, sentinel-file privacy check, smaller development groups, a gate manifest. Owner choices: **AT-37 moves
  to slice 5** (its setup needs the journal offer); **Codex is the blind second grader** of a gate sample; **Claude
  drives the manual tests and the owner grades the transcripts**. Review private in `.local/t2-plan/`.
- 2026-10-22: Codex re-check (same thread): the 3 High findings fixed; 3 new Medium (blind sample covers only the six
  paired tests, manual-run permissions and tool results, smoke-check criteria) and 1 Low (FR-1.7 qualifiers), each
  fixed in plan.md. The second grading is split into a blind paired sample and an open audit.
- 2026-10-22: **T2.1 done** (FR-0.1, QR-11, QR-9, RC-02). Real `.claude-plugin/plugin.json` (0.1.0) and a
  frontmatter-only `skills/pause/SKILL.md` (`disable-model-invocation: true`); RC-06 passes; 18/18 dialogues build.
  A sentinel probe showed that a run started from the repository can `Read` `.local/`, `.env` and journal files by
  exact path in the plugin root, so **runs start from an allowlisted staging copy** (`/private/tmp/think-twice-run`),
  where no sentinel is reachable; a smoke run invoked `/think-twice:pause` from it ([evaluation.md](evaluation.md)).
  Two follow-ups added to plan.md: T2.2 fails a run that reads `evals/`, and T2.9 re-runs the probe after a CLI
  change. The CLI moved to **2.1.309** during the session.
- 2026-10-22: **T2.2 done** (SC-1, QR-8, RC-05, D49 item 2). `scripts/sc1-gate.py` now judges a subcase named in
  `--tests` (AT-39a, AT-34c) on its own cases; requires every grader each `case.yaml` defines in every run; runs the
  D49 book check on plugin replies (with no card shipped, naming *Beyond Feelings* or one of its chapters is
  critical); treats a run whose tools touch an eval folder as critical; and gives any test with incomplete evidence
  (a missing case, run, grader, trace or reply) the verdict **incomplete**, which never passes the gate and is never
  counted as a failure, so a baseline cannot look worse than it was (SC-2). Self-test 38/38 (21 earlier checks kept). Checked on
  two real one-run results: real grader names match `case.yaml`, and a real trace parses with no false hit. The gate
  command is in [plan.md](plan.md); gate runs need `--keep-temp`. Consequence: earlier result files without kept
  traces (the T1.11 and D49 baselines) now report incomplete, so T2.9 re-runs the six paired baselines.
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
| T1.9 Owner test review (D44) | Done 2026-10-20 |
| T1.10 Freeze | Done 2026-10-20 (tag `tests-v1.0`) |
| Judge pinning (before T1.11) | Done 2026-10-20 (`claude-opus-5-5`) |
| T1.11 Plain-Claude baseline | Done 2026-10-21 (8 of 10 at ≤1/3) |
| T1.12 Slice review | Done 2026-10-21 (D49 applied; owner read the review) |

The test-level gaps from the Codex review (#7, #10, #12, #13, #18) are all settled; see
[plan.md](plan.md#test-level-gaps-to-settle-in-t16t18-codex-review). [HANDOFF.md](HANDOFF.md) lists the next steps
in order, with the proposed T1.9 sample.

## Next action

T2.3: judge calibration on CLI 2.1.309 before any graded result counts (SC-1, SC-2; D48 rule 2). About $8.

## Waiting on the owner

- Nothing at the moment.
