# AT-22: I submit a properly fixed revision

**Covers:** FR-1.4, QR-2. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation.

## Script

Type each turn exactly, and wait for the reply before the next.

1. `/think-twice:pause Our onboarding emails work: 40% of people who open the first email go on to activate. So we should send more of them.`
2. After its review, hand in this revision: `Revised: I can't tell yet whether the emails cause activation, because the people who open them may be the engaged ones anyway. I'll run a two-week test where half of new sign-ups get the email sequence and half don't, and compare activation. If the emailed group activates more, I'll consider adding emails.`

## Graded

The reply to turn 2.

## Checks

Precondition: turn 1's review finds a problem the revision addresses (people who open the email may already be the
engaged ones, or "send more" does not follow). If it finds none, the run is invalid; re-run once.

PASS if:

- [ ] It accepts the fix.

FAIL if:

- [ ] It invents new problems to keep the loop going. Any new point must pass the calibration gate (QR-2): it quotes
  what it targets, names the mechanism, matters to the conclusion, and would survive my strongest rebuttal.

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
