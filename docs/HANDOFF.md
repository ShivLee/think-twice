# Handoff: 2026-10-18 (planning session)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The tasks are in [plan.md](plan.md).

## Where things stand

- **Requirements:** approved v1.0 (tag `requirements-v1.0`), now with **D44 and D45** added. `git diff
  requirements-v1.0 -- docs/REQUIREMENTS.md` shows only the lines that cite them.
- **Plan:** `docs/plan.md` exists, has had the Codex rule 9 review, and all findings are fixed.
- **Built:** nothing yet. No skill text, no tests, no scripts. T1.1 (eval privacy) is in place: `evals/results/` is
  ignored by git, and `--no-publish` applies from the first eval run.
- **Git:** D44, D45 and the plan are committed and pushed to <https://github.com/ShivLee/think-twice> (`f7795fa`,
  `c6e4471`), followed by one commit with this handoff and the matching progress.md update.
- **Next:** slice 1, task **T1.2: probe P-1**.

## What this session decided

| # | Decision | Where |
| --- | --- | --- |
| — | **Keep the original plan:** 7 slices, all 48 tests, tests frozen before any skill text. Streamlining by cutting tests or slices was rejected after a Codex review; time is saved by how the work is run, not by changing the rules. | plan.md, "Working practices" |
| D44 | **Slice 1 ends with an owner test review**, not real use, because slice 1 builds no product feature. Before the freeze, I read a sample of test cases chosen in advance (three phases, four failure modes) and check: is this a situation I actually encounter, and would the PASS behaviour really help me? | decisions.md |
| D45 | **SC-3 counting starts after slice 6** passes its tests; the ~3 weeks of real use run alongside slice 7. Earlier use is feedback only. Six counting rules: every real situation counts; extend only for coverage, never for scores; same percentages above 10 uses; earlier lessons count if applied unprompted; a material change restarts the period; during the period, only critical failures are fixed. | decisions.md (protected item: success criteria) |
| — | **Eval privacy first:** every `claude plugin eval` run uses `--no-publish` (the default publishes the report to claude.ai), and `evals/results/` is ignored by git. | plan.md T1.1, `.gitignore` |
| — | **`docs/plan.md`** holds the slices and tasks; **`docs/progress.md`** holds status only, so it stays short. | plan.md, progress.md |

## How the plan works (one minute)

- **Each slice's gate** is a fixed list of tests in plan.md. A slice passes when its own tests **and every earlier
  slice's tests** pass under the SC-1 rule (≥2 of 3 runs, no critical failure). Tests for later slices are "not
  implemented", not failures.
- **Each slice ends with** its gate passing, me using it once on something real (slice 1: the D44 test review),
  and a Codex review of the diff.
- **Before each later slice starts**, its tasks are written into plan.md and Codex reviews them (rule 9).
- **Version:** `0.x` until SC-1–SC-4 are all met; then `1.0.0`. The earliest `1.0.0` is about 3 weeks after
  slice 6 is done.
- **The biggest unknown is P-1.** If `claude plugin eval` can't invoke a manual-only skill, every auto test becomes
  manual and the work grows. Re-estimate the timeline after slice 2, from measured times.

## Where to pick up

**Slice 1, in plan.md order:** T1.2 probe P-1 → T1.3 probes P-2–P-7 → T1.4 set the "How" column → T1.5 validation
script (RC-06) → T1.6–T1.8 write the tests → **T1.9 my test review** → T1.10 freeze → T1.11 plain-Claude baseline
on the SC-2 cases → T1.12 slice review.

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md and docs/plan.md.
Then start T1.2, probe P-1, with a throwaway skill. Run every eval with --no-publish.
Name the requirement IDs each step serves.
```

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen. Every change cites a decision entry; `git diff requirements-v1.0` shows drift.
- Every new decision gets the D40 drift check: *Serves* and *Protected item*.
- Tests are frozen before skill text. Never weaken a test to make it pass.
- Write the skill from the tests, not by copying the requirements; SKILL.md stays under about 4,000 tokens (QR-13).
- Every eval run uses `--no-publish`. Real-use logs stay private in `.local/`, never in progress.md.
- No commit, push, tag or release unless I ask.

## Codex threads

All on gpt-6-astra, high effort. Resume with `/cc-suite:continue <thread>`.

| Thread | What it reviewed |
| --- | --- |
| `01a14e42-3bc6-7750-bd9b-be610089efce` | Requirements v0.4 → v0.7.1 (earlier session) |
| `01a15259-f481-73d2-8658-a609e2c89b01` | The streamlining proposal; recommendations for D44 and D45 |
| `01a15293-dbca-75b0-b297-9ea90c69f2e3` | Rule 9 review of plan.md: NEEDS REVISION, 6 findings, all fixed |

## Lessons from this session

- **Cutting tests and slices saves less than it seems.** Most of the time comes from SC-3's three weeks and from
  repeat runs. Running the work well (targeted checks, early baseline, real use as feedback) saves more than changing
  the rules.
- **An "obvious" test merge can drop a requirement.** AT-03 and AT-32, or AT-38 and AT-31b, look alike but check
  different things.
- **Parent IDs hide scope.** Writing "FR-0" for slice 2 silently pulled in situations from slice 4. Gates now list
  exact tests.
