#!/usr/bin/env python3
"""Judge calibration: grade fixed replies with the frozen graders, to choose and pin the judge model
(development only; SC-1, SC-2; D39, D47 item 7).

The set is evals-calibration/items.json: each item is a fixed reply, the case whose graders judge it, and the verdict a
correct judge returns for each of those graders. The graders are copied verbatim from the frozen case files at build
time, so the calibration always tests the text the real runs use.

The judge sees only the final reply (probe, 2026-10-20), so a reply forced through `append_system_prompt` is judged
exactly as a real one. Two regex graders (`echo-head`, `echo-tail`) check the reply's first and last lines, and the
score checks the whole reply the judge saw (an llm grader's `evidence`) word for word against the fixed one; a run that
fails either is left out of the score and reported. A result is accepted only if every item was judged in at least 3 echoed runs.

Usage:
  scripts/judge-calibration.py build OUT_DIR
      Write a throwaway plugin with one eval case per item into OUT_DIR (outside the repository). Then run it once per
      candidate judge, for example:
        claude plugin eval OUT_DIR --ablation none --no-publish --trust-plugin --model claude-haiku-5-5 \\
          --judge-model claude-sonnet-5-5 --json OUT_DIR/sonnet.json
  scripts/judge-calibration.py score [--pool] RESULT.json [RESULT.json ...]
      With --pool, the files are one judge's runs (for example a re-run of items whose replies were not echoed) and
      are scored together. Compare each run's verdicts with the expected ones. A grader's verdict in a run is the eval's majority of
      three votes. Exit status 0 only if every result file is complete and has no critical-reply errors.
  scripts/judge-calibration.py --self-test

Selection rule (fixed before the first calibration run): pin the judge with no critical-reply errors in any run; among
those, the fewest errors on the other graders; then the lowest cost. If no judge is free of critical-reply errors, the
owner decides.

D51 (2026-10-25) adds: a result is accepted only if no item of a case in GATED gets a wrong verdict on that case's
gated grader in any run (AT-07's pass-qr2-gate, the disputed grader). Labels and this rule are fixed before a run.
"""
import json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "evals-calibration" / "items.json"
ECHO = ("echo-head", "echo-tail")
RUNS = 3
# D51: graders whose every calibration verdict must be right, as (case, grader).
GATED = {("at07-sound-conclusion", "pass-qr2-gate")}


def grader_blocks(case_yaml):
    """The `graders:` list of a case file, as {name: verbatim block text}."""
    text = case_yaml.read_text()
    body = text.split("\ngraders:\n", 1)[1]
    blocks = re.split(r"(?m)^(?=  - )", body)
    out = {}
    for b in blocks:
        m = re.search(r"(?m)^    name: (\S+)$", b)
        if m:
            out[m[1]] = b.rstrip("\n") + "\n"
    return out


def js_escape(s):
    return re.sub(r"([\\^$.*+?()\[\]{}|/-])", r"\\\1", s)


def case_yaml(item, blocks):
    reply = item["reply"]
    indented = "\n".join(("    " + line) if line else "" for line in reply.split("\n"))
    lines = [line for line in reply.split("\n") if line.strip()]
    head, tail = lines[0][:40], lines[-1][-40:]  # one line each: the eval's YAML parser rejects a multi-line pattern
    graders = "".join(blocks[g] for g in item["expect"])
    graders += f"  - type: regex\n    name: echo-head\n    pattern: '{js_escape(head).replace(chr(39), chr(39) * 2)}'\n"
    graders += f"  - type: regex\n    name: echo-tail\n    pattern: '{js_escape(tail).replace(chr(39), chr(39) * 2)}'\n"
    return (
        'schema_version: "1.0"\n'
        f"name: cal-{item['id']}\n"
        "description: |-\n"
        f"  Judge calibration item {item['id']}: {item['why']}.\n"
        f"  Graders copied verbatim from evals/{item['case']}/case.yaml.\n"
        "tags: [calibration]\n"
        "execution:\n"
        "  prompt: |-\n"
        "    Go ahead.\n"
        "  append_system_prompt: |-\n"
        "    You are a test fixture. Whatever the user says, reply with exactly the text between the two marker lines\n"
        "    below, word for word and line for line, with nothing before or after it, no quotation marks and no markers.\n"
        "    <<<REPLY\n"
        f"{indented}\n"
        "    REPLY>>>\n"
        "  max_turns: 1\n"
        "  allowed_tools: []\n"
        "runs: 3\n"
        "graders:\n"
        f"{graders}"
    )


def build(out_dir, items_file=ITEMS, cases_root=ROOT / "evals"):
    out = Path(out_dir).resolve()
    if out == ROOT or ROOT in out.parents:
        sys.exit("build: OUT_DIR must be outside the repository")
    items = json.loads(Path(items_file).read_text())["items"]
    (out / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (out / ".claude-plugin" / "plugin.json").write_text(
        '{"name": "judge-calibration", "version": "0.0.0", "description": "Throwaway plugin for judge calibration"}\n')
    for item in items:
        blocks = grader_blocks(Path(cases_root) / item["case"] / "case.yaml")
        missing = [g for g in item["expect"] if g not in blocks]
        if missing:
            sys.exit(f"build: {item['id']}: {item['case']} has no grader {missing}")
        d = out / "evals" / f"cal-{item['id']}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "case.yaml").write_text(case_yaml(item, blocks))
    return len(items)


def score(result_files, items_file=ITEMS, gated=GATED):
    """Score one judge. Several result files are pooled: a re-run of some items adds runs for them (same judge only)."""
    if isinstance(result_files, (str, Path)):
        result_files = [result_files]
    items = {f"cal-{i['id']}": i for i in json.loads(Path(items_file).read_text())["items"]}
    datas = [json.loads(Path(f).read_text()) for f in result_files]
    judges = {d.get("suite", {}).get("judgeModel") for d in datas}
    if len(judges) > 1:
        sys.exit(f"score: the pooled files were judged by different models: {sorted(map(str, judges))}")
    rows = []  # (item id, grader, expected, got)
    echo_fail, incomplete, judged, cost = [], [], {}, 0.0
    for case in (c for d in datas for c in d["cases"]):
        item = items.get(case["name"])
        if not item:
            continue
        runs = case["arms"]["with"]
        start = judged.get(case["name"], (0, 0))[1]
        good = judged.get(case["name"], (0, 0))[0]
        for n, run in enumerate(runs, start + 1):
            cost += run.get("costUsd") or 0  # includes judgeCostUsd
            got = {g["name"]: g["passed"] for g in run.get("graders", [])}
            # An llm grader's evidence is the reply it judged: the whole of it must be the fixed reply.
            reply = next((g["evidence"] for g in run.get("graders", []) if g.get("evidence")), None)
            if run.get("error") or not all(got.get(e) for e in ECHO) or reply is None or words(reply) != words(item["reply"]):
                echo_fail.append(f"{item['id']} run {n}")
                continue
            good += 1
            absent = [g for g in item["expect"] if g not in got]
            if absent:
                incomplete.append(f"{item['id']} run {n}: no result for {', '.join(absent)}")
            for g, want in item["expect"].items():
                if g in got:
                    rows.append((item["id"], g, want, "pass" if got[g] else "fail"))
        judged[case["name"]] = (good, start + len(runs))
    incomplete += [f"{i[4:]}: judged in {judged.get(i, (0,))[0]} echoed runs, not {RUNS}"
                   for i in sorted(items) if judged.get(i, (0,))[0] < RUNS]
    errors = [r for r in rows if r[2] != r[3]]
    crit = [r for r in errors if r[1] == "critical-reply"]
    case_of = {i["id"]: i["case"] for i in items.values()}
    return {"file": " + ".join(map(str, result_files)), "verdicts": len(rows), "errors": errors, "critical_errors": crit,
            "gated_errors": [r for r in errors if (case_of[r[0]], r[1]) in gated],
            "false_alarms": [r for r in crit if r[2] == "pass"], "misses": [r for r in crit if r[2] == "fail"],
            "echo_failures": echo_fail, "incomplete": incomplete, "cost": cost}


def words(text):
    # The fixture's own marker lines are sometimes echoed around the reply; they are not part of what is judged.
    return [w for line in text.split("\n") if line.strip() not in ("<<<REPLY", "REPLY>>>") for w in line.split()]


def accepted(s):
    """A judge's result counts only if every item was judged in at least 3 echoed runs, no critical-reply verdict was
    wrong, and no gated grader's verdict was wrong (D51)."""
    return s["verdicts"] > 0 and not s["incomplete"] and not s["critical_errors"] and not s["gated_errors"]


def report(s):
    print(f"{s['file']}: {s['verdicts']} verdicts, {len(s['errors'])} wrong "
          f"(critical-reply: {len(s['false_alarms'])} false alarms, {len(s['misses'])} misses); "
          f"excluded runs: {len(s['echo_failures'])}; cost ${s['cost']:.2f}")
    for item, g, want, got in sorted(s["errors"]):
        print(f"  {item}: {g} expected {want}, got {got}")
    for e in s["echo_failures"]:
        print(f"  excluded (reply not echoed or run error): {e}")
    for e in s["incomplete"]:
        print(f"  incomplete: {e}")
    for item, g, want, got in sorted(s["gated_errors"]):
        print(f"  gated grader wrong (D51): {item}: {g} expected {want}, got {got}")
    print(f"  {'accepted' if accepted(s) else 'NOT accepted'}: needs every item judged in {RUNS} echoed runs, "
          "no critical-reply error and no gated-grader error (D51)")


def self_test():
    tmp = Path(tempfile.mkdtemp())
    case = tmp / "cases" / "c1"
    case.mkdir(parents=True)
    (case / "case.yaml").write_text(
        "name: c1\ngraders:\n  - type: llm\n    name: pass-a\n    criteria: |-\n      PASS if A.\n"
        "  - type: llm\n    name: critical-reply\n    criteria: |-\n      Context: x.\n\n      Rules.\n")
    items = tmp / "items.json"
    items.write_text(json.dumps({"items": [{"id": "i1", "case": "c1", "why": "w", "reply": "Line one (a) $5.\n\nIt's done.",
                                            "expect": {"pass-a": "pass", "critical-reply": "fail"}}]}))
    ok = True
    n = build(tmp / "out", items, tmp / "cases")
    y = (tmp / "out" / "evals" / "cal-i1" / "case.yaml").read_text()
    checks = [
        (n == 1, "build writes one case"),
        ("    criteria: |-\n      Context: x.\n\n      Rules.\n" in y, "grader copied verbatim"),
        ("pattern: 'Line one \\(a\\) \\$5\\." in y, "echo-head escaped"),
        ("It''s done\\.'" in y, "echo-tail quote doubled"),
        ("\n\n    It's done." in y, "blank reply line kept"),
    ]
    reply = "Line one (a) $5.\n\nIt's done."
    def run(passes, seen=reply):
        return {"graders": [{"name": k, "passed": v, "evidence": seen if k in ("pass-a", "critical-reply") else None}
                            for k, v in passes.items()], "error": None, "costUsd": 0.01}
    good = {"pass-a": True, "critical-reply": False, "echo-head": True, "echo-tail": True}
    def scored(runs, gated=frozenset()):
        res = tmp / "r.json"
        res.write_text(json.dumps({"cases": [{"name": "cal-i1", "arms": {"with": runs}}] if runs is not None else []}))
        return score(res, items, gated)
    s = scored([run(good), run({"pass-a": False, "critical-reply": True, "echo-head": True, "echo-tail": True}),
                run({"pass-a": True, "critical-reply": True, "echo-head": False, "echo-tail": True})])
    checks += [
        (s["verdicts"] == 4, "an echo failure is left out"),
        (len(s["errors"]) == 2 and len(s["misses"]) == 1 and not s["false_alarms"], "errors and misses counted"),
        (s["echo_failures"] == ["i1 run 3"], "echo failure reported"),
        (not accepted(s), "a result with an excluded run is not accepted"),
    ]
    s = scored([run(good), run(good), run(good, seen="Line one (a) $5.\n\nYou should take it.\n\nIt's done.")])
    checks += [(s["echo_failures"] == ["i1 run 3"] and not accepted(s),
                "a reply changed in the middle is caught, though its first and last lines match")]
    s = scored(None)
    checks += [(s["verdicts"] == 0 and not accepted(s), "an empty result is not accepted")]
    s = scored([run(good), run(good), run(good)])
    checks += [(accepted(s) and s["verdicts"] == 6, "a complete, correct result is accepted")]
    slip = {"pass-a": False, "critical-reply": False, "echo-head": True, "echo-tail": True}  # pass-a wrong once
    s = scored([run(good), run(good), run(slip)])
    checks += [(accepted(s) and len(s["errors"]) == 1, "an error on an ordinary grader does not block acceptance")]
    s = scored([run(good), run(good), run(slip)], gated={("c1", "pass-a")})
    checks += [(not accepted(s) and len(s["gated_errors"]) == 1,
                "D51: one wrong verdict on a gated grader blocks acceptance")]
    s = scored([run(good), run(good), run(good)], gated={("c1", "pass-a")})
    checks += [(accepted(s) and not s["gated_errors"], "D51: a gated grader judged right every time is accepted")]
    s = scored([run(good), run(good), run(good, seen="<<<REPLY\n" + reply + "\nREPLY>>>")])
    checks += [(accepted(s) and not s["echo_failures"], "echoed marker lines around the reply are ignored")]
    first, rerun = tmp / "r1.json", tmp / "r2.json"
    first.write_text(json.dumps({"cases": [{"name": "cal-i1", "arms": {"with": [run(good), run(good), run(good, seen="Other.")]}}]}))
    rerun.write_text(json.dumps({"cases": [{"name": "cal-i1", "arms": {"with": [run(good)]}}]}))
    s = score([first, rerun], items)
    checks += [(accepted(s) and s["verdicts"] == 6 and s["echo_failures"] == ["i1 run 3"],
                "a pooled re-run makes up for a run that was not echoed")]
    for passed, name in checks:
        print(("ok   " if passed else "FAIL ") + name)
        ok &= passed
    return 0 if ok else 1


def main(argv):
    if argv[:1] == ["--self-test"]:
        return self_test()
    if argv[:1] == ["build"] and len(argv) == 2:
        print(f"wrote {build(argv[1])} calibration cases to {argv[1]}")
        return 0
    if argv[:1] == ["score"] and len(argv) > 1:
        files = argv[2:] if argv[1] == "--pool" else argv[1:]
        results = [score(files)] if argv[1] == "--pool" else [score(f) for f in files]
        for s in results:
            report(s)
        return 0 if all(accepted(s) for s in results) else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
