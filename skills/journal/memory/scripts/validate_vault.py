#!/usr/bin/env python3
"""Check an agent-journal vault against the contract (AGENTS.md).

  python3 validate_vault.py <vault>            # report
  python3 validate_vault.py <vault> --all      # list every issue, not just the first 20 per kind

Errors: notes without a type, or with a type that doesn't belong in their folder.
Warnings: missing provenance on agent notes, unknown status values, broken links,
notes outside the known layout. Exit code 1 if there are errors.
Read-only: it never changes the vault.
"""
import argparse
import collections
import os
import re
import sys

FOLDER_TYPES = {
    "plans": {"goal", "project", "task", "decision", "event"},
    "records": {"person", "org", "item", "note", "list", "document"},
    "cases": {"case"},
}
STATUS = {
    "goal": {"open", "someday", "done", "dropped", "triage"},
    "project": {"open", "waiting", "someday", "done", "dropped", "triage"},
    "task": {"open", "waiting", "done", "dropped", "triage"},
    "decision": {"open", "done", "dropped", "triage"},
    "event": {"open", "done", "dropped", "triage"},
    "case": {"open", "waiting", "done", "dropped", "triage"},
    "run": {"active", "draft", "paused"},
    "scope": {"active", "ended"},
}
for t in FOLDER_TYPES["records"]:
    STATUS[t] = {"active", "archived", "triage"}
PERIODS = {"day", "week", "month", "quarter", "year"}
ROOT_FILES = {"AGENTS.md", "about.md", "home.md", "CLAUDE.md", "GEMINI.md", "README.md"}
SKIP_DIRS = {".obsidian", ".git", ".trash", "templates"}
NO_SOURCE_NEEDED = {"period", "session", "run", "scope", "dashboard"}
BASE_RUNS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "engine", "runs")
LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def frontmatter(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*(?:#.*)?$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vault")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.vault)

    scopes, notes, names = set(), [], set()
    for d, dirs, files in os.walk(root):
        rel = os.path.relpath(d, root).replace("\\", "/")
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        if "scope.md" in files and rel != ".":
            scopes.add(rel)
        for f in files:
            p = f"{rel}/{f}" if rel != "." else f
            names.add(os.path.splitext(f)[0])
            names.add(os.path.splitext(p)[0])
            names.add(f)
            if f.endswith(".md"):
                notes.append(p)

    issues = collections.defaultdict(list)

    def add(kind, path, msg):
        issues[kind].append(f"{path}: {msg}")

    for p in sorted(notes):
        text = open(os.path.join(root, p), encoding="utf-8", errors="replace").read()
        fm = frontmatter(text)
        t = fm.get("type", "")
        parts = p.split("/")

        for target in LINK.findall(text):
            target = target.strip()
            if "{{" in target or not target:
                continue
            if target not in names and os.path.splitext(target)[0] not in names:
                add("warning: broken link", p, f"[[{target}]]")

        if parts[0] in ("sources", "templates", "views") or (len(parts) == 1 and parts[0] in ROOT_FILES) or parts[-1] == "README.md":
            continue
        if not t:
            add("error: no type", p, "missing `type`")
            continue

        if parts[0] == "runs":
            expected = {"run"}
        elif parts[0] == "timeline":
            expected = {"session"} if len(parts) > 1 and parts[1] == "sessions" else {"period"}
            if t == "period" and fm.get("period") and fm["period"] not in PERIODS:
                add("warning: unknown value", p, f"period `{fm['period']}`")
        else:
            scope = max((s for s in scopes if p.startswith(s + "/")), key=len, default=None)
            if scope is None:
                add("warning: outside the layout", p, "not in a scope, runs/, timeline/ or sources/")
                continue
            inner = p[len(scope) + 1:].split("/")
            if inner == ["scope.md"]:
                expected = {"scope"}
            elif inner[0] in FOLDER_TYPES:
                expected = FOLDER_TYPES[inner[0]]
            else:
                add("warning: outside the layout", p, f"in `{scope}/{inner[0]}/`, expected plans/, records/ or cases/")
                continue
        if t not in expected:
            add("error: type in wrong folder", p, f"type `{t}`, expected {' | '.join(sorted(expected))}")

        st = fm.get("status")
        if st and t in STATUS and st not in STATUS[t]:
            add("warning: unknown value", p, f"status `{st}` for {t}")
        if t == "run":
            base = fm.get("base", "")
            if not fm.get("status"):
                add("warning: missing field", p, "run without `status`")
            if base:
                if not os.path.isfile(os.path.join(BASE_RUNS, base + ".md")):
                    add("error: unknown base run", p, f"`base: {base}` is not in engine/runs/")
            elif not fm.get("cadence"):
                add("warning: missing field", p, "run without `cadence` (or a `base`)")
        author = fm.get("author", "")
        if not author:
            add("warning: missing field", p, "no `author`")
        elif author != "human" and t not in NO_SOURCE_NEEDED and not fm.get("source"):
            add("warning: no provenance", p, f"written by {author} without `source`")

    errors = sum(len(v) for k, v in issues.items() if k.startswith("error"))
    print(f"Checked {len(notes)} notes in {root} - {len(scopes)} scopes: {', '.join(sorted(scopes)) or 'none'}")
    if not issues:
        print("No issues.")
    for kind in sorted(issues):
        items = issues[kind]
        print(f"\n{kind} ({len(items)})")
        for line in items if a.all else items[:20]:
            print(f"  {line}")
        if not a.all and len(items) > 20:
            print(f"  … {len(items) - 20} more (use --all)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
