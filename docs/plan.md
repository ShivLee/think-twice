# Implementation plan

The plan that section 9 rule 9 of [REQUIREMENTS.md](REQUIREMENTS.md) requires: every task names the IDs it serves
and the tests or checks that mark it done. **What gets built** is defined in REQUIREMENTS; **where the work stands**
is in [progress.md](progress.md). This file says **what comes next and how we know it is done**.

Only the current slice is planned task by task. **Before each later slice starts**, its tasks are written here, each
with its IDs and done-when, and Codex reviews them against REQUIREMENTS (section 9 rule 9). That plan review is
separate from the review at the end of the slice (section 9 rule 11).

## Slices

Every slice ends with its gate passing, the owner using it once on something real (slice 1: an owner test review,
D44), and a Codex review of the changes against section 1 and the ID list (section 9 rule 11). Each slice ships the
method cards and glossary entries its own tests need.

**The gate.** A slice passes when **its own tests and the tests of every earlier slice** pass under the SC-1 rule
(each auto test ≥2 of 3 runs, no critical failure in any run; each manual test passes). Tests of later slices are not
run and are reported as "not implemented", never as failures. A parent ID in the table means only the part named;
the tests column is the gate. AT-12 (questions per turn, length) runs over every auto case in the slice. AT-26 also
runs in any earlier slice that ships a method card.

| # | Slice | Serves | Tests in the gate |
| --- | --- | --- | --- |
| 1 | Test feasibility probe, validation script, tests written and frozen | 5.1 (P-1–P-7), RC-06, all AT (written, not run against a skill) | Slice 1 tasks below (D44) |
| 2 | Recognition, core and the quick after review | FR-0.1, FR-0.2 (recognising all three phases; after), FR-0.4, FR-0.5, FR-0.7, FR-0.8; FR-1.1–FR-1.5; FR-1.6 and FR-1.7 (after, without the journal offer); FR-1.3 (Claude-written summary); FR-2.1–FR-2.4 (after); FR-2.6, FR-2.7; FR-4; QR-1–QR-5; QR-6 (after); QR-10 | AT-01, 02, 04, 05, 07, 08, 09, 10, 11, 19, 20, 21, 22, 23, 24, 25, 29, 30, 31, 34c, 34d, 35, 36, 37, 38, 39a, 41 |
| 3 | Before and during | FR-0.2 (during), FR-0.4 (switching after a correction), FR-0.6; FR-1.3 (conversation material); FR-1.6 and FR-1.7 (during checkpoint); FR-2.1–FR-2.4 (before, during); FR-2.5; QR-6 (before, during); QR-12 | AT-03, 06, 13, 14, 15, 16, 17, 18, 32, 33, 34b, 39b, 40 |
| 4 | Situations S1–S6 | FR-0.3, FR-3 | AT-S1–S7 |
| 5 | Journal | FR-5, FR-1.7 (journal offer), QR-9 | AT-27a–g, AT-34a |
| 6 | Omission pass, remaining method cards and glossary | Section 7, FR-6, QR-7, QR-8 | AT-26, AT-28, RC-03, RC-04. Then **SC-3 start** (D45): date, plugin version and model version recorded privately before any use counts |
| 7 | Packaging and release | QR-11, QR-13, RC-01–RC-05, SC-1, SC-2, SC-4, SC-3 | Release checks pass; SC-1 and SC-2 met on the full suite; SC-4 install test passes. **SC-3 check:** all six D45 rules applied, and no material change during the period (or the period restarted). `1.0.0` only when SC-3 is met |

Slice 7 runs during the SC-3 period, so its packaging work must not change the skill's behaviour (D45 rule 6). A
change that might is treated as material and restarts the period.

## Working practices (no rule change)

- Every `claude plugin eval` run uses `--no-publish`; results stay in `evals/results/`, which git ignores.
- While developing, run a named smoke set plus the tests a change affects, with the baseline arm off. At the end of
  each slice, run the full gate for that slice. The full suite runs at release.
- When a slice is done, run the SC-2 paired comparison for the SC-2 cases in its gate.
- Check `SKILL.md` and card sizes against QR-13 at the end of every slice (section 9 rule 11).
- Slice reviews by Codex cover the diff, not the whole repository.
- Real use before the SC-3 start is feedback only (D45). The real-use log stays private in `.local/`.
- After slice 2, re-estimate the remaining work from measured times, and revisit whether AT-03, AT-21, AT-22, AT-32,
  AT-37 and AT-34 (c)/(d) should become Auto with saved histories (owner chose to keep them Manual for now; D47).

## Slice 1 tasks

Each task fits one session. Do them in this order.

| Task | What | Serves | Done when |
| --- | --- | --- | --- |
| T1.1 | Eval privacy (#14): `evals/results/` in `.gitignore`; `--no-publish` on every run | QR-9, RC-02 | Both in place before P-1 runs |
| T1.2 | Probe P-1 with a throwaway skill (exempt from the freeze rule) | FR-0.1, QR-11; prevents auto tests that cannot invoke the skill | Result and, if it fails, its fallback recorded in `docs/evaluation.md` with CLI and model versions |
| T1.3 | Probes P-2–P-7; record time spent per run and per case (#12) | FR-2.1, FR-2.2, QR-12, QR-13, RC-05, SC-1; prevents tests that cannot run as written | Each result and its fallback recorded in `docs/evaluation.md`; P-7's list of conversation-dependent cases written down |
| T1.4 | Set the "How" column of section 5 from the probe results | All AT (How column); prevents an Auto test the eval cannot run | Every test is Auto or Manual from evidence; the change to REQUIREMENTS cites a decision entry |
| T1.5 | Validation script `scripts/validate-plugin.sh` with RC-06 | RC-06; prevents untraced requirements and unknown IDs | Passes on the current docs; fails on each of: a missing ID, an unmapped requirement, a test citing an unknown ID, an undefined subcase |
| T1.6 | Write the tests in 5.2 (recognition, core, phases), and AT-12 as one reusable check | AT-01–AT-25, AT-30–AT-40; FR-0–FR-2, FR-4, QR-1–QR-6, QR-10, QR-12 | Each case declares its IDs, dialogue state and graded reply; **every PASS and FAIL condition in its row is checked by its grader or manual script**; the section 5 critical failures are checked in every grader; the gaps below that apply are written in and marked settled |
| T1.7 | Write the tests in 5.3 (situations) | AT-S1–AT-S7; FR-0.3, FR-3 | As T1.6 |
| T1.8 | Write the tests in 5.4 (methods, journal, language, safety) and the SC-1 gate (#13) | AT-26–AT-29, AT-41; FR-5, FR-6, QR-7–QR-10; SC-1 | As T1.6; the SC-1 gate is checked on three examples: 1 of 3 runs passing fails the case, 2 of 3 passes it, and a critical failure in one run fails it even when the other two pass |
| T1.9 | Owner test review (D44): a sample chosen in advance covering the three phases and the four failure modes | D44; QR-1 (substitution), QR-2 (manufactured objections), QR-3 (overstated facts), QR-4 (agreement), QR-5 | Owner has checked each case is realistic and its PASS would help; unrealistic tests are fixed |
| T1.10 | Freeze the prompts and graders | All AT; prevents tests tuned to fit the skill (section 9 rule 2) | Frozen; RC-06 passes; later changes need a decision entry |
| T1.11 | Run the plain-Claude baseline cases (D46) for the 10 SC-2 tests (information, not a gate) | SC-2 (AT-04, 06, 08, 09, 10, 14, 18, S1, S2, S5), D39; prevents finding out late that SC-2 is out of reach | Results recorded; if plain Claude already passes too many, the owner hears about it before slice 2 |
| T1.12 | Slice review: Codex compares the changes with section 1 and the ID list | All slice 1 IDs; prevents drift (section 9 rule 11) | Owner has read the review |

### Test-level gaps to settle in T1.6–T1.8 (Codex review)

Settle these while writing the tests, before freezing them. Numbers refer to the Codex review.

- #7 Behavioural coverage: QR-2's four conditions; FR-1.3's "examined and accepted" group; the before phase not
  reading anything on its own initiative; affected people and other fields (Perspectives lens).
- #12 Settled by the probe and D46: runs record CLI, model and judge model; each SC-2 test (the 10, plus AT-07 and
  AT-19) gets its own baseline case in D39 wording under `evals-baseline/`, written alongside its plugin case.
- #13 An SC-1 gate that computes "≥2 of 3 runs, no critical failure" from per-run results, even when P-6 passes;
  how manual tests are re-run.
- #18 Counting rules for QR-6 and QR-13 (tokenizer, mixed languages, tolerance) and which cards load first when more
  than 3 apply.
- #10 is decided by probe P-5.

**Later (no blocker for freezing):**

- #9 Procedure for changing method cards and tests (CONTRIBUTING.md covers situations only).
- #19 What "one pass" means alongside the correction loop.
- #21 Paired self-review cases: the same reasoning attributed to Claude, to me and to a third party.

## Slice 6 note: the omission pass (section 7)

Planned in full when slice 6 starts. It is one independent, chapter-by-chapter pass against the frozen reading map:
"Is any method in this chapter missing from the inventory?" Its inputs are private (the 58-method inventory in
book-experts `.local/eval/value-v3/drafts/` and the book), so access is checked before the slice starts. Its result
stays private; progress.md records only that it was done and on what date, with no book text. Cards that follow from
it need the FR-6.5 review record and pass RC-03.
