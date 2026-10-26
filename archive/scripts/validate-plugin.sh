#!/usr/bin/env bash
# validate-plugin.sh: repository checks for think-twice (development only).
#
# Implements RC-06 (traceability, REQUIREMENTS section 5.5) for T1.5:
#   - every FR and QR unit has at least one valid test or check in section 5.6;
#   - every FR and QR unit appears in the goal map (section 1), and G1-G6 each have a primary owner;
#   - every ID referenced in the goal map, section 5.6 and the tests' "Covers" column is defined;
#   - every eval case (evals/, evals-baseline/) declares at least one ID in its `tags`, every ID-shaped tag
#     exists, and a subcase letter (AT-27d) is accepted only if that test defines the subcase.
# FR and QR units are FR-x.y, the situations S1-S6 (FR-3), the four lenses "FR-4 <Lens>" and QR-n.
# RC-01-RC-05 are added in later slices.
#
# Usage: scripts/validate-plugin.sh [repo-root]    check a repository (default: this one)
#        scripts/validate-plugin.sh --self-test    check that each required failure is caught

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 -I - "$ROOT" "$@" <<'PY'
import re, shutil, sys, tempfile
from pathlib import Path

LENSES = ("Sound", "Independent", "Overlooked", "Perspectives")
ID_RE = re.compile(
    r"(?<![\w-])(?P<pre>FR|QR|AT|RC|SC|P|G)-(?P<num>S?\d+(?:\.\d+)?)(?P<sub>[a-z])?(?![\w.])"
    r"(?:(?P<sep>[–/])(?:(?P=pre)-)?(?P<num2>S?\d+(?:\.\d+)?)(?![\w.]))?"
    r"(?P<lens>\s+(?:" + "|".join(LENSES) + r")\b)?"
    r"(?:\s*\((?P<s1>[a-z])[–-](?P<s2>[a-z])\))?")
SIT_RE = re.compile(r"(?<![\w-])S(?P<a>[1-9])(?:–S?(?P<b>[1-9]))?\b")
TAG_ID_RE = re.compile(r"^[A-Z]+-")


def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def rows(lines):
    return [cells(l) for l in lines if l.startswith("|") and not re.match(r"^\|\s*-{3}", l)]


def section(lines, start, stop):
    """Lines after the first heading matching `start`, up to the next heading matching `stop`."""
    i = next(n for n, l in enumerate(lines) if re.match(start, l))
    j = next((n for n in range(i + 1, len(lines)) if re.match(stop, lines[n])), len(lines))
    return lines[i + 1:j]


def expand_num(num, num2):
    if num2 is None:
        return [num]
    if num.startswith("S"):
        return [f"S{k}" for k in range(int(num[1:]), int(num2.lstrip("S")) + 1)]
    if "." in num:
        major, lo = num.split(".")
        hi = num2.split(".")[-1]
        return [f"{major}.{k}" for k in range(int(lo), int(hi) + 1)]
    width = len(num)
    return [str(k).zfill(width) for k in range(int(num), int(num2) + 1)]


def refs(text):
    """Every reference in `text`, as (id, subcase-or-None)."""
    out = []
    for m in ID_RE.finditer(text):
        pre, num, sub, sep, num2 = m["pre"], m["num"], m["sub"], m["sep"], m["num2"]
        if m["lens"] and pre == "FR" and num == "4":
            out.append((f"FR-4 {m['lens'].strip()}", None))
            continue
        nums = [num, num2] if sep == "/" else expand_num(num, num2)
        if sep == "/" and "." in num and num2 and "." in num2 and num2.split(".")[0] != num.split(".")[0]:
            nums = [num, num2]
        for n in nums:
            if m["s1"]:
                out += [(f"{pre}-{n}", chr(c)) for c in range(ord(m["s1"]), ord(m["s2"]) + 1)]
            else:
                out.append((f"{pre}-{n}", sub))
    stripped = ID_RE.sub(" ", text)
    for m in SIT_RE.finditer(stripped):
        out += [(f"S{k}", None) for k in range(int(m["a"]), int(m["b"] or m["a"]) + 1)]
    return out


class Model:
    def __init__(self, req_text):
        lines = req_text.splitlines()
        self.units, self.defined, self.subcases, self.children = [], set(), {}, {}

        sec3 = section(lines, r"^## 3\. ", r"^## 4\. ")
        current = None
        for l in sec3:
            h = re.match(r"^### (FR-\d+)\b", l)
            if h:
                current = h[1]; self.defined.add(current); self.children[current] = []
                continue
            if current is None:
                continue
            first = cells(l)[0] if l.startswith("|") and not re.match(r"^\|\s*-{3}", l) else None
            bullet = re.match(r"^- \*\*(FR-\d+\.\d+)", l)
            found = []
            if first is not None:
                found = re.findall(r"FR-\d+\.\d+", first)
                s = re.fullmatch(r"\*\*(S[1-9])\*\*", first)
                if s and current == "FR-3":
                    found = [s[1]]
                lens = re.fullmatch(r"\*\*(\w+)\*\*", first)
                if lens and current == "FR-4" and lens[1] in LENSES:
                    found = [f"FR-4 {lens[1]}"]
            elif bullet:
                found = [bullet[1]]
            for u in found:
                if u not in self.defined:
                    self.defined.add(u); self.units.append(u); self.children[current].append(u)

        for r in rows(section(lines, r"^## 4\. ", r"^## 5\. ")):
            m = re.match(r"\*\*(QR-\d+)\b", r[0])
            if m:
                self.defined.add(m[1]); self.units.append(m[1])

        for start, stop, pat in [(r"^### 5\.1 ", r"^### ", r"P-\d+"), (r"^### 5\.5 ", r"^### ", r"RC-\d+"),
                                 (r"^## 6\. ", r"^## ", r"\*\*SC-\d+")]:
            for r in rows(section(lines, start, stop)):
                m = re.match(pat, r[0])
                if m:
                    self.defined.add(m[0].strip("*"))

        self.tests = {}
        for heading in (r"^### 5\.2 ", r"^### 5\.3 ", r"^### 5\.4 "):
            for r in rows(section(lines, heading, r"^###? ")):
                if re.fullmatch(r"AT-S?\d+", r[0]):
                    self.defined.add(r[0]); self.tests[r[0]] = r
                    self.subcases[r[0]] = set(re.findall(r"\(([a-z])\)", r[2]))

        self.goal_rows = rows(section(lines, r"^### Goal map", r"^###? "))[1:]
        for r in self.goal_rows:
            m = re.match(r"\*\*(G\d)\*\*", r[0])
            if m:
                self.defined.add(m[1])
        self.trace_rows = rows(section(lines, r"^### 5\.6 ", r"^(###? |---)"))[1:]

    def resolve(self, ref):
        """Units a reference stands for (a parent covers its children)."""
        rid, _ = ref
        if rid in self.children:
            return self.children[rid] or [rid]
        return [rid]


def problems_in(root):
    root = Path(root)
    req = root / "docs" / "REQUIREMENTS.md"
    if not req.exists():
        return [f"missing {req}"]
    m = Model(req.read_text())
    errs = []

    def check_ref(ref, where):
        rid, sub = ref
        if rid not in m.defined:
            errs.append(f"unknown ID {rid} ({where})")
        elif sub is not None and sub not in m.subcases.get(rid, set()):
            errs.append(f"undefined subcase {rid}{sub} ({where})")

    # Goal map: references exist, every goal has a primary owner, every unit appears.
    in_goal_map = set()
    for r in m.goal_rows:
        goal = r[0].strip("*").split("*")[0].strip()
        for cell in r[1:]:
            for ref in refs(cell):
                check_ref(ref, f"goal map, {goal}")
                in_goal_map.update(m.resolve(ref))
        if re.match(r"\*\*G\d", r[0]) and not any(x[0] in m.defined for x in refs(r[1])):
            errs.append(f"goal {r[0].strip('*').split('*')[0]} has no primary owner")
    for g in (f"G{k}" for k in range(1, 7)):
        if g not in m.defined:
            errs.append(f"goal element {g} missing from the goal map")
    for u in m.units:
        if u not in in_goal_map:
            errs.append(f"unmapped requirement {u}: not in the goal map")

    # Traceability table: references exist, every unit has a valid test or check.
    traced = set()
    for r in m.trace_rows:
        reqs, checks = refs(r[0]), refs(r[1])
        for ref in reqs + checks:
            check_ref(ref, f"5.6 row '{r[0]}'")
        valid = [c for c in checks if c[0] in m.defined and c[0].split("-")[0] in ("AT", "RC")]
        if valid:
            for ref in reqs:
                traced.update(m.resolve(ref))
    for u in m.units:
        if u not in traced:
            errs.append(f"unmapped requirement {u}: no test or check in 5.6")

    # Tests' "Covers" column.
    for tid, r in m.tests.items():
        for ref in refs(r[1]):
            check_ref(ref, f"{tid} Covers")

    # Eval cases.
    for d in ("evals", "evals-baseline"):
        base = root / d
        if not base.is_dir():
            continue
        for f in sorted(list(base.rglob("case.yaml")) + list(base.rglob("prompt.md"))):
            if "results" in f.relative_to(base).parts:
                continue
            name = str(f.relative_to(root))
            tags = read_tags(f.read_text())
            ids = [t for t in tags if TAG_ID_RE.match(t)]
            if not ids:
                errs.append(f"missing ID: {name} declares no requirement or test ID in its tags")
            for t in ids:
                found = refs(t)
                if len(found) != 1 or f"{found[0][0]}{found[0][1] or ''}" != t:
                    errs.append(f"unknown ID {t} ({name})")
                else:
                    check_ref(found[0], name)
    return errs


def read_tags(text):
    """Tags from case.yaml or prompt.md front matter: `tags: [a, b]`, a block list, or JSON."""
    m = re.search(r'^\s*"?tags"?\s*:\s*\[(.*?)\]', text, re.M | re.S)
    if m:
        return [t.strip().strip("'\"") for t in m[1].split(",") if t.strip()]
    m = re.search(r"^tags\s*:\s*\n((?:\s+-\s*.+\n?)+)", text, re.M)
    if m:
        return [t.strip().lstrip("-").strip().strip("'\"") for t in m[1].splitlines() if t.strip()]
    return []


def self_test(root):
    root = Path(root)
    req_text = (root / "docs" / "REQUIREMENTS.md").read_text()

    def case(tags):
        return {"evals/st-case/case.yaml": "schema_version: \"1.0\"\nname: st-case\ntags: [" + ", ".join(tags) + "]\n"}

    scenarios = [
        ("clean copy passes", None, {}, True),
        ("valid eval case passes", None, case(["AT-16", "FR-2.1", "smoke"]), True),
        ("valid subcase passes", None, case(["AT-27d"]), True),
        ("missing ID: a test referenced in 5.6 is not defined",
         lambda t: re.sub(r"^\| AT-38 \|.*\n", "", t, flags=re.M), {}, False),
        ("missing ID: an eval case declares no ID", None, case(["smoke"]), False),
        ("unmapped requirement: no 5.6 row", lambda t: t.replace("| FR-2.6 | AT-24 |\n", ""), {}, False),
        ("unmapped requirement: not in the goal map", lambda t: t.replace("QR-1, QR-4, QR-5 |", "QR-1, QR-5 |"), {}, False),
        ("goal without a primary owner", lambda t: t.replace("| **G3** What am I overlooking? | FR-4 Overlooked |", "| **G3** What am I overlooking? | |"), {}, False),
        ("test citing an unknown ID", None, case(["AT-99"]), False),
        ("5.6 citing an unknown ID", lambda t: t.replace("| QR-12 | AT-17 |", "| QR-12 | AT-17, AT-77 |"), {}, False),
        ("undefined subcase in an eval case", None, case(["AT-27h"]), False),
        ("undefined subcase in 5.6", lambda t: t.replace("AT-38, AT-31b |", "AT-38, AT-31c |"), {}, False),
        ("prompt.md block-list tags are read", None,
         {"evals-baseline/st/prompt.md": "---\ntags:\n  - AT-99\n---\n\nHello\n"}, False),
        ("JSON case.yaml tags are read", None,
         {"evals/st-json/case.yaml": '{\n "schema_version": "1.0",\n "tags": [\n  "AT-16",\n  "QR-77"\n ]\n}\n'}, False),
    ]
    failed = 0
    for name, mutate, files, should_pass in scenarios:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "docs").mkdir()
            text = mutate(req_text) if mutate else req_text
            if mutate and text == req_text:
                print(f"FAIL  {name}: the mutation did not apply"); failed += 1; continue
            (Path(tmp) / "docs" / "REQUIREMENTS.md").write_text(text)
            for rel, content in files.items():
                p = Path(tmp) / rel; p.parent.mkdir(parents=True); p.write_text(content)
            errs = problems_in(tmp)
            ok = (not errs) == should_pass
            failed += not ok
            detail = "passes" if not errs else f"fails: {errs[0]}" + (f" (+{len(errs) - 1} more)" if len(errs) > 1 else "")
            print(f"{'ok  ' if ok else 'FAIL'}  {name}: {detail}")
    print(f"\nself-test: {len(scenarios) - failed}/{len(scenarios)} scenarios behave as expected")
    return failed == 0


root, args = sys.argv[1], sys.argv[2:]
if args[:1] == ["--self-test"]:
    sys.exit(0 if self_test(root) else 1)
target = args[0] if args else root
errs = problems_in(target)
for e in errs:
    print(f"RC-06: {e}")
print("RC-06: pass" if not errs else f"\nRC-06: fail ({len(errs)} problem{'s' if len(errs) != 1 else ''})")
sys.exit(1 if errs else 0)
PY
