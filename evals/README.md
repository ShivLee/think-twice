# Acceptance tests

The tests in [REQUIREMENTS.md](../docs/REQUIREMENTS.md) section 5, as `claude plugin eval` cases and manual scripts.
They are written and **frozen before any skill text** (section 9, rule 2). After the freeze (T1.10), a change to a
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
- A test **passes** when it passes in at least 2 of 3 runs and **no `critical-` grader failed in any run**.
- AT-12 passes in a case when its `at12-` graders pass in at least 2 of 3 runs. AT-12 passes when it passes in every
  auto case. RC-05 fails if any run of any case loads more than 3 cards.
- T1.8 adds the script that computes this from the `--json` output (D47).

## Counting rules (gap #18, settled in T1.6)

- **Questions (QR-5, AT-12):** a question is counted by its question mark, `?` or `？`. Three or more in one reply
  fail. A quoted question counts too.
- **Length (QR-6):** words are whitespace-separated tokens of the reply, including Markdown markers. "About" means
  up to 10% over: before **275**, during **220**, after review **440**. When the phase is unclear, the tightest limit
  that could apply is used (stated in the case).
- **Length in Chinese (AT-28):** CJK characters count one each and other tokens count 1.5 characters each; limits
  **412 / 330 / 660** (375 / 300 / 600 plus 10%). Implemented with the Chinese cases (T1.8).
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

```sh
scripts/build-histories.py
claude plugin eval . --no-publish --scaffold --ablation none --runs 3 \
  --model <pinned model> --judge-model <pinned judge>
claude plugin eval . --eval-dir evals-baseline --no-publish --ablation with-without --runs 3 \
  --model <pinned model> --judge-model <pinned judge>
```

- `--no-publish` always (QR-9, RC-02). Results go to `evals/results/`, which git ignores.
- `--scaffold` runs the cases' own scaffold scripts, which only write fixtures.
- For the baseline cases, only the **without** arm counts (D46). The with arm loads the plugin, but the manual-only
  skill is invisible to the model, so it behaves the same.
- Record the CLI version, the model and the judge model with the results (D39, D47).
- While developing, run a smoke set with `--case` or `--tag`, plus the tests a change affects. Run the full gate at
  the end of each slice.

## Manual tests

Each script in `evals/manual/` gives the setup, the exact turns to type, the graded replies and a checklist. A manual
test is run once and re-run once on failure (SC-1). Results are recorded privately in `.local/`, never in the
repository.
