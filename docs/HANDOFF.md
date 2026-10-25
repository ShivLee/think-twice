# Handoff: 2026-10-25 (slice 2: T2.1–T2.8 done; next T2.7d, then the gate)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The slices and tasks are in [plan.md](plan.md) ("Slice 2 tasks").

## Where things stand

- **T2.1–T2.8 are done**, with three things carried to the gate: AT-07's last runs (2/3 on `tests-v1.2`, the
  failing run's cause unresolved), AT-23's split-vote critical failure in the last A–C smoke check (owner's choice:
  T2.9 decides it), and the FR-2.2 premise wording that did not take hold in T2.7a (owner may try again).
- **The skill:** `skills/pause/SKILL.md` (about 3,750 tokens by the fallback estimate; limit 4,400) and
  `standards.md` (about 1,530), SHA-256 `39703d89…` and `8093b6c2…`, as tested in D5 and the last smoke check.
- **Tests are frozen at `tests-v1.2`** (D50, owner approved 2026-10-24: what counts as a note in AT-07's gate
  grader, identical in both arms). `git diff tests-v1.2 --stat -- evals evals-baseline` shows nothing.
- **Gate tooling:** `scripts/sc1-gate.py` self-test 50/50. A judge call that threw, or a run cut off by the session
  limit, reads incomplete; any other error fails its test until investigated; baselines are graded on their
  `without` arm (Codex review, 2026-10-25).
- **Model and CLI:** `opus` = `claude-opus-5-5`; **CLI 2.1.310**. The calibration last ran on 2.1.309, so T2.7d
  re-runs it before any graded result counts.
- **Git:** `main` and the `tests-v1.2` tag pushed up to `63837b4`; the gate tooling fix after that is local.

## What this session did

| # | What | Where |
| --- | --- | --- |
| — | Start-up checks pass; CLI 2.1.310, `opus` = `claude-opus-5-5` throughout | progress.md |
| T2.7a | Confidence condition makes the verdict surer without changing it (FR-2.3); no claims of Claude's own (QR-3); premises in the user's terms (FR-2.2; did not take hold). C6: group C passes; smoke A+B 11/11. $8.20 | `8fd472e`; evaluation.md |
| T2.7b | D50 drafted, approved, applied to both AT-07 arms; tag `tests-v1.2`. AT-07 2/3. $1.34 | `64b1c1b`; decisions.md |
| T2.7c | Thrown judge calls and one-run AT-12 evidence read incomplete; self-test 44/44 | `2280fc0` |
| T2.8 | Group D: settled plans and own material (FR-0.2), settled questions, the strongest opposing view, check questions (FR-4), one repair per problem, every new point gated (QR-2). D5: all 3/3; smoke A–C 17/18 (AT-23 open). $40.78 | evaluation.md; `.local/t28/` |

Owner decisions this session: leave the premise wording for now (open); approve D50 as drafted; commit T2.7a,
T2.7c and T2.8; in T2.8, fix and re-run rather than stop, then close with AT-23 left to T2.9.

## What to do next time, in order

1. **Start-up.** Read [AGENTS.md](../AGENTS.md), this file, [progress.md](progress.md) and plan.md ("Slice 2
   tasks"). Then run, from the repository:

   ```sh
   scripts/validate-plugin.sh                  # RC-06: pass
   python3 scripts/build-histories.py --check  # 18/18 dialogues parsed
   python3 scripts/sc1-gate.py --self-test     # 50/50
   python3 scripts/judge-calibration.py --self-test
   git diff tests-v1.2 --stat -- evals evals-baseline   # empty
   ```

2. **Check the model and the CLI** (`< /dev/null`, or `claude -p` waits on stdin):

   ```sh
   claude --version
   claude -p --model opus --output-format json "Reply OK" < /dev/null | python3 -c 'import json,sys; print(*json.load(sys.stdin)["modelUsage"])'
   ```

3. **Ask the owner** about the open items in progress.md ("Waiting on the owner").
4. **T2.7d: calibration with AT-07 items** (SC-1, SC-2; D48 rule 2), on the CLI the gate will use. Draft the new
   items (neutral premises, genuine confidence conditions, disguised objections, unsupported additions; the
   "production-sized data" kind of line is a good candidate), have the **owner label them before the run**, then
   run `scripts/judge-calibration.py`. About $8–10. If it fails its rule, the owner decides before T2.9.
5. **T2.9–T2.15** as plan.md says: settle baseline compatibility and re-run the six paired baselines, the reach
   probe if the CLI changed, fix the two Codex samples, then the 26 auto cases ×3 with the manifest; manual tests
   (T2.10); Codex second grading in a **fresh** thread (T2.11).

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md and docs/plan.md
("Slice 2 tasks"). Run the start-up checks and record the CLI version and what opus resolves to.
Then ask me the open questions, and start T2.7d (draft the AT-07 calibration items for me to label).
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
  limit" as an error or a grader that threw, and the gate reads them incomplete. Re-run only those cases on the same
  skill text (check the SHA-256), as a fill-in for missing evidence, and say so; never re-run failures. In a gate
  attempt, the fill-in supplies only the missing run slots: completed runs of the original stay counted (plan.md,
  "Fill-ins supply only missing evidence").
- **Clearing kept eval folders** (`/private/tmp/e-*`, read-only): make the folder writable first, then the rest
  (`chmod u+w "$d"; chmod -R u+rwx "$d"; rm -rf "$d"`), and not under `set -e`.
- **Codex:** through cc-suite's runner, read-only, from the repository: `node
  ~/.claude/plugins/cache/xiaolai/cc-suite/2.3.5/scripts/codex-runner.mjs --kind review-plan --model gpt-6-astra
  --effort high --sandbox read-only --timeout-ms 1500000 -- "$(cat BRIEF.md)" > RESULT.json`. Keep the brief and the
  result in `.local/`; the answer is in `rawOutput`. Brief the owner before sending.

## Open items to keep in view

- **AT-07**: T2.7d (calibration items), then T2.11 in a fresh Codex thread. SC-2 for AT-07 is non-regression
  against plain Claude, graded by the same graders; D50 applies to both arms, so the AT-07 baseline is re-run in T2.9.
- **AT-23**: one split-vote critical failure in the last smoke check (re-judging gives PASS); T2.9 decides it.
- **AT-02's disputed runs** (T2.5–T2.6) still go to T2.11. The calibration set has no AT-02 item.
- **SC-2 has no margin** (plain Claude passes ≤1 of 3 on exactly 7 of 10). The six paired baselines are re-run in
  T2.9; if a valid new baseline removes a qualifying test, the owner hears about it, and tests are not weakened.
- **Cost:** T2.7 cost $32 and T2.8 $41, because each failing round needed a full group re-run. The gate (T2.9) runs
  26 cases ×3 plus six baselines; estimate it from the measured cost per case (about $0.25 a case-run) and tell the
  owner before starting.
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

- `.local/t27a/` (C6, smoke A+B), `.local/t27b/` (D50 draft, AT-07 on `tests-v1.2`), `.local/t28/` (D1–D5, D2b,
  two A–C smoke checks); earlier folders (`t2-plan`, `t23`–`t27`) as before. `.local/t27/replies.py` and `why.py`
  still serve every result file. Private; gitignored.
- `/private/tmp/e-*`: **358 kept eval folders** (about 61 MB). Keep them until T2.11: they hold the traces of the
  disputed AT-07 runs.
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
| `01a1734d-e06b-7e63-9368-62ca5e82e459` | How the gate counts errored runs; fill-ins (2026-10-25) |

## Lessons from this session

- **Each new review rule can create the next failure.** In T2.8, rules for one lens leaked into others: the
  one-sided rule was applied to a causal claim (AT-08), an ungated "ask how it could be checked" added a new point
  after an accepted revision (AT-25a, critical), and several repairs piled into one problem (AT-23, too long). Scope
  each rule to when it applies, put every new point through the gate, and run the cases that guard the other side.
- **A smoke check after a group run is worth its cost.** It caught two regressions that group D could not show.
- **Session limits hit long chains.** D2 and a smoke check were cut short; T2.7c's fix reported thrown judge calls
  as incomplete, as intended, but errored runs still read as failed. Fill in only the affected cases, on the same
  text, and say so.
- **Start background runs with the tool's background mode, never a shell `&`**: an untracked run cannot be waited
  for, and it had to be stopped.
- **Re-judging is a reconstruction.** Twice this session it disagreed with the judge's votes (AT-07 run 3, AT-23
  smoke); record the cause as unresolved rather than tuning towards either.
