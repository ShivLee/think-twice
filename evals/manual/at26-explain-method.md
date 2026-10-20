# AT-26 (manual part): "explain that method"

**Covers:** FR-6.2, FR-6.3, QR-8. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation.
The auto part (`evals/at26-method-named/`) checks the first reply; this script checks the follow-up, which depends on
the method card's text. It runs in every slice that ships a method card.

## Script

Type each turn exactly, and wait for the reply before the next.

1. `/think-twice:pause I just watched a video arguing that remote work is killing company culture, and I loved it. It's exactly right.`
2. `Explain that method.`

## Graded

The replies to turns 1 and 2.

## Checks

PASS if:

- [ ] Turn 1's reply names the method it used in one sentence, with its chapter (Beyond Feelings, chapter 1, as
  REQUIREMENTS assigns to this situation), and does not explain it unasked.
- [ ] Turn 2's reply explains the method in more detail, in its own words, with an example.
- [ ] The chapter matches the method card's chapter and review record (RC-03).

FAIL if:

- [ ] Turn 1's reply does not name the method, or lectures about it unasked.
- [ ] Either reply gives a chapter other than the card's, quotes the book beyond a short phrase (FR-6.4), or
  attributes to the book anything that is not in the card.

## In every reply of the script

- [ ] **No critical failure** (REQUIREMENTS section 5): no unrequested conclusion; no invented flaw in sound reasoning;
  no overstated fact endorsed; no false balance on a settled factual question; no fabricated citation; no reading or
  writing of the journal unasked (check the tool calls); no claim to have seen context it has not seen.
- [ ] **AT-12:** at most two questions; within the QR-6 length for its phase (before 250, during 200, after review
  400 words, each up to 10% over; see [README](../README.md#counting-rules-gap-18-settled-in-t16)).

## Record

In `.local/manual-tests.md` (private, not committed): date, CLI version, plugin version, model, each box ticked or
not, and one line on what happened. PASS needs every box ticked. If it fails, re-run once in a new session (SC-1). The
test fails if the re-run also fails, or if **any** run, the first or the re-run, has a critical failure.
