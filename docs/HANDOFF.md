# Handoff: 2026-10-21 (slice 1 closed: review, D49, `tests-v1.1`)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The slices and tasks are in [plan.md](plan.md).

## Where things stand

- **Slice 1 is done** (T1.1–T1.12, D44). **Next: plan slice 2**, then its Codex rule 9 review, before any skill text.
- **Tests are frozen at `tests-v1.1`** (D49, 2026-10-21), which replaces `tests-v1.0`. Any change to a prompt,
  dialogue, grader or manual script needs a decision entry. `git diff tests-v1.1 --stat -- evals evals-baseline`
  should show nothing.
- **Model and judge are `opus`** (D48), today `claude-opus-5-5`, CLI 2.1.307. The eval output records only the alias,
  so every run session records the resolved ID before and after.
- **Judge calibration holds** under the D49 graders: 37 fixed replies, 339 verdicts, 0 wrong, no `critical-reply`
  error ([evaluation.md](evaluation.md)). Re-run it if `opus` resolves to a new model or a grader changes.
- **SC-2 holds with no margin.** Plain Claude passes at most 1 of 3 runs on exactly 7 of the 10 SC-2 tests (AT-04,
  AT-08, AT-10, AT-14, AT-18, AT-S1, AT-S2). It passes AT-06, AT-09 and AT-S5 3/3. If any of the seven flips at
  release, SC-2 fails; tests are never weakened to protect it.
- **Built so far:**
  - `evals/`: 50 auto cases; `evals-baseline/`: 14 SC-2 baseline cases (D46); `evals/manual/`: 12 manual scripts;
  - `evals-calibration/items.json`: 37 fixed replies with expected verdicts;
  - `scripts/validate-plugin.sh` (RC-06), `scripts/build-histories.py`, `scripts/sc1-gate.py` (SC-1; self-test
    21/21), `scripts/judge-calibration.py` (self-test 14/14).

  Conventions, counting rules and run commands are in [evals/README.md](../evals/README.md).
- **No product skill text yet**, and no `.claude-plugin/plugin.json` yet.
- **Requirements:** v1.0 plus D44–D48. D49 changed tests only, not REQUIREMENTS. `git diff requirements-v1.0 --
  docs/REQUIREMENTS.md` shows only sentences citing D44–D48.
- **Git:** everything is committed and pushed to `main` of <https://github.com/ShivLee/think-twice> (public, D3).
  Tags: `requirements-v1.0`, `tests-v1.0`, `tests-v1.1`.
- **Fixture repository:** <https://github.com/ShivLee/think-twice-fixtures> holds the AT-31 and AT-41 pages, pinned by
  commit `0787d68`. **Never rewrite its history.**

## What this session did

| # | What | Where |
| --- | --- | --- |
| — | Start-up checks pass; `opus` resolved to `claude-opus-5-5` (CLI 2.1.306 → 2.1.307, no re-run needed) | progress.md |
| T1.12 | Codex reviewed `git diff 96748d6..HEAD`: NEEDS REVISION, 4 High, 4 Medium, 1 Low. Every finding checked against the files and confirmed. You read the review. | review private in `.local/t112/t112-review.md` |
| — | Tooling fixed (findings 1, 7): the SC-1 gate no longer passes incomplete evidence or lets a manual pass hide an auto critical failure; calibration checks the whole echoed reply and full coverage | `6ddfa0a` |
| D49 | Test corrections (findings 2–6, 8): requested views in three baselines; *Beyond Feelings* citations critical; `Grep`/`Glob` journal and card checks; leading questions count as conclusions; AT-06 sources; safe AT-27 setup | decisions.md; `d4e3729` |
| — | Re-calibration accepted; baseline re-run: SC-2 at exactly 7 of 10 | evaluation.md; raw results in `.local/t112/` |
| D44 | Slice 1 closed; tag `tests-v1.1`; pushed | progress.md, README.md |

Finding 9 (commit `3bc95ff` names no ID) is recorded in progress.md; no history rewrite.

## What to do next time, in order

1. **Start-up.** Read [AGENTS.md](../AGENTS.md), this file, [progress.md](progress.md) and [plan.md](plan.md). Then
   run, from the repository:

   ```sh
   scripts/validate-plugin.sh                  # RC-06: pass
   python3 scripts/build-histories.py --check  # 18/18 dialogues parsed
   python3 scripts/sc1-gate.py --self-test     # 21/21
   python3 scripts/judge-calibration.py --self-test
   git diff tests-v1.1 --stat -- evals evals-baseline   # empty
   ```

2. **Check the model.** Record `claude --version` and what `opus` resolves to:

   ```sh
   claude -p --model opus --output-format json "Reply OK" | python3 -c 'import json,sys; print(*json.load(sys.stdin)["modelUsage"])'
   ```

   If it is no longer `claude-opus-5-5`, D48 applies: re-run the judge calibration before any graded run, and re-run
   the baseline before comparing anything with it.
3. **Plan slice 2** (section 9 rule 9). Write its tasks into [plan.md](plan.md), each with IDs and done-when. Slice 2
   is "Recognition, core and the quick after review": its IDs and the 27 tests in its gate are in the plan's slice
   table (row 2), which is the authority. The plan must include:
   - the real `.claude-plugin/plugin.json`, and `SKILL.md` written from the frozen tests, within QR-13;
   - **method cards load with `Read` only** (D49 item 3: a `Grep` on the skill folder fails RC-05);
   - **if slice 2 ships any method card**, first build the chapter check in `scripts/sc1-gate.py` (D49 item 2;
     plan.md, "Later");
   - after slice 2, re-estimate the remaining work and revisit the Manual tests (D47).
4. **Codex rule 9 review of the slice 2 plan** (through cc-suite, read-only; earlier plan reviews used thread
   `01a15293-dbca-75b0-b297-9ea90c69f2e3`). Settle its findings before writing skill text.
5. **At slice 2's first gate:**
   - read the plugin's AT-07 replies in full: check the judge is not stricter than section 5 on a verdict on the
     reasoning;
   - SC-2 has **no margin**; AT-18's share of it is brevity and restraint;
   - read a sample of graded replies in full: the judge and the product are both Claude, so the calibration cannot
     catch a judge that favours Claude's style.

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md and docs/plan.md.
Run the start-up checks and record what opus resolves to. Then plan slice 2 in plan.md
(tasks with IDs and done-when) and prepare the Codex rule 9 review brief for me to see first.
Name the requirement IDs each step serves.
```

## How to run things

- **Eval runs:** the commands are in [evals/README.md](../evals/README.md). Until slice 2 adds the real
  `plugin.json`, run from a scratch copy of the working tree (outside the repository, without `.git` and `.local`)
  with a minimal `.claude-plugin/plugin.json`, then run `scripts/build-histories.py` there. Without a skill, the 5
  dialogues with a `### pause` turn do not build; the 4 baseline dialogues do.
- **Baseline (plain Claude):** copy `evals-baseline/` (with its built histories) into a folder with **no** plugin and
  run `claude plugin eval . --eval-dir evals-baseline --no-publish --trust-plugin --ablation none --runs 3 -j 3 --model
  opus --judge-model opus --json <file>`. Only the counted arm runs: about $10.
- **Judge calibration:** `scripts/judge-calibration.py build <dir outside the repo>`, then `claude plugin eval <dir>
  --ablation none --no-publish --trust-plugin --runs 3 -j 3 --model claude-haiku-5-5 --judge-model opus --json <file>`,
  then `scripts/judge-calibration.py score <file>`. About $8. If the echo model refuses to repeat an item, re-run just
  that case (`--case cal-<id>`, echo with Sonnet) and score both files with `score --pool`.
- **SC-1 gate:** `scripts/sc1-gate.py <result.json> [--root <suite dir>] [--manual <file>] [--tests "AT-01 ..."]`.
- **Codex:** through cc-suite's runner, read-only; brief the owner before sending.

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen. Every change cites a decision entry, and every new decision gets the D40 drift check.
- Tests are frozen at `tests-v1.1` and never weakened to make them pass. Write the skill from the tests.
- Every eval run uses `--no-publish`. Run `scripts/build-histories.py` before each run. Record the CLI version and the
  resolved model before and after each run session (D48).
- Committed histories hold only conversation entries. Raw session files contain your email and credential entries.
- Real-use logs, manual results, raw eval results and Codex reviews stay private in `.local/`.
- No commit, push, tag or release unless you ask. Stage files individually.

## Leftovers on this machine

- `.local/t112/`: the T1.12 brief and review, the calibration results (`opus.json`, `opus-rerun.json`) and the
  baseline results (`baseline.json`). Private; gitignored.
- This session's scratch folder (under `/private/tmp/claude-501/`) holds the same files plus the scratch copies used
  for the runs. It may be cleared by the system; nothing there is needed.
- No `/private/tmp/e-*` eval folders were kept (no run used `--keep-temp`).

## Codex threads

All on gpt-6-astra, high effort. Resume with `/cc-suite:continue <thread>`.

| Thread | What it reviewed |
| --- | --- |
| `01a14e42-3bc6-7750-bd9b-be610089efce` | Requirements v0.4 → v0.7.1 |
| `01a15259-f481-73d2-8658-a609e2c89b01` | The streamlining proposal; D44 and D45 |
| `01a15293-dbca-75b0-b297-9ea90c69f2e3` | Rule 9 review of plan.md; then (2026-10-19) best practice for AT-31 and AT-41 |
| `01a161b1-9ae3-78b2-a37f-75d80937f314` | T1.12: slice 1 review of `git diff 96748d6..HEAD` (2026-10-21) |

## Lessons from this session

- **A grader's context must match its prompt.** The judge sees only the final reply, so a baseline that asks "What do
  you think?" must say so in its grader, or a requested view is scored as substitution. That error had inflated SC-2's
  margin.
- **Carry probe limits into the tests.** P-4 noted that the card check counted `Read` only; the frozen graders missed
  it until the review. When a probe records a limit, check that a grader covers it.
- **A gate script needs tests for missing evidence**, not just for wrong results: one run, a missing case, or a
  manual line overwriting an auto failure all passed before.
- **The echo model can refuse.** Haiku would not repeat a reply containing a false claim. Re-run that item with
  another echo model and pool; the whole-reply check guarantees the judge saw the fixed text.
- **Tag after committing.** A tag marks a commit; tagging before the changes are committed marks the old tests.
- **Shell and Finder quirks:** in zsh, a word starting with `===` is expanded as a command lookup, so quote such
  markers. Finder hides `/private/tmp`; open a file there with `open -t <path>`.
