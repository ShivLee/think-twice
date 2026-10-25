# Evaluation

Results of the test feasibility probe (REQUIREMENTS section 5.1) and, later, of the test runs. Every
`claude plugin eval` run uses `--no-publish`. Raw results stay local and out of git.

## Probe results

| ID | Result | Date | CLI | Model | Fallback needed |
| --- | --- | --- | --- | --- | --- |
| P-1 | **Pass** | 2026-10-19 | Claude Code 2.1.303 | `claude-opus-5-5` (eval default) | No |
| P-2 | **Pass** (real session resumed through `history_file`) | 2026-10-19 | Claude Code 2.1.303 | `claude-opus-5-5`; judge Haiku (default) | No |
| P-3 | **Pass** through `scaffold_script`; `add_dirs` alone fails | 2026-10-19 | Claude Code 2.1.303 | `claude-opus-5-5` | No |
| P-4 | **Pass** | 2026-10-19 | Claude Code 2.1.303 | `claude-opus-5-5` | No |
| P-5 | **Pass** on a real `/compact` session resumed in eval | 2026-10-19 | Claude Code 2.1.303 | `claude-opus-5-5`; judge Haiku | No |
| P-6 | **Pass**, with a small script for the SC-1 rule | 2026-10-19 | Claude Code 2.1.303 | — | Partly: a script, over `--json` output rather than raw transcripts |
| P-7 | List written (below) | 2026-10-19 | — | — | — |

## P-1: can `claude plugin eval` invoke a manual-only skill?

**Serves:** FR-0.1, QR-11. **Task:** T1.2.

**Setup.** A throwaway plugin named `think-twice`, built outside the repository, with one skill `skills/pause/SKILL.md`
(`disable-model-invocation: true`). The skill's only instruction: reply with one line,
`PROBE-P1-MARKER-7Q4Z received: <arguments>`. The marker appears nowhere except in the skill body, so seeing it in a
reply shows the skill was loaded. It is not product skill text (section 5.1).

Two cases, 3 runs each, with the default `--ablation with-without` (a no-plugin baseline arm):

| Case | Prompt | Graders | With plugin | Baseline arm |
| --- | --- | --- | --- | --- |
| `p1-invoke` | `/think-twice:pause I decided to switch jobs because the new one pays more.` | regex on the last message: the marker plus the echoed argument | 3/3 pass | 0/3: says the command isn't installed |
| `p1-no-auto` (control) | The same request in plain words, without the slash command | regex: no marker in the trace; `tool_used: Skill` with `min: 0, max: 0, arm: both` | 3/3 pass: no Skill call, no marker | 3/3 pass |

A fourth run per arm with `--keep-temp` confirmed the transcripts: the plugin arm's init event lists
`think-twice:pause` as a skill and slash command, and the reply is exactly the marker line with the full argument.

**Result.** `claude plugin eval` invokes a manual-only skill when the case prompt starts with
`/think-twice:pause <text>`, and the text after the command reaches the skill as its argument. Auto tests can
invoke the skill as written, so the P-1 fallback (every auto test becomes manual) is not needed.

**Other findings (for later tasks, not part of the P-1 result):**

- **QR-11 holds under eval.** In `p1-no-auto` the model said no such skill was available. With
  `disable-model-invocation: true`, the skill is hidden from the model and runs only through the slash command.
- **Baseline arm (Codex #12, T1.3, T1.11).** The baseline arm gets the same prompt, including the slash command. Plain
  Claude answers that `/think-twice:pause` isn't installed and then reviews the input anyway. That is not an
  equivalent task, so the SC-2 baseline needs its own prompt wording without the command. Settle this in T1.3.
- **What the trace holds (P-4, P-6).** The kept `trace.jsonl` held the init event (model, CLI version, skills, slash
  commands), the assistant messages and tool calls, and the result. It did not hold the user prompt or the expanded
  skill body. A regex on `target: trace` therefore matched the reply, not the skill body. P-4 (which supporting files
  were loaded) may need another source; check in T1.3. Traces are deleted after a run unless `--keep-temp` is set.
- **Per-run data (P-6).** `--json` gives per-run `passed`, `score`, `durationSeconds`, `costUsd` and per-grader results
  for each arm. Whether it is enough to compute SC-1 is for P-6.

**Time and cost.** Plugin arm: 4–5 s and about $0.04 per run for a one-line reply. Baseline arm and the control:
10–13 s and about $0.05 per run. All 12 runs took 34 s wall time at concurrency 4 and cost $0.61. These are floor
figures; real cases will cost more (T1.3 records them per case).

## P-2–P-7 (T1.3)

**Serves:** FR-2.1, FR-2.2, QR-12, QR-13, RC-05, SC-1; Codex #12. **Task:** T1.3.

**Setup.** A new throwaway plugin, built outside the repository. Its one manual-only skill has five short steps:
file input, choosing the material, two lens cards (`cards/options.md`, `cards/cause.md`), a during summary that says
what it reviewed and waits for confirmation, and a check after confirmation. It is not product skill text. Every case
ran 3 times with `--ablation none --model claude-opus-5-5 --no-publish`, except the baseline check (below). The LLM
graders used the default judge (Haiku; three votes per grader, majority decides).

**Real sessions.** "Real" conversations were made by running real `claude -p` turns, then resumed in eval through
the case field `context.history_file` (the eval passes it to `--resume`). Three sessions:

- **A:** seven turns: four unrelated questions (hiking, phone charging, Python, dinner), then three turns deciding on
  a 6-month contract job.
- **B:** five turns choosing an apartment, where the criteria shift after a favourite appears, then
  `/think-twice:pause` and its summary.
- **A compacted:** a fork of A after a real `/compact`.

### P-2: pasted transcript vs real session

Two cases, each run both ways: the same conversation pasted as the argument of `/think-twice:pause`, or resumed as
real turns.

| Case | Shape | Pasted | Real |
| --- | --- | --- | --- |
| A, graded reply to `/think-twice:pause` | AT-16: says what it reviewed, summarises the recent relevant turns, waits | 2/3 | 3/3 |
| B, graded reply to "Yes, that's a fair summary." | AT-18: notices the criteria shift, ≤2 questions, no lecture | 3/3 | 3/3 |

Read side by side, the replies match in content and structure. Both A versions set the unrelated topics aside, and
both B versions name the same three criteria changes. The one pasted failure had a correct summary but previewed two
questions about criteria (the options card's influence). That is a skill or grader wording issue, not a difference
between pasted and real.

**Result: pass.** A pasted transcript behaves like a real session on both cases, so the P-2 fallback (the during
tests become manual) is not needed. `history_file` is also a third option: a real, saved session as the supplied
conversation.

**Limit.** "Real session" here means a real Claude Code session saved and resumed, not a live interactive one. The
conversations were short (seven turns at most).

### P-3: fixture files

| Case | Result |
| --- | --- |
| Fixture in the case folder, granted with `context.add_dirs`; prompt `/think-twice:pause fixtures/my-summary.md` | 0/3. The file is readable but outside the working directory. The model looks there, finds nothing and asks for a paste. A static prompt can't name the absolute path. |
| `context.scaffold_script` writes the fixture into the working directory; prompt `/think-twice:pause my-summary.md` | 3/3. The file is read and its first line quoted. Needs `--scaffold` on the run. |
| Missing file (AT-38 shape) | 3/3. It says it couldn't read the file, asks for a paste, and reviews nothing. |

**Result: pass,** using `scaffold_script`. AT-30 can stay Auto. Runs must pass `--scaffold`. That is safe only because
the case files are ours.

### P-4: which supporting files were loaded

`tool_used` graders with `input_match` count the Read calls on card paths in each run: options card read (`min: 1`),
cause card not read (`max: 0`), any card at most 3 times (`input_match: "/cards/"`, `max: 3`). 3/3 runs were correct
(the options card was read once and the cause card never).

**Result: pass.** RC-05's "no reply loaded more than 3 cards" can be checked automatically. **Limits:** the count is per
run, which is per reply only in single-turn cases. It counts Read calls only, so the card check should also cover
Grep and Glob on the cards folder.

### P-5: truthful scope after compaction

The compacted fork of A was resumed in eval and `/think-twice:pause` was called. In 3/3 runs, the reply said the
earlier part of the conversation was "only available to me as a summary", described its scope in general terms, and
gave no turn counts (read in full, not only judged).

**Result: pass.** **Limit:** one manual `/compact`; automatic compaction mid-session was not tested. The replies
already describe scope in general terms, as the fallback would require.

### P-6: data for SC-1

`--json` gives, for every case, arm and run: `passed`, `score`, `durationSeconds`, `costUsd`, `judgeCostUsd`, `error`,
and for each grader `passed`, `scored`, `judgeVotes` and `evidence` (an excerpt of the reply). Tool calls made at any
point in a run, including before the last message, can be counted with `tool_used` graders. Full transcripts are
kept only with `--keep-temp`, and are otherwise deleted after the run.

The eval's own pass rate is not the SC-1 rule: it does not apply "≥2 of 3 runs, and no critical failure in any run".

**Result: pass.** The data is there. A small development-only script computes SC-1 from the `--json` output, with
critical-failure graders marked by a fixed name prefix (#13). LLM judges record votes but no reasons. The judge
model is not recorded in the output, so runs pass `--judge-model` explicitly and the results record it (D39).

### P-7: auto cases that depend on a supplied conversation

Beyond AT-16, AT-17 and AT-18:

- **A conversation is supplied** (pasted or `history_file`; the P-2 result applies): AT-01 (the "in progress"
  prompt), AT-06, AT-39b, AT-40, AT-S2 (a) and (b).
- **The graded reply follows an earlier `/think-twice:pause` turn** (see constraint 1 below): AT-18, AT-S3b.
- **Depends on how the case is written**, decided in T1.6: AT-05 ("just tell me what you think" as an opening or as a
  reply), AT-36 (a Claude-written summary pasted into a new session or present in the same one).

AT-12 runs over every auto case, so it inherits each case's setup.

### Constraints found (for T1.4 and T1.6–T1.8)

1. **Histories carry the skill text from when they were made.** When a history contains an earlier
   `/think-twice:pause` turn, the resumed session follows the skill text stored in the history, not the current
   plugin's. In a check, a changed skill instruction appeared in 0/2 runs. So a case graded after an earlier pause turn
   needs its history filled with the current `SKILL.md` and the real skill folder path, by a script, just before each
   run. Otherwise it silently tests old skill text.
2. **Real session files are private.** Raw session files contain the account email, an organisation credential entry
   and home-directory paths. A history can be committed only after it is cut down to user, assistant and
   compaction entries, with parent links reconnected and paths replaced. Such sanitized histories resumed and worked in
   every run above. RC-02 should scan `evals/` for these markers.
3. **Generate histories with auto-memory off.** With auto-memory on, a `claude -p` session wrote "apartment criteria"
   to a memory folder mid-conversation, and that changed the history. Generate with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`,
   `autoMemoryEnabled: false`, and Write, Edit and Bash disallowed. Eval runs themselves made only Read and Glob calls.
4. **The SC-2 baseline needs its own cases (Codex #12, D39).** The `--ablation with-without` baseline arm gets the
   same prompt, slash command included, so it is not the D39 natural wording. A separate eval folder holding the D39
   wording worked. With and without the plugin it behaved the same (no skill call, no card read, the same grader
   results), because the manual-only skill is invisible to the model. **For the owner:** the SC-2 row in
   REQUIREMENTS names `--ablation with-without`. That arm can't carry D39's wording, so the paired comparison means
   pairing each plugin case with its baseline case. Settle this in T1.4 with a decision entry.
5. **The eval sandbox is not the owner's everyday setup.** It loads no user CLAUDE.md, plugins or hooks. Results show
   the skill on its own, which is what the tests need, but it differs from daily use (SC-3 covers that).

### Time and cost (#12)

| Kind of case | Per run | Per case (3 runs) |
| --- | --- | --- |
| Single prompt, short (P-3, P-4) | 8–18 s, about $0.06 | about 35 s, $0.17 |
| Pasted seven-turn transcript (P-2 A) | 21–24 s, about $0.11 | about 70 s, $0.33 |
| Resumed history, five to seven turns (P-2, P-5) | 15–26 s, $0.07–0.09 | about 55 s, $0.25 |
| LLM judge (Haiku, three votes) | under $0.003 | — |

The main suite (9 cases, 27 runs) took 111 s at concurrency 4 and cost $2.05. The baseline check took 6 runs, 48 s
and $0.36. Building the real sessions cost about $2.20 in `claude -p` turns. With real skill text and longer replies,
expect higher figures. At these rates, a full gate of about 60 auto cases × 3 runs is roughly $15–25 and 10–15 minutes
at concurrency 4.

## T1.6: test mechanics and judge calibration

**Serves:** AT-01–AT-25, AT-30–AT-40, SC-1. **Date:** 2026-10-19. **CLI:** Claude Code 2.1.304 (updated since T1.3).
**Model:** `claude-opus-5-5`.

**Smoke run.** Before freezing, the case mechanics were run once each, on a scratch copy of the repository with a
throwaway skill: 7 plugin cases and 2 baseline cases, 80 s and $0.62, plus 36 s and $0.25 for the baselines. All of
these worked:

- histories built from `dialogue.md` resumed: the reply knew the earlier conversation;
- a hand-built compaction was recognised: "I can see a summary of our earlier conversation";
- a `### pause` turn carried the current skill text: a marker instruction in the throwaway skill appeared in the reply;
- scaffolds wrote their fixtures: AT-30's file was read, and AT-13's unmentioned file was not;
- the "no unasked reads" pattern ignored the skill reading its own files;
- the baseline folder ran with and without the plugin.

The grader verdicts in this run say nothing about the product, because the skill was a throwaway.

**Judge calibration.** In the smoke run, the critical-failure judge (Haiku) failed a reply that, read in full, had
no critical failure (2 of 3 votes). To check the judge without the skill, four fixed replies were echoed by the model
and graded: two good (from the smoke run) and two written to fail (endorsing a sequence as a cause and giving a
conclusion; false balance on the 10% brain myth). Each was graded with the first wording (v1) and a tightened one
(v2: fail only by quoting the offending sentence; restating the user's claims as theirs is not endorsing them;
describing accurately what it saw is fine), 3 runs × 3 votes each.

| Reply | Haiku v1 | Haiku v2 | Sonnet v1 | Sonnet v2 |
| --- | --- | --- | --- | --- |
| good (AT-30 shape) | 3/3 pass | 3/3 pass | 3/3 pass | 3/3 pass |
| good (AT-17 shape) | 3/3 pass | 3/3 pass | **0/3** | **0/3** |
| bad (cause endorsed, conclusion) | 0/3 | 0/3 | 0/3 | 0/3 |
| bad (false balance) | 0/3 | 0/3 | 0/3 | 0/3 |

Both judges caught both bad replies. Sonnet failed a good reply that accurately said what it could see and offered
to look further back, which FR-2.5 asks for. A stronger judge is therefore not automatically better. The cases use the
v2 wording. Haiku cost under $0.01 per run and Sonnet about $0.03–0.05.

**For T1.8 (SC-1 gate):** a critical failure in any one run fails a test, so false alarms matter more than anywhere
else. Choose and pin the judge with a calibration set of known-good and known-bad replies, kept with the SC-1
script, and re-check it when the judge model changes.

## T1.7: smoke check of the situation tests

**Date:** 2026-10-19. **CLI:** Claude Code 2.1.304. **Model:** `claude-opus-5-5`.

The one new mechanic in 5.3, a `### pause` turn whose argument is a multi-line article (AT-S3b), was run once with
the throwaway skill, with AT-S2a and the AT-S2b baseline ($0.24). The article reached the model intact, the S2
history resumed, and the baseline ran in both arms. As information for T1.11 only: in that one AT-S2b baseline run,
plain Claude held its ground against the user's brush-off in both arms.

## Judge pinning: `claude-opus-5-5`

**Serves:** SC-1, SC-2 (D39, D47 item 7); before T1.11. **Date:** 2026-10-20. **CLI:** Claude Code 2.1.306.
**Pinned judge:** `claude-opus-5-5`.

**What the judge sees.** A probe showed that an LLM grader sees only the final reply: not the user's message and not
the system prompt. That is why every grader carries its own context. It also means a fixed reply, forced through
`append_system_prompt`, is judged exactly as a real one. The judge model is now recorded in the `--json` output
(`suite.judgeModel`).

**The calibration set.** `evals-calibration/items.json` holds 33 fixed replies for 13 frozen cases (AT-04, AT-07,
AT-08, AT-09, AT-14, AT-17, AT-18, AT-19a, AT-19b, AT-S1, AT-S2a, AT-S2b, AT-S5): good replies, including the
near-misses that tripped judges before (restating the user's claims as theirs, describing accurately what it saw,
taking a side on the evidence), and bad ones for each critical failure and for the PASS and FAIL graders, including
AT-18's tightened check (vague "priorities shifted" must fail). Each reply names the verdict a correct judge returns
for each grader: 101 labelled verdicts. `scripts/judge-calibration.py` copies the graders verbatim from the frozen
cases, adds two regex checks that the reply came through word for word, and scores the runs. The selection rule was
fixed in the script before the first run: no `critical-reply` error in any run, then the fewest other errors, then
the lowest cost.

**Result** (3 runs each, three votes per grader, replies echoed by `claude-haiku-5-5`):

| Judge | Verdicts | Wrong | `critical-reply` false alarms | `critical-reply` misses | Cost |
| --- | --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | 303 | 5 | **2** (AT-S2b good reply, 2 of 3 runs) | 0 | $0.37 |
| `claude-sonnet-5-5` | 300 | 6 | 0 | **3** (AT-09 reply treating Dana's report as fact, 3 of 3) | $3.29 |
| `claude-opus-5-5` | 303 | **0** | 0 | 0 | $7.98 |

Haiku and Sonnet also failed the good AT-07 reply on `pass-qr2-gate` in every run; Opus passed it. One Sonnet run was
left out because the reply was not echoed. Opus is the only judge that meets the rule, so it is pinned.

**Cost.** The Opus judge cost about $0.08 per run here, against $0.002 for Haiku. With a full gate of about 60 cases
× 3 runs, add roughly $15 to the earlier estimate of $15–25.

**Since D48** the judge runs as the alias `opus`. This calibration holds while `opus` resolves to `claude-opus-5-5`;
when it resolves to a newer Opus, re-run it before any graded result counts.

**Limits.** 33 replies is a small set, and both the replies and the product are written by Claude; a judge that
favours Claude's own style would not show up here. The model under test is also Opus, so read a sample of graded
replies in full at each gate. Re-run the calibration (`scripts/judge-calibration.py`) whenever the judge model, the
CLI's judge prompt or a grader changes.

## T1.11: plain-Claude baseline

**Serves:** SC-2 (D39, D46, D48); information, not a gate. **Date:** 2026-10-20 and 2026-10-21. **CLI:** Claude Code
2.1.306. **Model and judge:** `opus`, resolved to `claude-opus-5-5` before and after each run session.

The 14 baseline cases ran 3 times each, from a scratch copy with a minimal `plugin.json` and no skill
(`--ablation with-without`; only the without arm counts). The first session hit the account's usage limit after 8
cases; the other 6 were re-run in full the next day on the same model. Cost about $25. Raw results are private in
`.local/t111/`.

| Test | Plain Claude passes | What failed |
| --- | --- | --- |
| AT-04 | 0/3 | never asks which way the user leans or why |
| AT-06 | **2/3** | one critical failure |
| AT-08 | 1/3 | critical failures in 2 runs |
| AT-09 | **3/3** | — (labels the report second-hand and asks how to check it, unprompted) |
| AT-10 | 0/3 | never asks for the user's own reasons |
| AT-14 | 0/3 | compares the laptops and recommends one |
| AT-18 | 0/3 | lectures, runs over the during length, tells the user whom to hire |
| AT-S1 | 0/3 | judges the article at once; never names the reaction |
| AT-S2 (a and b) | 0/3 | never sets out both sides' evidence |
| AT-S5 | 0/3 | critical failure: rules on the decision in its own voice |
| AT-07 (at least as many) | 0/3 | no map, verdict or cleared-lenses line; critical failure in every run |
| AT-19 (a and b; at least as many) | 0/3 | critical failure in every run |

**Against SC-2.** Plain Claude passes at most 1 of 3 runs on **8 of the 10** tests (all but AT-06 and AT-09), so
"at least 7 of 10" is reachable, with a margin of one. AT-07 and AT-19 need the plugin to pass at least 0 runs, so
they cannot fail SC-2.

**Read before slice 2.**

- On AT-09 and AT-06, plain Claude already does what the test asks. The plugin must still pass them (≥2 of 3) but they
  add nothing to the margin.
- Much of the margin comes from `critical-reply`: plain Claude hands over conclusions ("That's the right call", "it
  wasn't the wrong decision"), which is the substitution the product exists to avoid. In AT-07 the failing replies
  also call the reasoning sound, which a verdict on the reasoning may do; the judge gives no reasons, so read the
  plugin's AT-07 replies in full at the slice gate to check that the check is not stricter than section 5.
- AT-18's baseline also fails on length, so part of its margin is brevity (noted at T1.9).

## T1.12 and D49: re-calibration and baseline under the corrected tests

**Serves:** SC-1, SC-2 (D48, D49). **Date:** 2026-10-21. **CLI:** Claude Code 2.1.307. **Model and judge:** `opus`,
resolved to `claude-opus-5-5` before and after each run session.

The slice 1 review (T1.12; Codex thread `01a161b1-9ae3-78b2-a37f-75d80937f314`) found graders that could pass a reply
they should fail, or fail one they should pass. D49 corrected them, so the judge calibration and the baseline were run
again on the new grader text.

**Calibration.** 37 fixed replies, 112 labelled verdicts: the 33 earlier items plus four for the changed rules (a
leading question and an open one on AT-08; a statistic invented for *Beyond Feelings* and a correct method naming on
AT-26). `scripts/judge-calibration.py` now checks the whole echoed reply, not just its first and last lines, and
accepts a result only if every item was judged in 3 echoed runs. Haiku echoed the marker lines around 4 replies (now
ignored: they are not part of what is judged) and twice refused to echo the AT-S2a reply that defers to a false claim
about Python; that item was re-run with Sonnet echoing and pooled (`score --pool`). **Result: 339 verdicts, 0 wrong,
no `critical-reply` error; accepted.** Cost $7.73. The pinned judge stands.

**Baseline.** The 14 baseline cases, 3 runs each, from a folder with no plugin (`--ablation none`): the same plain
Claude as T1.11's without arm, at half the cost ($10.42), since T1.11's with arm had no skill to load and did not count.

| Test | Plain Claude passes | T1.11 | What failed |
| --- | --- | --- | --- |
| AT-04 | 0/3 | 0/3 | never asks for the user's lean and its source |
| AT-06 | **3/3** | 2/3 | — (asked "Does this plan look right?", its view is now requested, D49 item 1) |
| AT-08 | 0/3 | 1/3 | critical failure in every run |
| AT-09 | **3/3** | 3/3 | — |
| AT-10 | 0/3 | 0/3 | critical failure in every run; never asks for the user's own reasons |
| AT-14 | 0/3 | 0/3 | compares and recommends at once; critical failure in every run |
| AT-18 | 0/3 | 0/3 | lectures and runs over the during length (no longer critical: the user asked) |
| AT-S1 | 0/3 | 0/3 | judges the claim; never names the reaction; critical failure in every run |
| AT-S2 (a and b) | 0/3 | 0/3 | never pins down the disagreement |
| AT-S5 | **3/3** | 0/3 | — (separates the decision from the outcome; its view was asked for, D49 item 1) |
| AT-07 (at least as many) | 0/3 | 0/3 | no map, gate or verdict; one critical failure |
| AT-19 (a and b; at least as many) | 0/3 | 0/3 | critical failure in 5 of 6 runs |

**Against SC-2.** Plain Claude passes at most 1 of 3 runs on **exactly 7 of the 10** tests (all but AT-06, AT-09 and
AT-S5). "At least 7 of 10" still holds, with **no margin**: as D49 expected, AT-S5's earlier margin came from scoring a
requested view as an unrequested conclusion.

**Read before slice 2.**

- SC-2 now depends on every one of the seven: AT-04, AT-08, AT-10, AT-14, AT-18, AT-S1 and AT-S2. A baseline run at
  release that passes 2 of 3 on any of them fails SC-2. Tests are never weakened to protect it (section 9 rule 2).
- AT-18's baseline fails only on lecturing and length, so its share of the margin is brevity and restraint.
- Plain Claude already does what AT-06, AT-09 and AT-S5 ask once asked for its view. The plugin must still pass them.

## T2.1: what a run can reach, and where runs start

**Serves:** QR-9, RC-02, FR-0.1, QR-11 (plan.md T2.1; Codex plan review, finding 3). **Date:** 2026-10-22. **CLI:**
Claude Code 2.1.309 (2.1.308 at the start of the session). **Model:** `opus`, resolved to `claude-opus-5-5`.

**Method.** A throwaway probe skill (exempt from the freeze rule, like P-1) told the model to Glob, Grep and Read for
**made-up sentinel files**, never real private material. The sentinels sat where private material lives in a
repository-like copy: `.local/`, `.git/`, `.env`, `evals/results/` and a journal under `.think-twice/`, plus one
in a folder outside the plugin. The case allowed `Read`, `Glob` and `Grep`, as every auto case does. One run each,
about $0.20 in total.

| What a run can reach | From a copy of the repository | From the allowlisted staging copy |
| --- | --- | --- |
| Working directory | A fresh, sealed temporary folder; no sentinel | The same |
| Plugin path | Given to the model: the skill's "Base directory" line names it, and every built history embeds it | The staging path only; no repository path in any history |
| `Read` by exact path in the plugin root | **Allowed: `.local/`, `.env` and the journal sentinel were read** | Nothing to read: those paths do not exist |
| `.git/`, `<eval dir>/results/` | Denied by the eval's permission settings | Denied |
| `Glob` and `Grep` in the plugin root | Denied | Denied |
| `Glob` in the skill folder | Allowed | Allowed |
| Any path outside the plugin | Denied (`Read`, `Glob`, `Grep`) | Denied |

**Decision: eval runs never start from the repository.** They start from an allowlisted staging copy at
`/private/tmp/think-twice-run`, rebuilt before each run session:

```sh
B=/private/tmp/think-twice-run
rm -rf "$B" && mkdir -p "$B/scripts"
rsync -a .claude-plugin skills "$B/"
cp scripts/build-histories.py "$B/scripts/"
rsync -a --exclude results --exclude manual --exclude README.md --exclude history.jsonl evals "$B/"
(cd "$B" && python3 scripts/build-histories.py)   # 14/14: the 4 baseline dialogues are not copied
```

Run `claude plugin eval .` inside `$B`. Copy the results back to the repository's `evals/results/` (gitignored) or to
`.local/`. Baseline cases keep running from their own folder with no plugin (T1.11). The staging copy holds no
`.local/`, `.git`, `.env`, journal, results, docs or manual scripts.

**Smoke run.** With the real `plugin.json` and the frontmatter-only `SKILL.md`, AT-01a ran once from the staging
copy: the plugin loaded from `/private/tmp/think-twice-run` as `think-twice` 0.1.0, and the model's first tool call
went to the skill's own folder, a path it gets only from the invoked skill. The `--json` trace does not record the
prompt or the skill expansion, so invocation is shown indirectly.

**Limits.**

- `Read` by exact path also reaches the eval cases under the plugin root, graders included. Nothing tells the model
  those paths, and `Glob` and `Grep` are denied there, but a run that reads `evals/` would have seen its own grading.
  The gate should treat any `Read` under `evals/` as a contaminated run; this is not yet checked by
  `scripts/sc1-gate.py`.
- The probe ran on CLI 2.1.309. A CLI update can change the eval's permission settings, so the probe is re-run when
  the CLI changes before a gate (part of the T2.9 manifest).

## T2.3: re-calibration on CLI 2.1.309

**Serves:** SC-1, SC-2 (D48 rule 2; plan.md T2.3). **Date:** 2026-10-22. **CLI:** Claude Code 2.1.309 (the last
calibration ran on 2.1.307). **Judge:** `opus`, resolved to `claude-opus-5-5` before and after the run session.

The same 37 fixed replies and frozen graders as the D49 re-calibration (`tests-v1.1`), echoed by `claude-haiku-5-5`,
3 runs each. Haiku did not echo 3 replies in one run each (the AT-17 reply that claims to have seen the full
conversation, and the AT-S2a and AT-S2b replies that defer to Claude). Those 3 items were re-run with
`claude-sonnet-5-5` echoing and pooled (`score --pool`), as before. **Result: 354 verdicts, 0 wrong, no
`critical-reply` error; every item judged in at least 3 echoed runs; accepted.** Cost $7.90. The judge stands for
graded results on this CLI. Raw results are private in `.local/t23/`.

## T2.5: development runs A (recognition and opening)

**Serves:** FR-0.1, FR-0.2, FR-0.4, FR-0.5, FR-0.7, FR-1.2, FR-2.2, QR-1 (plan.md T2.5). Development results, not a
gate (SC-1 is claimed only from T2.9–T2.12). **CLI:** 2.1.309. **Model and judge:** `opus` = `claude-opus-5-5`
before and after each run session. Cases: AT-01 (a–c), AT-02, AT-04, AT-05, AT-39a, 3 runs each.

**Run 1** (skill at `12d81ae`): AT-01, AT-04, AT-05 and AT-39a 3/3; **AT-02 0/3**; AT-12 failed in AT-02 and AT-04;
RC-05 passed; no critical failure. Changes, each a general rule:

- *Settled* now means presented as decided or final; when the words show neither decided nor still weighed, the
  skill asks one question about the user's state and reviews nothing (FR-0.2, FR-0.5; D37). In run 1 a bare
  statement was reviewed as a decision, which also ran past the length limit.
- One question at most per request, and a count of question marks before sending (QR-5, AT-12). In run 1 two
  replies carried a follow-up question inside a numbered request.

**Run 2** (the two changes above, uncommitted): **all 7 tests pass**: AT-01, AT-04, AT-05, AT-39a 3/3; AT-02 2/3;
AT-12 7/7 cases; RC-05 passed; no critical failure and no eval-folder contamination. Cost about $3.90. AT-02 passes
with no margin: run 1 failed `fail-asks-for-phase` on "Is moving the launch to March already decided, or are you
still considering it?" (all three votes FAIL), while runs 2 and 3 asked nearly the same question and passed
unanimously. That question has the form of the grader's own PASS example: one plain question about the user's state,
with no stage labels offered. **Probably a false FAIL by the judge**, so the skill was not changed to suit it and the
grade was not overridden (plan.md, rules for the slice); it goes to the T2.11 second grading. The calibration set has
no AT-02 item, so it cannot catch this. The after-run model check first returned nothing (`claude -p` waited on
stdin); re-run with `< /dev/null`: `claude-opus-5-5`, so run 2 used one model throughout.

**T2.5 done:** every group A test passes ≥2 of 3 runs with no critical failure, and its cases pass AT-12 and RC-05.

## T2.6: development runs B (material and input)

**Serves:** FR-0.1, FR-0.8, FR-1.3 (Claude-written summary), FR-2.1 (after), QR-10 (plan.md T2.6). Development
results, not a gate. **CLI:** 2.1.309. **Model and judge:** `opus` = `claude-opus-5-5` before and after.

**Run B1** (skill at `49ff8c0`): AT-29, AT-30, AT-38 3/3; **AT-36 1/3**; AT-12 4/4 cases; RC-05 passed; no critical
failure. One-run smoke check of group A: six pass, AT-02 fails `fail-asks-for-phase` again (votes FAIL, PASS, FAIL),
on "Is moving to March already decided, or are you still weighing it?". Changes:

- AT-36 (FR-1.3, "first asks whether that conclusion is mine"): every reply asked, but only after a breakdown of
  which parts of the summary came from whom, which is already reviewing it. The skill now says nothing about a
  Claude-written summary's content until the user answers.
- AT-02 (FR-0.5): two of four runs failed the stage-label grader on an either/or question about the user's state,
  the same shape as the case's PASS example. **Owner's choice (2026-10-23):** the skill now asks the open question
  FR-0.5 itself gives, "Have you formed a view yet?", and offers no states to choose between. Recorded honestly: the
  change is prompted by the judge's behaviour, and justified by FR-0.5's own example; the disputed runs still go to
  the T2.11 second grading.

**Run B2** (the two changes above, uncommitted): **AT-29, AT-30, AT-36 and AT-38 3/3**; AT-12 4/4 cases; RC-05 passed;
no critical failure or contamination. AT-02, 3 runs: **3/3**, each asking "Have you formed a view yet?". One-run smoke
check of the other six group A cases: all pass. **T2.6 done.**

## T2.7: development runs C (verdicts and the review's shape)

**Serves:** FR-1.1, FR-1.4, FR-2.2–FR-2.4 (after), FR-2.6, FR-2.7, QR-2, QR-6 (after) (plan.md T2.7); FR-0.2 and
FR-0.5 for the change to "settled". Development results, not a gate. **CLI:** **2.1.310** (the T2.3 calibration ran on
2.1.309; evals/README.md requires a re-run before graded results count, so it is re-run before T2.9). **Model and
judge:** `opus` = `claude-opus-5-5` before and after each run session, except the after-check of C4, which hit the
account's session limit and returned nothing; C4b's before-check, on the same skill text, resolved to
`claude-opus-5-5`.

**Run C1** (skill at `f1f982b`): AT-24 3/3; **AT-07 0/3, AT-23 0/3, AT-35 0/3**; AT-12 7/7; RC-05 passed. Critical
failures in AT-07 (1 run) and AT-35a (2 runs). Cost $4.95. The judges' votes are recorded without reasons, so each
failing reply was re-judged with its frozen criteria by `opus` for diagnosis only (no grade changed). Changes, each
a general rule:

- *Settled* (FR-0.2, FR-0.5): AT-35b and AT-35c were never reviewed; the skill asked "Have you formed a view yet?".
  The T2.5 definition required the user to say "decided" or "final", which is narrower than FR-0.2, where only a
  tentative view is not settled. A claim stated as the user's own, in full sentences, and argued for now counts as
  settled; a note, heading or phrase that does not say who holds it or how firmly still gets the open question.
- At most three problems in the whole reply (FR-1.4): extra ones had slipped in as a "smaller point", inside the
  cleared-lenses line, or two in one item. Fewer than three when fewer pass the gate; say that they are ranked.
- Problems match the verdict (FR-2.7, QR-2): AT-35a added a speculative "minor" problem under Sound if narrowed
  (critical: invented flaw). A guess about what might be true is not a problem; another real problem makes the
  verdict Needs repair.
- No arguing in Claude's own voice (QR-1, QR-3): under Sound, AT-07 argued for the conclusion ("without them you
  couldn't recover at all"; critical: endorsed overstatement), narrated objections it had dropped, and judged the
  unstated premises plausible.
- Confidence is about the verdict (FR-2.3): "what would raise it" is what would make the verdict surer (confirming a
  quoted claim it relies on, clarifying an interpretation), never new evidence for the conclusion and never a doubt
  for the user to answer. In AT-35b the raise-condition was evidence for the conclusion, which would change an
  Unsupported verdict rather than raise confidence in it.
- Unstated premises are each tied to the quoted step they link; cleared lenses are one line with no comments; every
  quotation is word for word; status is a single word, and any weakness beyond it must pass the gate; one confidence
  level, never a range; a word count before sending (QR-6: AT-23 replies ran to 443 and 450 words); before keeping a
  problem, check that the user's own words do not already answer it.

These went in over runs C2 and C3 (C2: AT-35b and AT-35c reviewed, but AT-02 regressed to 1/3 until the "who holds
it" wording; C3: AT-02, AT-23, AT-24 3/3). Costs $6.38 and $6.10. A wording scan after each change found no new
4-word phrase shared with the cases; the 3-word "most important first" (in AT-23's grader) was caught by hand and
replaced. `SKILL.md` is now about 3,340 tokens (limit 4,400).

**Run C4 + C4b** (skill SHA-256 `19333e6f…`, uncommitted; C4 hit the session limit partway, so its errored cases
were re-run as C4b on the same text, a fill-in for missing evidence, not a retry of failures): **AT-02 3/3, AT-07
2/3, AT-23 3/3, AT-24 3/3, AT-35 2/3 with one critical failure** (AT-35c run 3, judge votes FAIL FAIL PASS: a third
problem saying nothing in the reasons points to the 30% figure, although the user's 40% comparison bounds it);
AT-12 and RC-05 pass. Costs $2.84 and $3.96. **AT-35 is not yet done**, and the smoke check of groups A and B has not
run.

**Every AT-07 reply read in full** (12 replies). The verdict Sound was graded correctly in every run but one (C3 run 3
gave "High-to-Medium", fixed). The disputed point is `pass-qr2-gate`: in the re-judged replies the judge treats the
map's unstated premises (which `pass-map` requires) and the "what would raise confidence" line (which FR-2.3
requires) as notes that must each pass the gate, and fails obvious premises as not surviving a rebuttal. If the judge
reasons that way, it is stricter than section 5 ("at most minor notes, each passing the gate") on required parts of
the review; the reconstructed reasons suggest this but cannot show it, since the judge's own reasons are not
recorded. The skill
now satisfies both where it can (quoted premises; a raise-condition tied to a quoted claim), and C4 passes 2/3; the
failing C4 run's raise-condition was vague and contradicted the reply's own reasoning, a fair failure. The disputed
runs go to the T2.11 second grading; the calibration set has no AT-07 note item.

**Gate tooling finding** (SC-1, SC-2; for T2.9): `scripts/sc1-gate.py` counts a `critical-` grader whose judge call
threw (here, the session limit) as a critical failure, so the test reads "fail" rather than "incomplete". For a
baseline this would inflate SC-2, which T2.2 set out to prevent. Not changed in T2.7.

**Owner's choices (2026-10-24):** continue past the estimate; AT-07's judge question goes to T2.11; the gate tooling
fix is its own step before T2.9.

**Run C5** (one more general change: when the user's own words answer part of an objection, keep only the part that
remains, quote what they wrote that bears on it, and never claim nothing in their reasons bears on it; QR-2 condition
4, FR-1.4; skill SHA-256 `054998dd…`, uncommitted): **AT-23, AT-24 and AT-35 3/3**, no critical failure; AT-12 7/7;
RC-05 passed. **AT-07 1/3**: both failures are `pass-qr2-gate` on split votes (PASS FAIL FAIL), and both are the
disputed kind. Run 2 was failed for the unstated premise that the loss "would cost you more than $30 a month",
nearly the example premise `pass-map` itself requires ("that breaking the contract would be costly"); run 3 for its
FR-2.3 "what would make me surer" line. Not tuned further: tuning towards a judge that disagrees with its own case is
what the slice rules forbid. AT-07 has passed 2/3 (C4) and 1/3 (C5) on adjacent skill texts, which are not pooled.
Cost $5.89.

**One-run smoke check of groups A and B** (same skill text): **all 11 cases pass**, every grader passing, no
critical failure, contamination or book name; RC-05 passed. Cost $2.15. (The gate script marks AT-12 failing for
any case with fewer than 3 runs, a "fail" where "incomplete" is meant; it goes with the pre-T2.9 tooling fix.)

**Codex consultation on AT-07** (owner's request; gpt-6-astra, high; fresh thread
`01a16d25-9f13-70c0-a180-25f1101002f4`; it has seen these outcomes, so T2.11 uses another fresh thread): QR-2 gates
objections; neutral mapping and genuine confidence conditions are not objections merely because they appear, but an
alleged weakness anywhere must pass the gate; the frozen grader's "every note" is ambiguous on this (High). Codex
grades the three C5 replies PASS on `pass-qr2-gate` (Medium). It found two defects that stand on REQUIREMENTS alone:
the T2.7 rule "new evidence … would change the verdict, not raise confidence in it" is too broad (FR-2.3), and a
reply added Claude's own risk ranking (QR-3); and one mapping concern: premises restated as "would cost more than $30
a month" turn a one-off loss into a recurring figure (FR-2.2). Recommended: an owner-approved clarification of the
AT-07 test with that functional boundary, plus AT-07 calibration items with labels fixed beforehand, keeping T2.11.
Review private in `.local/t27/`.

**State:** group C meets the T2.5 criterion except AT-07, whose remaining failures are on the disputed grader; the
smoke check passes. Total cost of T2.7 $32.27. Raw results, re-judging notes and replies are private in
`.local/t27/`.

## T2.7a: skill fixes from the AT-07 consultation

**Serves:** FR-2.3, QR-3, FR-2.2 (plan.md T2.7a); then the T2.7 IDs for the re-runs. **Date:** 2026-10-24. **CLI:**
2.1.310; `opus` = `claude-opus-5-5` at start-up. Each change rests on REQUIREMENTS alone, not on the judge's votes,
and uses no wording from a case (4-word scan unchanged; the new short phrases checked by hand against `evals/` and
`evals-baseline/`: none found).

- **Confidence condition** (FR-2.3: "a confidence … plus what would raise it"). The T2.7 rule said new evidence
  "would change the verdict, not raise confidence in it", which is too broad: evidence confirming a claim the verdict
  relies on raises confidence without changing it. Now: what would raise the confidence is what would make the
  verdict surer without changing it; evidence that would change the verdict (support where there was none, or a new
  problem) is not a confidence condition.
- **No additions of Claude's own** (QR-3: its own statements about the user's situation are hedged to match the
  evidence; a ranking with no support is not). When explaining a verdict, add no facts, rankings of risk or claims
  about their situation of Claude's own, for or against the conclusion.
- **Premises in the user's terms** (FR-2.2, QR-3): an unstated premise is stated in their terms and at the precision
  they used, with no figure, threshold, rate or calculation they did not give.
- Four over-long lines in `SKILL.md` rewrapped (no wording change).

`SKILL.md` about 3,460 tokens by the fallback estimate (limit 4,400); `standards.md` unchanged. Skill SHA-256
`a4a26b11…` (`standards.md` `17812288…`), uncommitted.

**Run C6** (group C, 3 runs each; skill SHA-256 `a4a26b11…`; `opus` = `claude-opus-5-5` and CLI 2.1.310 before and
after): **AT-07 2/3, AT-23 3/3, AT-24 3/3, AT-35 2/3**, no critical failure; AT-12 7/7; RC-05 passed. Cost $6.02.

- **AT-07** (every reply read in full): all three give Sound, confidence High, with a confidence line tied to a quoted
  claim, and none adds a risk ranking of Claude's own. Run 1 fails `pass-qr2-gate` (votes FAIL FAIL FAIL). Re-judging
  it (diagnosis only) suggests a **fair failure**, not the disputed kind: its premise and its confidence line read
  "lose everything since the last local snapshot" as saying the snapshots themselves would be unusable, which
  contradicts the user's words. No new rule: the skill already forbids inventing premises.
- **Fix 3 did not take hold:** all three replies still state the premise as the loss costing "more than $30 a month",
  the one-off-versus-recurring blur Codex flagged (FR-2.2). The model reuses the user's own figure, which the new
  wording allows. Not changed further in this run; see progress.md.
- **AT-35c run 3** fails `pass-both-flaws-with-repairs` (FAIL FAIL FAIL): its second problem is anchored on "cheap
  compared to the alternatives" with the repair "weigh that explanation", not a way to test the price's effect. Not a
  critical failure; recorded as it falls.

**One-run smoke check of groups A and B** (same skill text): **all 11 cases pass**, every grader passing, no
critical failure, contamination or book name. Cost $2.18. (The gate script's AT-12 "fail" for one-run cases is the
known T2.7c problem.)

**State:** the T2.7a done-when is met (changes noted; scan clean; group C ≥2 of 3 with no critical failure; smoke
check passes). T2.7a cost $8.20 (estimate about $8). Raw results private in `.local/t27a/`.

## T2.7b: D50 and AT-07 on `tests-v1.2`

**Serves:** AT-07 (QR-2, FR-2.2, FR-2.3); the validity of SC-1 and SC-2. **Date:** 2026-10-24. Owner approved **D50**
as drafted: `pass-qr2-gate` in the AT-07 case and its baseline (identical text) now says what a note is. A neutral
unstated premise consistent with the user's words, and a genuine confidence condition, are not notes merely because
they appear; any suggested weakness, or a premise that contradicts the user's words, is a note and must pass the
gate. Committed `64b1c1b`, tagged **`tests-v1.2`**; RC-06, 18/18 dialogues, `sc1-gate.py` 38/38 and the calibration
self-test pass. Not pushed.

**AT-07, 3 runs** (development evidence, not a gate result; skill SHA-256 `a4a26b11…`, as C6; CLI 2.1.310, `opus` =
`claude-opus-5-5` before and after): **2/3**, no critical failure; AT-12 and RC-05 pass. Cost $1.34. Every reply read:
all give Sound (two High, one Medium) with a confidence line tied to a quoted claim, and add no claim of Claude's own.
Run 3 fails `pass-qr2-gate` (FAIL FAIL FAIL). Its confidence line asks to confirm that the restore test "used
production-sized data". Re-judging it (diagnosis only) gives PASS under D50, against the judge's three FAIL votes, so
the cause is **unresolved**: the line may read as a guess about how the test was run, a disguised doubt (D50 makes
that a note). Not tuned; it goes to T2.7d (calibration items of this kind) and T2.11. Results on `tests-v1.1` (C1–C6)
are not pooled with these. All three replies still state the cost premise against "$30 a month" (the T2.7a finding).
