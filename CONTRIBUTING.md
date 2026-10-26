# Contributing to think-twice

How to change this project. *What* the product does is defined in
[docs/REQUIREMENTS.md](docs/REQUIREMENTS.md). Decisions are recorded in [docs/decisions.md](docs/decisions.md).

## Ground rules

- Every change names the requirement IDs (FR, QR or AT) it serves.
- Real use decides what gets built: a feature is built only when real use shows it is needed, recorded in
  `docs/reactions.md` (D55).
- Tests come before fixes. A test is added or changed only for a requirement breach the owner saw in real use
  (citing its `docs/reactions.md` entry), or with the owner's explicit approval, and before the skill change it
  checks. A test is never weakened so that it passes. During development only the active tests in `evals/` run; the
  rest are kept unchanged in `archive/` for the release candidate (D55).
- Changes to the goal, the four questions, the success criteria, the delivery form, privacy or the role of the book
  need an owner-approved entry in `docs/decisions.md` first.
- Never commit book text, journal entries or other personal reasoning content. `docs/reactions.md`, the real-use
  log, is private and local (gitignored, never committed; D56): a test or commit that follows from an entry cites it
  by date and number only and uses invented material, never the entry's content.

## Adding a situation

A new situation is worth adding when the same gap has come up about **three times** in real use. It also needs all
three of these:

- the core and the existing situations did not catch it;
- it has a distinct, one-line extra check;
- it can be recognised from cues in the material.

Candidates come mainly from `docs/reactions.md`, from journal entries marked `other: ___` (FR-5.8) and from
corrections to think-twice's opening line.

Steps, in this order:

1. **Decision entry** in `docs/decisions.md`, with the evidence: where it came up (citing the `docs/reactions.md`
   entries), and why the core and the existing situations missed it.
2. **A new row in FR-3** in `docs/REQUIREMENTS.md`: the cue, the usual phase, and the one extra check.
3. **A new `AT-S` test**, citing those entries, written and frozen before any skill text changes.
4. **A method card**, if a *Beyond Feelings* method fits. It is paraphrased, cites the chapter, and is checked against
   its source passage.
5. **The skill change.** Then run the new test and the active tests once each, and read the replies. The archived
   situation tests (AT-S1–AT-S7) run again at the release candidate (D55).

To ask Claude to do this:

```text
In think-twice, I want to add a new situation: <describe it, plus 1–2 real
examples of when it came up>. Follow "Adding a situation" in CONTRIBUTING.md:
draft the decision entry and the FR-3 row, and write the AT-S test. Show me
before changing any skill text.
```
