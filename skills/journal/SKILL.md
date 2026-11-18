---
name: journal
description: Maintain a personal markdown journal (Obsidian vault or plain folder) under a strict contract. Use for morning/evening digests, the weekly review, importing notes or files (e.g. Google Keep), saving something from the conversation to the journal, or setting up a new journal. Also keeps a catalog of personal documents stored outside the vault. Triggers - "digest", "weekly review", "import this", "keep this document", "what does my <document> say", "save this to my journal", "remember this", "set up my journal".
---

# Journal

## 1. Find the vault

- The current folder, if it has `journal/` and `00-inbox/` (or an `AGENTS.md` that describes a journal).
- Otherwise ask the human for the path. Never guess.

## 2. Load the rules

- If the vault has its own `AGENTS.md`, **it wins** — it's the human's version.
- Otherwise use `AGENTS.md` bundled with this skill.

Follow the rules strictly: append-only, signed blocks, private by default, no secrets.

## 3. Pick the task

| Request | Do |
|---|---|
| Digest (morning/evening) | `playbooks/morning.md`, `playbooks/evening.md` |
| Weekly review | `playbooks/weekly.md` |
| Monthly review | `playbooks/monthly.md` |
| Import notes from other apps | `playbooks/import.md` |
| Keep or look up a document | `playbooks/documents.md` |
| "Save / remember this" | Capture (below) |
| Set up a new journal | Init (below) |

## Capture

Write a new file `00-inbox/YYYY-MM-DD-HHmm-<slug>.md` with frontmatter (`type: inbox`, `author: chat-agent`, `visibility: private`) and a signed `note` block. Confirm in one line what was saved and where.

## Init

Only in an empty or new folder, and after the human confirms the path:

1. Copy `starter/` contents into it. It starts with one scope, `personal/`; ask whether to add others now (family, a company…), each with its own `scope.md` from `_templates/scope.md`.
2. Copy `AGENTS.md` and `playbooks/` into its root.
3. Ask for the Settings values (timezone, digest times) and fill them in.

## No file access

If this agent can't read or write the vault (e.g. a chat app without a connector), don't pretend to save. Answer with a "📌 Save" block (date, one line, suggested folder) for the human to paste into `00-inbox/`.
