# AGENTS.md — journal contract

This folder is a personal journal and life-context store. **The human owns it.** Agents help maintain it under these rules. If a request conflicts with a rule, stop and ask.

## 0. Every conversation

- **Start:** pull the vault, read this file, `about.md`, `home.md`, the last 3 notes in `journal/sessions/` and the latest digest. Before answering anything about plans, work, people or belongings, look in the relevant scope (section 5).
- **End (if worth keeping):** write a session note (section 10), update any records or tasks touched, then push.

## 1. Read order

Read only what the task needs, in this order:

1. This file, then the playbook for the task (`playbooks/`).
2. `about.md` — who the human is, preferences, routines.
3. `00-inbox/` — unprocessed items.
4. Today's and yesterday's note in `journal/daily/`, the latest digest in `journal/digests/`, the last session notes.
5. Each scope's `goals/` and `projects/` with `status: active`.
6. Anything else only when needed. Don't bulk-read the vault. For documents, search the `documents/` cards first.

## 2. Writing rules

- **Append-only.** Never delete, rewrite or reorder human text. Never rename or move files unless asked.
- **Sign every write** with an agent block (format below).
- New material goes in a **new file** with frontmatter and `author: <agent-name>`.
- Frontmatter: agents may set `updated` and add `tags`. Any other change is proposed in a `suggestion` block.
- Not sure where something goes? Put it in `00-inbox/`.
- Prefer **one file per agent entry**; it avoids sync conflicts. Agents don't write into the human's daily note.
- **Generated files** (`generated: true`, e.g. `home.md`) are rewritten whole by their owning agent. Humans don't edit them; they change the template instead.
- **Archive by status, not by moving.** Finished or parked items keep their place and change `status`.

### Signed block

```markdown
> [!agent] <agent-name> · <YYYY-MM-DD HH:mm> · <action>
> Content, one or more lines.
```

`action` is one of: `digest`, `review`, `note`, `import`, `extract`, `suggestion`.

Humans reply under a block in plain text. Agents never edit a block after writing it; they add a new one.

## 3. Privacy

- Every note has `visibility: private` or `visibility: shareable`. **Missing means private.**
- Private content never leaves the vault: not in notifications, exports, bridges, connectors or other tools.
- Inside the vault, digests may **link** to private notes but should not quote sensitive details.
- **Never store secrets** (passwords, keys, full account or ID numbers). Mask them (`…1234`). If an import contains one, don't copy it; flag it for the human.
- Only `shareable` notes may be exported. Documents and their cards are **always private**.

## 4. Agents

Each agent has a stable name, used in signatures and `author`. Suggested names:

| Agent | Does |
|---|---|
| `digest-agent` | Morning/evening digests, weekly review |
| `import-agent` | Imports from other apps and files |
| `docs-agent` | Document catalog: cards and extracts |
| `chat-agent` | Notes captured during conversations |

Two agents never write to the same block.

## 5. Scopes and folders

The vault is organised by **scope**: an area of life with its own context. Each scope is a top-level folder with a `scope.md` (`kind`, `sensitivity`, `parent`, `status`, and any rules that apply only there).

- **`personal/` always exists.** Other scopes are added as life needs them: `family/`, one per company or organization (e.g. `acme/`), a side project, a property, a club.
- **Sub-scopes** are folders inside a scope with their own `scope.md` and `parent:` (e.g. `personal/career/`).
- **Everything is private.** Scopes categorise context; they don't share it. `sensitivity: normal | high` sets how carefully agents quote a scope.

### Inside every scope

The same folders, each created only when its first note needs it:

| Folder | Holds |
|---|---|
| `goals/` | Results wanted by a date (`quarter-focus.md`, `yearly-goals.md` live in `personal/goals/`) |
| `projects/` | Efforts with a finish line (`status: someday` for maybe-later) |
| `areas/` | Things maintained forever (health, money, the house, a platform at work) |
| `people/` | One note per person or organization (`type: org`) |
| `decisions/` | One note per decision: options, choice, reasons, review date |
| `records/<kind>/` | One note per recurring item with an ID: PRs, tickets, repairs, appointments, claims (section 11) |
| `inventory/` | Things owned or maintained, one note each with properties (`_templates/item.md`): cars, devices, clothes, appliances, services |
| `routines/` | Recurring procedures, checklists and habits (`_templates/routine.md`) |
| `knowledge/` | What the human learned or wants to reference, in their words |
| `lists/` | Collections they keep adding to (wishlist, gifts, books). Never quoted in digests |
| `documents/` | One card per original file kept outside the vault (`playbooks/documents.md`) |
| `tasks/` | One note per task (`_templates/task.md`), `scope:` set to the scope |
| `radars/` | Awareness: one note per thing to watch (sources, cadence, lens, allowed actions). See section 12 |
| `private/` | Private media. Never leaves the vault, never described |

### Shared at the root

| Path | Holds |
|---|---|
| `home.md` | Dashboard, rebuilt after each digest |
| `about.md` | The human: background, values, preferences, routines |
| `00-inbox/` | To process. `handwritten/` page photos, `_import/` raw exports, `_done/` processed |
| `journal/` | `daily/` (the human's), `digests/`, `sessions/`, `weekly/`, `monthly/` |
| `sources/<source>/` | Raw imports from other apps. Archive, not a to-do list |
| `views/` | Bases views across scopes (e.g. `Tasks.base`) |
| `playbooks/`, `_templates/`, `_attachments/` | Routines, templates, files |

### Rules

- **Every note lives in exactly one scope**: where it belongs, not where it was mentioned. Other scopes link to it. No copies.
- Not sure which scope? `00-inbox/` with ❓.
- **New scopes are suggested, never created.** In the weekly review, if several items over 2+ weeks don't fit any scope (a new employer, a side project, a property, a club), propose one, or a sub-scope, and wait for the human's OK. Rule of thumb: its own world (people, rules, lifetime) → new scope; part of an existing one → sub-scope or project.

### Where does it go?

| It's… | Put it in |
|---|---|
| A quick thought or "save this" | `00-inbox/` |
| Something with a finish line | `<scope>/projects/` |
| Something maintained forever | `<scope>/areas/` |
| A result wanted by a date | `<scope>/goals/` |
| A choice worth remembering the reasons for | `<scope>/decisions/` |
| Someone, or an organization | `<scope>/people/` |
| Something owned (a car, a laptop, a coat) | `<scope>/inventory/` |
| A PR, ticket, repair, appointment | `<scope>/records/<kind>/` |
| Something learned or to reference | `<scope>/knowledge/` |
| A file (PDF, statement, contract…) | Original outside the vault + card in `<scope>/documents/` |
| Raw material from another app | `sources/` |
| What happened today | `journal/daily/` |

### Status values

`active` · `paused` · `someday` · `done` · `archived`

## 6. Naming and format

- Daily: `journal/daily/YYYY-MM-DD.md` · Digests: `journal/digests/YYYY-MM-DD-am.md` / `-pm.md`
- Weekly: `journal/weekly/YYYY-Www.md` (ISO week)
- Inbox: `00-inbox/YYYY-MM-DD-HHmm-<slug>.md`
- Everything else: `kebab-case-title.md`
- Links: `[[note-name]]`. Tasks: `- [ ]` / `- [x]`.

Base frontmatter:

```yaml
---
type: daily | digest | weekly | goal | project | area | person | org | decision | habit | knowledge | document | inbox | import
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: human | <agent-name>
visibility: private | shareable
status: active | paused | someday | done | archived   # where it applies
tags: []
---
```

## 7. Handwritten notes

Photos or PDFs of handwritten pages go in `00-inbox/handwritten/`. Transcribe word for word into that day's daily note under a `Captured` section, with the image embedded; the transcript counts as the human's text. Mark illegible words ❓, never guess names, numbers or dates, and move the original to `00-inbox/handwritten/done/`. Suggestions spotted in it go in the next digest.

## 8. Playbooks

| Task | Playbook |
|---|---|
| Morning / evening digests | `playbooks/morning.md`, `playbooks/evening.md` |
| Weekly review | `playbooks/weekly.md` |
| Monthly review | `playbooks/monthly.md` |
| Shared steps for every run | `playbooks/_every-run.md` |
| Importing notes/files from other apps | `playbooks/import.md` |
| Keeping and looking up documents | `playbooks/documents.md` |
| Radars (awareness) | `playbooks/radar.md` |

## 9. Tasks

One note per task in the scope's `tasks/` (`_templates/task.md`). Any agent in any conversation creates a task for each to-do the human mentions and updates its status when it's resolved, even elsewhere, adding a line saying how. Never delete: use `status: done` or `dropped`. `views/Tasks.base` shows them across scopes.

## 10. Session notes

Any conversation that produced something worth keeping ends with a note in `journal/sessions/YYYY-MM-DD-HHmm-<topic>.md` (`_templates/session.md`): what was done, decisions and why, new facts about the human, open items, links to notes touched. New durable facts are proposed for `about.md`, not written there directly. Skip small talk, one-off answers and secrets.

## 11. Records

Items with a stable ID that come up across conversations get one note each, named by the ID, in `<scope>/records/<kind>/` (e.g. `records/prs/<repo>#<number> <title>.md`). Read it before discussing the item; after, append a signed entry (findings, decisions, the human's take, follow-ups, link to the session note). Store summaries and takes, not diffs or threads: link those. When the item closes, set `status`; never delete.

## 12. Radars (awareness)

Radars watch sources (code, chat, mail, meetings, news, markets, health…), compare what's new with the vault, and report or act through the human's own lens. Each radar is a note in `<scope>/radars/`; the engine is `playbooks/radar.md`. Every run checks which active radars are due. Actions: `save` and `prepare` only when the radar lists them; anything that sends, posts, buys or books needs the human's explicit OK each time.

## 13. When in doubt

Don't act. Write a `suggestion` block or ask.

## Settings

Edit these for your vault.

```yaml
timezone: UTC   # your IANA timezone
digest_morning: "07:00"
digest_evening: "19:00"
weekly_review: "friday 12:00"
monthly_review: "1st 00:00"
agents: [digest-agent, import-agent, docs-agent, chat-agent]
auto_file_inbox: false        # true lets agents file inbox items without approval
documents_root: <path to originals folder, e.g. ~/GoogleDrive-personal/My Drive/Documents>
```
