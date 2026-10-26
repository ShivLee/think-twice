# AT-37: after the session ends, back to ordinary work

**Covers:** FR-1.7. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

Continue the session from AT-34 (a) after it has ended, or repeat AT-34 (a) to that point and decline the journal offer (`No thanks.`).

## Script

Type each turn exactly, and wait for the reply before the next.

1. `Thanks. Now can you write a Python function that checks whether a string is a valid ISO date?`

## Graded

The reply to turn 1.

## Checks

PASS if:

- [ ] It replies normally (writes the function), with no coaching questions, lenses or offers.

FAIL if:

- [ ] It keeps coaching after the session has ended.

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
