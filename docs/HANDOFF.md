# Handoff: 2026-10-25 (slice 2: T2.1–T2.8 done; next T2.7d, T2.8b, then the T2.9 gate)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The slices and tasks are in [plan.md](plan.md) ("Slice 2 tasks").

## Where things stand

- **T2.1–T2.8 and T2.7a–T2.7c are done.** Left before the gate: **T2.7d** (judge calibration with AT-07 items) and
  **T2.8b** (all 14 baselines, to confirm SC-2 is still reachable; D52). Then **T2.9–T2.15** close slice 2.
- **The path to 1.0.0 (D52–D54, 2026-10-25):** slices 3+4 and 5+6 each share one gate (full ×3 at every gate); the
  **release candidate** passes the full suite, the live manual tests, all 14 baselines, a blind second grading and
  the install check **before** SC-3 starts; development stays on `opus`, but the release candidate and the SC-3
  period use **one pinned model ID**; calibration re-runs on an effective judging change, with a cheap check for a
  CLI update. Rejected as lowering evidence: tiered regression, and replacing live manual tests.
- **Carried to the gate, not fixed:** AT-07's last 3 runs passed 2/3 (the failing run's cause is unresolved); AT-23
  had one split-vote critical failure in the last A–C smoke check (owner: let T2.9 decide); the FR-2.2 premise wording
  from T2.7a did not take hold (open).
- **The skill:** `skills/pause/SKILL.md` (about 3,750 tokens by the fallback estimate; QR-13 about 4,000, tolerance
  4,400) and `standards.md` (about 1,530), SHA-256 `39703d89…` and `8093b6c2…`, committed at `ee428f8` as tested.
- **Tests are frozen at `tests-v1.3`** (D53: `evals/README.md` run recipe and calibration trigger; before that D50,
  `tests-v1.2`). `git diff tests-v1.3 --stat -- evals evals-baseline` shows nothing.
- **Calibration (D51):** `at07-good` relabelled FAIL on `pass-qr2-gate`; a judge is accepted only with **no wrong
  AT-07 `pass-qr2-gate` verdict**. The old T2.3 calibration, re-scored under D51, would fail, so T2.7d may fail too.
- **Gate tooling:** `scripts/sc1-gate.py` self-test 50/50; `scripts/judge-calibration.py` self-test passes (17).
- **Model and CLI:** `opus` = `claude-opus-5-5`; **CLI 2.1.310**. T2.7d must run before any graded result counts.
- **Git:** everything committed and pushed; `main` = `origin/main` at `4cce1ef` or later; tags up to `tests-v1.3`
  pushed.

## What this session did (2026-10-24 to 2026-10-25)

| # | What | Where |
| --- | --- | --- |
| — | Start-up checks pass; CLI 2.1.310, `opus` = `claude-opus-5-5` throughout | progress.md |
| T2.7a | Confidence condition makes the verdict surer without changing it (FR-2.3); no claims of Claude's own (QR-3); premises in the user's terms (FR-2.2; did not take hold). Group C passes; smoke A+B 11/11. $8.20 | `8fd472e` |
| T2.7b | D50 drafted, approved, applied to both AT-07 arms; tag `tests-v1.2`. AT-07 2/3. $1.34 | `64b1c1b` |
| T2.7c | Thrown judge calls and one-run AT-12 evidence read incomplete | `2280fc0` |
| T2.8 | Group D: settled plans and own material (FR-0.2), settled questions, the strongest opposing view, check questions (FR-4), one repair per problem, every new point gated (QR-2). D5: all 3/3; smoke A–C 17/18 (AT-23 open). $40.78 | `ee428f8` |
| — | Codex review of errored runs (`01a1734d…`): six findings fixed in the gate script; fill-in rule in plan.md | `2c8be00`, `d887a26` |
| — | Drift review, mine then Codex's (`01a1736c…`): no abandonment of the goal; Medium drift towards optimising graded replies. **D51** (calibration label and rule) | `65bedba`, `7e300c3` |
| — | Speed-up review (`01a17392…`): **D52** (combined gates, release candidate before SC-3, one plan review, T2.8b, development loop), **D53** (calibration triggers, README run recipe), **D54** (pinned model for release and SC-3). Tag `tests-v1.3` | `09fd37d`, `4cce1ef` |

Owner decisions: leave the premise wording for now (open); approve D50 as drafted; close T2.8 with AT-23 left to
T2.9; apply Codex's narrowed option for errored runs; D51 with `at07-good` relabelled FAIL and zero wrong verdicts
allowed; D52–D54 as Claude recommended (owner: "make all the revisions according to your recommendation").

## What to do next time, in order

1. **Start-up.** Read [AGENTS.md](../AGENTS.md), this file, [progress.md](progress.md) and plan.md ("Slice 2
   tasks"). Then run, from the repository:

   ```sh
   scripts/validate-plugin.sh                  # RC-06: pass
   python3 scripts/build-histories.py --check  # 18/18 dialogues parsed
   python3 scripts/sc1-gate.py --self-test     # 50/50
   python3 scripts/judge-calibration.py --self-test
   git diff tests-v1.3 --stat -- evals evals-baseline   # empty
   git status -sb                              # clean, main...origin/main
   ```

2. **Check the model and the CLI** (`< /dev/null`, or `claude -p` waits on stdin). Record both in progress.md.

   ```sh
   claude --version
   claude -p --model opus --output-format json "Reply OK" < /dev/null | python3 -c 'import json,sys; print(*json.load(sys.stdin)["modelUsage"])'
   ```

   If `opus` is no longer `claude-opus-5-5`, D48 applies: every comparison re-runs on the new model. If only the
   CLI changed, T2.7d still runs in full (D50 and D51 changed a grader, a label and the rule), and T2.9 re-runs the
   T2.1 reach probe.
3. **Ask the owner** the open items (progress.md, "Waiting on the owner"): the FR-2.2 premise wording (recommendation:
   leave it; a fix would need wording close to AT-07's own content); whether they have used the plugin for real yet
   (feedback in `.local/real-use-log.md`).
4. **T2.7d: calibration with AT-07 items** (SC-1, SC-2; D48 rule 2, D51, D53). Steps:
   1. **Draft new items** in `evals-calibration/items.json` (same format as `at07-good`: `id`, `case`
      `at07-sound-conclusion`, `why`, `expect`, `reply`). Write fixed replies of four kinds: a neutral unstated
      premise; a genuine confidence condition; a disguised objection placed in a premise or a confidence line (the
      "used production-sized data" line from T2.7b is a good model); an unsupported addition of Claude's own (a risk
      ranking). Several of each, some that should pass and some that should fail, and **at least one whose note
      genuinely passes the gate** (`at07-good` is now a FAIL example). **Leave `expect` empty**; do not pick items
      to vindicate the plugin. The file is public: no private material.
   2. **The owner labels every new item** (`pass` or `fail`, at least `pass-qr2-gate` and `critical-reply`)
      **before any run**. Record that the labels came first.
   3. **Build and run**, from the repository. `SCRATCH` is any folder outside the repository (the session's
      scratchpad); each built case already carries `runs: 3`.

      ```sh
      mkdir -p .local/t27d
      python3 scripts/judge-calibration.py build "$SCRATCH/t27d-cal"
      claude plugin eval "$SCRATCH/t27d-cal" --ablation none --no-publish --trust-plugin \
        --model claude-haiku-5-5 --judge-model opus --json .local/t27d/opus.json
      python3 scripts/judge-calibration.py score .local/t27d/opus.json
      ```

      Haiku only echoes the fixed replies; `opus` is the judge being calibrated. Items Haiku fails to echo are
      re-run with `--model claude-sonnet-5-5` and pooled (`score --pool`), as in T2.3. Record the CLI and the
      resolved model before and after (D48). Cost about $8–10.
   4. **Accept** only under the selection rule: no `critical-reply` error, every item judged in at least 3 echoed
      runs, and **no wrong `pass-qr2-gate` verdict on any AT-07 item** (D51). If it fails, **the owner decides
      before T2.9**, and AT-07's graded results wait for T2.11. Record the result in evaluation.md and progress.md.
5. **T2.8b: SC-2 feasibility** (D52). Right after T2.7d is accepted: all 14 baseline cases ×3, one arm, from a copy
   of `evals-baseline/` in a folder with no plugin (`--ablation none --trust-plugin --keep-temp`, as
   evals/README.md says). About $10.50. Record plain Claude's pass count for each of the 10 SC-2 tests; if fewer than
   7 still have plain Claude at ≤1 of 3, tell the owner before T2.9 and weaken nothing.
6. **T2.9: the auto gate.** Tell the owner the estimate first: about $20 (26 cases ×3 at about $0.25 a case-run).
   In order: reuse T2.8b's baselines for the six paired tests if compatible (D48 rule 1); the T2.1 reach probe if
   the CLI changed; fix the two Codex samples (plan.md, "A second grader"); then the gate command block in plan.md,
   with the manifest in `.local/<attempt>/`. Fill-ins after a session limit follow plan.md, "Fill-ins supply only
   missing evidence".
7. **T2.10–T2.15** as plan.md says: manual tests driven by Claude and graded by the owner (time each one: T2.15
   needs it); Codex second grading in a **fresh** thread (T2.11); the SC-1 gate and SC-2 comparison (T2.12); one
   real use (T2.13); T2.14's slice review **plus the one plan review for slices 3–7** (D52); the re-estimate (T2.15).

**How to work from now on (D52):** in development, run affected and guard cases once while diagnosing and 3 times
only for a clean candidate; change the skill only for a requirement breach read in the reply, and first check
whether an existing rule covers it; after three failed rounds, stop and diagnose. A disputed verdict can go to the
owner, whose ruling is diagnosis stored next to the original verdict, never a score. The owner can use the plugin at
any time as feedback: `claude --plugin-dir ~/projects/think-twice`, then `/think-twice:pause …`.

**Later, when the release candidate is fixed (D54):** record the model ID `opus` resolves to, then pass that full ID
as `--model` and `--judge-model` for every release-candidate run, and tell the owner to use it for every session
in which think-twice may run during SC-3 (`claude --model <ID>`).

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md and docs/plan.md
("Slice 2 tasks"). Run the start-up checks and record the CLI version and what opus resolves to.
Then ask me the open questions, and start T2.7d: draft the AT-07 calibration items for me to label.
```

## How to run things

- **Development runs:** `.local/devrun.sh OUT_DIR RUNS CASE [CASE]` rebuilds the staging copy at
  `/private/tmp/think-twice-run` with only the named cases, records the CLI, the resolved model, the skill hashes and
  the commit before and after, and runs `claude plugin eval` with `--keep-temp` (`opus` as model and judge). Score
  with `scripts/sc1-gate.py OUT_DIR/result.json --root . --tests "<IDs> AT-12 RC-05"`. A one-run check reports its
  tests and AT-12 as incomplete, so read its per-case results directly. Start long runs with the tool's background
  mode, never a shell `&`. Runs share the staging folder, so chain them, never run two at once.
- **Reading replies and diagnosing a failure:** `python3 .local/t27/replies.py RESULT_JSON [CASE]` prints each run's
  final reply, tools and failing graders. `python3 .local/t27/why.py RESULT_JSON CASE RUN GRADER` asks `opus` to
  re-apply one frozen grader to one stored reply and quote its reasons: **diagnosis only, never a grade**, and not
  the judge's own reasons.
- **Case groups:** C: `at07-sound-conclusion at23-many-small-issues at24-complete-argument
  at35a-overgeneralised-only at35b-circular at35c-two-flaws at35d-overgeneralised-plus`. D: `at08-cause-from-sequence
  at09-colleague-report at10-consensus at19a-one-sided-policy at19b-settled-fact at20-hidden-assumption
  at25a-lesson-after-repair at25b-sound-no-lesson`. Smoke A+B: `at01a-before-bare-question at01b-during-in-progress
  at01c-after-stated-conclusion at02-ambiguous-state at04-decision-without-view at05-opt-out at39a-settled-new-session
  at29-embedded-instruction at30-own-summary-file at36-claude-written-summary at38-missing-file`.
- **Wording scan before any skill run:** `python3 .local/t24/overlap.py`, diffed against its previous output; then
  `grep -ril` each new short phrase against `evals/` and `evals-baseline/`. Phrases shared with a grader are fine
  only if they come from REQUIREMENTS.
- **Gate runs** (T2.9): the command block in plan.md, below the slice 2 task table.
- **Never run evals from the repository** (T2.1, D53): always from the staging copy.
- **Calibration after a CLI update alone** (D53): run the compatibility check in evals/README.md (every AT-07 item
  plus `at08-good`, `at08-fabricated-source`, `at08-leading-question`, one run each, with `--case`); any wrong
  verdict means the full calibration.
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
  result in `.local/`; the answer is in `rawOutput`. Brief the owner before sending; present options neutrally.

## Open items to keep in view

- **AT-07**: T2.7d (calibration items, D51 rule), then T2.11 in a fresh Codex thread. SC-2 for AT-07 is
  non-regression against plain Claude, graded by the same graders; D50 applies to both arms, so the AT-07 baseline
  is re-run in T2.8b.
- **AT-23**: one split-vote critical failure in the last smoke check (re-judging gives PASS; an existing rule covers
  it, so nothing was added); T2.9 decides it.
- **AT-02's disputed runs** (T2.5–T2.6) still go to T2.11. The calibration set has no AT-02 item.
- **SC-2 has no margin** (plain Claude passed ≤1 of 3 on exactly 7 of 10). T2.8b re-runs all 14 baselines; if a
  qualifying test is lost, the owner hears it, and no test is weakened.
- **Four product rules from the drift review**, to revisit at T2.13–T2.14 after real use: quoted question marks
  counted against the question limit; "settled" said without a source; an argued first-person position read as
  settled; "do not list the answers" (evaluation.md, "Drift review and D51").
- **QR-13 budget:** about 250 tokens of headroom to 4,000 with slices 3–6 still to add; T2.14's plan for slices 3–7
  must budget it (consolidate rules, move material to `standards.md`).
- **Cost:** T2.7 cost $32 and T2.8 $41. Give the owner an estimate before each paid step, and say so before going
  far past it.
- **`evals/README.md` says "Anything missing fails the test"**; the script reports such evidence as incomplete,
  which, like a failure, never passes. The difference is recorded in evaluation.md.
- **FR-2.5** (offer to look further back when a summary can't be confirmed) is deferred to slice 3, with AT-17.
- **`Read` by exact path reaches the eval cases** under the plugin root; the gate fails any run that touches an eval
  folder.

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen; every change cites a decision entry with the D40 drift check.
- Tests are frozen at `tests-v1.3` and never weakened. A failing test is fixed in the skill; every skill change is
  noted in evaluation.md with the general rule and ID it implements, and uses no wording from a case. When a judge
  disagrees with its own case, record it for the second grader; do not tune towards it.
- Every gate attempt is kept; unchanged skill text is never re-run to get a pass.
- Every eval run uses `--no-publish` and starts from the staging copy. Record the CLI and the resolved model before
  and after each run session (D48).
- Real-use logs, manual results, raw eval results and Codex reviews stay private in `.local/`.
- No commit, push, tag or release unless the owner asks. Stage files individually.

## Leftovers on this machine

- `.local/t27a/` (C6, smoke A+B), `.local/t27b/` (D50 draft, AT-07 on `tests-v1.2`), `.local/t27e/` (errored-run
  brief and answer), `.local/t28/` (D1–D5, D2b, two A–C smoke checks), `.local/t2-drift/` (drift brief, answer, D51
  draft), `.local/t2-speed/` (speed-up brief and answer), `.local/real-use-log.md` (the template for real-use notes);
  earlier folders (`t2-plan`, `t23`–`t27`) as before. Private; gitignored.
- `/private/tmp/e-*`: **358 kept eval folders** (about 61 MB). Keep them until T2.11: they hold the traces of the
  disputed AT-07 runs.
- `/private/tmp/think-twice-run`: the staging copy, rebuilt before every run; nothing in it is needed.

## Codex threads

All on gpt-6-astra, high effort. Resume with `--resume <thread>` on the runner. **T2.11 uses a new thread.**

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
| `01a1736c-f570-74d0-a9e9-9e5e50bfaf2a` | Drift review against section 1; led to D51 (2026-10-25) |
| `01a17392-1a16-76b3-be51-0d153ff493f4` | Speed-up review; led to D52–D54 (2026-10-25) |

## Lessons from this session

- **Each new review rule can create the next failure.** In T2.8, rules for one lens leaked into others (AT-08,
  AT-25a, AT-23). Scope each rule to when it applies, put every new point through the gate, and run the cases that
  guard the other side.
- **A smoke check after a group run is worth its cost.** It caught two regressions that group D could not show.
- **Session limits hit long chains.** Fill in only the affected cases, on the same text, and say so.
- **Ask what a reviewer would find beyond the question,** and reproduce every finding before changing code. The
  errored-run review found a worse defect than the one asked about.
- **A calibration label can be wrong.** `at07-good` expected PASS for a note that fails the gate's own third
  condition; check labels against the requirement's wording, not against which judge agreed.
- **Measure a saving before claiming it.** The tiered-regression saving was overstated; Codex's arithmetic ($10.50
  per gate) changed the recommendation.
- **Re-judging is a reconstruction.** Twice it disagreed with the judge's votes (AT-07 run 3, AT-23 smoke); record
  the cause as unresolved rather than tuning towards either.
- **Shell quirks:** zsh aborts a `for` loop on a glob that matches nothing (use `find`); loading the gate script as a
  module leaves `scripts/__pycache__/`, which must be removed.
