# AT-15: a full before exchange ends with a brief

**Covers:** FR-2.4 before, QR-1. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation.

## Script

Type each turn exactly, and wait for the reply before the next.

1. `/think-twice:pause I want to ask Claude to help me plan moving our app off Heroku, but I don't know where to start.`

Then answer its questions naturally, in your own words, using only these facts:

- The question: which platform to move to, and how to move without downtime.
- Current view: leaning towards Render or Fly.io, because they seem cheap and similar to Heroku.
- Where that view comes from: two blog posts and a friend's recommendation.
- Criteria: under $300 a month, zero-downtime deploys, managed Postgres.
- Unsure about: how hard moving the database will be.

When it asks for your view in one sentence, give it.

## Graded

The final reply of the exchange (the brief).

## Checks

PASS if:

- [ ] It ends with a brief **in my words** covering my question, my current view, my criteria, and what I need to
  find out.
- [ ] What I need to find out starts with the strongest evidence against my current view.

FAIL if:

- [ ] It writes the prompt for me, or gives the conclusion (which platform to choose).

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
