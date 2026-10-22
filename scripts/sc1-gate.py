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


def test_of(case_dir):
    return re.sub(r"(?<=\d)[a-z]$", "", tags_of(case_dir)[0])


def suite_cases(suite_dir, cache):
    """Every case in a suite folder, by test: the cases a complete result for that test must include."""
    if suite_dir not in cache:
        by_test = {}
        for f in sorted(suite_dir.glob("*/case.yaml")):
            by_test.setdefault(test_of(f.parent), set()).add(f.parent.name)
        cache[suite_dir] = by_test
    return cache[suite_dir]


def majority(passes, runs):
    return runs > 0 and 3 * passes >= 2 * runs


def evaluate(result_files, root=None, manual_lines=(), gate=None):
    tests, at12, rc05_fail, notes, expected, cache, rc05_seen = {}, {}, [], [], {}, {}, False
    for path in result_files:
        data = json.loads(Path(path).read_text())
        base = Path(root or data["suite"]["root"])
        for case in data["cases"]:
            runs = case["arms"].get("with") or next(iter(case["arms"].values()))
            case_dir = base / case["dir"]
            tags = tags_of(case_dir)
            test = re.sub(r"(?<=\d)[a-z]$", "", tags[0])
            expected.setdefault(test, set()).update(suite_cases(case_dir.parent, cache).get(test, ()))
            # Every auto case carries the shared graders (evals/README.md); a baseline case carries only critical-.
            required = ("critical-",) if "sc2-baseline" in tags else ("critical-", "at12-", "rc05-")
            if len(runs) != RUNS:
                notes.append(f"{case['name']}: {len(runs)} runs, not {RUNS}; its test cannot pass")
            passed, critical, at12_ok = [], [], []
            for i, run in enumerate(runs):
                graders = run.get("graders") or []
                own = [g for g in graders if g["name"].startswith(OWN)]
                missing = [p for p in required if not any(g["name"].startswith(p) for g in graders)]
                if run.get("error"):
                    notes.append(f"{case['name']} run {i + 1}: error ({str(run['error'])[:80]}); counted as failed")
                elif missing:
                    notes.append(f"{case['name']} run {i + 1}: no {', '.join(missing)} grader; counted as failed")
                passed.append(not run.get("error") and not missing and bool(own) and all(g["passed"] for g in own))
                critical.append(any(not g["passed"] for g in graders if g["name"].startswith("critical-")))
                at12_g = [g for g in graders if g["name"].startswith("at12-")]
                if at12_g:
                    at12_ok.append(all(g["passed"] for g in at12_g))
                rc05_g = [g for g in graders if g["name"].startswith("rc05-")]
                rc05_seen = rc05_seen or bool(rc05_g)
                if any(not g["passed"] for g in rc05_g):
                    rc05_fail.append(f"{case['name']} run {i + 1}")
            tests.setdefault(test, []).append({"name": Path(case["dir"]).name, "passed": passed, "critical": critical})
            if at12_ok:
                at12[case["name"]] = at12_ok

    verdicts = {}
    for test, cases in tests.items():
        n = min(len(c["passed"]) for c in cases)
        run_pass = [all(c["passed"][i] for c in cases) for i in range(n)]
        crit = [f"{c['name']} run {i + 1}" for c in cases for i, x in enumerate(c["critical"]) if x]
        absent = sorted(expected[test] - {c["name"] for c in cases})
        short = [c["name"] for c in cases if len(c["passed"]) != RUNS]
        ok = majority(sum(run_pass), n) and not crit and not absent and not short
        detail = f"{sum(run_pass)}/{n} runs" + (f"; critical failure: {', '.join(crit)}" if crit else "") + (
            f"; cases with no results: {', '.join(absent)}" if absent else "") + (
            f"; not {RUNS} runs: {', '.join(short)}" if short else "")
        verdicts[test] = ("pass" if ok else "fail", detail)

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
            manual = ("pass" if auto[0] == manual[0] == "pass" else "fail", f"{auto[1]}; {manual[1]}")
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
    """The three examples T1.8 requires, plus multi-case tests, AT-12, RC-05, errors, manual results and the gate."""
    def run(own=True, crit=True, at12=True, rc05=True, error=None):
        return {"error": error, "graders": [{"name": "pass-x", "passed": own}, {"name": "critical-reply", "passed": crit},
                                            {"name": "at12-questions", "passed": at12}, {"name": "rc05-cards-loaded", "passed": rc05}]}
    P, F = run(), run(own=False)
    no_crit = {"error": None, "graders": [g for g in P["graders"] if not g["name"].startswith("critical-")]}
    base_P = {"error": None, "graders": [{"name": "pass-x", "passed": True}, {"name": "critical-reply", "passed": True}]}
    with tempfile.TemporaryDirectory() as tmp:
        cases = {"one-of-three": ("AT-90", [P, F, F]), "two-of-three": ("AT-91", [P, P, F]),
                 "critical-once": ("AT-92", [P, P, run(crit=False)]),
                 "multi-a": ("AT-93a", [P, P, F]), "multi-b": ("AT-93b", [F, P, P]),
                 "errored": ("AT-94", [P, run(error="timeout"), F]),
                 "at12-weak": ("AT-95", [run(at12=False), run(at12=False), P]),
                 "rc05-over": ("AT-96", [P, run(rc05=False), P]),
                 "one-run": ("AT-80", [P]), "partial-b": ("AT-81b", [P, P, P]),
                 "auto-critical": ("AT-82", [P, P, run(crit=False)]), "auto-pass": ("AT-83", [P, P, P]),
                 "no-critical": ("AT-84", [no_crit, no_crit, no_crit]),
                 "baseline": ("AT-85", [base_P, base_P, base_P])}
        data = {"suite": {"root": tmp}, "cases": []}
        for name, (tag, runs) in cases.items():
            (Path(tmp) / "evals" / name).mkdir(parents=True)
            tags = f"{tag}, sc2-baseline" if name == "baseline" else f"{tag}, AT-12"
            (Path(tmp) / "evals" / name / "case.yaml").write_text(f"name: {name}\ntags: [{tags}]\n")
            data["cases"].append({"name": name, "dir": f"evals/{name}", "arms": {"with": runs}})
        (Path(tmp) / "evals" / "partial-a").mkdir()  # a case of AT-81 with no results
        (Path(tmp) / "evals" / "partial-a" / "case.yaml").write_text("name: partial-a\ntags: [AT-81a, AT-12]\n")
        (Path(tmp) / "r.json").write_text(json.dumps(data))
        manual = ["AT-70 pass", "AT-71 fail pass", "AT-72 fail fail", "AT-73 critical pass", "# a comment",
                  "AT-82 pass", "AT-83 fail fail"]
        verdicts, gate_ids, gate_ok, _ = evaluate([Path(tmp) / "r.json"], manual_lines=manual,
                                                  gate=["AT-91", "AT-70", "AT-71", "AT-99"])
    expect = {"AT-90": "fail", "AT-91": "pass", "AT-92": "fail", "AT-93": "fail", "AT-94": "fail", "AT-95": "pass",
              "AT-96": "pass", "AT-12": "fail", "RC-05": "fail", "AT-70": "pass", "AT-71": "pass", "AT-72": "fail",
              "AT-73": "fail", "AT-99": "not run", "AT-80": "fail", "AT-81": "fail", "AT-82": "fail", "AT-83": "fail",
              "AT-84": "fail", "AT-85": "pass"}
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
           "AT-84": "a run without its critical- grader counts as failed",
           "AT-85": "a baseline case needs only its critical- grader"}
    bad = 0
    for t, want in expect.items():
        got = verdicts.get(t, ("missing",))[0]
        bad += got != want
        print(f"{'ok  ' if got == want else 'FAIL'}  {t}: {got:8} {why[t]}")
    gate_right = gate_ok is False
    bad += not gate_right
    print(f"{'ok  ' if gate_right else 'FAIL'}  the gate fails, because AT-99 was not run")
    print(f"\nself-test: {len(expect) + 1 - bad}/{len(expect) + 1} checks behave as expected")
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
