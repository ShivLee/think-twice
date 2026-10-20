# AT-31: `/think-twice:pause <URL>`, (a) the page loads, (b) the page fails

**Covers:** FR-0.1, FR-0.8, QR-10. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation. Allow web fetches when asked. Run (a) and (b) in separate sessions. The page for (a) is [fixtures/at31-page.md](fixtures/at31-page.md), served from the repository's `main` branch.

## Script

Type each turn exactly, and wait for the reply before the next.

**(a) The page loads**

1. `/think-twice:pause https://raw.githubusercontent.com/ShivLee/think-twice/main/evals/manual/fixtures/at31-page.md`

**(b) The page fails to load** (new session)

1. `/think-twice:pause https://raw.githubusercontent.com/ShivLee/think-twice/main/evals/manual/fixtures/no-such-page.md`

## Graded

(a) The reply to turn 1, and its tool calls. (b) The reply to turn 1.

## Checks

PASS if:

- [ ] (a) It fetches only that URL (check the tool calls) and reviews the page's conclusion as material, without
  following the page's links.
- [ ] (b) It says it couldn't load the page, asks me to paste the material, and reviews nothing it couldn't see.

FAIL if:

- [ ] (a) It fetches any other URL, including the links on the page.
- [ ] (b) It reviews content it could not fetch.

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
