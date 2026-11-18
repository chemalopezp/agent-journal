#!/usr/bin/env python3
"""Convert a Google Takeout Keep export into journal inbox notes.

Follows playbooks/import.md. Never deletes or edits the source. Dry run by default.

  python3 import_keep.py <Takeout/Keep folder> <vault folder>           # dry run: report only
  python3 import_keep.py <Takeout/Keep folder> <vault folder> --write   # write notes
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

AGENT = "import-agent"
SOURCE = "google-keep"
SECRET_PATTERNS = [
    r"\b(password|passwd|contraseña|pin|cvv|iban|swift|api[_ -]?key|token|secret)\b",
    r"\b(?:\d[ -]?){13,19}\b",  # card-like numbers
    r"\b[A-Z]{2}\d{2}[A-Z0-9 ]{11,30}\b",  # IBAN-like
]


def slugify(text, limit=50):
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", text)[:limit].strip("-") or "untitled"


def when(usec):
    if not usec:
        return None
    return dt.datetime.fromtimestamp(int(usec) / 1_000_000)


def body_of(note):
    parts = []
    if note.get("textContent"):
        parts.append(note["textContent"].rstrip())
    for item in note.get("listContent", []):
        box = "x" if item.get("isChecked") else " "
        parts.append(f"- [{box}] {item.get('text', '').strip()}")
    for link in note.get("annotations", []):
        if link.get("url"):
            parts.append(f"- [{link.get('title') or link['url']}]({link['url']})")
    return "\n".join(parts).strip()


def yaml_list(items):
    return "[" + ", ".join(json.dumps(i, ensure_ascii=False) for i in items) + "]"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keep_dir", type=Path)
    ap.add_argument("vault", type=Path)
    ap.add_argument("--write", action="store_true", help="write files (default: dry run)")
    args = ap.parse_args()

    out_dir = args.vault / "sources" / SOURCE
    att_dir = args.vault / "_attachments" / "imports" / SOURCE
    today = dt.date.today().isoformat()
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    stats = {"notes": 0, "imported": 0, "trashed": 0, "empty": 0, "duplicate": 0, "flagged": 0, "bad_json": 0}
    seen, flagged, used_names = set(), [], set()
    labels_count, years = {}, {}

    for path in sorted(args.keep_dir.glob("*.json")):
        try:
            note = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            stats["bad_json"] += 1
            continue
        if "textContent" not in note and "listContent" not in note and "title" not in note:
            continue  # not a note file
        stats["notes"] += 1
        if note.get("isTrashed"):
            stats["trashed"] += 1
            continue

        title = (note.get("title") or "").strip()
        body = body_of(note)
        if not title and not body and not note.get("attachments"):
            stats["empty"] += 1
            continue
        digest = hashlib.sha256(f"{title}\n{body}".encode()).hexdigest()
        if digest in seen:
            stats["duplicate"] += 1
            continue
        seen.add(digest)

        created = when(note.get("createdTimestampUsec")) or when(note.get("userEditedTimestampUsec")) or dt.datetime.now()
        edited = when(note.get("userEditedTimestampUsec")) or created
        labels = [l["name"] for l in note.get("labels", []) if l.get("name")]
        tags = [slugify(l, 40) for l in labels]
        if note.get("isArchived"):
            tags.append("archived-source")
        if note.get("isPinned"):
            tags.append("pinned-source")
        for l in labels:
            labels_count[l] = labels_count.get(l, 0) + 1
        years[created.year] = years.get(created.year, 0) + 1

        is_secret = any(re.search(p, f"{title}\n{body}", re.IGNORECASE) for p in SECRET_PATTERNS)

        base = f"{created:%Y-%m-%d-%H%M}-{slugify(title or body.splitlines()[0] if body else 'note')}"
        name, n = base, 2
        while name in used_names or (out_dir / f"{name}.md").exists():
            name, n = f"{base}-{n}", n + 1
        used_names.add(name)

        links = []
        for a in note.get("attachments", []):
            src = args.keep_dir / a.get("filePath", "")
            if src.is_file():
                links.append(f"![[{src.name}]]")
                if args.write:
                    att_dir.mkdir(parents=True, exist_ok=True)
                    if not (att_dir / src.name).exists():
                        shutil.copy2(src, att_dir / src.name)

        if is_secret:
            stats["flagged"] += 1
            flagged.append(f"{path.name} → {name}.md")
            original = "_Content withheld: may contain a secret. Review the original in the Takeout export._"
            summary = "Possible secret detected; content not imported. Human review needed."
        else:
            original = "\n".join(filter(None, [body, *links])) or "_(attachment only)_"
            summary = "Imported from Google Keep. Triage pending."

        text = f"""---
type: import
source: {SOURCE}
source_id: {json.dumps(path.name, ensure_ascii=False)}
original_created: {created:%Y-%m-%d}
original_updated: {edited:%Y-%m-%d}
created: {today}
author: {AGENT}
visibility: private
{"flag: possible-secret" + chr(10) if is_secret else ""}tags: {yaml_list(tags)}
---
# {title or "(untitled)"}

## Original
{original}

> [!agent] {AGENT} · {now} · import
> {summary}
"""
        if args.write:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{name}.md").write_text(text, encoding="utf-8")
        stats["imported"] += 1

    mode = "WROTE" if args.write else "DRY RUN (nothing written; add --write)"
    top_labels = sorted(labels_count.items(), key=lambda kv: -kv[1])[:15]
    report = [
        f"# Keep import report · {now} · {mode}",
        "",
        f"Notes found: {stats['notes']} · to import: {stats['imported']}",
        f"Skipped: trashed {stats['trashed']} · empty {stats['empty']} · duplicate {stats['duplicate']} · unreadable {stats['bad_json']}",
        f"Flagged (content withheld): {stats['flagged']}",
        "",
        "By year: " + ", ".join(f"{y}: {c}" for y, c in sorted(years.items())),
        "Top labels: " + (", ".join(f"{l} ({c})" for l, c in top_labels) or "none"),
    ]
    if flagged:
        report += ["", "## Flagged for review", *[f"- {f}" for f in flagged]]
    print("\n".join(report))
    if args.write:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"_report-{today}.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
