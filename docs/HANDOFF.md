# Handoff: 2026-10-18

A snapshot of what was done in the requirements-review session, and where to pick up. **For live status, read
[progress.md](progress.md)**; it wins if the two ever disagree.

## Where things stand

The requirements are **approved as v1.0**, tagged `requirements-v1.0` and pushed to
<https://github.com/ShivLee/think-twice>. The feature discussion is closed. **Nothing is built yet**: no skill
text, no tests, no scripts. The next work is slice 1.

## Completed

### 1. Codex review of the v0.4 requirements

- Checked against three principles: goals written into files, boundaries written as rules, work in short sessions.
  Also checked goal clarity and how features map to the goal.
- Verdict: **NEEDS REVISION**, 23 findings. The product goal was clear, but there was no persistent task record,
  no goal-to-requirement mapping, and several rules conflicted.

### 2. Decisions D30–D43 (all owner-approved, in [decisions.md](decisions.md))

| # | In one line |
| --- | --- |
| D30 | "Sound if narrowed" names what to narrow; **I** write the narrower claim |
| D31 | Privacy guarantee covers only the plugin's own actions |
| D32 | SC-3 measures learning: in ≥3 of 10 real uses, I apply an earlier practice unprompted |
| D33 | No quotas: up to 3 risks (zero allowed); a lesson only when a pattern showed up |
| D34 | A first rule for when a session ends (refined by D36) |
| D35 | v0.5 clarifications: goal map, progress.md, aligned tests, reordered slices, full install test |
| D36 | How a session ends: phase output → my view → journal offer (only where allowed); "stop" ends at once |
| D37 | Phase precedence: a *settled* conclusion means after; a tentative view does not |
| D38 | Verdict meanings; confidence is in the verdict, not in the conclusion's truth |
| D39 | Fair SC-2 baseline: the words I would naturally type, with no coaching cue |
| D40 | **Drift check on every decision:** *Serves* (G1–G6) and *Protected item* (yes/no) |
| D41 | v0.6 fixes: AT-31 split, FR-5.7 headline, AT-29b → AT-41, lesson timing |
| D42 | Verdict order: Unsupported → Sound if narrowed → Needs repair → Sound |
| D43 | Freeze small: approve v1.0; tests and real use drive later changes |

### 3. New structure in the requirements

- **Goal map (G1–G6)** in section 1: every FR and QR serves a goal element, and each goal has one primary owner.
- **docs/progress.md:** the persistent task record. AGENTS.md now says to read it at the start of a session and
  update it at the end.
- **New requirements:** FR-0.8 (material it can't read), FR-1.7 (how a session ends), FR-2.7 (verdict meanings).
- **New tests:** AT-37 to AT-41, plus subcases in AT-25, AT-27, AT-31, AT-34, AT-35 and AT-S3.
- **New probes:** P-5 to P-7.
- **Slice order:** the validation script moves to slice 1, and method cards arrive with the slice that needs them.

### 4. Codex verification passes

| Version | Result | What it caught |
| --- | --- | --- |
| v0.5 | NOT MET | N1: the session could end before its work was done; 4 smaller issues |
| v0.6 | NOT MET | V1, V2: verdict levels overlapped; AT-06 inferred unexamined adoption from silence |
| v0.7 | NOT MET | W1: the verdict order made "Sound if narrowed" unreachable |
| v0.7.1 | **MET** | No High-severity consistency or ambiguity issue left |

Codex used gpt-6-astra at high effort, all on one thread: `01a14e42-3bc6-7750-bd9b-be610089efce`.

### 5. Git and GitHub

- `3be7e5d`: first commit (v0.7.1 as it stood).
- `ed7a8fd`: v1.0 approval (D43), tagged `requirements-v1.0`.
- Pushed `main` and the tag to `origin` (<https://github.com/ShivLee/think-twice.git>).

## Where to pick up

**Slice 1: the test feasibility probe, the validation script and the test-level gaps.** Steps, in order:

1. **Probe P-1:** can `claude plugin eval` invoke a manual-only skill through `/think-twice:pause`? Use a throwaway
   skill (it is exempt from the freeze rule).
2. Probes P-2 to P-7. Record the results, with CLI and model versions, in `docs/evaluation.md`.
3. Set each test's Auto or Manual from the probe results.
4. Write the validation script with RC-06.
5. Settle the test-level gaps #7, #12, #13 and #18 (listed in progress.md) while writing the tests.
6. Freeze the tests before any skill text is written.

To resume, paste this:

```text
In ~/projects/think-twice, read AGENTS.md, docs/HANDOFF.md and docs/progress.md.
Then start slice 1 with probe P-1. Name the requirement IDs each step serves.
```

## Rules that apply from now on

- REQUIREMENTS v1.0 is frozen. Every change cites a decision entry, and `git diff requirements-v1.0` shows drift.
- Every new decision gets the D40 drift check: *Serves* and *Protected item*.
- Tests are frozen before skill text. Never weaken a test to make it pass.
- Write the skill from the tests, not by copying the requirements; SKILL.md stays under about 4,000 tokens (QR-13).
- Each slice ends with its tests passing, me using it once on something real, and a Codex review against section 1.
- No commit, push, tag or release unless I ask.

## Lessons from this session

- **Check each batch of edits, not only the original draft.** Three of Codex's blocking findings (N1, V1, W1) were
  errors introduced by the fixes themselves. A narrow Codex check after each batch caught all three.
- **Run a drift test before approving.** It caught two problems before they shipped: D37 was too broad, and D39 would
  have made SC-2 unreachable.
- **Know when to stop.** Once the document was consistent, further review had diminishing returns. The remaining
  risk is behavioural, and only the probe and real use will show it.
