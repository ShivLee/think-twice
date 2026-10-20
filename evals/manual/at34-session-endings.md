# AT-34: how a session ends

**Covers:** FR-1.6, FR-1.7. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation. Run each part in its own session.

## Script

Type each turn exactly, and wait for the reply before the next.

**(a) An after review that produced a lesson**

1. `/think-twice:pause We should stop paying for the premium support plan. In the last three months we only opened two tickets, so we clearly don't need it.`
2. After its review: `Revised: how often we open tickets doesn't tell us whether we need the plan. Last year's two-hour outage would have cost us about $20,000 in refunds without the one-hour response the plan guarantees, and the plan costs $6,000 a year. So I'll keep it, unless we can get the same response time more cheaply.`
3. When it asks for my view: `I'm keeping the plan unless we find the same response time for less.`

**(b) A during checkpoint**

1. Have this short conversation with Claude first, without the plugin command: `I run a team of six and I'm thinking about replacing our daily standup with written updates in Slack.` Then: `Two people are seven hours ahead, and the meeting runs 25 minutes most days.` Then: `I'm leaning towards async with one live meeting on Mondays.`
2. `/think-twice:pause`
3. When it asks you to confirm its summary: `Yes, that's right.`
4. When it asks for your view: `Async with a Monday meeting, and I'll check after a month whether people read the updates.`

**(c) My view at the start, then a revision**

1. `/think-twice:pause I think we should rewrite the billing service in Go, because the Python version is slow. That's my view.`
2. After its reply: `Revised: the slow part is the invoice export, which takes 40 seconds. I'll profile it first and only consider a rewrite if the fix needs a different language.`

**(d) "Stop" mid-session**

1. `/think-twice:pause I'm deciding whether to move my blog from WordPress to a static site.`
2. After its reply: `stop`

## Graded

(a) The replies to turns 2 and 3. (b) The replies to turns 3 and 4. (c) The reply to turn 2. (d) The reply to turn 2.

## Checks

PASS if:

- [ ] (a) The reply to turn 2 gives its output, then asks for my view in one sentence (or has me confirm a summary in
  my words), and **waits**. The journal offer comes only after my answer, in one line.
- [ ] (b) After the check, it gives its output and asks for my view. There is no journal offer at any point.
- [ ] (c) The session continues: it checks my revision.
- [ ] (d) It stops at once, with no closing question and no offer.

FAIL if:

- [ ] (a) It ends with its own summary as the conclusion, or offers the journal before I have answered.
- [ ] (b) It offers the journal at the checkpoint.
- [ ] (c) It ends the session.
- [ ] (d) It keeps going.

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
