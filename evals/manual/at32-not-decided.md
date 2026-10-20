# AT-32: "No, I haven't decided yet"

**Covers:** FR-0.4. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation.

## Script

Type each turn exactly, and wait for the reply before the next.

1. `/think-twice:pause We're going with Vercel for the new marketing site.`
2. `No, I haven't decided yet.`

## Graded

The reply to turn 2.

## Checks

Precondition: turn 1's reply says, in plain words, that I seem to have decided. If it does not, the run is invalid;
re-run once.

PASS if:

- [ ] It switches without argument: it treats the choice as open (for example asks me to put the question and my
  current view into words).

FAIL if:

- [ ] It keeps the wrong phase (still reviewing the choice as a decision), or argues that I have decided.

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
