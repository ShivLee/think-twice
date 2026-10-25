# Implementation plan

The plan that section 9 rule 9 of [REQUIREMENTS.md](REQUIREMENTS.md) requires: every task names the IDs it serves
and the tests or checks that mark it done. **What gets built** is defined in REQUIREMENTS; **where the work stands**
is in [progress.md](progress.md). This file says **what comes next and how we know it is done**.

Slice 2 is planned task by task. **After the slice 2 gate**, the tasks of slices 3–7 are written here together, each
with its IDs and done-when, and Codex reviews them once against REQUIREMENTS (section 9 rule 9; D52); a later material
deviation is reviewed when it happens. That plan review is separate from the review at the end of each gate (section
9 rule 11).

## Slices

Every gate ends with its tests passing, the owner using it once on something real (slice 1: an owner test review,
D44), and a Codex review of the changes against section 1 and the ID list (section 9 rule 11). **Slices 3 and 4
share one gate, and so do slices 5 and 6** (D52): they are built in order, the combined gate runs both slices' tests
and every earlier slice's under the SC-1 rule, and one real use exercises both feature groups. Each slice ships the
method cards and glossary entries its own tests need.

**The gate.** A slice passes when **its own tests and the tests of every earlier slice** pass under the SC-1 rule
(each auto test ≥2 of 3 runs, no critical failure in any run; each manual test passes). Tests of later slices are not
run and are reported as "not implemented", never as failures. A parent ID in the table means only the part named;
the tests column is the gate. AT-12 (questions per turn, length) runs over every auto case in the slice. AT-26 also
runs in any earlier slice that ships a method card.

| # | Slice | Serves | Tests in the gate |
| --- | --- | --- | --- |
| 1 | Test feasibility probe, validation script, tests written and frozen | 5.1 (P-1–P-7), RC-06, all AT (written, not run against a skill) | Slice 1 tasks below (D44) |
| 2 | Recognition, core and the quick after review | FR-0.1, FR-0.2 (recognising all three phases; after), FR-0.4, FR-0.5, FR-0.7, FR-0.8; FR-1.1–FR-1.5; FR-1.6 and FR-1.7 (after, without the journal offer; partly: continuing after a revision and stopping at once, AT-34c/d); FR-1.3 (Claude-written summary); FR-2.1–FR-2.4 (after); FR-2.6, FR-2.7; FR-4; QR-1–QR-5; QR-6 (after); QR-10 | AT-01, 02, 04, 05, 07, 08, 09, 10, 11, 19, 20, 21, 22, 23, 24, 25, 29, 30, 31, 34c, 34d, 35, 36, 38, 39a, 41 (AT-37 moved to slice 5) |
| 3 | Before and during (gate shared with slice 4; D52) | FR-0.2 (during), FR-0.4 (switching after a correction), FR-0.6; FR-1.3 (conversation material); FR-1.6 and FR-1.7 (during checkpoint); FR-2.1–FR-2.4 (before, during); FR-2.5; QR-6 (before, during); QR-12 | AT-03, 06, 13, 14, 15, 16, 17, 18, 32, 33, 34b, 39b, 40 |
| 4 | Situations S1–S6 (combined 3+4 gate) | FR-0.3, FR-3 | AT-S1–S7 |
| 5 | Journal (gate shared with slice 6; D52; journal privacy also gets its own early live check) | FR-5, FR-1.7 (journal offer; no coaching after the session ends, AT-37), QR-9 | AT-27a–g, AT-34a, AT-37 (from slice 2; its setup needs the journal offer) |
| 6 | Omission pass, remaining method cards and glossary (combined 5+6 gate) | Section 7, FR-6, QR-7, QR-8 | AT-26, AT-28, RC-03, RC-04 |
| RC | Release-candidate acceptance, before SC-3 (D52, D54) | SC-1, SC-2, SC-4; QR-13, RC-01–RC-06 | On one pinned model ID (D54), with a full calibration: the full suite, 3 runs; every live manual test; all 14 paired baselines (SC-2); a blind second grading of a sample fixed in advance; the SC-4 install check. Then **SC-3 start** (D45): date, plugin version and the pinned model recorded privately before any use counts |
| 7 | Packaging and release, during and after SC-3 | QR-11, RC-01–RC-05, SC-3, SC-4 | Release checks pass on the packaged plugin; **SC-3 check:** all six D45 rules applied, on the pinned model, and no material change during the period (or the period restarted). `1.0.0` only when SC-3 is met |

Slice 7 runs during the SC-3 period, so its packaging work must not change the skill's behaviour (D45 rule 6). A
change that might is treated as material and restarts the period.

## Working practices (no rule change)

- Every `claude plugin eval` run uses `--no-publish`; results stay in `evals/results/`, which git ignores.
- **Development loop (D52):** while diagnosing, run the affected cases and a few guard cases once each; run 3 times
  only for a candidate that is clean at one run, then the one-run smoke check. Change the skill only for a
  requirement breach read in the reply, never for a split vote alone, and check first whether an existing rule
  already covers it. After three failed rounds on a group, stop changing the skill and diagnose (grader, material or
  requirement). At each gate, run the full gate; the full suite runs for the release candidate.
- **Disputed verdicts (D52):** when the judge splits or disagrees with its own case, the owner may read that reply
  and rule on it, with reasons tied to the criteria. The ruling is diagnosis: it is stored next to the original
  verdict, never replaces it, and cannot turn a failed run into a pass; a grading interpretation that changes applies
  to both arms and to earlier passes, through a decision entry.
- **Records:** progress.md one entry per task; evaluation.md one short entry per run (version, IDs, result, failure
  classification, cost, next step); HANDOFF.md rewritten at session end only. Every gate attempt, manifest,
  unresolved finding and decision stays recorded.
- **Real use now:** the owner may use the plugin at any time as feedback (`claude --plugin-dir ~/projects/think-twice`);
  it does not count towards SC-3 (D45). Notes go in `.local/real-use-log.md`.
- When a slice is done, run the SC-2 paired comparison for the SC-2 cases in its gate.
- Check `SKILL.md` and card sizes against QR-13 at the end of every slice (section 9 rule 11).
- Slice reviews by Codex cover the diff, not the whole repository.
- Real use before the SC-3 start is feedback only (D45). The real-use log stays private in `.local/`.
- Runs use the latest Opus as both model and judge (`opus`, D48), with the resolved ID recorded; the release
  candidate and the SC-3 period use one pinned ID (D54). The judge was chosen by a calibration set (evaluation.md,
  2026-10-20), because one false critical failure fails a test. Re-run the full calibration when the effective
  judging system changes; a CLI version change alone gets the compatibility check in evals/README.md first (D53).
- After slice 2, re-estimate the remaining work from measured times, including the owner's grading time per manual
  test. Manual tests stay live (D52): frozen-dialogue checks may be added as diagnostics only, piloted on AT-03,
  AT-32 and AT-34d, and never replace a live manual test.

## Slice 1 tasks

Each task fits one session. Do them in this order.

| Task | What | Serves | Done when |
| --- | --- | --- | --- |
| T1.1 | Eval privacy (#14): `evals/results/` in `.gitignore`; `--no-publish` on every run | QR-9, RC-02 | Both in place before P-1 runs |
| T1.2 | Probe P-1 with a throwaway skill (exempt from the freeze rule) | FR-0.1, QR-11; prevents auto tests that cannot invoke the skill | Result and, if it fails, its fallback recorded in `docs/evaluation.md` with CLI and model versions |
| T1.3 | Probes P-2–P-7; record time spent per run and per case (#12) | FR-2.1, FR-2.2, QR-12, QR-13, RC-05, SC-1; prevents tests that cannot run as written | Each result and its fallback recorded in `docs/evaluation.md`; P-7's list of conversation-dependent cases written down |
| T1.4 | Set the "How" column of section 5 from the probe results | All AT (How column); prevents an Auto test the eval cannot run | Every test is Auto or Manual from evidence; the change to REQUIREMENTS cites a decision entry |
| T1.5 | Validation script `scripts/validate-plugin.sh` with RC-06 | RC-06; prevents untraced requirements and unknown IDs | Passes on the current docs; fails on each of: a missing ID, an unmapped requirement, a test citing an unknown ID, an undefined subcase |
| T1.6 | Write the tests in 5.2 (recognition, core, phases), and AT-12 as one reusable check | AT-01–AT-25, AT-30–AT-40; FR-0–FR-2, FR-4, QR-1–QR-6, QR-10, QR-12 | Each case declares its IDs (in its `tags`, checked by `scripts/validate-plugin.sh`), dialogue state and graded reply; **every PASS and FAIL condition in its row is checked by its grader or manual script**; the section 5 critical failures are checked in every grader; the gaps below that apply are written in and marked settled |
| T1.7 | Write the tests in 5.3 (situations) | AT-S1–AT-S7; FR-0.3, FR-3 | As T1.6 |
| T1.8 | Write the tests in 5.4 (methods, journal, language, safety) and the SC-1 gate (#13) | AT-26–AT-29, AT-41; FR-5, FR-6, QR-7–QR-10; SC-1 | As T1.6; the SC-1 gate is checked on three examples: 1 of 3 runs passing fails the case, 2 of 3 passes it, and a critical failure in one run fails it even when the other two pass |
| T1.9 | Owner test review (D44): a sample chosen in advance covering the three phases and the four failure modes | D44; QR-1 (substitution), QR-2 (manufactured objections), QR-3 (overstated facts), QR-4 (agreement), QR-5 | Owner has checked each case is realistic and its PASS would help; unrealistic tests are fixed |
| T1.10 | Freeze the prompts and graders | All AT; prevents tests tuned to fit the skill (section 9 rule 2) | Frozen; RC-06 passes; later changes need a decision entry |
| T1.11 | Run the plain-Claude baseline cases (D46) for the 10 SC-2 tests (information, not a gate) | SC-2 (AT-04, 06, 08, 09, 10, 14, 18, S1, S2, S5), D39; prevents finding out late that SC-2 is out of reach | Results recorded; if plain Claude already passes too many, the owner hears about it before slice 2 |
| T1.12 | Slice review: Codex compares the changes with section 1 and the ID list | All slice 1 IDs; prevents drift (section 9 rule 11) | Owner has read the review |

### Test-level gaps to settle in T1.6–T1.8 (Codex review)

Settle these while writing the tests, before freezing them. Numbers refer to the Codex review.

- #7 **Settled in T1.6.** QR-2's four conditions: AT-07's gate grader (and the AT-22 manual check). FR-1.3's
  "examined and accepted" group: AT-06 checks that the user's own price research is not flagged. The before phase
  reading nothing on its own initiative: AT-13 has a fixture the user never mentions, with `pass-fr21-` graders.
  Affected people and other fields (Perspectives): AT-19a's steelman grader names them.
- #12 Settled by the probe and D46: runs record CLI, model and judge model; each SC-2 test (the 10, plus AT-07 and
  AT-19) gets its own baseline case in D39 wording under `evals-baseline/`, written alongside its plugin case
  (T1.6: the 5.2 tests; T1.7: AT-S1, AT-S2, AT-S5).
- #13 **Settled in T1.8.** `scripts/sc1-gate.py` computes "≥2 of 3 runs, no critical failure" from the `--json`
  output, per test (all of a test's cases must pass in the same run), plus AT-12, RC-05 and a manual results file
  (run once, re-run once on failure; a critical failure in any run fails). Its self-test covers the three required
  examples. Before the first gate run (slice 2), pin the judge with a calibration set (evaluation.md, T1.6).
- #18 **Settled in T1.6** (`evals/README.md`, "Counting rules"): questions by question mark; QR-6 in
  whitespace tokens with 10% tolerance; Chinese by CJK characters (implemented in T1.8); QR-13 by the token-counting
  endpoint, with a fallback estimate and 10% tolerance. Card order when more than 3 apply: no test depends on it; it is
  chosen with the cards in slice 6.
- #10 **Settled by P-5:** a general description of what was reviewed is enough; AT-16 and AT-17 do not require turn
  counts.

**Later (no blocker for freezing):**

- #9 Procedure for changing method cards and tests (CONTRIBUTING.md covers situations only).
- #19 What "one pass" means alongside the correction loop.
- #21 Paired self-review cases: the same reasoning attributed to Claude, to me and to a third party.
- **Before the first slice that ships a method card (D49 item 2):** `scripts/sc1-gate.py` checks every chapter a reply
  names for *Beyond Feelings* against the shipped cards; a mismatch is a critical failure. Slice 2 builds it with an
  empty card set (T2.2).
- FR-0.8's redirect rule (follow a redirect only within the same site, otherwise ask) has no test case. Owner decision
  2026-10-19: record it as a known gap; add redirect cases only if real use shows a need. They would need a definition
  of "same site" and a host that serves real HTTP redirects.

## Slice 2 tasks

Slice 2 builds recognition, the core and the quick after review: the IDs and the 26 tests in row 2 of the slice
table. Codex reviewed the first version of this plan (section 9 rule 9; 2026-10-22, thread
`01a1668c-f769-7e60-8f52-38161738a006`): NEEDS REVISION, 3 High and 4 Medium findings, each checked against the
files and fixed here. Codex's re-check (same thread): the 3 High findings fixed; 3 new Medium and 1 Low on the
sample, manual-run and smoke-check procedures, also fixed here. **AT-37 moved to slice 5** (owner, 2026-10-22): its frozen setup declines a journal offer,
which only slice 5 builds, so it runs there as written; FR-1.7's "no coaching after the session ends" is checked
then. Do the tasks in this order, with two exceptions: T2.7d (the calibration) and T2.8b (the SC-2 feasibility check)
run right before T2.9, on the CLI the gate will use; and while D50 (T2.7b) waited for the owner, T2.7c and T2.8 went
ahead.

**Rules for the slice:**

- **Tests stay frozen.** `git diff tests-v1.3 --stat -- evals evals-baseline` is empty at the end of every task
  (`tests-v1.1` until D50, `tests-v1.2` until D53). A failing test is fixed in the skill. If a test itself looks wrong, stop and
  bring a decision entry to the owner.
- **The skill is written from REQUIREMENTS; the tests check it.** `SKILL.md` and `standards.md` contain no names,
  numbers or wording from a case prompt, dialogue or fixture, and no instruction that applies to one case's content.
  Every change made after a failed run is noted in [evaluation.md](evaluation.md) with the general rule it
  implements and its ID. This prevents a skill tuned to the tests (SC-1, SC-2 validity).
- **Development results are not gate results.** The one-run smoke checks in T2.6–T2.8 only catch regressions: a
  smoke failure is fixed like any other failure. SC-1 is claimed only from T2.9–T2.12, and results from different
  skill versions are never combined.
- **Every gate attempt is kept** and recorded, pass or fail. Unchanged skill text is never re-run to get a pass. If
  SC-2's zero margin is lost, the owner hears about it; tests are not weakened.
- **Fill-ins supply only missing evidence** (Codex review, 2026-10-25, thread `01a1734d-e06b-7e63-9368-62ca5e82e459`).
  A run interrupted by the account limit, or a judge call that threw, reads incomplete in `scripts/sc1-gate.py`; any
  other error fails its test until investigated. The affected cases are re-run on the same skill text and manifest.
  Every completed run of the original attempt stays counted, passed, failed or critical; the fill-in supplies only
  the missing run slots, taken from the re-run in run order (fixed before its results are seen). The script does not
  merge result files, so the manifest records the combination: for each fill-in, the original result file, the case
  and run slot, the full error, and the re-run that supplies the slot, plus counts of interrupted runs and thrown
  graders per arm.
- **The core works in every phase, as far as slice 2's tests reach.** Recognition (FR-0) and the core (FR-1) are not
  limited to after: AT-01b needs the during summary and the wait for confirmation; AT-04 and AT-05 need my view
  first and the opt-out in before; AT-11 needs the hint steps in before; AT-34d needs "stop" in before. The before
  and during work of FR-2.3 and FR-2.4 is slice 3.
- **No method cards and no glossary.** No slice 2 test needs one (AT-26 runs in slice 6; the S1 chapter 1 method
  belongs to slice 4). The skill attributes nothing to *Beyond Feelings* (QR-8). The D49 chapter check is built now
  with an empty card set (T2.2), so any chapter a reply names fails as critical.
- **No journal:** no offer, no read, no write (FR-5 is slice 5).
- **Supporting files load with `Read` only** (D49 item 3), and `standards.md` only when a check runs (QR-13).
- **One version per gate.** Each gate attempt has a manifest in `.local/`: the tests tag, CLI version, resolved model
  and judge (D48), the calibration result, the SHA-256 of `SKILL.md` and `standards.md`, the rebuilt histories, the
  plugin path the run actually loaded, and the manual session IDs. The auto gate and the manual tests share one
  manifest. A skill change after either re-runs both.
- **Manual tests are driven by Claude, graded by the owner** (owner, 2026-10-22). Claude types each script's turns
  exactly and hands the owner the full transcripts; the owner ticks the checklists. Each part and each re-run gets a
  fresh session with its own `--session-id`, resumed only within that part. "Allow web fetches when asked" is met by
  pre-allowing `WebFetch` (recorded in the manifest), which never blocks a fetch the script forbids, so it cannot
  manufacture an AT-31 or AT-41 pass. The transcript keeps every tool call **with its result** and every permission
  denial (AT-41 needs to know whether the fetched content still showed the instruction). Preflight files stay outside
  anything the session can read. A setup or permission problem makes the run incomplete, never a pass. Transcripts
  stay private in `.local/`.
- **A second grader: Codex** (owner, 2026-10-22). The judge, the product and the calibration replies are all Claude.
  Before each gate run, with baseline compatibility already settled (T2.9), two samples are fixed. **(a) Blind,
  paired:** the six slice 2 tests that have baseline cases (AT-04, AT-07, AT-08, AT-09, AT-10, AT-19): for each, the
  same number of plugin and baseline replies, every AT-07 reply included, under random opaque IDs and in shuffled
  order, each with only the material and its criteria, the reply text unchanged. **(b) Audit, not blind:** one graded
  reply for each of the other 13 auto tests. Codex grades both in a fresh read-only thread (cc-suite), **before** it
  sees the key or the judge's verdicts. Reply style may still hint at the arm; that limit is recorded. Any
  disagreement with the judge stops acceptance until it is explained; the owner decides. No grader is edited because
  of it.

| Task | What | Serves | Done when |
| --- | --- | --- | --- |
| T2.1 | Plugin skeleton and run location. The real `.claude-plugin/plugin.json` (name `think-twice`, version `0.1.0`, description, keywords; section 8) and `skills/pause/SKILL.md` with its frontmatter only (`disable-model-invocation: true`). Find out, with **made-up sentinel files** in a throwaway copy (never real private material), what a run can reach: the working directory, the plugin loading or copy path, histories (including absolute paths in them), results and logs. Choose the run location from that evidence, preferring a staging copy that holds only the files a run needs | FR-0.1, QR-11, QR-9, RC-02; prevents private material reaching an eval run, and a skill that cannot be invoked | No sentinel is reachable from the chosen location, with the evidence and the copy procedure recorded in [evaluation.md](evaluation.md); `scripts/validate-plugin.sh` passes; all 18 dialogues build, including the 5 with a `### pause` turn; one smoke run invokes `/think-twice:pause` from that location |
| T2.2 | Gate tooling, from the plan review. `scripts/sc1-gate.py`: (1) a subcase named in `--tests` (AT-39a, AT-34c) is judged on its own cases, without its later-slice siblings; (2) every run must carry **every** grader its frozen `case.yaml` defines, not just one per prefix; (3) the D49 chapter check, with an empty card set: any *Beyond Feelings* chapter a graded reply names is a critical failure; (4) a run that reads anything under `evals/` is contaminated and fails (T2.1 found that `Read` by exact path reaches the cases). Write the exact slice 2 gate command, AT-12 and RC-05 included | SC-1, QR-8, RC-05, D49 item 2; prevents a gate that passes incomplete evidence, or an invented chapter | `--self-test` passes, with new checks: a complete AT-39a passes alone; a run missing one case-specific grader fails; a chapter named with no cards is critical; a run that reads `evals/` fails; AT-34c and AT-34d count from manual lines; the 21 existing checks still pass. The gate command is written below this table |
| T2.3 | Judge calibration on the current CLI (2.1.308; it was 2.1.307), before any graded result counts | SC-1, SC-2; D48 rule 2, evals/README.md | It passes its selection rule, recorded in evaluation.md with the CLI and resolved IDs. If it fails, the owner decides before T2.5 |
| T2.4 | First draft of `SKILL.md` and `skills/pause/standards.md`, from REQUIREMENTS: recognition (FR-0), the core (FR-1), the after phase (FR-2), the lenses (FR-4), QR-1–QR-6 and QR-10, scoped by the rules above. `standards.md` holds the lenses, the calibration gate, the hint steps and the verdicts (section 8) | The slice 2 IDs in the slice table | `SKILL.md` ≤ 4,400 tokens, counted as [evals/README.md](../evals/README.md) says; `standards.md` loaded with `Read`, only when a check runs; a search of both files finds no wording from the slice 2 cases; no book attribution and no journal path; RC-06 passes; the freeze diff is empty |
| T2.5 | Development runs A, recognition and opening: AT-01 (a–c), AT-02, AT-04, AT-05, AT-39a | FR-0.1, FR-0.2, FR-0.4, FR-0.5, FR-0.7, FR-1.2, FR-2.2, QR-1 | Each test passes ≥2 of 3 runs with no critical failure, and its cases pass AT-12 and RC-05 (gate tool from T2.2); each change noted as the rules say |
| T2.6 | Development runs B, material and input: AT-29, AT-30, AT-36, AT-38. Then one run of each group A case, for regressions | FR-0.1, FR-0.8, FR-1.3 (Claude-written summary), FR-2.1 (after), QR-10 | As T2.5 for group B; a **one-run smoke check** of every group A case passes, with no critical failure |
| T2.7 | Development runs C, verdicts and the review's shape: AT-07, AT-23, AT-24, AT-35 (a–d). Then one run of each earlier case | FR-1.1, FR-1.4, FR-2.2–FR-2.4 (after), FR-2.6, FR-2.7, QR-2, QR-6 (after) | As T2.5 for group C, plus every AT-07 reply read in full: the judge is not stricter than section 5 on the verdict; the one-run smoke check of groups A and B passes |
| T2.7a | Skill fixes from the Codex consultation on AT-07 (2026-10-24; owner accepted), each resting on REQUIREMENTS alone, not on the judge: (1) the confidence rule in Step 3 is too broad: evidence that confirms a claim the verdict relies on can raise confidence without changing the verdict; only evidence that would change the verdict belongs elsewhere; (2) when explaining a verdict, add no facts, risk rankings or claims of Claude's own; (3) unstated premises are stated in the user's own terms, with no invented quantitative rule (a one-off loss is not a monthly figure). Rewrap the four over-long lines in `SKILL.md`. Then group C, 3 runs each, and a one-run smoke check of groups A and B. About $8 | FR-2.3, QR-3, FR-2.2; then the T2.7 IDs | Each change noted in evaluation.md with its rule and ID; the wording scan finds no new phrase from a case; group C as T2.5, with AT-07 recorded as it falls and not tuned towards the judge; the smoke check passes |
| T2.7b | Draft **D50** for the owner: clarify AT-07's `pass-qr2-gate` with a functional boundary: neutral mapping (the required unstated premises) and genuine confidence conditions (FR-2.3's "what would raise it") are not objections merely because they appear; any allegation of a weakness in the reasoning, wherever it sits, must pass the QR-2 gate. A blanket "required sections are not notes" is not acceptable: it would let a disguised objection through. Protected item: success criteria. After approval: edit the frozen case and its baseline identically, run RC-06, tag `tests-v1.2`, and from then on check the freeze against `tests-v1.2`. Then AT-07, 3 runs | AT-07; QR-2, FR-2.2, FR-2.3; SC-1, SC-2 validity | The owner has approved or declined D50 in decisions.md with the D40 drift check; if approved, both arms carry the same wording, the tag exists, and AT-07's 3 runs are recorded |
| T2.7c | Gate tooling fix in `scripts/sc1-gate.py`: a `critical-` (or any) grader whose judge call threw is missing evidence, so the test reads **incomplete**, not a critical failure; a case with fewer than 3 runs makes AT-12 incomplete, not failing | SC-1, SC-2 (a baseline counted as failing would inflate SC-2) | `--self-test` passes with a check for each, and every earlier check still passes |
| T2.7d | Judge calibration on the CLI the gate will use (2.1.310 on 2026-10-24), run **immediately before T2.9**, with new AT-07 items: neutral premises, genuine confidence conditions, disguised objections and unsupported additions, labelled by the owner **before** the run, not chosen to vindicate the plugin, and at least one item whose note genuinely passes the gate (D51). About $8–10 | SC-1, SC-2; D48 rule 2; D51; evals/README.md | It passes its selection rule, including D51 (no wrong AT-07 `pass-qr2-gate` verdict), recorded in evaluation.md with the CLI and resolved IDs; if it fails, the owner decides before T2.9 |
| T2.8 | Development runs D, lenses and lessons: AT-08, AT-09, AT-10, AT-19, AT-20, AT-25. Then one run of each earlier case | FR-4, FR-2.4 (lesson), QR-3, QR-5 | As T2.5 for group D; the one-run smoke check of groups A–C passes |
| T2.8b | **SC-2 feasibility** (D52): right after T2.7d, run all 14 baseline cases, 3 runs each, from a copy of `evals-baseline/` with no plugin (`--ablation none`, one arm; evals/README.md), on the accepted judge, with `--keep-temp`. About $10.50 | SC-2; D46, D48 | Every baseline case has 3 complete runs; for each of the 10 SC-2 tests, plain Claude's pass count recorded in evaluation.md; if fewer than 7 of the 10 still have plain Claude at ≤1 of 3, the owner hears it before T2.9 and no test is weakened |
| T2.9 | Auto gate: first settle baseline compatibility for the six paired tests (T2.8b's results if the resolved model, CLI and grader set are compatible; otherwise re-run those baselines, D48 rule 1), re-run the T2.1 reach probe if the CLI has changed, then fix the two samples, then run the 26 auto cases of the slice 2 tests, 3 runs each, with the manifest | All slice 2 auto tests, AT-12, RC-05; SC-1 | Every case has 3 runs carrying every frozen grader; manifest complete; time and cost per case recorded |
| T2.10 | Manual tests on the same manifest, driven by Claude: AT-11, AT-21 (a, b), AT-22, AT-31 (a, b), AT-34 (c, d), AT-41, with the AT-31 and AT-41 preflights first. The owner grades the transcripts | QR-5, FR-1.5, QR-4, FR-1.4, QR-2, FR-0.1, FR-0.8, QR-10, FR-1.6, FR-1.7 | Each script run as written and re-run once on failure; the owner's ticks in `.local/manual-tests.md` and the results in `.local/manual-results.txt`; a critical failure in any run recorded as one |
| T2.11 | Second grading by Codex of the two samples fixed in T2.9 | SC-1, SC-2 validity; QR-1, QR-2, QR-3 | Every sampled reply graded; agreement with the judge recorded; each disagreement explained and decided by the owner before T2.12 |
| T2.12 | SC-1 gate and SC-2 comparison: the gate command on T2.9's results and T2.10's file. Paired comparison (D46) for AT-04, AT-08, AT-09 and AT-10, and for AT-07 and AT-19, against the baseline results settled in T2.9 | SC-1, SC-2 (its slice 2 tests), QR-13, RC-05 | The gate passes, AT-12 and RC-05 included; the SC-2 results for the six recorded in evaluation.md (plugin ≥2 of 3 on the four; at least as many runs as plain Claude on AT-07 and AT-19); `SKILL.md` ≤ 4,400 tokens. On any failure, go back to T2.5–T2.8, then re-run T2.9–T2.12 in full |
| T2.13 | The owner uses it once on something real (section 9 rule 10). Feedback only, not SC-3 (D45) | Section 9 rule 10; G1–G6 as far as slice 2 reaches | The owner has used it once; problems logged privately in `.local/`; progress.md records only that it happened |
| T2.14 | Slice review: Codex compares the slice 2 diff with section 1 and the ID list (section 9 rule 11); in the same session, the tasks of slices 3–7 are written here and Codex reviews them once (D52) | All slice 2 IDs; prevents drift | The owner has read the review; every High finding and any critical, privacy or gate failure is fixed before slice 2 closes; a skill change re-runs T2.9–T2.12 |
| T2.15 | Re-estimate the remaining work from the measured times, including the owner's grading time per manual test; pilot frozen-dialogue diagnostic checks for AT-03, AT-32 and AT-34d only if they would save measured time (D52) | D47, D52; prevents planning slices 3–7 on guesses | Estimate written here; the owner's choice recorded, and any change of method made through a decision entry |

**The slice 2 gate command** (written in T2.2). Run it with `bash`: zsh does not split the word list. The staging
copy (T2.1) holds only the 26 slice 2 auto cases, so the eval runs exactly those. `--keep-temp` keeps each run's
trace, which the contamination check needs.

```sh
CASES="at01a-before-bare-question at01b-during-in-progress at01c-after-stated-conclusion at02-ambiguous-state
at04-decision-without-view at05-opt-out at07-sound-conclusion at08-cause-from-sequence at09-colleague-report
at10-consensus at19a-one-sided-policy at19b-settled-fact at20-hidden-assumption at23-many-small-issues
at24-complete-argument at25a-lesson-after-repair at25b-sound-no-lesson at29-embedded-instruction
at30-own-summary-file at35a-overgeneralised-only at35b-circular at35c-two-flaws at35d-overgeneralised-plus
at36-claude-written-summary at38-missing-file at39a-settled-new-session"
B=/private/tmp/think-twice-run; OUT="$PWD/.local/<attempt>"   # <attempt>: a new folder per gate attempt
rm -rf "$B" && mkdir -p "$B/scripts" "$B/evals" "$OUT"
rsync -a .claude-plugin skills "$B/" && cp scripts/build-histories.py "$B/scripts/"
for c in $CASES; do rsync -a --exclude history.jsonl "evals/$c" "$B/evals/"; done
(cd "$B" && python3 scripts/build-histories.py)
(cd "$B" && claude plugin eval . --no-publish --trust-plugin --scaffold --ablation none --runs 3 -j 3 \
  --keep-temp --model opus --judge-model opus --json "$OUT/result.json")
scripts/sc1-gate.py "$OUT/result.json" --root . --manual .local/manual-results.txt --tests \
  "AT-01 AT-02 AT-04 AT-05 AT-07 AT-08 AT-09 AT-10 AT-11 AT-19 AT-20 AT-21 AT-22 AT-23 AT-24 AT-25 AT-29 AT-30
   AT-31 AT-34c AT-34d AT-35 AT-36 AT-38 AT-39a AT-41 AT-12 RC-05"
```

`--root .` judges completeness against the repository's own case folders, so a case missing from the staging copy
still fails its test. After the second grading (T2.11), the kept `/private/tmp/e-*` folders can be removed: they
are read-only: make each folder writable first, then its `sealed/` subfolder (`chmod u+w "$d"; chmod -R u+rwx
"$d"`), then remove it. Do not run this under `set -e`; a permission message there is harmless.

## Slice 6 note: the omission pass (section 7)

Planned with slices 3–7 (T2.14), and it may run in parallel with slices 3–4 (D52): it touches no skill text. It adds
no card beyond those a requirement or test needs (section 7). It is one independent, chapter-by-chapter pass against
the frozen reading map:
"Is any method in this chapter missing from the inventory?" Its inputs are private (the 58-method inventory in
book-experts `.local/eval/value-v3/drafts/` and the book), so access is checked before the slice starts. Its result
stays private; progress.md records only that it was done and on what date, with no book text. Cards that follow from
it need the FR-6.5 review record and pass RC-03.
