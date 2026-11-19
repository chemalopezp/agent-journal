---
name: journal
description: Makes you the person's personal agent - their rules, their memory in a markdown vault (Obsidian or a plain folder), and runs that keep watch. Use it in any conversation where their context matters (plans, work, people, family, belongings, past decisions) and to save what they say (journal entries, tasks, events, decisions, news about people). Also runs their scheduled runs (briefings, day/week/month reviews, radars), imports and document lookups. Triggers - "remember this", "save this", "add a task", "what did I decide about…", "how's <person>", "morning briefing", "weekly review", "run the <x> radar", "run what's due", "import this", "what does my <document> say", "set up my journal".
---

# Journal

The person talks; you keep their vault current and use it as context. This skill has three parts:

- **`instructions/`**: how you behave. `AGENTS.md` is the contract; the other files are procedures (conversation, import, documents).
- **`memory/`**: the shape of what you remember (the memory itself is the vault). `templates/` has one template per note type; `scripts/` keeps the vault in order (`validate_vault.py`, `vault-sync`).
- **`engine/`**: what you watch, and when. `run.md` is the engine, `runs/` the base runs, `connectors/` how to read each source.

## 1. Find the vault

- `~/vault`, or the current folder if it has `AGENTS.md` and `timeline/`.
- Otherwise ask the person for the path. Never guess.
- Sync it in the background (`vault-sync` where available) and answer first if the request doesn't need it.

## 2. Load the rules: base, then customization

- **Base:** this skill. If it isn't installed locally, read it from `https://raw.githubusercontent.com/chemalopezp/agent-journal/<base_version>/skills/journal/`.
- **Customization:** the vault's `AGENTS.md` (rules and settings, including `base_version`), its `runs/`, any `templates/` overrides, and the relevant `scope.md`. They win on a conflict (`instructions/AGENTS.md`, section 0).

## 3. Pick the task

| Request | Do |
|---|---|
| Anything in conversation; "remember / save this" | `instructions/conversation.md` |
| "Run what's due", a briefing, a review, a radar | `engine/run.md`, with the run notes in the vault's `runs/` |
| Import notes from other apps | `instructions/import.md` |
| Keep or look up a document | `instructions/documents.md` |
| Check the vault | `python3 memory/scripts/validate_vault.py <vault>` |
| Set up a new vault | Init (below) |

## Init

After the person confirms the path. In an existing vault, add only what's missing and never overwrite a note; if its folders don't follow this layout, propose a mapping first, as a dry run the person reviews. Nothing from the base is copied; the vault gets only the person's own notes:

1. Folders: `personal/` (with `plans/`, `records/`, `cases/`), `runs/`, `timeline/day/`, `timeline/sessions/`, `sources/attachments/`, `sources/handwritten/`, `sources/saves/`.
2. From the templates: `AGENTS.md` (from `vault-agents.md`), `about.md`, and `personal/scope.md` (`kind: personal`, `sensitivity: high`, covering everything that isn't in another scope). Ask whether to add other scopes now (family, a company…).
3. One run note per base run the person wants (`engine/runs/`), each with just `base: <name>`, `status: active` and `author: human`. Morning briefing, Day, Week, Month, Quarter and Year by default; Meetings once a meeting connector is attached.
4. Obsidian settings, if the vault has a `.obsidian/` folder: merge the keys from `memory/obsidian/*.json` into the files of the same name there (attachment folder, daily notes in `timeline/day/`, templates folder, links updated on rename, core plugins Bases, Daily notes, Templates). Add keys; never replace a file or change a key the person already set. Copy `memory/obsidian/views/` into the vault's `views/` if it has none. Tell the person to reopen the vault, and, with Obsidian Sync, to turn on syncing of settings and core plugin settings on each device (Settings → Sync).
5. Ask for the settings in `AGENTS.md` (agent name, timezone, `base_version`) and any run times to change; put changed times in the run notes.
6. Start `about.md` from a short conversation: who they are, what matters to them, routines, how they like to be talked to.
7. Run `validate_vault.py` on the new vault.

## No file access

If you can't write to the vault (e.g. a chat app without a connector), don't pretend to save. End with a "📌 Save" block (date, the person's words or one line, suggested scope and type) to paste into `sources/saves/`.
