# Handoff: 2026-10-19 (slice 1: probes and tests)

A snapshot of where things stand and where to pick up. **For live status, read [progress.md](progress.md)**; it wins
if the two ever disagree. The tasks are in [plan.md](plan.md).

## Where things stand

- **Slice 1, tasks T1.1–T1.8 are done.** All 48 acceptance tests in REQUIREMENTS section 5 are written. They are
  **not frozen yet**: the freeze is T1.10, after your review (T1.9).
- **Probes P-1 to P-7 all passed** (T1.2–T1.3), so every Auto test can stay automatic. Results, constraints and costs
  are in [evaluation.md](evaluation.md).
- **Built so far:**
  - `evals/`: 50 auto cases;
  - `evals-baseline/`: 14 SC-2 baseline cases (D46);
  - `evals/manual/`: 12 manual scripts;
  - `scripts/validate-plugin.sh`: RC-06;
  - `scripts/build-histories.py`: builds session histories from `dialogue.md`, with the current skill filled in;
  - `scripts/sc1-gate.py`: computes SC-1.

  Conventions are in [evals/README.md](../evals/README.md).
- **No product skill text yet**, and no `.claude-plugin/plugin.json` yet. Both are deliberate: tests come first.
- **Requirements:** v1.0 plus D44–D47. `git diff requirements-v1.0 -- docs/REQUIREMENTS.md` shows only lines citing
  them.
- **Git:** everything is committed and pushed. The last commit is `5ee37d5` on `main` of
  <https://github.com/ShivLee/think-twice>, which is **public** since 2026-10-19 (D3). A scan of the whole history
  found no email, local path, username or credential.
- **New public repository:** <https://github.com/ShivLee/think-twice-fixtures> holds the synthetic web pages for AT-31
  and AT-41. They are pinned by commit `0787d68`. **Never rewrite its history**, because that would break the frozen
  URLs.

## What this session decided

| # | Decision | Where |
| --- | --- | --- |
| D46 | Each SC-2 test (the 10, plus AT-07 and AT-19) gets its own baseline case, in the words you'd naturally type, run as plain Claude. The eval's built-in baseline arm can't do this: it gets the slash command too. | decisions.md (protected: success criteria) |
| D47 | How the auto cases run: pasted text or saved sessions; sanitized histories only; the current skill filled into pause turns; fixtures by scaffold script; card loads counted for RC-05; SC-1 computed by script; CLI, model and judge recorded. Every Manual test stays Manual for now, to be revisited after slice 2. | decisions.md |
| — | Eval cases declare their IDs in `tags`; RC-06 checks them. | evals/README.md |
| — | During cases use saved sessions, not pasted transcripts: FR-0.2 defines *during* by a conversation in this session. | evals/README.md |
| — | Counting rules (gap #18): questions by question mark; QR-6 length in whitespace tokens, +10%; Chinese in CJK characters, +10%. | evals/README.md |
| — | AT-31 and AT-41 fetch commit-pinned pages from a separate public fixture repository, after a Codex consultation. FR-0.8's redirect rule is a **known gap**, not tested. | plan.md, progress.md |
| — | A critical failure in **any** run, the first or the re-run, fails a manual test. | every manual script |

## What to do next time, in order

1. **Start-up.** Read [AGENTS.md](../AGENTS.md), this file, [progress.md](progress.md) and [plan.md](plan.md). Run
   `scripts/validate-plugin.sh` and `scripts/build-histories.py --check`; both should pass with no skill present.
2. **T1.9, your test review (D44).** Claude prepares the sample below as one readable page: each case's situation,
   dialogue, graded reply and PASS/FAIL conditions. For each case you answer: *is this a situation I actually meet?*
   and *would its PASS behaviour really help me?* Unrealistic cases get fixed. The sample is chosen in advance, as D44
   requires, though you may change it before reading:

   | Area | Cases |
   | --- | --- |
   | Before | AT-04 (substitution), AT-14 (criteria first), AT-33 (a flaw in early reasoning) |
   | During | AT-16 (summarise recent turns), AT-18 (criteria shift after a favourite), AT-S2b (resisting Claude) |
   | After | AT-07 (sound: no invented flaws), AT-08 (cause vs sequence), AT-35c (two flaws), AT-25a (the lesson) |
   | Situations | AT-S1 (strong reaction), AT-S5 (hindsight) |
   | Failure modes | QR-1: AT-04, AT-05 · QR-2: AT-07, AT-22 · QR-3: AT-08, AT-09 · QR-4: AT-21, AT-S2a · QR-5: AT-11 |
   | Also check | the plain-Claude wordings in all 14 baseline cases (D39), the Chinese prompts in AT-28a–d, and AT-26's "chapter 1" anchor |

3. **T1.10, the freeze.** Freeze the prompts, dialogues and graders. RC-06 must pass. From then on, any change needs a
   decision entry. Consider tagging the commit, for example `tests-v1.0`, so drift shows in a diff as it does for
   REQUIREMENTS.
4. **Pin the judge before any graded run.** Build a calibration set of known-good and known-bad replies, and choose and
   pin the judge model with it. In T1.6, Haiku once failed a good reply, and Sonnet failed another good reply in every
   run ([evaluation.md](evaluation.md)). One false critical failure fails a whole test.
5. **T1.11, the plain-Claude baseline** on the 14 baseline cases. This is information, not a gate. The repository has
   no `plugin.json` yet, so run it from a scratch copy with a minimal one (as the T1.6 smoke test did), or decide to
   add the real one. Tell the owner before slice 2 if plain Claude already passes too many.
6. **T1.12, the slice review.** Codex compares slice 1's changes with section 1 and the ID list; you read the review.
7. **Before slice 2:** write slice 2's tasks into plan.md, with IDs and done-when, and get the Codex rule 9 review.
   Slice 2 is the first time skill text gets written.

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md, docs/progress.md and docs/plan.md.
Then prepare T1.9: the owner test review sample from HANDOFF.md as one readable page.
Name the requirement IDs each step serves.
```

## How to change a test before the freeze

The case files were generated by scripts that lived in the session's scratch folder. Private copies are in
`.local/t1-generators/` (gitignored), for reference only. **Edit the case files directly.** Keep the shared grader
text identical in every case: `critical-reply`, the `at12-` and `rc05-` graders, and the critical tool checks. After
any edit, run `scripts/validate-plugin.sh` and `scripts/build-histories.py --check`.

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen. Every change cites a decision entry, and every new decision gets the D40 drift check.
- Tests are frozen at T1.10 and never weakened to make them pass. Write the skill from the tests; SKILL.md stays under
  about 4,000 tokens (QR-13).
- Every eval run uses `--no-publish`. Run `scripts/build-histories.py` before each run. Record the CLI, model and judge
  versions: the CLI moved from 2.1.303 to 2.1.304 during this session.
- Committed histories hold only conversation entries. Raw session files contain your email and credential entries.
- Real-use logs and manual results stay private in `.local/`.
- No commit, push, tag or release unless you ask. Stage files individually.

## Leftovers on this machine

None. The kept eval run folders (`/private/tmp/e-*`) and the T1.3 probe session files, which contained your email,
were deleted on 2026-10-19 at your request. Runs with `--keep-temp` leave such folders behind, so delete them after
inspecting.

## Codex threads

All on gpt-6-astra, high effort. Resume with `/cc-suite:continue <thread>`.

| Thread | What it reviewed |
| --- | --- |
| `01a14e42-3bc6-7750-bd9b-be610089efce` | Requirements v0.4 → v0.7.1 |
| `01a15259-f481-73d2-8658-a609e2c89b01` | The streamlining proposal; D44 and D45 |
| `01a15293-dbca-75b0-b297-9ea90c69f2e3` | Rule 9 review of plan.md; then (2026-10-19) best practice for AT-31 and AT-41 |

## Lessons from this session

- **Probe the real mechanics before writing frozen tests.** Several findings would have quietly broken the tests:
  - a resumed session follows the skill text stored in its history, not the current plugin's;
  - raw session files carry private data;
  - auto-memory can write during history generation;
  - the eval's baseline arm gets the slash command too.
- **The judge is part of the test.** With "one critical failure fails the test", a jumpy judge sinks good behaviour.
  Check a judge against known answers before trusting it; a stronger model is not automatically safer.
- **Read the replies, not just the verdicts.** Both suspicious grader results in this session were settled only by
  reading the full reply.
- **Situations interact.** AT-31's page was someone else's post, which made S3 apply and contradicted the test's own
  PASS condition. Codex caught it. Check each fixture against FR-0.2 and FR-3 before freezing.
