#!/usr/bin/env python3
"""SC-1 gate: per-test verdicts from `claude plugin eval --json` output (development only; D47, gap #13).

The rules (evals/README.md, "How results count"):
  - A case passes a run when all its `pass-`, `fail-` and `critical-` graders pass and the run has no error. A run
    without the shared graders (`critical-`, `at12-`, `rc05-`; a baseline case needs only `critical-`) fails.
  - A test with several cases (its first tag, without a subcase letter: AT-35a -> AT-35) passes a run only if every
    case passes in that run. Every case of the test in its suite folder must have results, each with exactly 3 runs.
  - A test passes when it passes in at least 2 of 3 runs AND no `critical-` grader failed in any run of any case.
  - AT-12 passes in a case when its `at12-` graders pass in at least 2 of 3 runs; AT-12 passes when every case does.
  - RC-05 fails if any `rc05-` grader failed in any run.
  - A manual test passes if its first run passes, or its first run fails and the one re-run passes; a critical failure
    in any run fails it. A test with auto and manual parts (AT-26) passes only if both parts pass.

Added for slice 2 (plan.md T2.2, from the Codex plan review):
  - A subcase named in --tests (AT-39a, AT-34c) is judged on its own cases, without its siblings from later slices.
  - Every run must carry every grader its case.yaml defines; a missing one fails the run.
  - Book check (D49 item 2), on plugin cases only: a graded reply that names *Beyond Feelings* is checked against the
    shipped method cards (skills/pause/methods/). Every chapter it names must be a card's chapter, and while no card
    ships, naming the book at all is unsupported. Either is a critical failure.
  - Contamination (T2.1): a run whose tools touch an eval folder (evals/, evals-baseline/, evals-calibration/) could
    have read its own graders, so it counts as a critical failure. This needs each run's trace: run the eval with
    --keep-temp. Missing evidence (a case, a run, a grader, a trace or the reply) gives the verdict "incomplete": it
    never passes the gate, and it is never counted as a failure, so a baseline cannot look worse than it was.

Usage:
  scripts/sc1-gate.py RESULT.json [RESULT.json ...] [--root DIR] [--manual FILE] [--tests "AT-01 AT-02 ..."]
  scripts/sc1-gate.py --self-test

  --root DIR    where the cases live (default: the suite root recorded in each result file)
  --manual FILE manual results, one test per line: `AT-03 pass`, `AT-11 fail pass`, `AT-21 critical`
                (# starts a comment)
  --tests IDS   the gate: these tests must all pass; a listed test with no results is "not run" and fails the gate.
                Without --tests, every test found is in the gate.
Exit status: 0 if the gate passes, 1 if not.
"""
import json, re, sys, tempfile
from pathlib import Path

OWN = ("pass-", "fail-", "critical-")
RUNS = 3  # SC-1: each auto case runs 3 times


def read_tags(text):
    m = re.search(r'^\s*"?tags"?\s*:\s*\[(.*?)\]', text, re.M | re.S)
    if m:
        return [t.strip().strip("'\"") for t in m[1].split(",") if t.strip()]
    m = re.search(r"^tags\s*:\s*\n((?:\s+-\s*.+\n?)+)", text, re.M)
    return [t.strip().lstrip("-").strip().strip("'\"") for t in m[1].splitlines() if t.strip()] if m else []


def tags_of(case_dir):
    for name in ("case.yaml", "prompt.md"):
        f = case_dir / name
        if f.exists():
            tags = read_tags(f.read_text())
            if tags:
                return tags
    raise ValueError(f"{case_dir}: no tags, so its test is unknown")


def test_key(tag, subcases=()):
    """The test a case counts toward: its first tag without a subcase letter, unless the gate names that subcase."""
    return tag if tag in subcases else re.sub(r"(?<=\d)[a-z]$", "", tag)


def grader_names(case_dir):
    """The names of the graders a case.yaml defines: every run must report all of them."""
    text = (case_dir / "case.yaml").read_text()
    m = re.search(r"^graders\s*:", text, re.M)
    names = re.findall(r"^\s*-?\s*name\s*:\s*['\"]?([\w.-]+)", text[m.end():], re.M) if m else []
    if not names:
        raise ValueError(f"{case_dir}: no graders defined, so a complete run cannot be checked")
    return names


def suite_cases(suite_dir, cache, subcases=()):
    """Every case in a suite folder, by test: the cases a complete result for that test must include."""
    if suite_dir not in cache:
        by_test = {}
        for f in sorted(suite_dir.glob("*/case.yaml")):
            by_test.setdefault(test_key(tags_of(f.parent)[0], subcases), set()).add(f.parent.name)
        cache[suite_dir] = by_test
    return cache[suite_dir]


BOOK = re.compile(r"beyond\s+feelings|超越感觉", re.I)
CHAPTER = re.compile(r"\b(?:chapter|ch\.?)\s*(\d{1,2})\b|第\s*([0-9]{1,2}|[一二三四五六七八九十]{1,3})\s*章", re.I)
CN = {c: i for i, c in enumerate("一二三四五六七八九十", 1)}
EVAL_DIR = re.compile(r"(?:^|[/\\])(?:evals|evals-baseline|evals-calibration)(?:[/\\]|$)")


def chapter_number(m):
    if m[1]:
        return int(m[1])
    s = m[2]
    if s.isdigit():
        return int(s)
    tens, _, ones = s.rpartition("十") if "十" in s else ("", "", s)
    return (CN.get(tens, 1) * 10 if "十" in s else 0) + CN.get(ones, 0)


def card_chapters(root):
    """The chapters the shipped method cards cite; None when no card ships."""
    cards = sorted((Path(root) / "skills" / "pause" / "methods").glob("*.md"))
    if not cards:
        return None
    return {chapter_number(m) for f in cards for m in CHAPTER.finditer(f.read_text())}


def book_problems(reply, chapters):
    """D49 item 2: what a reply says about Beyond Feelings that the shipped cards do not support."""
    if not BOOK.search(reply):
        return []
    if chapters is None:
        return [f"names the book while no method card ships: {BOOK.search(reply)[0]!r}"]
    return [f"names chapter {chapter_number(m)}, which no card cites: {m[0]!r}"
            for m in CHAPTER.finditer(reply) if chapter_number(m) not in chapters]


def trace_tools(path):
    """Every tool call in a run's trace, or None if the trace cannot be read."""
    try:
        lines = Path(path).read_text().splitlines() if path else None
    except OSError:
        return None
    if lines is None:
        return None
    calls = []
    for line in lines:
        try:
            msg = json.loads(line).get("message")
        except ValueError:
            continue
        content = msg.get("content") if isinstance(msg, dict) else None
        for block in content if isinstance(content, list) else []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                calls.append((block.get("name"), block.get("input") or {}))
    return calls


def touches_evals(calls):
    return [f"{name} {v}" for name, args in calls for v in args.values()
            if isinstance(v, str) and EVAL_DIR.search(v)]


def reply_of(run):
    """The graded reply, as the LLM graders saw it."""
    return next((g["evidence"] for g in run.get("graders") or [] if g.get("evidence")), None)


def majority(passes, runs):
    return runs > 0 and 3 * passes >= 2 * runs


def evaluate(result_files, root=None, manual_lines=(), gate=None):
    tests, at12, rc05_fail, notes, expected, cache, rc05_seen = {}, {}, [], [], {}, {}, False
    subcases = {t for t in gate or () if re.fullmatch(r"AT-S?\d+[a-z]", t)}
    chapters = {}
    for path in result_files:
        data = json.loads(Path(path).read_text())
        base = Path(root or data["suite"]["root"])
        if base not in chapters:
            chapters[base] = card_chapters(base)
        for case in data["cases"]:
            runs = case["arms"].get("with") or next(iter(case["arms"].values()))
            case_dir = base / case["dir"]
            tags = tags_of(case_dir)
            test = test_key(tags[0], subcases)
            expected.setdefault(test, set()).update(suite_cases(case_dir.parent, cache, subcases).get(test, ()))
            baseline = "sc2-baseline" in tags
            # Every auto case carries the shared graders (evals/README.md); a baseline case carries only critical-.
            required = ("critical-",) if baseline else ("critical-", "at12-", "rc05-")
            defined = grader_names(case_dir)
            if len(runs) != RUNS:
                notes.append(f"{case['name']}: {len(runs)} runs, not {RUNS}; its test cannot pass")
            passed, critical, at12_ok, gaps = [], [], [], []
            for i, run in enumerate(runs):
                label = f"{case['name']} run {i + 1}"
                graders = run.get("graders") or []
                own = [g for g in graders if g["name"].startswith(OWN)]
                missing = [p for p in required if not any(g["name"].startswith(p) for g in graders)]
                absent = [n for n in defined if n not in {g["name"] for g in graders}]
                calls = trace_tools(run.get("tracePath"))
                reply = reply_of(run)
                extra = []  # critical failures found here, beyond the graders
                if calls is not None:
                    extra += [f"touches an eval folder ({t[:100]})" for t in touches_evals(calls)]
                if not baseline and reply is not None:
                    extra += book_problems(reply, chapters[base])
                incomplete = (calls is None and "no readable trace (run with --keep-temp)") or (
                    not baseline and reply is None and "no graded reply in the grader evidence")
                if run.get("error"):
                    notes.append(f"{label}: error ({str(run['error'])[:80]}); counted as failed")
                elif missing:
                    notes.append(f"{label}: no {', '.join(missing)} grader; counted as failed")
                elif absent:
                    notes.append(f"{label}: missing graders {', '.join(absent)}; counted as failed")
                elif incomplete:
                    notes.append(f"{label}: {incomplete}; counted as failed")
                if not run.get("error") and (missing or absent or incomplete):
                    gaps.append(label)  # incomplete evidence fails the test, not just the run (evals/README.md)
                notes += [f"{label}: critical: {e}" for e in extra]
                passed.append(not run.get("error") and not missing and not absent and not incomplete and not extra
                              and bool(own) and all(g["passed"] for g in own))
                critical.append(bool(extra) or any(not g["passed"] for g in graders if g["name"].startswith("critical-")))
                at12_g = [g for g in graders if g["name"].startswith("at12-")]
                if at12_g:
                    at12_ok.append(all(g["passed"] for g in at12_g))
                rc05_g = [g for g in graders if g["name"].startswith("rc05-")]
                rc05_seen = rc05_seen or bool(rc05_g)
                if any(not g["passed"] for g in rc05_g):
                    rc05_fail.append(f"{case['name']} run {i + 1}")
            tests.setdefault(test, []).append({"name": Path(case["dir"]).name, "passed": passed, "critical": critical,
                                              "gaps": gaps})
            if at12_ok:
                at12[case["name"]] = at12_ok

    verdicts = {}
    for test, cases in tests.items():
        n = min(len(c["passed"]) for c in cases)
        run_pass = [all(c["passed"][i] for c in cases) for i in range(n)]
        crit = [f"{c['name']} run {i + 1}" for c in cases for i, x in enumerate(c["critical"]) if x]
        absent = sorted(expected[test] - {c["name"] for c in cases})
        short = [c["name"] for c in cases if len(c["passed"]) != RUNS]
        gaps = [g for c in cases for g in c["gaps"]]
        ok = majority(sum(run_pass), n) and not crit and not absent and not short and not gaps
        # Incomplete evidence is its own verdict, never "fail": a baseline counted as failing would inflate SC-2.
        # A critical failure is a real failure whatever else is missing.
        status = "pass" if ok else "fail" if crit or not (absent or short or gaps) else "incomplete"
        detail = f"{sum(run_pass)}/{n} runs" + (f"; critical failure: {', '.join(crit)}" if crit else "") + (
            f"; cases with no results: {', '.join(absent)}" if absent else "") + (
            f"; not {RUNS} runs: {', '.join(short)}" if short else "") + (
            f"; incomplete evidence: {', '.join(gaps)}" if gaps else "")
        verdicts[test] = (status, detail)

    if at12:
        bad = [name for name, runs in at12.items() if len(runs) != RUNS or not majority(sum(runs), len(runs))]
        verdicts["AT-12"] = ("fail" if bad else "pass",
                             f"{len(at12) - len(bad)}/{len(at12)} cases" + (f"; failing: {', '.join(bad)}" if bad else ""))
    if rc05_seen:  # baseline cases have no rc05- grader, so they say nothing about RC-05
        verdicts["RC-05"] = ("fail" if rc05_fail else "pass",
                             "more than 3 cards in " + ", ".join(rc05_fail) if rc05_fail else "no reply loaded more than 3 cards")

    for line in manual_lines:
        line = line.split("#")[0].split()
        if not line:
            continue
        test, results = line[0], [r.lower() for r in line[1:]]
        if not results or any(r not in ("pass", "fail", "critical") for r in results):
            raise ValueError(f"manual result line for {test}: use pass, fail or critical")
        counted = results[:2] if results[0] != "pass" else results[:1]
        ok = "critical" not in results and counted[-1] == "pass"
        manual = ("pass" if ok else "fail", "manual: " + " then ".join(results[:2]) + (
            " (only the first run and one re-run count)" if len(results) > 2 else ""))
        if test in verdicts:  # a test with auto and manual parts (AT-26) passes only if both do
            auto = verdicts[test]
            both = "pass" if auto[0] == manual[0] == "pass" else "incomplete" if "incomplete" in (auto[0], manual[0]) \
                and "fail" not in (auto[0], manual[0]) else "fail"
            manual = (both, f"{auto[1]}; {manual[1]}")
        verdicts[test] = manual

    gate_ids = gate if gate is not None else sorted(verdicts)
    for t in gate_ids:
        verdicts.setdefault(t, ("not run", "no results"))
    gate_ok = all(verdicts[t][0] == "pass" for t in gate_ids)
    return verdicts, gate_ids, gate_ok, notes


def report(verdicts, gate_ids, gate_ok, notes):
    for t in sorted(verdicts, key=lambda x: (x not in gate_ids, x)):
        mark = "" if t in gate_ids else "  (not in the gate)"
        print(f"{verdicts[t][0]:8} {t:8} {verdicts[t][1]}{mark}")
    for n in notes:
        print("note:", n)
    print(f"\nSC-1 gate: {'PASS' if gate_ok else 'FAIL'} ({sum(verdicts[t][0] == 'pass' for t in gate_ids)}/{len(gate_ids)} tests pass)")


def self_test():
    """The three examples T1.8 requires, plus multi-case tests, AT-12, RC-05, errors, manual results, the gate, and the
    T2.2 checks: subcases in the gate, every defined grader, the book check and eval-folder contamination."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        clean = tmp / "trace-clean.jsonl"
        clean.write_text(json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Read", "input": {"file_path": "/x/skills/pause/standards.md"}}]}}) + "\n")
        peek = tmp / "trace-peek.jsonl"
        peek.write_text(json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Read", "input": {"file_path": "/x/evals/at64/case.yaml"}}]}}) + "\n")

        def run(own=True, crit=True, at12=True, rc05=True, error=None, reply="A plain reply.", trace=clean):
            r = {"error": error, "tracePath": str(trace) if trace else None,
                 "graders": [{"name": "pass-x", "passed": own}, {"name": "critical-reply", "passed": crit, "evidence": reply},
                             {"name": "at12-questions", "passed": at12}, {"name": "rc05-cards-loaded", "passed": rc05}]}
            return r
        P, F = run(), run(own=False)
        no_crit = dict(P, graders=[g for g in P["graders"] if not g["name"].startswith("critical-")])
        base_P = {"error": None, "tracePath": str(clean),
                  "graders": [{"name": "pass-x", "passed": True}, {"name": "critical-reply", "passed": True,
                                                                     "evidence": "Beyond Feelings, chapter 4, says so."}]}
        names = ["pass-x", "critical-reply", "at12-questions", "rc05-cards-loaded"]
        cases = {"one-of-three": ("AT-90", [P, F, F]), "two-of-three": ("AT-91", [P, P, F]),
                 "critical-once": ("AT-92", [P, P, run(crit=False)]),
                 "multi-a": ("AT-93a", [P, P, F]), "multi-b": ("AT-93b", [F, P, P]),
                 "errored": ("AT-94", [P, run(error="timeout"), F]),
                 "at12-weak": ("AT-95", [run(at12=False), run(at12=False), P]),
                 "rc05-over": ("AT-96", [P, run(rc05=False), P]),
                 "one-run": ("AT-80", [P]), "partial-b": ("AT-81b", [P, P, P]),
                 "auto-critical": ("AT-82", [P, P, run(crit=False)]), "auto-pass": ("AT-83", [P, P, P]),
                 "no-critical": ("AT-84", [no_crit, no_crit, no_crit]),
                 "baseline": ("AT-85", [base_P, base_P, base_P]),
                 "sub-a": ("AT-60a", [P, P, P]),
                 "grader-gone": ("AT-61", [P, P, P]),
                 "book-chapter": ("AT-62", [P, P, run(reply="As Beyond Feelings argues in chapter 3, ...")]),
                 "book-named": ("AT-63", [P, P, run(reply="This is a method from Beyond Feelings.")]),
                 "peeks-evals": ("AT-64", [P, P, run(trace=peek)]),
                 "no-trace": ("AT-65", [P, P, run(trace=None)]),
                 "other-chapter": ("AT-67", [run(reply="Chapter 11 protects the firm from creditors."), P, P])}
        data = {"suite": {"root": str(tmp)}, "cases": []}
        for name, (tag, runs) in cases.items():
            (tmp / "evals" / name).mkdir(parents=True)
            tags = f"{tag}, sc2-baseline" if name == "baseline" else f"{tag}, AT-12"
            defined = names[:2] if name == "baseline" else names + (["pass-y"] if name == "grader-gone" else [])
            graders = "".join(f"  - type: llm\n    name: {n}\n" for n in defined)
            (tmp / "evals" / name / "case.yaml").write_text(f"name: {name}\ntags: [{tags}]\ngraders:\n{graders}")
            data["cases"].append({"name": name, "dir": f"evals/{name}", "arms": {"with": runs}})
        for name, tag in (("partial-a", "AT-81a"), ("sub-b", "AT-60b")):  # cases with no results
            (tmp / "evals" / name).mkdir()
            (tmp / "evals" / name / "case.yaml").write_text(f"name: {name}\ntags: [{tag}, AT-12]\ngraders:\n  - name: pass-x\n")
        (tmp / "r.json").write_text(json.dumps(data))
        manual = ["AT-70 pass", "AT-71 fail pass", "AT-72 fail fail", "AT-73 critical pass", "# a comment",
                  "AT-82 pass", "AT-83 fail fail", "AT-34c pass", "AT-34d fail pass"]
        verdicts, _, gate_ok, _ = evaluate([tmp / "r.json"], manual_lines=manual,
                                           gate=["AT-91", "AT-70", "AT-71", "AT-99"])
        sub, _, sub_ok, _ = evaluate([tmp / "r.json"], manual_lines=manual, gate=["AT-60a", "AT-34c", "AT-34d"])
    expect = {"AT-90": "fail", "AT-91": "pass", "AT-92": "fail", "AT-93": "fail", "AT-94": "fail", "AT-95": "pass",
              "AT-96": "pass", "AT-12": "fail", "RC-05": "fail", "AT-70": "pass", "AT-71": "pass", "AT-72": "fail",
              "AT-73": "fail", "AT-99": "not run", "AT-80": "incomplete", "AT-81": "incomplete", "AT-82": "fail", "AT-83": "fail",
              "AT-84": "incomplete", "AT-85": "pass", "AT-60": "incomplete", "AT-61": "incomplete", "AT-62": "fail", "AT-63": "fail",
              "AT-64": "fail", "AT-65": "incomplete", "AT-67": "pass", "AT-34c": "pass", "AT-34d": "pass"}
    why = {"AT-90": "1 of 3 runs passing fails the test", "AT-91": "2 of 3 runs passing passes it",
           "AT-92": "a critical failure in one run fails it, though the other two pass",
           "AT-93": "two cases each passing 2 of 3, but together only in 1 run, fail",
           "AT-94": "an errored run counts as failed", "AT-95": "AT-12 is counted apart from the test's own result",
           "AT-96": "RC-05 is counted apart from the test's own result", "AT-12": "one case fails AT-12 in 2 of 3 runs",
           "RC-05": "one run loaded more than 3 cards", "AT-70": "manual: first run passes",
           "AT-71": "manual: fails, re-run passes", "AT-72": "manual: fails twice",
           "AT-73": "manual: a critical failure fails it, though the re-run passes",
           "AT-99": "a gate test with no results is not run",
           "AT-80": "one run, though it passes, is not 3", "AT-81": "a case of the test has no results",
           "AT-82": "a manual pass does not erase an auto critical failure",
           "AT-83": "an auto pass does not erase a manual failure",
           "AT-84": "runs without their critical- grader make the test incomplete",
           "AT-85": "a baseline case needs only its critical- grader, and is not book-checked",
           "AT-60": "without AT-60a in the gate, AT-60 needs its AT-60b case too",
           "AT-61": "runs missing a grader their case.yaml defines make the test incomplete",
           "AT-62": "a chapter of the book named while no card ships is critical",
           "AT-63": "naming the book while no card ships is critical",
           "AT-64": "a run that reads an eval folder is critical",
           "AT-65": "one run with no trace makes the test incomplete, not passed",
           "AT-67": "a chapter that is not the book's is not flagged",
           "AT-34c": "manual subcase result counts", "AT-34d": "manual subcase: fails, re-run passes"}
    sub_expect = {"AT-60a": ("pass", "a complete AT-60a passes alone when the gate names it"),
                  "AT-34c": ("pass", "a manual subcase in the gate"), "AT-34d": ("pass", "a manual subcase in the gate")}
    unit = [(book_problems("Beyond Feelings, chapter 1, describes it.", {1}) == [], "a chapter a card cites is fine"),
            (len(book_problems("Beyond Feelings, ch. 4, says so.", {1})) == 1, "a chapter no card cites is flagged"),
            (len(book_problems("《超越感觉》第四章讲过。", {1})) == 1, "a Chinese chapter no card cites is flagged"),
            (book_problems("《超越感觉》第一章讲过。", {1}) == [], "a Chinese chapter a card cites is fine")]
    bad, total = 0, 0
    for t, want in expect.items():
        got = verdicts.get(t, ("missing",))[0]
        bad += got != want; total += 1
        print(f"{'ok  ' if got == want else 'FAIL'}  {t}: {got:8} {why[t]}")
    for t, (want, reason) in sub_expect.items():
        got = sub.get(t, ("missing",))[0]
        bad += got != want; total += 1
        print(f"{'ok  ' if got == want else 'FAIL'}  {t}: {got:8} {reason}")
    for ok, reason in unit + [(gate_ok is False, "the gate fails, because AT-99 was not run"),
                              (sub_ok is True, "the subcase gate passes")]:
        bad += not ok; total += 1
        print(f"{'ok  ' if ok else 'FAIL'}  {reason}")
    print(f"\nself-test: {total - bad}/{total} checks behave as expected")
    return bad == 0


def main(argv):
    if argv[:1] == ["--self-test"]:
        return 0 if self_test() else 1
    files, root, manual, gate, i = [], None, [], None, 0
    while i < len(argv):
        a = argv[i]
        if a in ("--root", "--manual", "--tests"):
            if i + 1 >= len(argv):
                print(f"{a} needs a value", file=sys.stderr); return 2
            v = argv[i + 1]; i += 2
            if a == "--root": root = v
            elif a == "--manual": manual = Path(v).read_text().splitlines()
            else: gate = re.split(r"[\s,]+", v.strip())
        else:
            files.append(a); i += 1
    if not files and not manual:
        print(__doc__); return 2
    verdicts, gate_ids, gate_ok, notes = evaluate(files, root, manual, gate)
    report(verdicts, gate_ids, gate_ok, notes)
    return 0 if gate_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
