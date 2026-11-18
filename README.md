# agent-journal

A personal journal that AI agents can read and help maintain, safely.

It keeps three things separate:

| Layer | What | Where |
|---|---|---|
| **Storage** | Your notes, as plain markdown | Your vault (Obsidian, a synced folder, Drive…) — yours, portable |
| **Instructions** | The contract and playbooks agents follow | This repo — versioned, improvable |
| **Agents** | Whatever runs the instructions | Claude Code, ChatGPT, others — replaceable |

Change agents without moving your notes. Improve instructions without touching your notes.

## What's in here

```
skills/journal/         The skill (installable in any agent that supports SKILL.md)
  SKILL.md              Entry point: find vault, load rules, pick task
  AGENTS.md             The contract: read order, signed writes, privacy, naming
  playbooks/            morning · evening · weekly · monthly · _every-run · radar · import · documents
  scripts/              import_keep.py, import_gemini.py (Takeout → notes)
  starter/              Empty vault: a personal/ scope, shared folders, about.md, templates
scripts/                vault-sync (safe Obsidian sync), drive-setup (read-only Drive originals)
connectors/             How radars read each source: GitHub, Slack, Granola, Gmail, Drive, web
adapters/
  claude-code/          Claude Code setup, scheduling, cloud sessions
  chatgpt/              ChatGPT + Google Drive (no hosting)
.claude-plugin/         Lets Claude Code install this repo as a plugin
```

## Install

**Claude Code, from your GitHub repo** (updates with `/plugin update`):

```
/plugin marketplace add <github-user>/agent-journal
/plugin install journal@agent-journal
```

**Claude Code, manual:** copy `skills/journal/` to `~/.claude/skills/journal/` (all projects) or `<vault>/.claude/skills/journal/` (that vault only).

**Claude apps (web/desktop/mobile):** zip `skills/journal/` and upload it under Settings → Capabilities → Skills. Without a connector to your notes it falls back to "📌 Save" blocks.

**Other agents:** many read `AGENTS.md` from the folder they work in, and several support the `SKILL.md` format — copy `skills/journal/` to wherever that agent loads skills. Agents with neither (e.g. ChatGPT) use an adapter in `adapters/`.

**Then:** ask the agent to "set up my journal in <folder>". For an existing vault, copy `skills/journal/AGENTS.md` into its root.

## Principles

- **Humans own the text.** Agents append; they never rewrite or delete what you wrote.
- **Every agent write is signed**, so you always know who wrote what.
- **Private by default.** Nothing leaves the vault unless a note is marked `visibility: shareable`.
- **Originals stay outside.** Documents live in your own drive; the vault keeps a card per document.
- **Organised by scope.** `personal/` always; add `family/`, a company, a side project… Each scope has the same folders (goals, projects, people, records, inventory, routines…). Agents suggest new scopes, never create them.
- **Plain files.** Markdown + YAML frontmatter + `[[wikilinks]]`. Works with or without Obsidian.

## Roadmap

- Bridge export: publish `shareable` notes to a place other chat apps can read (Notion, Drive, GitHub)
- More importers (Apple Notes, Evernote, Notion export)
- Small CLI: `init`, `digest`, `import`, `check` (validate frontmatter and signatures)
