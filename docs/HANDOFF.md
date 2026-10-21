# Handoff: 2026-10-21 (slice 1: review, freeze, judge, baseline)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The tasks are in [plan.md](plan.md).

## Where things stand

- **Slice 1, tasks T1.1–T1.11 are done; T1.12 (the slice review) is next.** Then slice 2's plan and its Codex review,
  before any skill text.
- **Tests are frozen** since 2026-10-20 (T1.10, tag `tests-v1.0`), after your review (T1.9). Any change to a prompt,
  dialogue or grader now needs a decision entry. `git diff tests-v1.0 --stat -- evals evals-baseline` should show
  only `evals/README.md` (run instructions, not tests).
- **Judge chosen by calibration:** Opus made no error on 303 labelled verdicts; Haiku gave false critical failures and
  Sonnet missed real ones ([evaluation.md](evaluation.md)). Re-run with `scripts/judge-calibration.py`.
- **Model and judge are `opus`** (D48): the alias for the latest Opus, today `claude-opus-5-5`. The eval output
  records only the alias, so every run session records the resolved ID before and after.
- **Plain-Claude baseline (T1.11):** plain Claude passes at most 1 of 3 runs on 8 of the 10 SC-2 tests, so "at least
  7 of 10" is reachable with a margin of one. It already passes AT-09 (3/3) and AT-06 (2/3).
- **Built so far:**
  - `evals/`: 50 auto cases; `evals-baseline/`: 14 SC-2 baseline cases (D46); `evals/manual/`: 12 manual scripts;
  - `evals-calibration/items.json`: 33 fixed replies with expected verdicts, for choosing the judge;
  - `scripts/validate-plugin.sh` (RC-06), `scripts/build-histories.py`, `scripts/sc1-gate.py` (SC-1),
    `scripts/judge-calibration.py`.

  Conventions and run commands are in [evals/README.md](../evals/README.md).
- **No product skill text yet**, and no `.claude-plugin/plugin.json` yet. Runs so far used a scratch copy with a
  minimal one.
- **Requirements:** v1.0 plus D44–D48. `git diff requirements-v1.0 -- docs/REQUIREMENTS.md` shows only sentences
  citing them.
- **Git:** everything is committed and pushed to `main` of <https://github.com/ShivLee/think-twice> (public, D3).
  Tags: `requirements-v1.0`, `tests-v1.0`.
- **Fixture repository:** <https://github.com/ShivLee/think-twice-fixtures> holds the AT-31 and AT-41 pages, pinned by
  commit `0787d68`. **Never rewrite its history.**

## What this session did

| # | What | Where |
| --- | --- | --- |
| T1.9 | Your test review: all 18 sample cases are realistic and their PASS would help; the Chinese prompts and AT-26's anchor are right. 9 baselines now use your own wording (the plugin text with nothing added); AT-06 keeps one question. AT-18's check now requires naming the standard set before the favourite and the one applied after. | progress.md; answers private in `.local/t19-owner-review.md` |
| T1.10 | Prompts, dialogues and graders frozen; tag `tests-v1.0`. | evals/README.md |
| — | The judge sees only the final reply (probe). Judge chosen by a calibration set, with a selection rule fixed in advance. | evaluation.md |
| D48 | Runs use `--model opus --judge-model opus` (`claude-opus` is not a valid name). Record the resolved ID; one comparison never mixes versions; a new judge re-runs the calibration first; a model change restarts SC-3 (D45). | decisions.md (protected: success criteria) |
| T1.11 | Plain-Claude baseline on the 14 baseline cases: 8 of 10 at ≤1/3. | evaluation.md; raw results private in `.local/t111/` |
| — | `evals-baseline/results/` is now gitignored. | .gitignore |

The T1.9 review page is a private artifact, which also stores your answers:
<https://claude.ai/artifact/P84bfSY8c5QhF93SCoxBa7>.

## What to do next time, in order

1. **Start-up.** Read [AGENTS.md](../AGENTS.md), this file, [progress.md](progress.md) and [plan.md](plan.md). Run
   `scripts/validate-plugin.sh` and `scripts/build-histories.py --check`; both pass with no skill present. Check that
   `git diff tests-v1.0 --stat -- evals evals-baseline` shows only `evals/README.md`.
2. **Check the model.** Record `claude --version` and what `opus` resolves to:

   ```sh
   claude -p --model opus --output-format json "Reply OK" | python3 -c 'import json,sys; print(*json.load(sys.stdin)["modelUsage"])'
   ```

   If it is no longer `claude-opus-5-5`, D48 applies: re-run the judge calibration before any graded run, and re-run
   the T1.11 baseline before comparing anything with it.
3. **T1.12, the slice review** (section 9; all slice 1 IDs). Codex (through cc-suite) reviews slice 1's changes,
   `git diff 96748d6..HEAD`, against REQUIREMENTS section 1 and the ID list: does every change name the IDs it
   serves, is anything built that no test needs, does anything weaken a failure-mode guard. You read the review. A
   finding that would change a frozen test needs a decision entry.
4. **Close slice 1** (D44): mark it done in progress.md once T1.12's findings are settled, and update README.md's
   status line.
5. **Before slice 2:** write slice 2's tasks into plan.md, with IDs and done-when, and get the Codex rule 9 review.
   Slice 2 is the first time skill text gets written: write it from the frozen tests and keep `SKILL.md` within
   QR-13. Slice 2 also adds the real `.claude-plugin/plugin.json`.
6. **At slice 2's first gate:**
   - read the plugin's AT-07 replies in full. Plain Claude's AT-07 replies failed `critical-reply` while calling the
     reasoning sound, which a verdict on the reasoning may do; check the judge is not stricter than section 5;
   - remember the SC-2 margin is one test, and part of AT-18's margin is brevity;
   - read a sample of graded replies in full: the judge and the product are both Claude, so the calibration cannot
     catch a judge that favours Claude's style.

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md and docs/plan.md.
Run the start-up checks and record what opus resolves to. Then start T1.12, the slice 1 review with Codex.
Name the requirement IDs each step serves.
```

## How to run things

- **Eval runs:** the commands are in [evals/README.md](../evals/README.md). Until slice 2 adds the real
  `plugin.json`, run from a scratch copy (`git archive HEAD | tar -x -C <dir>`) with a minimal
  `.claude-plugin/plugin.json`, then run `scripts/build-histories.py` there. Without a skill, the 5 dialogues with a
  `### pause` turn do not build; the 4 baseline dialogues do.
- **Judge calibration:** `scripts/judge-calibration.py build <dir outside the repo>`, then one `claude plugin eval`
  per candidate judge (the script's help has the command), then `scripts/judge-calibration.py score <json>...`.
  About $8 with the Opus judge.
- **Measured cost:** the 14 baseline cases × 3 runs × 2 arms cost about $25 with Opus as model and judge.

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen. Every change cites a decision entry, and every new decision gets the D40 drift check.
- Tests are frozen at `tests-v1.0` and never weakened to make them pass. Write the skill from the tests.
- Every eval run uses `--no-publish`. Run `scripts/build-histories.py` before each run. Record the CLI version and the
  resolved model before and after each run session (D48).
- Committed histories hold only conversation entries. Raw session files contain your email and credential entries.
- Real-use logs, manual results and raw eval results stay private in `.local/`.
- No commit, push, tag or release unless you ask. Stage files individually.

## Leftovers on this machine

- No `/private/tmp/e-*` eval folders remain (no run used `--keep-temp`).
- This session's scratch folder holds the review page sources, the calibration runs and the T1.11 scratch copy. They
  hold only synthetic test material.

## Codex threads

All on gpt-6-astra, high effort. Resume with `/cc-suite:continue <thread>`. None was used this session.

| Thread | What it reviewed |
| --- | --- |
| `01a14e42-3bc6-7750-bd9b-be610089efce` | Requirements v0.4 → v0.7.1 |
| `01a15259-f481-73d2-8658-a609e2c89b01` | The streamlining proposal; D44 and D45 |
| `01a15293-dbca-75b0-b297-9ea90c69f2e3` | Rule 9 review of plan.md; then (2026-10-19) best practice for AT-31 and AT-41 |

## Lessons from this session

- **The judge sees only the final reply**, not your message or the system prompt. That is why every grader carries
  its own context, and why fixed replies can calibrate it.
- **Neither a stronger nor a weaker judge is automatically safer.** Haiku raised false critical failures; Sonnet
  missed real ones. Fix the selection rule before the results come in.
- **Check the `error` field before reading scores.** A usage limit cut T1.11 short: 31 runs scored 0 on an API error,
  not on behaviour. Re-run them only after checking the model resolves to the same ID.
- **Eval CLI quirks:** only the last `--case` flag applies (use one glob); `costUsd` already includes
  `judgeCostUsd`; the eval's YAML parser rejects a quoted pattern that spans lines, even where Ruby accepts it.
  `claude plugin eval <dir> --case zzz-none` lists case files that fail to load, without running anything.
- **Your natural wording has no added question.** You state the situation and stop; the baselines now do the same.
