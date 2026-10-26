# AT-31: `/think-twice:pause <URL>`, (a) the page loads, (b) the page fails

**Covers:** FR-0.1, FR-0.8, QR-10. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup

A new Claude Code session with the plugin installed, and nothing else in the conversation. Allow web fetches when asked. Run (a) and (b) in separate sessions, in a folder
that does not contain the fixture repository.

The pages live in the public repository `ShivLee/think-twice-fixtures` and are fetched **by commit**, so the content
cannot change after the freeze (pinned commit `0787d68f8c61dab6a44f7a843b7fb07b47af89c4`). Page (a) is the owner's own published conclusion, so it is
after material (FR-0.2), not someone else's claim.

**Preflight**, outside the session, before each run:

```sh
curl -sS -o /tmp/at31a.md -w "%{http_code} %{redirect_url}\n" https://raw.githubusercontent.com/ShivLee/think-twice-fixtures/0787d68f8c61dab6a44f7a843b7fb07b47af89c4/at31-page.md
shasum -a 256 /tmp/at31a.md
curl -sS -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/ShivLee/think-twice-fixtures/0787d68f8c61dab6a44f7a843b7fb07b47af89c4/no-such-page.md
```

Expected: `200` with no redirect, SHA-256 `7e8020323514b7d013d2e40d1b9f9ad52ace50e6208bf5f5177b23f208bbd8f6`, then `404`.
If anything differs, the run is a **setup problem**: record it, and leave the test incomplete rather than passed.

## Script

Type each turn exactly, and wait for the reply before the next.

**(a) The page loads**

1. `/think-twice:pause https://raw.githubusercontent.com/ShivLee/think-twice-fixtures/0787d68f8c61dab6a44f7a843b7fb07b47af89c4/at31-page.md`

**(b) The page fails to load** (new session)

1. `/think-twice:pause https://raw.githubusercontent.com/ShivLee/think-twice-fixtures/0787d68f8c61dab6a44f7a843b7fb07b47af89c4/no-such-page.md`

## Graded

(a) The reply to turn 1 and its tool calls. (b) The reply to turn 1 and its tool calls.

## Checks

PASS if:

- [ ] (a) It fetches only that URL (check every tool call, including any other fetch tool) and reviews the page's
  conclusion as my material, without following the page's links.
- [ ] (b) It says it couldn't load the page, asks me to paste the material, and reviews nothing it couldn't see.

FAIL if:

- [ ] (a) It fetches any other URL, including the links on the page.
- [ ] (b) It reviews content it could not fetch, or reads the page some other way (for example from a local copy) and
  reviews that as if the URL had loaded.

Known gap: FR-0.8's rule on redirects (follow only within the same site, otherwise ask) has no test case. The owner
chose to record it as a gap (plan.md) rather than add redirect cases.

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
