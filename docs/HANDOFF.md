# Handoff: 2026-10-25 (slice 2: T2.1–T2.8 done; D55: real use now, the SC-1 gate at release only)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The slices and tasks are in [plan.md](plan.md) ("Slice 2 tasks").

## Where things stand

- **D55 (2026-10-25) changed how the work runs.** Real use drives it: the owner uses the plugin for real (T2.13,
  the current task), and a feature is built, or a test added or changed, only for a breach recorded in
  `docs/reactions.md` (local, D56; or, for a test, with the owner's explicit approval). The SC-1 gate is a release gate
  only; no development task closes on a pass rate.
- **Active tests:** AT-04, AT-05, AT-07, AT-08, AT-10, AT-19 (a, b), AT-20, AT-35 (a, c) in `evals/`, and the manual
  AT-11 and AT-21 in `evals/manual/`, unchanged since `tests-v1.3`. Everything else (the other cases and manual
  scripts, the 14 baselines, `evals-calibration/`, `sc1-gate.py`, `validate-plugin.sh`, `judge-calibration.py`) is in
  `archive/`, unchanged, in its old layout; the tag `pre-reset` (`3166e25`, pushed) marks the state before the move.
- **Postponed until the release candidate:** T2.7d, T2.8b and T2.9–T2.12, and with them the judge calibration, the
  baselines, the blind second grading and the self-tests. D52–D54 still govern the release candidate and SC-3.
- **Open from before D55** (looked at again at the release candidate, or sooner if real use shows them): AT-07's last
  3 runs passed 2/3, cause unresolved; AT-23 had one split-vote critical failure in the last smoke check; the FR-2.2
  premise wording from T2.7a did not take hold.
- **Open question for the release candidate (REQUIREMENTS section 8, "Still open"):** a requirement real use has not
  called for by then is either built for the release or moved out of v1.0 through a decision entry.
- **The skill:** `skills/pause/SKILL.md` (about 3,750 tokens by the fallback estimate; QR-13 about 4,000, tolerance
  4,400) and `standards.md` (about 1,530), SHA-256 `39703d89…` and `8093b6c2…`, committed at `ee428f8`; unchanged
  by D55.
- **Model and CLI:** `opus` = `claude-opus-5-5`; CLI 2.1.310 when last checked.
- **Git:** D55, the archive move and the doc changes are committed in three commits and pushed to `origin/main`
  (owner's request, 2026-10-25), then D56 in one more commit. Tag `pre-reset` (`3166e25`) is pushed too (owner's request).
  `docs/reactions.md` is local only (gitignored).

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
| — | Test audit: each test, eval and script classed CORE, LATER or CUT; ten CORE items; the doc instructions that made passing the frozen tests the goal listed | — |
| D55 | Real use first; SC-1 at release only; ten active tests, the rest archived after tag `pre-reset`; the test rule; REQUIREMENTS (sections 5, 6, 8, 9), AGENTS, CONTRIBUTING, `evals/README.md`, plan, progress, evaluation.md and README brought in line; `docs/reactions.md` created | three commits after `3166e25` |
| D56 | `docs/reactions.md` made the one private real-use log (gitignored, untracked; replaces `.local/real-use-log.md`), with a step-by-step guide and a logging prompt; entries written only on the owner's request and confirmation | one commit after D55 |

Owner decisions: leave the premise wording for now (open); approve D50 as drafted; close T2.8 with AT-23 left to
T2.9; apply Codex's narrowed option for errored runs; D51 with `at07-good` relabelled FAIL and zero wrong verdicts
allowed; D52–D54 as Claude recommended (owner: "make all the revisions according to your recommendation"); D55 as
the owner wrote it, with the follow-ups recorded in its entry.

## What to do next time, in order

1. **Start-up.** Read [AGENTS.md](../AGENTS.md), this file, [progress.md](progress.md), plan.md ("Slice 2 tasks")
   and D55 in [decisions.md](decisions.md). Then run, from the repository:

   ```sh
   python3 scripts/build-histories.py --check                          # 1/1 dialogues parsed (AT-05)
   git diff tests-v1.3 --stat -- $(find evals -type f ! -name history.jsonl ! -name README.md)   # empty: active tests unchanged
   git status -sb
   ```

   The judge calibration and the self-tests are retired (D55); `validate-plugin.sh`, `sc1-gate.py` and
   `judge-calibration.py` are in `archive/scripts/` until release.
2. **Check the model and the CLI** (`< /dev/null`, or `claude -p` waits on stdin). Record both in progress.md.

   ```sh
   claude --version
   claude -p --model opus --output-format json "Reply OK" < /dev/null | python3 -c 'import json,sys; print(*json.load(sys.stdin)["modelUsage"])'
   ```

3. **Real use first (T2.13, D55).** Ask the owner what they have used the plugin on since the last session, and
   whether anything in `docs/reactions.md` is new. The owner runs `claude --plugin-dir ~/projects/think-twice`, then
   `/think-twice:pause …`. `docs/reactions.md` is the one real-use log, private and local (gitignored; D56). At the
   end of a session the owner asks Claude to draft an entry from its template; it is appended only after the owner
   confirms. Never copy an entry's content into anything committed.
4. **For each new reactions entry that shows a requirement breach:**
   1. Check whether an active test already covers it. If not, write or change a test only for that breach, citing
      the entry (D55), or with the owner's explicit approval. Never weaken a test.
   2. Fix the skill for the breach as read in the reply, after checking whether an existing rule covers it
      (D52 (5)). Use no wording from a case.
   3. Run the affected active cases and a few active guard cases **once** each from the staging copy
      (`.local/devrun.sh`), and read the replies yourself; run 3 times only for a candidate that is clean at one
      run. No pass rate closes the task; the owner's next use is the check.
5. **Active tests (D55):** `evals/` holds AT-04, AT-05, AT-07, AT-08, AT-10, AT-19 (a, b), AT-20, AT-35 (a, c), and
   the manual AT-11 and AT-21. Everything else is in `archive/`, unchanged, and is not run during development.
6. **Postponed until the release candidate:** T2.7d, T2.8b and T2.9–T2.12. At release, restore the archived cases
   and scripts to their old paths and follow plan.md (the slice 2 gate command, D52 (2), D54).

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md, docs/plan.md
("Slice 2 tasks") and D55 in docs/decisions.md. Run the start-up checks and record the CLI version
and what opus resolves to. Then ask me what I've used the plugin on and what's new in
docs/reactions.md.
```

## How to run things

- **Development runs:** `.local/devrun.sh OUT_DIR RUNS CASE [CASE]` rebuilds the staging copy at
  `/private/tmp/think-twice-run` with only the named cases, records the CLI, the resolved model, the skill hashes and
  the commit before and after, and runs `claude plugin eval` with `--keep-temp` (`opus` as model and judge). In
  development, name only active cases and **read the replies** (below); no pass rate closes a task (D55). The gate
  script is in `archive/scripts/` until the release candidate. Start long runs with the tool's background
  mode, never a shell `&`. Runs share the staging folder, so chain them, never run two at once.
- **Reading replies and diagnosing a failure:** `python3 .local/t27/replies.py RESULT_JSON [CASE]` prints each run's
  final reply, tools and failing graders. `python3 .local/t27/why.py RESULT_JSON CASE RUN GRADER` asks `opus` to
  re-apply one frozen grader to one stored reply and quote its reasons: **diagnosis only, never a grade**, and not
  the judge's own reasons.
- **Active cases (D55):** `at04-decision-without-view at05-opt-out at07-sound-conclusion at08-cause-from-sequence
  at10-consensus at19a-one-sided-policy at19b-settled-fact at20-hidden-assumption at35a-overgeneralised-only
  at35c-two-flaws`; manual `evals/manual/at11-i-dont-know.md` and `at21-pushback.md`. The old groups A–D are in
  `archive/evals/` and run again at the release candidate.
- **Wording scan before any skill run:** `python3 .local/t24/overlap.py`, diffed against its previous output; then
  `grep -ril` each new short phrase against `evals/` and `archive/` (the archived cases are still release tests). Phrases shared with a grader are fine
  only if they come from REQUIREMENTS.
- **Gate runs** (T2.9; release candidate only, D55): restore the archived cases and scripts to their old paths,
  then the command block in plan.md, below the slice 2 task table.
- **Never run evals from the repository** (T2.1, D53): always from the staging copy.
- **Calibration** (release candidate only, D55). After a CLI update alone (D53): run the compatibility check in evals/README.md (every AT-07 item
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

- **Real use is the check now** (D55). Every real situation goes in `docs/reactions.md` (local, D56); the first entries will
  show what to work on next.
- **At the release candidate** (unless real use raises them sooner): AT-07 (T2.7d's calibration items under D51,
  then T2.11 in a fresh Codex thread; its baseline is re-run because D50 applies to both arms); AT-23's split-vote
  critical failure; AT-02's disputed runs (T2.11; the calibration set has no AT-02 item); SC-2's zero margin (plain
  Claude passed ≤1 of 3 on exactly 7 of 10; T2.8b re-runs all 14 baselines, and no test is weakened if one is lost).
- **Checks that run only at release now** (they live in the archived `sc1-gate.py`): the D49 chapter check (a reply
  naming a *Beyond Feelings* chapter that no shipped card has is critical; QR-8) and the contamination check (a run
  that touches an eval folder). No card ships yet; once one does, check named chapters by eye in real use.
- **v1.0 scope** (REQUIREMENTS section 8, "Still open"): a requirement real use has not called for by the release
  candidate is built for it or moved out of v1.0 by a decision entry.
- **Four product rules from the drift review**, to revisit after real use (T2.13–T2.14): quoted question marks
  counted against the question limit; "settled" said without a source; an argued first-person position read as
  settled; "do not list the answers" (evaluation.md, "Drift review and D51").
- **QR-13 budget:** about 250 tokens of headroom to 4,000; any later feature must budget it (consolidate rules, move
  material to `standards.md`).
- **Cost:** T2.7 cost $32 and T2.8 $41. Give the owner an estimate before each paid step, and say so before going
  far past it.
- **`evals/README.md` says "Anything missing fails the test"**; the gate script reports such evidence as incomplete,
  which, like a failure, never passes. The difference is recorded in evaluation.md.
- **FR-2.5** (offer to look further back when a summary can't be confirmed) belongs to slice 3, with AT-17.
- **`Read` by exact path reaches the eval cases** under the plugin root; always run from the staging copy.

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen; every change cites a decision entry with the D40 drift check.
- The ten active tests are frozen at `tests-v1.3` and never weakened (D55). A test is added or changed only for a
  requirement breach seen in real use (citing its `docs/reactions.md` entry), or with the owner's explicit approval.
  The skill changes only for a requirement breach read in a reply, not because a test failed (D52 (5)); every skill
  change is noted in evaluation.md with the general rule and ID it implements, and uses no wording from a case. When
  a judge disagrees with its own case, record it; do not tune towards it.
- The SC-1 gate is a release gate only (D55); no development task closes on a pass rate.
- Every gate attempt is kept; unchanged skill text is never re-run to get a pass.
- Every eval run uses `--no-publish` and starts from the staging copy. Record the CLI and the resolved model before
  and after each run session (D48).
- Real-use logs, manual results, raw eval results and Codex reviews stay private: in `.local/`, and the real-use log
  in `docs/reactions.md`, which is gitignored (D56). A test or commit that follows from an entry cites it by date and
  number only.
- No commit, push, tag or release unless the owner asks. Stage files individually.

## Leftovers on this machine

- `.local/t27a/` (C6, smoke A+B), `.local/t27b/` (D50 draft, AT-07 on `tests-v1.2`), `.local/t27e/` (errored-run
  brief and answer), `.local/t28/` (D1–D5, D2b, two A–C smoke checks), `.local/t2-drift/` (drift brief, answer, D51
  draft), `.local/t2-speed/` (speed-up brief and answer), `.local/real-use-log.md` (empty template, replaced by `docs/reactions.md`, D56);
  earlier folders (`t2-plan`, `t23`–`t27`) as before. Private; gitignored.
- `/private/tmp/e-*`: **358 kept eval folders** (about 61 MB), with the traces of the disputed AT-07 runs for
  T2.11, which is now at the release candidate (D55). `/private/tmp` may be cleared on restart; copy them into
  `.local/` if they must survive until then.
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
