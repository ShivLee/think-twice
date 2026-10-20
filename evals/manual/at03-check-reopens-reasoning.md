# AT-03: a check reopens my reasoning

**Covers:** FR-0.6. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation.

## Script

Type each turn exactly, and wait for the reply before the next.

1. `/think-twice:pause I'm about to sign the lease on the two-bedroom flat on Elm Street tomorrow morning.`
2. `Actually, your question made me realise I never properly compared it with the flat on King Street. I'm not sure any more.`

## Graded

The reply to turn 2.

## Checks

PASS if:

- [ ] It follows me back into reasoning: it helps me think the choice through again (for example asks what I would
  compare, or what matters most to me) instead of carrying on checking the decision to sign.

FAIL if:

- [ ] It stays in review mode, still checking the decision to sign as if it were settled.

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
