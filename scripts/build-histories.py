#!/usr/bin/env python3
"""Build eval histories from frozen dialogues (development only; D47).

Each `dialogue.md` under evals/ and evals-baseline/ is a frozen test dialogue. This script turns it into the
`history.jsonl` next to it, which the case passes to `claude plugin eval` as `context.history_file`. Run it before
every eval run: a `### pause` turn gets the current skills/pause/SKILL.md (and the real skill folder path), so a
resumed session never follows old skill text (evaluation.md, constraint 1). The generated files are not committed.

Dialogue format: turns start with a level-3 heading; anything before the first heading is a comment.

    ### user           a message I typed
    ### assistant      Claude's reply
    ### pause          a /think-twice:pause call; the text under it (may be empty) is its argument
    ### compacted      a compaction: the text is the summary that replaces all earlier turns

Usage: scripts/build-histories.py [--skill PATH] [--check]
  --skill PATH   use another SKILL.md (for probes); default skills/pause/SKILL.md
  --check        parse every dialogue and report, without writing
"""
import json, re, subprocess, sys, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TURN_RE = re.compile(r"^### (user|assistant|pause|compacted)\s*$", re.M)
COMPACT_PREFIX = ("This session is being continued from a previous conversation that ran out of context. "
                  "The summary below covers the earlier portion of the conversation.\n\n")


def parse(text):
    parts = TURN_RE.split(text)
    return [(parts[i], parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def skill_text(skill_path, args):
    text = skill_path.read_text()
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    body = (text[m.end():] if m else text).strip()
    body = body.replace("$ARGUMENTS", args).replace("${CLAUDE_SKILL_DIR}", str(skill_path.parent))
    return f"Base directory for this skill: {skill_path.parent}\n\n{body}"


def cli_version():
    try:
        out = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=30).stdout
        return out.split()[0]
    except (OSError, IndexError, subprocess.SubprocessError):
        return "unknown"


def build(dialogue, skill_path, version):
    turns = parse(dialogue.read_text())
    if not turns:
        raise ValueError("no turns")
    if turns[-1][0] not in ("assistant", "compacted"):
        raise ValueError("the last turn must be an assistant reply (the case prompt is the next user turn)")
    session = str(uuid.uuid5(uuid.NAMESPACE_URL, f"think-twice:{dialogue.relative_to(ROOT)}"))
    entries, parent = [], None

    def add(kind, n, **fields):
        nonlocal parent
        uid = str(uuid.uuid5(uuid.UUID(session), str(n)))
        entry = {"parentUuid": parent, "isSidechain": False, "type": kind, "uuid": uid,
                 "timestamp": f"2026-01-01T00:{n // 60:02d}:{n % 60:02d}.000Z", "userType": "external",
                 "sessionId": session, "version": version, "cwd": "/tmp/fixture"}
        entry.update(fields)
        entries.append(entry)
        parent = uid

    for n, (kind, text) in enumerate(turns):
        n *= 2
        if kind == "user":
            add("user", n, message={"role": "user", "content": text})
        elif kind == "assistant":
            add("assistant", n, message={
                "id": f"msg_fixture{n:04d}", "type": "message", "role": "assistant", "model": "claude-opus-5-5",
                "content": [{"type": "text", "text": text}], "stop_reason": "end_turn", "stop_sequence": None,
                "usage": {"input_tokens": 0, "output_tokens": 0}})
        elif kind == "pause":
            if skill_path is None:
                skill_path = ROOT / "skills" / "pause" / "SKILL.md (not checked)"
            elif not skill_path.exists():
                raise FileNotFoundError(f"{skill_path} does not exist yet; a pause turn needs it")
            command = "<command-message>think-twice:pause</command-message>\n<command-name>/think-twice:pause</command-name>"
            if text:
                command += f"\n<command-args>{text}</command-args>"
            add("user", n, message={"role": "user", "content": command})
            body = skill_text(skill_path, text) if skill_path.exists() else "(skill text not checked)"
            add("user", n + 1, isMeta=True, message={"role": "user", "content": [{"type": "text", "text": body}]})
        elif kind == "compacted":
            parent = None
            add("system", n, subtype="compact_boundary", content="Conversation compacted", isMeta=False,
                level="info", compactMetadata={"trigger": "auto", "preTokens": 160000})
            add("user", n + 1, isCompactSummary=True, isVisibleInTranscriptOnly=True,
                message={"role": "user", "content": COMPACT_PREFIX + text})
    return entries


def main(argv):
    skill = ROOT / "skills" / "pause" / "SKILL.md"
    if "--skill" in argv:
        skill = Path(argv[argv.index("--skill") + 1]).resolve()
    check = "--check" in argv
    version = cli_version()
    dialogues = sorted(p for d in ("evals", "evals-baseline") for p in (ROOT / d).rglob("dialogue.md"))
    failed = 0
    for dialogue in dialogues:
        name = dialogue.parent.relative_to(ROOT)
        try:
            entries = build(dialogue, None if check else skill, version)
        except (ValueError, FileNotFoundError) as e:
            print(f"error  {name}: {e}")
            failed += 1
            continue
        if not check:
            out = dialogue.parent / "history.jsonl"
            out.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries))
        print(f"{'checked' if check else 'built'}  {name}: {len(entries)} entries")
    print(f"\n{len(dialogues) - failed}/{len(dialogues)} dialogues {'parsed' if check else 'built'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
