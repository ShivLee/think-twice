# Contributing to think-twice

How to change this project. *What* the product does is defined in
[docs/REQUIREMENTS.md](docs/REQUIREMENTS.md). Decisions are recorded in [docs/decisions.md](docs/decisions.md).

## Ground rules

- Every change names the requirement IDs (FR, QR or AT) it serves.
- Tests come before skill text. Acceptance tests are frozen before the skill is written or changed. A frozen test
  changes only through a decision entry, and never just so that it passes.
- Changes to the goal, the four questions, the success criteria, the delivery form, privacy or the role of the book
  need an owner-approved entry in `docs/decisions.md` first.
- Never commit book text, journal entries or other personal reasoning content.

## Adding a situation

A new situation is worth adding when the same gap has come up about **three times** in real use. It also needs all
three of these:

- the core and the existing situations did not catch it;
- it has a distinct, one-line extra check;
- it can be recognised from cues in the material.

Candidates come mainly from journal entries marked `other: ___` (FR-5.8) and from corrections to think-twice's
opening line.

Steps, in this order:

1. **Decision entry** in `docs/decisions.md`, with the evidence: where it came up, and why the core and the existing
   situations missed it.
2. **A new row in FR-3** in `docs/REQUIREMENTS.md`: the cue, the usual phase, and the one extra check.
3. **A new `AT-S` test**, written and frozen before any skill text changes.
4. **A method card**, if a *Beyond Feelings* method fits. It is paraphrased, cites the chapter, and is checked against
   its source passage.
5. **The skill change.** Then re-run AT-S7 and the existing situation tests to catch regressions.

To ask Claude to do this:

```text
In think-twice, I want to add a new situation: <describe it, plus 1–2 real
examples of when it came up>. Follow "Adding a situation" in CONTRIBUTING.md:
draft the decision entry and the FR-3 row, and write the AT-S test. Show me
before changing any skill text.
```
