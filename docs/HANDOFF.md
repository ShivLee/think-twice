# Handoff: 2026-10-24 (slice 2: T2.1–T2.7 done, except AT-07)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The slices and tasks are in [plan.md](plan.md) ("Slice 2 tasks").

## Where things stand

- **T2.1–T2.7 are done, except AT-07.** Group C (verdicts and the review's shape) passes: AT-23, AT-24 and AT-35
  (a–d) 3/3 with no critical failure; AT-12 and RC-05 pass; the one-run smoke check of groups A and B passes (11/11).
  **AT-07 passed 1 of 3** in the last run, both failures on `pass-qr2-gate` split votes, on what looks like a
  disputed reading of the grader (below). Not tuned further.
- **The owner accepted a four-step plan for AT-07**, now tasks **T2.7a–T2.7d** in plan.md: skill fixes that rest on
  REQUIREMENTS alone, a decision entry D50 to clarify the AT-07 test, a gate tooling fix, and a judge calibration
  with AT-07 items. **Next is T2.7a.**
- **The skill:** `skills/pause/SKILL.md` (about 3,380 tokens by the fallback estimate; limit 4,400) and
  `skills/pause/standards.md` (about 1,450), committed at `9edac17` as tested (SHA-256 `054998dd…`).
- **Tests are frozen at `tests-v1.1`.** `git diff tests-v1.1 --stat -- evals evals-baseline` shows nothing. If the
  owner approves D50, the AT-07 case and its baseline change and the freeze tag becomes `tests-v1.2`.
- **Model and CLI:** `opus` = `claude-opus-5-5`; **CLI 2.1.310** (it was 2.1.309 at the last calibration, T2.3). The
  calibration must be re-run before graded results count: that is T2.7d, right before T2.9.
- **Git:** the T2.7 skill and results are committed and pushed to `main` (`9edac17`, `0b74e81`); the only later
  change is this handoff update with plan.md and progress.md. No new tags this slice.

## The AT-07 question, in short

The judge passes and fails almost identical AT-07 replies. Re-judging the stored replies (diagnosis only; the judge
records votes, not reasons) suggests it grades two **required** parts of the quick review as "notes" that must pass
the calibration gate: the map's unstated premises (which `pass-map` requires) and FR-2.3's "what would raise the
confidence" line. Codex (thread `01a16d25-9f13-70c0-a180-25f1101002f4`) agreed that QR-2 gates **objections**, and
that the frozen grader's "every note" is ambiguous; it graded the three latest replies PASS. It also found three real
skill defects, which T2.7a fixes. Its recommendation, which the owner accepted: clarify the test with a functional
boundary (D50), add calibration items, keep the T2.11 second grading. That Codex thread has seen the outcomes, so
**T2.11 must use a fresh thread.**

## What this session did

| # | What | Where |
| --- | --- | --- |
| — | Start-up checks pass; `opus` = `claude-opus-5-5`; CLI now 2.1.310 | progress.md |
| T2.7 | Runs C1–C5 and a smoke check. General skill changes: an argued claim stated as the user's own is settled (FR-0.2), a bare note still gets FR-0.5's question; at most three problems, ranked, none added to fill the list (FR-1.4); problems match the verdict (FR-2.7); no arguing in Claude's own voice (QR-1, QR-3); confidence about the verdict, one level (FR-2.3); premises tied to quoted steps; a word count before sending (QR-6); an objection the user's own words answer is dropped or narrowed (QR-2). Cost $32.27 (estimate was about $8) | `9edac17`; evaluation.md; `.local/t27/` |
| — | Two gate tooling problems found in `scripts/sc1-gate.py` (not yet fixed): a judge call that threw reads as a critical failure; a one-run case reads as an AT-12 failure. Both should be "incomplete" | evaluation.md; plan.md T2.7c |
| — | Codex consultation on AT-07 (owner's request), checked finding by finding; the AT-07 plan accepted | evaluation.md; `0b74e81`; `.local/t27/at07-codex-*` |
| — | plan.md: tasks T2.7a–T2.7d added; progress.md and this file updated | plan.md; progress.md |

Owner decisions this session: continue T2.7 past the estimate; the AT-07 judge question to T2.11, plus the four-step
plan (T2.7a–T2.7d); the gate tooling fix as its own step before T2.9.

## What to do next time, in order

1. **Start-up.** Read [AGENTS.md](../AGENTS.md), this file, [progress.md](progress.md) and plan.md ("Slice 2
   tasks"). Then run, from the repository:

   ```sh
   scripts/validate-plugin.sh                  # RC-06: pass
   python3 scripts/build-histories.py --check  # 18/18 dialogues parsed
   python3 scripts/sc1-gate.py --self-test     # 38/38
   python3 scripts/judge-calibration.py --self-test
   git diff tests-v1.1 --stat -- evals evals-baseline   # empty
   ```

2. **Check the model and the CLI.** Note `< /dev/null`: without it, `claude -p` waits on stdin and prints nothing.

   ```sh
   claude --version
   claude -p --model opus --output-format json "Reply OK" < /dev/null | python3 -c 'import json,sys; print(*json.load(sys.stdin)["modelUsage"])'
   ```

   If `opus` is no longer `claude-opus-5-5`, D48 applies: re-run the calibration before any graded run. Development
   runs may go ahead on a new CLI; T2.7d calibrates on the CLI the gate will use.
3. **T2.7a: skill fixes** (FR-2.3, QR-3, FR-2.2), each from REQUIREMENTS, using no wording from a case:
   - Step 3's confidence rule is too broad. It now says new evidence "would change the verdict, not raise confidence
     in it"; evidence that confirms a claim the verdict relies on can raise confidence without changing it.
   - When explaining a verdict, add no facts, risk rankings or claims of Claude's own.
   - State unstated premises in the user's own terms, with no invented quantitative rule.
   - Rewrap the four over-long lines in `SKILL.md` (78, 81, 128, 141).

   Then run the wording scan (`.local/t24/overlap.py`, and check any short phrase by hand against the cases), group C
   3 runs each, and the A+B smoke check. About $8. Record AT-07 as it falls; do not tune towards the judge.
4. **T2.7b: draft D50** for the owner (AT-07; QR-2, FR-2.2, FR-2.3; protected item: success criteria). Use the
   functional boundary in plan.md, never a blanket exemption. Follow the form of D47–D49, with the D40 drift check.
   Show it to the owner and wait. If approved: edit the AT-07 case and its baseline identically, RC-06, tag
   `tests-v1.2`, re-run AT-07 3 times.
5. **T2.7c: gate tooling fix** (SC-1, SC-2), while D50 waits: both problems read "incomplete", each with a new
   self-test check.
6. **T2.8: development runs D** (FR-4, FR-2.4 lesson, QR-3, QR-5): AT-08, AT-09, AT-10, AT-19, AT-20, AT-25, then
   the smoke check of groups A–C.
7. **T2.7d, then T2.9–T2.15:** the calibration with AT-07 items (the owner labels them first), then the gate as
   plan.md says (re-run the six paired baselines first; re-run the T2.1 reach probe if the CLI changed).

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md and docs/plan.md
("Slice 2 tasks"). Run the start-up checks and record the CLI version and what opus resolves to.
Then start T2.7a (the skill fixes from the AT-07 consultation), and name the requirement IDs each step serves.
```

## How to run things

- **Development runs:** `.local/devrun.sh OUT_DIR RUNS CASE [CASE]` rebuilds the staging copy at
  `/private/tmp/think-twice-run` with only the named cases, records the CLI, the resolved model, the skill hashes and
  the commit before and after, and runs `claude plugin eval` with `--keep-temp` (`opus` as model and judge). Score
  with `scripts/sc1-gate.py OUT_DIR/result.json --root . --tests "<IDs> AT-12 RC-05"`. A smoke check is one run: read
  its per-case results directly (the gate script reports one-run results as incomplete or, for AT-12, failing).
- **Reading replies and diagnosing a failure** (T2.7): `python3 .local/t27/replies.py RESULT_JSON [CASE]` prints
  each run's final reply, tools and failing graders. `python3 .local/t27/why.py RESULT_JSON CASE RUN GRADER` asks
  `opus` to re-apply one frozen grader to one stored reply and quote its reasons: **diagnosis only, never a grade**,
  and not the judge's own reasons.
- **Group C cases:** `at07-sound-conclusion at23-many-small-issues at24-complete-argument
  at35a-overgeneralised-only at35b-circular at35c-two-flaws at35d-overgeneralised-plus`. **Smoke A+B:**
  `at01a-before-bare-question at01b-during-in-progress at01c-after-stated-conclusion at02-ambiguous-state
  at04-decision-without-view at05-opt-out at39a-settled-new-session at29-embedded-instruction at30-own-summary-file
  at36-claude-written-summary at38-missing-file`.
- **Gate runs** (T2.9): the command block in plan.md, below the slice 2 task table.
- **Never run evals from the repository** (T2.1): always from the staging copy.
- **Account session limits:** a run can hit the limit partway; the affected runs show "You've hit your session
  limit" as an error or a grader that threw. Re-run only those cases on the same skill text (check the SHA-256), as a
  fill-in for missing evidence, and say so; never re-run failures.
- **Clearing kept eval folders** (`/private/tmp/e-*`, read-only): make the folder writable first, then the rest
  (`chmod u+w "$d"; chmod -R u+rwx "$d"; rm -rf "$d"`), and not under `set -e`.
- **Codex:** through cc-suite's runner, read-only, from the repository: `node
  ~/.claude/plugins/cache/xiaolai/cc-suite/2.3.5/scripts/codex-runner.mjs --kind review-plan --model gpt-6-astra
  --effort high --sandbox read-only --timeout-ms 1500000 -- "$(cat BRIEF.md)" > RESULT.json`. Keep the brief and the
  result in `.local/`; the answer is in `rawOutput`. Brief the owner before sending.

## Open items to keep in view

- **AT-07**: T2.7a–T2.7d, then T2.11 in a fresh Codex thread. SC-2 for AT-07 is non-regression against plain Claude,
  graded by the same graders; D50 would apply to both arms.
- **AT-02's disputed runs** (T2.5–T2.6) still go to T2.11. The calibration set has no AT-02 item.
- **SC-2 has no margin** (plain Claude passes ≤1 of 3 on exactly 7 of 10). The six paired baselines are re-run in
  T2.9; if a valid new baseline removes a qualifying test, the owner hears about it, and tests are not weakened.
- **Cost:** T2.7 cost about four times its estimate, because each failing round needed a full group re-run. Expect
  T2.8 to cost more than its first estimate; say so before going far past it.
- **FR-2.5** (offer to look further back when a summary can't be confirmed) is deferred to slice 3, with AT-17.
- **`Read` by exact path reaches the eval cases** under the plugin root; the gate fails any run that touches an eval
  folder.

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen; every change cites a decision entry with the D40 drift check.
- Tests are frozen and never weakened. A failing test is fixed in the skill; every skill change is noted in
  evaluation.md with the general rule and ID it implements, and uses no wording from a case. When a judge disagrees
  with its own case, record it for the second grader; do not tune towards it.
- Every gate attempt is kept; unchanged skill text is never re-run to get a pass.
- Every eval run uses `--no-publish` and starts from the staging copy. Record the CLI and the resolved model before
  and after each run session (D48).
- Real-use logs, manual results, raw eval results and Codex reviews stay private in `.local/`.
- No commit, push, tag or release unless the owner asks. Stage files individually.

## Leftovers on this machine

- `.local/t27/`: raw results of runs C1–C5 and the smoke check (`c1`…`c5`, `c4b`, `smokeAB`), `replies.py`,
  `why.py`, and the Codex brief and answer (`at07-codex-*`). Earlier folders (`t2-plan`, `t23`–`t26`) as before.
  Private; gitignored.
- `/private/tmp/e-*`: **140 kept eval folders** (about 26 MB) from T2.7. Keep them until T2.11: they hold the traces
  of the disputed AT-07 runs.
- `/private/tmp/think-twice-run`: the staging copy, rebuilt before every run; nothing in it is needed.

## Codex threads

All on gpt-6-astra, high effort. Resume with `--resume <thread>` on the runner.

| Thread | What it reviewed |
| --- | --- |
| `01a14e42-3bc6-7750-bd9b-be610089efce` | Requirements v0.4 → v0.7.1 |
| `01a15259-f481-73d2-8658-a609e2c89b01` | The streamlining proposal; D44 and D45 |
| `01a15293-dbca-75b0-b297-9ea90c69f2e3` | Rule 9 review of plan.md (slice 1); best practice for AT-31 and AT-41 |
| `01a161b1-9ae3-78b2-a37f-75d80937f314` | T1.12: slice 1 review |
| `01a1668c-f769-7e60-8f52-38161738a006` | Rule 9 review of the slice 2 plan, and its re-check |
| `01a1670a-3660-7ae0-9cc0-0b11fad47237` | The first skill draft against the goal, and its re-check |
| `01a16d25-9f13-70c0-a180-25f1101002f4` | AT-07: is `pass-qr2-gate` stricter than section 5? (has seen outcomes: not for T2.11) |

## Lessons from this session

- **A fix for one test can break another.** Widening "settled" for AT-35 pulled AT-02's bare note into review. Run the
  case that guards the other side of a rule (here AT-02) with every change to that rule.
- **The judge records votes, not reasons.** Re-judging a stored reply with its frozen criteria shows a likely reason
  quickly and cheaply, but it is a reconstruction: write "suggests", not "is". Codex caught an overstatement of this
  kind in evaluation.md.
- **A rule written for one verdict can be wrong for another.** The confidence rule written for an Unsupported verdict
  was too broad for a Sound one. State a rule at the level REQUIREMENTS states it.
- **The 4-word wording scan misses short phrases.** "most important first" (3 words, from a grader) got past it; check
  new phrases by hand with `grep` against the cases.
- **Shell quirks:** `claude -p --tools ""` treats the next argument as a tool list and swallows the prompt, so send
  the prompt on stdin; there is no PyYAML, so read `case.yaml` blocks with a small parser (as `why.py` does).
