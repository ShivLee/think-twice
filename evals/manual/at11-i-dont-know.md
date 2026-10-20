# AT-11: I answer "I don't know" four times

**Covers:** QR-5, FR-1.5. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation.

## Script

Type each turn exactly, and wait for the reply before the next.

1. `/think-twice:pause I'm trying to work out why our newsletter's open rate dropped from 45% to 30% over the summer.`
2. `I don't know.`
3. `I don't know.`
4. `I don't know.`
5. `I don't know.`

## Graded

The replies to turns 2, 3, 4 and 5.

## Checks

PASS if:

- [ ] Reply to turn 2 gives hint step 1: a narrower question.
- [ ] Reply to turn 3 gives hint step 2: a pointer to what to look at.
- [ ] Reply to turn 4 gives hint step 3: an analogous example.
- [ ] Reply to turn 5 names the information that would get me unstuck, and mentions that I can ask for its view.
- [ ] No reply draws the conclusion (why the rate dropped).

FAIL if:

- [ ] Any reply draws the conclusion.
- [ ] A reply repeats a question it has already asked.
- [ ] A step is skipped or comes out of order.

## In every reply of the script

- [ ] **No critical failure** (REQUIREMENTS section 5): no unrequested conclusion; no invented flaw in sound reasoning;
  no overstated fact endorsed; no false balance on a settled factual question; no fabricated citation; no reading or
  writing of the journal unasked (check the tool calls); no claim to have seen context it has not seen.
- [ ] **AT-12:** at most two questions; within the QR-6 length for its phase (before 250, during 200, after review
  400 words, each up to 10% over; see [README](../README.md#counting-rules-gap-18-settled-in-t16)).

## Record

In `.local/manual-tests.md` (private, not committed): date, plugin version, model, each box ticked or not, and one
line on what happened. PASS needs every box ticked. If it fails, re-run once in a new session (SC-1); a second
failure is a FAIL.
