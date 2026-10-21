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
