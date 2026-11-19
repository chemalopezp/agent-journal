#!/usr/bin/env python3
"""Convert a Google Takeout "My Activity > Gemini Apps" export into monthly source notes.

Follows instructions/import.md. One file per month in sources/gemini/, each entry with the
prompt in full and the response in a collapsed callout. Never edits the source. Dry run by default.

  python3 import_gemini.py "<.../My Activity/Gemini Apps/My Activity.html>" <vault>           # dry run
  python3 import_gemini.py "<.../My Activity/Gemini Apps/My Activity.html>" <vault> --write
"""
import argparse
import os
import collections
import datetime as dt
import html
import re
import sys
from pathlib import Path

AGENT = os.environ.get("AGENT_NAME", "Claude")
SOURCE = "gemini"
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
DATE_RE = re.compile(r"(\d{1,2}) ([A-Za-z]{3})[a-z]* (\d{4}), (\d{1,2}):(\d{2}):(\d{2})")
SECRET_PATTERNS = [
    r"\b(password|passwd|contraseña|pin|cvv|iban|swift|api[_ -]?key|secret key|token)\b\s*[:=]",
    r"\b(?:\d[ -]?){13,19}\b",
    r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}\b",
]
ENTRY_RE = re.compile(
    r'<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">(.*?)'
    r'</div><div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right">',
    re.S)


def to_text(fragment):
    s = fragment
    s = re.sub(r"<h\d[^>]*>", "\n\n### ", s)
    s = re.sub(r"<li[^>]*>", "\n- ", s)
    s = re.sub(r"<(br|/p|/h\d|/ul|/ol|/blockquote|/li)[^>]*>", "\n", s)
    s = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", s, flags=re.S)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"[ \t]+\n", "\n", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def parse(cell):
    parts = re.split(r"<br\s*/?>", cell)
    head = to_text(parts[0])
    when, rest = None, ""
    for i, p in enumerate(parts[1:], 1):
        m = DATE_RE.search(re.sub(r"<[^>]+>", "", html.unescape(p)))
        if m and len(re.sub(r"<[^>]+>", "", p)) < 80:
            d, mon, y, hh, mm, ss = m.groups()
            when = dt.datetime(int(y), MONTHS.get(mon.lower()[:3], 1), int(d), int(hh), int(mm), int(ss))
            rest = "<br>".join(parts[i + 1:])
            break
        head += "\n" + to_text(p)
    m = re.match(r"\s*(\S+)\s*(.*)", head, re.S)
    kind, prompt = (m.group(1), m.group(2)) if m else ("Unknown", "")
    return kind, prompt.strip(), when, to_text(rest)


def quote(text):
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("activity_html", type=Path)
    ap.add_argument("vault", type=Path)
    ap.add_argument("--write", action="store_true", help="write files (default: dry run)")
    args = ap.parse_args()

    raw = args.activity_html.read_text(encoding="utf-8", errors="replace")
    out_dir = args.vault / "sources" / SOURCE
    today = dt.date.today().isoformat()
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    by_month = collections.defaultdict(list)
    kinds, stats = collections.Counter(), collections.Counter()
    for cell in ENTRY_RE.findall(raw):
        stats["entries"] += 1
        kind, prompt, when, response = parse(cell)
        kinds[kind] += 1
        if not when:
            stats["no_date"] += 1
            continue
        if not prompt and not response:
            stats["empty"] += 1
            continue
        secret = any(re.search(p, f"{prompt}\n{response}", re.IGNORECASE) for p in SECRET_PATTERNS)
        if secret:
            stats["flagged"] += 1
        by_month[f"{when:%Y-%m}"].append((when, kind, prompt, response, secret))

    for month, items in sorted(by_month.items()):
        items.sort()
        lines = [
            "---",
            "type: import",
            f"source: {SOURCE}",
            f"source_id: \"{args.activity_html.name}\"",
            f"original_created: {month}-01",
            f"created: {today}",
            f"author: {AGENT}",
            f"entries: {len(items)}",
            "tags: [gemini]",
            "---",
            f"# Gemini — {month}",
            "",
            f"### 🤖 {AGENT} · import: gemini · {now}",
            f"{len(items)} entries imported. Summary pending (topics, projects, people, decisions).",
            "",
        ]
        for when, kind, prompt, response, secret in items:
            title = (prompt.splitlines() or [kind])[0][:80] or kind
            lines.append(f"## {when:%Y-%m-%d %H:%M} · {title}")
            if secret:
                lines += ["", "_Content withheld: may contain a secret. Review the original export._", ""]
                continue
            lines += ["", f"**{kind}:** {prompt}" if prompt else f"**{kind}**", ""]
            if response:
                lines += ["> [!quote]- Response", quote(response), ""]
        if args.write:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{month}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    years = collections.Counter(m[:4] for m, items in by_month.items() for _ in items)
    mode = "WROTE" if args.write else "DRY RUN (nothing written; add --write)"
    report = [
        f"# Gemini import report · {now} · {mode}",
        "",
        f"Entries found: {stats['entries']} · to import: {sum(len(v) for v in by_month.values())} in {len(by_month)} monthly files",
        f"Skipped: no date {stats['no_date']} · empty {stats['empty']}",
        f"Flagged (content withheld): {stats['flagged']}",
        "Kinds: " + ", ".join(f"{k} ({c})" for k, c in kinds.most_common()),
        "By year: " + ", ".join(f"{y}: {c}" for y, c in sorted(years.items())),
        "Attachments (images, audio) are not imported; they stay in the Takeout export.",
    ]
    print("\n".join(report))
    if args.write:
        (out_dir / f"_report-{today}.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
