# Handoff: 2026-10-23 (slice 2 under way: T2.1–T2.6 done)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The slices and tasks are in [plan.md](plan.md) ("Slice 2 tasks").

## Where things stand

- **Slice 2 is planned and half built.** T2.1–T2.15 are in plan.md. Codex reviewed the plan twice (fresh thread
  `01a1668c-f769-7e60-8f52-38161738a006`); every finding was fixed. **T2.1–T2.6 are done; next is T2.7.**
- **The skill exists:** `skills/pause/SKILL.md` (about 2,810 tokens by the fallback estimate; limit 4,400) and
  `skills/pause/standards.md` (about 1,450), plus `.claude-plugin/plugin.json` (0.1.0). Codex reviewed the draft
  against the goal (thread `01a1670a-3660-7ae0-9cc0-0b11fad47237`): 1 High (premises attributed to the owner) and 6
  more, all fixed; the re-check found one new conflict, also fixed.
- **Development runs so far** (not gate results): group A (recognition, opening: AT-01, 02, 04, 05, 39a) and group B
  (material, input: AT-29, 30, 36, 38) all pass ≥2 of 3, with AT-12 and RC-05, and no critical failure.
- **Tests are frozen at `tests-v1.1`.** `git diff tests-v1.1 --stat -- evals evals-baseline` shows nothing.
- **Model and judge:** `opus` = `claude-opus-5-5`; **CLI 2.1.309**. The judge calibration was re-run on 2.1.309
  (T2.3): 354 verdicts, 0 wrong, accepted.
- **AT-37 moved to slice 5** (owner): its frozen setup declines a journal offer that only slice 5 builds. Slice 2's
  gate is now 26 tests: 19 auto (26 cases) and 7 manual.
- **Git:** everything is committed and pushed to `main` (last commit `915ac98`). No new tags this slice.

## What this session did

| # | What | Where |
| --- | --- | --- |
| — | Start-up checks pass; `opus` = `claude-opus-5-5`; the CLI moved 2.1.307 → 2.1.309 during the session | progress.md |
| Plan | Slice 2 tasks T2.1–T2.15; Codex plan review (3 High, 4 Medium) and re-check (3 Medium, 1 Low), all fixed | plan.md; review private in `.local/t2-plan/` |
| T2.1 | Real `plugin.json` and skill frontmatter. A sentinel probe showed a run started from the repository can `Read` `.local/`, `.env` and journal files, so **runs start from an allowlisted staging copy** | evaluation.md |
| T2.2 | `scripts/sc1-gate.py`: subcases in `--tests`, every defined grader required, the D49 book check (no card yet, so naming the book is critical), eval-folder contamination, and an **incomplete** verdict so a baseline cannot look worse than it was. Self-test 38/38. The gate command is in plan.md | `883557c` |
| T2.3 | Judge re-calibration on CLI 2.1.309, accepted | evaluation.md; `.local/t23/` |
| T2.4 | First draft of `SKILL.md` and `standards.md`, then the Codex goal review and fixes | `b50d139`, `12d81ae`; `.local/t24/` |
| T2.5 | Group A runs; "settled" defined; one question per request | evaluation.md; `49ff8c0`; `.local/t25/` |
| T2.6 | Group B runs; nothing said about a Claude-written summary until the owner answers; on the owner's choice, an unclear state gets FR-0.5's own question "Have you formed a view yet?" | evaluation.md; `915ac98`; `.local/t26/` |

Owner decisions this session (recorded in plan.md and progress.md; none needed a decision entry): AT-37 to slice 5;
Codex as the second grader (a blind paired sample plus an open audit, T2.11); Claude drives the manual tests and the
owner grades the transcripts (T2.10); no nlpm in the process for now (its vague-word rule would push the verdict
definitions away from REQUIREMENTS' wording).

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

   If `opus` is no longer `claude-opus-5-5`, D48 applies: re-run the judge calibration before any graded run. If the
   CLI is no longer 2.1.309, re-run the calibration (evals/README.md) before results count, and the T2.1 reach probe
   before the gate (T2.9).
3. **T2.7: development runs C** (verdicts and the review's shape): AT-07, AT-23, AT-24, AT-35 (a–d), 3 runs each,
   then a one-run smoke check of groups A and B. About $8. **Read every AT-07 reply in full**: the judge must not be
   stricter than section 5 on a Sound verdict.
4. **T2.8: development runs D** (lenses and lessons): AT-08, AT-09, AT-10, AT-19, AT-20, AT-25, then a one-run smoke
   check of groups A–C.
5. Then T2.9–T2.15 as plan.md says: the auto gate (re-run the six paired baselines first: the old results kept no
   traces, so they now read "incomplete"), the manual tests, Codex's second grading, the SC-1 and SC-2 results, the
   owner's real use, the slice review, and the re-estimate.

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md and docs/plan.md
("Slice 2 tasks"). Run the start-up checks and record the CLI version and what opus resolves to.
Then start T2.7 (development runs C), and name the requirement IDs each step serves.
```

## How to run things

- **Development runs** (T2.5–T2.8): `.local/devrun.sh OUT_DIR RUNS CASE [CASE]` rebuilds the staging copy at
  `/private/tmp/think-twice-run` with only the named cases, builds their histories, records the CLI, the resolved
  model, the skill hashes and the commit before and after, and runs `claude plugin eval` with `--keep-temp`
  (`opus` as model and judge). Score with `scripts/sc1-gate.py OUT_DIR/result.json --root . --tests "<IDs> AT-12
  RC-05"`. A smoke check is one run; read its per-case results directly, since the gate script reports a one-run
  result as incomplete.
- **Gate runs** (T2.9): the command block in plan.md, below the slice 2 task table.
- **Never run evals from the repository** (T2.1): always from the staging copy.
- **Clearing kept eval folders** (`/private/tmp/e-*`, read-only): make the folder writable first, then the rest
  (`chmod u+w "$d"; chmod -R u+rwx "$d"; rm -rf "$d"`), and not under `set -e`.
- **Codex:** through cc-suite's runner (`node <cc-suite>/scripts/codex-runner.mjs --kind review-plan --model
  gpt-6-astra --effort high --sandbox read-only -- "<brief>"`), read-only; brief the owner before sending.
- **Judge calibration and baseline:** as before (evals/README.md; evaluation.md).

## Open items to keep in view

- **AT-02's disputed runs.** Two of four runs failed `fail-asks-for-phase` on an either/or question about the
  owner's state, the same shape as the case's own PASS example: probably a judge error. The skill now asks FR-0.5's
  open question instead (owner's choice, recorded as prompted by the judge). The disputed runs go to T2.11. The
  calibration set has no AT-02 item; adding one is the owner's call (about $8 to re-run).
- **SC-2 has no margin** (plain Claude passes ≤1 of 3 on exactly 7 of 10). The six paired baselines are re-run in
  T2.9; if a valid new baseline removes a qualifying test, the owner hears about it, and tests are not weakened.
- **FR-2.5** (offer to look further back when a summary can't be confirmed) is deferred to slice 3, with AT-17.
- **`Read` by exact path reaches the eval cases** under the plugin root; the gate now fails any run that touches an
  eval folder.

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen; every change cites a decision entry with the D40 drift check.
- Tests are frozen at `tests-v1.1` and never weakened. A failing test is fixed in the skill; every skill change is
  noted in evaluation.md with the general rule and ID it implements, and uses no wording from a case.
- Every gate attempt is kept; unchanged skill text is never re-run to get a pass.
- Every eval run uses `--no-publish` and starts from the staging copy. Record the CLI and the resolved model before
  and after each run session (D48).
- Real-use logs, manual results, raw eval results and Codex reviews stay private in `.local/`.
- No commit, push, tag or release unless the owner asks. Stage files individually.

## Leftovers on this machine

- `.local/t2-plan/`, `.local/t23/`, `.local/t24/`, `.local/t25/`, `.local/t26/`: briefs, reviews and raw results;
  `.local/devrun.sh` and `.local/t24/overlap.py` (the case-wording scan). Private; gitignored.
- `/private/tmp/think-twice-run`: the staging copy, rebuilt before every run; nothing in it is needed.
- No kept `/private/tmp/e-*` eval folders remain.

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

## Lessons from this session

- **Probe before trusting a run location.** Sentinel files showed that `Read` by exact path reaches the plugin root;
  the denials covered only Glob, Grep, `.git` and results.
- **"Incomplete" is not "fail".** Counting missing evidence as a failure is safe for the plugin and backwards for a
  baseline, where failures make SC-2 look better.
- **Define the words the skill depends on.** "Settled" without a definition made the skill review an ambiguous
  statement; "first asks" without "and says nothing else" let it review a summary before asking.
- **A judge can disagree with its own case.** AT-02's two graders pulled against each other on an either/or
  question. Record such cases for the second grader; do not quietly tune towards them.
- **Shell quirks:** zsh does not split a word list in `for c in $CASES` (use `bash`); the mac-it-guy-pro guard
  blocks any Bash command containing `..`, including `...` in a comment (write such files with the Write tool);
  `set -e` hides a later status line when `claude plugin eval` exits 1, which only means a case scored below its
  threshold; `claude -p` needs `< /dev/null` inside scripts.
