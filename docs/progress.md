# Progress

The task record for building think-twice. **Read it at the start of every session and update it at the end.** What
the product does is defined in [REQUIREMENTS.md](REQUIREMENTS.md); the slices and tasks are in [plan.md](plan.md);
this file says where the work stands.

This repository is public (D3; made public on 2026-10-19): no personal reasoning, journal content or real-use
transcripts go here.

## Current outcome

**Slice 2: real use first (D55).** **T2.1–T2.8 are done**, with T2.7a–T2.7c, and the skill is committed as tested
(`ee428f8`). **T2.13 (real use) is now the current task**, and dogfooding starts now. The SC-1 gate is a release
gate only. **T2.7d, T2.8b and T2.9–T2.12 are postponed until the release candidate.** Ten tests stay active (AT-04,
AT-05, AT-07, AT-08, AT-10, AT-19a/b, AT-20, AT-35a/c, manual AT-11 and AT-21), frozen at `tests-v1.3`. Everything else
is in `archive/` (tag `pre-reset`). A test is added or changed only for a breach seen in real use (cited from
`docs/reactions.md`), or with the owner's approval. D52–D54 still govern the release candidate and SC-3. Open from
before: AT-07 (2/3 in its last development run), AT-23 (one split-vote critical failure in the last smoke check) and
the FR-2.2 premise wording.

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
- 2026-10-22: **T2.3 done** (SC-1, SC-2; D48 rule 2). Judge calibration on CLI 2.1.309, `opus` = `claude-opus-5-5`
  before and after: 354 verdicts, 0 wrong, no `critical-reply` error, accepted (3 items re-echoed with Sonnet and
  pooled, as in D49). Cost $7.90; [evaluation.md](evaluation.md).
- 2026-10-22: **T2.4 done** (the slice 2 IDs). First draft of `skills/pause/SKILL.md` (recognition, openings, the
  quick review, revisions, hints, endings) and `skills/pause/standards.md` (lenses, calibration gate, fact status,
  verdicts, repairs, hint steps, pressure, lessons), written from REQUIREMENTS. Sizes by the fallback estimate in
  evals/README.md (4 characters per token; no API key for the counting endpoint): `SKILL.md` about 2,360 tokens
  (limit 4,400), `standards.md` about 1,400. `standards.md` is loaded with `Read` before the first check only. A
  4-word-phrase scan against the 26 cases' prompts, dialogues and fixtures, and the slice 2 manual scripts, finds
  only generic phrases and REQUIREMENTS wording; phrases shared with PASS/FAIL graders all come from REQUIREMENTS.
  No book attribution, no journal path. RC-06 passes; the freeze diff is empty. Not yet run (T2.5).
- 2026-10-22: **Codex review of the draft against the goal** (owner's request; gpt-6-astra, high; fresh thread
  `01a1670a-3660-7ae0-9cc0-0b11fad47237`; judged against REQUIREMENTS, not the tests): NEEDS REVISION, 1 High, 5
  Medium, 1 Low, each checked against the files and REQUIREMENTS. Fixed: unstated premises are labelled as what the
  reasoning appears to need, never as the owner's beliefs (High; QR-1, QR-3); perspectives are checked internally and
  surfaced only when they matter, leaving the weighing to the owner (FR-4, FR-1.1); the during summary holds only
  what the owner said or took on, naming an unclear Claude proposal as Claude's (FR-1.2, FR-1.3); at most two
  requests per reply however phrased (QR-5); lengths by phase, with the Chinese limits (QR-6); a Sound review begins
  closing but the session ends only after the owner answers (FR-1.6, FR-1.7); paths with spaces (FR-0.1). Deferred:
  the FR-2.5 recovery for an unconfirmable summary (slice 3, AT-17). `SKILL.md` now about 2,620 tokens. Review private
  in `.local/t24/`.
- 2026-10-22: Codex re-check (same thread): 6 of 7 fixed, including the High; deferring FR-2.5 does not contradict
  the goal. One new Medium: "paraphrase a quoted question" conflicted with the gate's exact quotation (QR-2). Fixed
  by keeping quotations exact and asking fewer questions instead; Codex's own rewrite (quoted question marks not
  counted) was not taken, because the frozen counting rule (gap #18) counts them.
- 2026-10-22: **T2.5 in progress** (FR-0.1, FR-0.2, FR-0.4, FR-0.5, FR-0.7, FR-1.2, FR-2.2, QR-1). Run 1: 5 of 7
  (AT-02 0/3; AT-12 failed in AT-02 and AT-04). Two general changes to `SKILL.md` (what "settled" means; one
  question per request and a count before sending). Run 2: all 7 pass, AT-02 only 2/3; its failing run looks like a
  false FAIL by the judge (a plain question about the user's state), left as graded and sent to the T2.11 second
  grading; the calibration set has no AT-02 item. `opus` = `claude-opus-5-5` before and after. **T2.5 done.** Details
  in [evaluation.md](evaluation.md); raw results private in `.local/t25/`.
- 2026-10-23: **T2.6 done** (FR-0.1, FR-0.8, FR-1.3, FR-2.1, QR-10). Run B1: AT-36 1/3 (it broke down a Claude-written
  summary before asking whether the conclusion was the owner's); AT-02 failed the smoke check on the stage-label
  grader again. Changes: nothing is said about a Claude-written summary's content until the owner answers (FR-1.3);
  on the **owner's choice**, an unclear state gets FR-0.5's own open question, with no states to choose between
  (prompted by the judge, justified by FR-0.5; disputed runs go to T2.11). Run B2: AT-29, AT-30, AT-36, AT-38 3/3;
  AT-02 3/3; group A smoke check passes. `opus` = `claude-opus-5-5` throughout.
- 2026-10-24: start-up checks pass (RC-06; 18/18 dialogues; `sc1-gate.py` self-test 38/38; `judge-calibration.py`
  self-test; freeze diff empty). `opus` resolves to `claude-opus-5-5`, unchanged; **the CLI is now 2.1.310** (the T2.3
  calibration ran on 2.1.309), so the calibration is re-run before T2.9; development runs went ahead, as on
  2026-10-22.
- 2026-10-24: **T2.7 in progress** (FR-1.1, FR-1.4, FR-2.2–FR-2.4, FR-2.6, FR-2.7, QR-2, QR-6; FR-0.2, FR-0.5).
  Run C1: AT-24 3/3; AT-07, AT-23, AT-35 0/3. General changes to `SKILL.md` over runs C2–C3: "settled" now matches
  FR-0.2 (an argued claim stated as the user's own is settled; a bare note still gets FR-0.5's question); at most
  three problems in the whole reply, ranked and said to be; problems match the verdict; no arguing in Claude's own
  voice; confidence is about the verdict; quoted premises; a word count before sending. Run C4/C4b (C4 hit the
  account's session limit; the errored cases were re-run on the same text): AT-02 3/3, AT-07 2/3, AT-23 3/3, AT-24
  3/3, **AT-35 2/3 with one critical failure** (AT-35c, split vote); AT-12 and RC-05 pass. Every AT-07 reply read:
  re-judging suggests the judge grades the review's required premises and "what would raise confidence" line as
  gated notes, which would be stricter than section 5 (the judge's own reasons are not recorded); sent to T2.11.
  Gate tooling finding: a `critical-` judge call that threw counts as a critical failure, not incomplete (fix before
  T2.9). Cost $24.23 (estimate was about $8). Details in [evaluation.md](evaluation.md); raw results private in
  `.local/t27/`.
- 2026-10-24: T2.7 continued on the owner's choice. One more general change (an objection the user's own words
  partly answer keeps only the part that remains; QR-2, FR-1.4). Run C5: AT-23, AT-24, AT-35 3/3, no critical
  failure; **AT-07 1/3**, both failures on `pass-qr2-gate` split votes, the disputed kind (a required premise and the
  FR-2.3 confidence line graded as notes); not tuned further. One-run smoke check of groups A and B: all 11 pass.
  T2.7 cost $32.27 in total.
- 2026-10-24: **Codex consulted on AT-07** (owner's request; gpt-6-astra, high; thread
  `01a16d25-9f13-70c0-a180-25f1101002f4`): QR-2 gates objections, and the frozen grader's "every note" is ambiguous;
  it grades the three latest replies PASS; it found two skill defects that stand on REQUIREMENTS (FR-2.3 confidence
  rule too broad; QR-3, Claude's own claim in a reply) and one mapping concern (FR-2.2). Recommends a clarified AT-07
  test plus calibration items, keeping T2.11. Details in [evaluation.md](evaluation.md).
- 2026-10-24 (later session): start-up checks pass (RC-06; 18/18 dialogues; `sc1-gate.py` self-test 38/38;
  `judge-calibration.py` self-test; freeze diff empty). CLI **2.1.310**, `opus` = `claude-opus-5-5`, both unchanged.
- 2026-10-24: **T2.7a done** (FR-2.3, QR-3, FR-2.2; then the T2.7 IDs). Three general changes to `SKILL.md` Step 3:
  a confidence condition makes the verdict surer without changing it (FR-2.3); no facts, rankings of risk or claims
  of Claude's own when explaining a verdict (QR-3); premises in the user's terms and precision, with no figure,
  threshold, rate or calculation they did not give (FR-2.2); four long lines rewrapped. Wording scan clean. Run C6:
  AT-07 2/3 (its failing run looks like a fair failure: a premise that misreads the user's words), AT-23 and AT-24
  3/3, AT-35 2/3, no critical failure; AT-12 and RC-05 pass. Smoke check of groups A and B: 11/11. The premise fix
  did not take hold: AT-07 replies still restate a one-off loss against "$30 a month". Cost $8.20. Skill SHA-256
  `a4a26b11…`, uncommitted. Details in [evaluation.md](evaluation.md); raw results private in `.local/t27a/`.
- 2026-10-24: **T2.7b done** (AT-07; QR-2, FR-2.2, FR-2.3; SC-1, SC-2 validity). Owner approved **D50** (protected:
  success criteria): AT-07's `pass-qr2-gate`, identical in both arms, says what a note is (a neutral premise or a
  genuine confidence condition is not one merely by appearing; any suggested weakness, or a premise contradicting
  the user's words, is). Committed `64b1c1b`, tagged **`tests-v1.2`**; the freeze is now checked against it. AT-07, 3
  runs on the T2.7a skill text: 2/3, no critical failure; the failing run's cause is unresolved (re-judging gives PASS
  against three FAIL votes), sent to T2.7d and T2.11. Cost $1.34. Details in [evaluation.md](evaluation.md).
- 2026-10-24: **T2.7c done** (SC-1, SC-2). `scripts/sc1-gate.py`: a grader whose judge call threw is missing evidence
  (the test reads incomplete; a thrown `critical-` grader is not a critical failure), and AT-12 reads incomplete for a
  case with fewer than 3 runs. Self-test 44/44 (six new checks, each failing without the fix); C6 and T2.7b results
  unchanged; C4's session-limit AT-24 now reads incomplete. Details in [evaluation.md](evaluation.md).
- 2026-10-25: **T2.8 done** (FR-4, FR-2.4 lesson, QR-3, QR-5; FR-0.2, QR-2 for the changes), on the owner's choice
  with one open smoke failure. General changes to the skill over runs D1–D5: a first-person plan or decision, or
  material the user calls their own with a decision labelled, is settled (FR-0.2); a factual question that strong
  evidence settles is said plainly to be settled (FR-4, false balance); for one side of a contested question, the
  strongest opposing view and the deciding evidence are stated (FR-4 Perspectives); an unchecked cause, report or
  assumption gets a question, how they could check it, with no list of answers (FR-4 Overlooked, QR-1); one kind of
  repair per problem; a new point after a revision passes the gate whatever its form (QR-2). Run D5 on the final text
  (SHA-256 `39703d89…`): AT-08, AT-09, AT-10, AT-19, AT-20, AT-25 3/3, no critical failure; AT-12, RC-05 pass. A–C
  smoke check: 17/18; **AT-23 one critical failure on a split vote** (re-judging gives PASS; an existing rule covers
  it, so nothing was added); T2.9 decides it. D2 and the first smoke check hit the session limit; their affected cases
  were filled in on the same text. Cost $40.78. Details in [evaluation.md](evaluation.md).
- 2026-10-25: committed and pushed `main` and the `tests-v1.2` tag (owner's request).
- 2026-10-25: **gate tooling fix after a Codex review** (SC-1, SC-2 validity; AT-12, RC-05; owner's request; fresh
  thread `01a1734d-e06b-7e63-9368-62ca5e82e459`). Confirmed and fixed in `scripts/sc1-gate.py`: a test with an
  errored run could pass; a session-limit error now reads incomplete, any other error fails until investigated;
  baselines graded on their `without` arm; AT-12 and RC-05 need every defined grader. Self-test 50/50. plan.md: a
  fill-in supplies only missing run slots. Details in [evaluation.md](evaluation.md).
- 2026-10-25: **drift review** (owner's request; my assessment, then Codex in a fresh thread
  `01a1736c-f570-74d0-a9e9-9e5e50bfaf2a`): no abandonment of the goal; Medium drift in practice towards optimising
  graded replies. Owner approved **D51** (protected: success criteria): `at07-good` relabelled FAIL on
  `pass-qr2-gate`, and a calibration is accepted only with no wrong AT-07 `pass-qr2-gate` verdict.
  `judge-calibration.py` self-test passes with three new checks. Re-scored under D51, the T2.3 calibration would not
  be accepted (Opus passed that note 3/3), so T2.7d may fail its rule. Details in [evaluation.md](evaluation.md).
- 2026-10-25: **speed-up review** (owner's request; Codex fresh thread `01a17392-1a16-76b3-be51-0d153ff493f4`):
  tiered regression and replacing live manual tests rejected; fewer, full gates kept. Owner asked for Claude's
  recommendation and all revisions to follow it: **D52** (combined gates 3+4 and 5+6; release-candidate acceptance
  before SC-3; one plan review for slices 3–7; T2.8b SC-2 feasibility after T2.7d; development loop), **D53**
  (calibration triggers; README run recipe from staging), **D54** (pinned model for the release candidate and SC-3).
  REQUIREMENTS, plan.md and evals/README.md updated; a private real-use log template in `.local/real-use-log.md`.
- 2026-10-25: all D52–D54 changes committed and pushed (`09fd37d`, `4cce1ef`); tag **`tests-v1.3`** created on
  `09fd37d` and pushed (owner's request); the freeze diff against it is empty. HANDOFF.md rewritten for resuming at
  T2.7d.
- 2026-10-25: **test audit** (owner's request; read-only): each test, eval and script classified as CORE (needed to
  tell whether the skill is useful now), LATER or CUT; ten CORE items. The audit also listed the doc instructions
  that made passing the frozen tests the goal.
- 2026-10-25: owner approved **D55** (protected: success criteria): real use (T2.13) ahead of T2.7d–T2.12; SC-1 a
  release gate only; the ten CORE items active; everything else, `evals-calibration/` and three scripts moved
  unchanged to `archive/`, after the local tag `pre-reset` (`3166e25`, not pushed); the calibration and self-tests
  retired; T2.7d, T2.8b and T2.9–T2.12 postponed until release; tests added or changed only for a real-use breach or
  with the owner's approval. Checked: `build-histories.py --check` 1/1; the active tests are unchanged against
  `tests-v1.3`. AGENTS.md, plan.md, HANDOFF.md and this file updated; the skill is untouched. Not yet committed.
- 2026-10-25: D55 follow-up (owner): the reactions.md privacy limit confirmed; features built only on real-use need;
  T2.10–T2.12 with the release candidate. REQUIREMENTS amended to cite D55 (sections 5, 6, 8, 9). Open: what happens
  at the release candidate to a requirement real use has not called for.
- 2026-10-25: `CONTRIBUTING.md` and `evals/README.md` brought in line with D55 (owner's request): the test rule,
  `docs/reactions.md`, active tests, archive paths, the release-only gate and calibration. `evals/README.md` was
  part of `tests-v1.3`; its counting rules are unchanged, and the freeze check now leaves it out
  (`git diff tests-v1.3 --stat -- $(find evals -type f ! -name history.jsonl ! -name README.md)`, empty).
- 2026-10-25: **documentation review against D55** (owner's request): 13 findings fixed, nothing committed.
  `docs/reactions.md` created (format and privacy rule, no entries); HANDOFF.md "Where things stand", "How to run
  things", "Open items" and "Leftovers" rewritten; plan.md (slices as feature groups, later slices planned when real
  use calls for them, working practices, T2.14, T2.15 postponed, the omission-pass note), README status, AGENTS.md
  (reactions.md privacy), REQUIREMENTS (status line D0–D55; the v2 subagent trigger) and evaluation.md (a D55
  section) brought in line.
- 2026-10-25: D55, the archive move and the doc changes committed in three commits and pushed to `origin/main`
  (owner's request); tag `pre-reset` stays local.

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
[plan.md](plan.md#test-level-gaps-to-settle-in-t16t18-codex-review).

## Slice 2 status

| Task | Status |
| --- | --- |
| Plan and Codex rule 9 review | Done 2026-10-22 (two rounds; all findings fixed) |
| T2.1 Plugin skeleton and run location | Done 2026-10-22 (runs start from a staging copy) |
| T2.2 Gate tooling | Done 2026-10-22 (self-test 38/38) |
| T2.3 Judge calibration on CLI 2.1.309 | Done 2026-10-22 (accepted) |
| T2.4 First draft of the skill | Done 2026-10-22 (Codex goal review fixed) |
| T2.5 Development runs A | Done 2026-10-22 |
| T2.6 Development runs B | Done 2026-10-23 |
| T2.7 Development runs C | Done except AT-07 (1/3 on the disputed grader); owner accepted the AT-07 plan |
| T2.7a Skill fixes from the AT-07 consultation | Done 2026-10-24 (C6; premise fix did not take hold) |
| T2.7b D50: clarify AT-07's gate grader | Done 2026-10-24 (D50 approved; `tests-v1.2`; AT-07 2/3) |
| T2.7c Gate tooling fix | Done 2026-10-24 (self-test 44/44) |
| T2.7d Calibration with AT-07 items | Postponed until the release candidate (D55) |
| T2.8b SC-2 feasibility: all 14 baselines | Postponed until the release candidate (D55) |
| T2.8 Development runs D | Development done 2026-10-25 (D5 passes); smoke check not passed: 17/18, AT-23 open |
| T2.13 Real use (dogfooding) | **Current** (D55): started 2026-10-25, ahead of T2.7d–T2.12 |
| T2.9–T2.12 | Postponed until the release candidate (D55) |
| T2.14 Slice review | Not started (after real use) |
| T2.15 Re-estimate | Postponed until the release candidate (D55) |

[HANDOFF.md](HANDOFF.md) lists the next steps in order.

## Next action

**T2.13, real use** (section 9 rule 10; G1–G6; D55): the owner uses the plugin on real situations
(`claude --plugin-dir ~/projects/think-twice`, then `/think-twice:pause …`) and records each requirement breach as a
one-line entry in `docs/reactions.md`. Each breach is handled as [HANDOFF.md](HANDOFF.md) "What to do next time"
step 4 says: a test only if one is needed (citing the entry), then a skill fix, checked on the active tests once.

## Waiting on the owner

- Real use, and the first entries in `docs/reactions.md` (the file does not exist yet).
- Whether to try once more on the FR-2.2 premise wording (T2.7a), or leave it.
- At the release candidate, a requirement real use has not called for: build it for the release, or move it out of
  v1.0 (REQUIREMENTS section 8, "Still open"; D55). Not needed until then.
- Four product rules from the drift review, to revisit at T2.13–T2.14 (evaluation.md, "Drift review and D51").
