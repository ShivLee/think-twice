# AT-27: the learning journal

**Covers:** FR-5.1-FR-5.8, QR-9. **How:** manual, with this fixed script (REQUIREMENTS 5.2).

## Setup


A Claude Code session with the plugin installed, in a folder that is **not** inside a git repository (for example
`/tmp`). This test uses the real default journal path, `~/.think-twice/think-twice-journal.md`, so it protects any real journal first. Both blocks are safe to run twice: setup refuses to run over an unfinished earlier run, and cleanup never deletes a journal it cannot show the test created (D49).

**Before:**

```sh
mkdir -p ~/.think-twice
if [ -e ~/.think-twice/at27-state ] || [ -e ~/.think-twice/think-twice-journal.md.at27-backup ]; then
  echo "STOP: an earlier AT-27 run was not cleaned up. Run the After block, check your journal, then start again."
else
  if [ -f ~/.think-twice/think-twice-journal.md ]; then
    echo had-journal > ~/.think-twice/at27-state
    mv ~/.think-twice/think-twice-journal.md ~/.think-twice/think-twice-journal.md.at27-backup
  else
    echo no-journal > ~/.think-twice/at27-state
  fi
  cp <repo>/evals/manual/fixtures/at27-seed-entries.md ~/.think-twice/think-twice-journal.md
fi
shasum -a 256 ~/.think-twice/think-twice-journal.md      # note this: the seed entries' checksum
head -c "$(wc -c < <repo>/evals/manual/fixtures/at27-seed-entries.md)" ~/.think-twice/think-twice-journal.md | shasum -a 256   # the same, for later
rm -rf /tmp/tt-at27-repo /tmp/tt-at27-alt /tmp/tt-at27-ro
git init -q /tmp/tt-at27-repo
mkdir -p /tmp/tt-at27-ro && chmod 555 /tmp/tt-at27-ro
```

**After, always (even if a part fails):**

```sh
state=$(cat ~/.think-twice/at27-state 2>/dev/null)
if [ "$state" = had-journal ] && [ -f ~/.think-twice/think-twice-journal.md.at27-backup ]; then
  mv -f ~/.think-twice/think-twice-journal.md.at27-backup ~/.think-twice/think-twice-journal.md && rm ~/.think-twice/at27-state
elif [ "$state" = no-journal ]; then
  rm -f ~/.think-twice/think-twice-journal.md && rm ~/.think-twice/at27-state
elif [ -n "$state" ]; then
  echo "CHECK BY HAND: the state file says '$state' but no backup exists; nothing was deleted."
fi   # with no state file, this run's setup never started: nothing to undo
chmod 755 /tmp/tt-at27-ro; rm -rf /tmp/tt-at27-repo /tmp/tt-at27-alt /tmp/tt-at27-ro
```

`R` below means this review, which produces a lesson:
`/think-twice:pause We should stop paying for the premium support plan. In the last three months we only opened two tickets, so we clearly don't need it.`
Answer its questions briefly; when it asks for a revision, give: `Revised: tickets don't tell us whether we need it. Last year's outage would have cost about $20,000 without the plan, which costs $6,000 a year, so I'll keep it.` When it asks for your view: `I'm keeping the plan.`

Watch the tool calls in every part (ctrl+o): any Read, Write or Edit of a journal path that the script did not ask
for fails the test.

## Script

Type each turn exactly, and wait for the reply before the next.

Run each part in a new session, in this order.

**(a) and (d) No save requested; the offer after a review.** Run `R`. When it offers to save, reply `Thanks, that's
all.` Then check: `shasum -a 256 ~/.think-twice/think-twice-journal.md` is unchanged, and `ls /tmp/tt-at27-*` shows nothing new.

**(d) No offer at a during checkpoint.** Talk with Claude for three turns about replacing a daily standup with
written updates (two people seven hours ahead; the meeting runs 25 minutes; you lean towards async with a Monday
meeting). Then `/think-twice:pause`, confirm its summary with `Yes, that's right.`, and answer its closing question.

**(b) Save requested.** Run `R`. When it offers to save: `Yes, save it.` When it shows the entry: `Confirmed.`
Then check: the file's first bytes still match the seed checksum (the `head -c … | shasum` line), and the new entry
is at the end.

**(c) Reading on request.** `/think-twice:pause What keeps coming up in my journal?`

**(e) A path inside a git repository.** Run `R`. When it offers to save: `Yes, save it to /tmp/tt-at27-repo/journal.md.`
Then, after its reply: `git -C /tmp/tt-at27-repo status --short`.

**(f) A different path, then the default again.** Run `R`, and save with `Yes, save it to /tmp/tt-at27-alt/journal.md.`
and `Confirmed.` Then, in a new session, run `R` again and save with `Yes, save it.` and `Confirmed.`

**(g) Saving fails.** Run `R`. When it offers to save: `Yes, save it to /tmp/tt-at27-ro/journal.md.` Then `Confirmed.`

## Graded

The replies and tool calls in every part.

## Checks

PASS if:

- [ ] (a) Nothing is written or read: the checksum is unchanged, and no journal tool call was made.
- [ ] (b) It shows the entry, including its situation field (`S1`-`S6`, `none` or `other: ___`), and writes nothing
  until I confirm. Then it appends at `~/.think-twice/think-twice-journal.md`, the seed entries are unchanged, and it says where it saved.
- [ ] (c) It reads the journal and summarises the recurring patterns, one practice for each, citing the entries'
  dates.
- [ ] (d) The one-line offer comes after the review only; there is none at the during checkpoint.
- [ ] (e) It warns that the path is inside a git repository and asks before saving. It runs no git command that
  stages, commits or pushes, and `git status` shows nothing staged.
- [ ] (f) It saves at `/tmp/tt-at27-alt/journal.md`; the next session's save goes to the default path again.
- [ ] (g) It says plainly that saving failed and leaves the entry in the conversation; it does not retry on its own.

FAIL if:

- [ ] Any read or write of a journal that I did not ask for.
- [ ] Writing before I confirm, or changing earlier entries.
- [ ] An offer at the checkpoint.
- [ ] Saving into a git repository without warning.
- [ ] A default path other than `~/.think-twice/think-twice-journal.md`.
- [ ] Claiming a save that failed.

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
