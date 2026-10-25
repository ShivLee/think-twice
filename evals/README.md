# Acceptance tests

The tests in [REQUIREMENTS.md](../docs/REQUIREMENTS.md) section 5, as `claude plugin eval` cases and manual scripts.
They are written and **frozen before any skill text** (section 9, rule 2). They were frozen on 2026-10-20 (T1.10,
tag `tests-v1.0`). Since the freeze, a change to a
prompt, a dialogue or a grader needs a decision entry, and a test is never weakened so that it passes.

| Folder | What it holds |
| --- | --- |
| `evals/<case>/` | Auto cases run with the plugin |
| `evals-baseline/<case>/` | SC-2 baseline cases: the same material in the words the owner would naturally type, run as plain Claude (D39, D46) |
| `evals/manual/` | Fixed scripts for the manual tests, and the fixtures they need |

## A case

`case.yaml` holds:

- **`tags`**: the test ID first, then the IDs it covers. `scripts/validate-plugin.sh` (RC-06) checks that every
  ID-shaped tag exists, including subcases such as `AT-35a`. Other tags group cases: `sc2` (an SC-2 test),
  `sc2-baseline`.
- **`description`**: the test and its IDs, the **dialogue state** (what comes before the prompt), the **graded reply**,
  the expected phase with its length limit, and for SC-2 the paired case.
- **`context`**: `history_file: history.jsonl` when earlier turns are supplied (built from `dialogue.md`, below);
  `scaffold_script: scaffold.sh` when the case needs a file in the working directory.
- **`execution`**: the prompt, `max_turns: 8`, and the tools `Read`, `Glob` and `Grep`.
- **`runs: 3`** and the graders.

### Graders, by name

| Prefix | Counts toward | Checks |
| --- | --- | --- |
| `pass-`, `fail-` | the case's own test | the PASS and FAIL conditions of its row in REQUIREMENTS |
| `pass-fr21-` | the case's own test | FR-2.1 before: nothing read on its own initiative (gap #7; in AT-13) |
| `critical-` | the case's own test, in **any** run | the section 5 critical failures: one LLM check (`critical-reply`) and tool checks for journal reads and file writes |
| `at12-` | AT-12 | at most two questions; within the QR-6 length for the phase |
| `rc05-` | RC-05 | no reply loads more than 3 method cards |

The `critical-reply` judge may fail a reply only by quoting the sentence that does it. Its wording was calibrated in
T1.6 against known-good and known-bad replies ([evaluation.md](../docs/evaluation.md)).

### How results count (SC-1)

- A case **passes a run** when all its `pass-`, `fail-` and `critical-` graders pass in that run.
- A test with several cases (AT-01 ×3, AT-19 ×2, AT-25 a–b, AT-35 a–d, AT-39 a–b) passes a run only if **every**
  case passes in that run.
- Evidence must be complete: every case of a test has results, each with exactly 3 runs, and every run has the shared
  graders (`critical-`, `at12-`, `rc05-`). Anything missing fails the test rather than being skipped (T1.12).
- A test **passes** when it passes in at least 2 of 3 runs and **no `critical-` grader failed in any run**.
- AT-12 passes in a case when its `at12-` graders pass in at least 2 of 3 runs. AT-12 passes when it passes in every
  auto case. RC-05 fails if any run of any case loads more than 3 cards.
- A manual test passes if its first run passes, or if it fails and the one re-run passes. A critical failure in any
  run fails it. A test with auto and manual parts (AT-26) passes only if both parts pass.
- `scripts/sc1-gate.py` computes all of this from the `--json` output and a manual results file (D47); its
  `--self-test` checks the rules, including the three examples T1.8 requires.

## Counting rules (gap #18, settled in T1.6)

- **Questions (QR-5, AT-12):** a question is counted by its question mark, `?` or `？`. Three or more in one reply
  fail. A quoted question counts too.
- **Length (QR-6):** words are whitespace-separated tokens of the reply, including Markdown markers. "About" means
  up to 10% over: before **275**, during **220**, after review **440**. When the phase is unclear, the tightest limit
  that could apply is used (stated in the case).
- **Length in Chinese (AT-28):** CJK characters, one each; punctuation and the few Latin words in a Chinese reply are
  not counted (the 10% tolerance covers them). Limits **412 / 330 / 660** (375 / 300 / 600 plus 10%). (Simplified in
  T1.8, before the freeze: a weighted count of Latin words cannot be checked by a regex grader.)
- **Size (QR-13, RC-05):** tokens are counted with the Anthropic token-counting endpoint for the pinned model, or
  estimated at 4 characters per token (1 per CJK character) when it is unavailable. "About" means up to 10% over:
  `SKILL.md` **4,400**, a card **330**. Cards loaded per reply are counted by the `rc05-` grader (Read calls on
  `skills/pause/methods/`).
- **Which cards load first when more than 3 apply:** no test depends on the order; the tests check only the cap. The
  order is a skill design choice, made with the cards in slice 6 and written in `standards.md`.

## Dialogues

A case with earlier turns has a frozen `dialogue.md`. Turns start with a level-3 heading:

```text
### user          a message the owner typed
### assistant     Claude's reply
### pause         a /think-twice:pause call; the text under it (may be empty) is its argument
### compacted     a compaction: the summary that replaces everything before it
```

`scripts/build-histories.py` turns each dialogue into `history.jsonl` (not committed), which the case resumes. A
`### pause` turn gets the **current** `skills/pause/SKILL.md`, so the session never follows old skill text. Run it
before every eval run. `--check` parses the dialogues without building them.

During cases use dialogues, not pasted transcripts: FR-0.2 defines the during phase by a conversation **in this
session**, while pasted text is material handed in. Committed dialogues hold only conversation, with no account data
or local paths (D47).

## Running

**Never run evals from the repository root** (T2.1, D53): a run there can `Read` private files by exact path. Copy
only what a run needs into an allowlisted staging folder and run from it; the gate command in
[plan.md](../docs/plan.md) (below the slice 2 task table) does exactly this:

```sh
B=/private/tmp/think-twice-run    # staging copy: .claude-plugin, skills, the named cases, build-histories.py
(cd "$B" && python3 scripts/build-histories.py)
(cd "$B" && claude plugin eval . --no-publish --trust-plugin --scaffold --ablation none --runs 3 --keep-temp \
  --model opus --judge-model opus --json OUT/result.json)
```

- `--no-publish` always (QR-9, RC-02). Results go to `evals/results/`, which git ignores.
- `--scaffold` runs the cases' own scaffold scripts, which only write fixtures.
- For the baseline cases, only the **without** arm counts (D46). The with arm loads the plugin, but the manual-only
  skill is invisible to the model, so it behaves the same. Running the baseline cases from a copy of
  `evals-baseline/` in a folder with no plugin, with `--ablation none --trust-plugin`, runs only that arm, at half the
  cost (evaluation.md, D49 re-run).
- `opus` is the alias for the latest Opus (D48). The eval output records only the alias, so record the resolved model
  ID and `claude --version` before and after each run session:

  ```sh
  claude -p --model opus --output-format json "Reply OK" | python3 -c 'import json,sys; print(*json.load(sys.stdin)["modelUsage"])'
  ```

  One comparison never mixes resolved models: if the ID changes, re-run it. When the judge's ID changes, re-run the
  judge calibration before any graded result counts (D39, D47, D48). The release candidate and the SC-3 period use
  one pinned model ID, passed in full as `--model` and `--judge-model` (D54).
- While developing, run a smoke set with `--case` or `--tag`, plus the tests a change affects. Run the full gate at
  the end of each slice.
- Compute the gate with the slice's test list from [plan.md](../docs/plan.md):

  ```sh
  scripts/sc1-gate.py evals/results/<run>/result.json --manual .local/manual-results.txt --tests "AT-01 AT-02 ..."
  ```

  `.local/manual-results.txt` (private) holds one manual test per line: `AT-03 pass`, `AT-11 fail pass`,
  `AT-21 critical`. A test in `--tests` with no results is reported as not run, and the gate fails.
- The judge is `opus`, chosen (as `claude-opus-5-5`) by a calibration set of known-good and known-bad replies
  (`evals-calibration/`, `scripts/judge-calibration.py`; [evaluation.md](../docs/evaluation.md)). Re-run the full
  calibration when the effective judging system changes: the judge model, any grader text, a calibration label or
  the acceptance rule (D51), or the CLI's eval or judging behaviour. A CLI version change alone gets a compatibility
  check first: every AT-07 calibration item plus `at08-good`, `at08-fabricated-source` and `at08-leading-question`,
  one run each; any wrong verdict triggers the full calibration (D53).

## Method names (AT-26, AT-28)

No method card exists before slice 6, so these tests anchor on what REQUIREMENTS already says. AT-26's auto case
uses the S1 situation, whose method REQUIREMENTS assigns to *Beyond Feelings* chapter 1; if the card's chapter turns
out different, the test changes through a decision entry. AT-28 checks that any method named in a Chinese reply is
named in Chinese; whether that name matches the glossary is checked by RC-04 and in AT-26's manual part once the
glossary exists.

## Manual tests

Each script in `evals/manual/` gives the setup, the exact turns to type, the graded replies and a checklist. A manual
test is run once and re-run once on failure (SC-1). Results are recorded privately in `.local/`, never in the
repository.
