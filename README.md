# Personal Agent Journal

**Make any AI agent your personal agent.**
Instructions, context and awareness, in plain markdown you own.

You talk to your agent, by voice or text, in any conversation. It files what matters into your vault: what you said about your day (in your own words), tasks, events, decisions, people, projects, things you own. Runs keep it current on their own: they consolidate each day, week, month and year into what's true now, brief you, and watch your code, chat, mail and meetings for what needs you. You read and correct all of it in Obsidian.

## Three components

A model on its own knows nothing about you and does nothing until asked. Three things make it a personal agent:

| Component | What it is | Base (this repo, `skills/journal/`) | Yours (your vault) |
|---|---|---|---|
| **Instructions** | How agents behave: what to save and where, how to write, what it may never do | `instructions/`: the contract (`AGENTS.md`) and procedures for conversation, imports, documents | `AGENTS.md`: your rules and settings · `scope.md` per scope |
| **Context** | Memory. What it knows about you, as notes with types | `memory/`: a template per note type; scripts to sync and check the vault | Your notes · `templates/` overrides |
| **Awareness** | Gather and parse data souruces. What it does on its own, and when | `engine/`: the run engine, base runs (briefings, day to year), connectors (GitHub, Slack, mail, meetings…) | `runs/`: which runs are on, when, and your changes |

In the skill, the folders use the technical names: `instructions/`, `memory/` (the shape of memory: templates and scripts; the memory itself is your vault) and `engine/`.

The base is the same for everyone, versioned, and never copied into your vault. Your vault holds only your notes and what you customise; on a conflict, yours wins. Which agent runs it is replaceable: Claude Code today, others through [`agents/`](agents/README.md).

```
 you ──talk (voice / text)──▶ agent ──files & updates──▶ vault (markdown, synced)
        instructions           ▲                            │  context
                               └── reads context ◀──────────┘
 runs (each with its cadence) ─▶ briefings · day/week/month/year: consolidate + review      awareness
                                 radars: GitHub · Slack · mail · meetings · news …
```

## Context: the memory model

Every note is one of four kinds of memory, which decides where it lives and how agents write it:

| Memory | Question | Lives in | Written |
|---|---|---|---|
| **Episodic** | What happened? | `timeline/` (days, weeks… and sessions), `sources/` (raw material) | Append only |
| **Semantic** | What's true? | `<scope>/records/`: people, orgs, items, notes, lists, documents | Updated in place, with a log line |
| **Prospective** | What's intended? | `<scope>/plans/`: goals, projects, tasks, decisions, events · `<scope>/cases/`: PRs, tickets, repairs | Status changes, never deleted |
| **Procedural** | How should agents behave? | `AGENTS.md`, `scope.md`, `runs/` | Only with your OK |

```
<scope>/        scope.md · plans/ · records/ · cases/       (personal/ always; add family/, a company…)
runs/           the runs you turned on, and your own
timeline/       day/ · week/ · month/ · quarter/ · year/ · sessions/
sources/        imports, meetings, handwritten pages, pasted saves, attachments
templates/      only templates that differ from the base
views/          saved views (Obsidian Bases)
about.md · AGENTS.md · home.md (optional)
```

Scopes separate parts of your life; each has the same three folders. Notes are found by their `type`, so you can organise subfolders however you like.

## Awareness: runs

A run is any agent job with a cadence, from live and hourly to yearly. Period runs (day, week, month, quarter, year) first **consolidate** what happened into what's true (project status daily, people and decisions weekly, goals monthly, yearly goals at year end), then **review** it for you. Briefings tell you what needs you; radars watch outside sources.

The base runs live in the repo. A note in your `runs/` with `base: Day` turns the Day run on, holds its state, and changes only what you want (time, sources, an extra line in its lens). Base runs improve with each version; your changes stay. One "run what's due" schedule is enough to drive them all.

## Principles

- **You talk, agents write.** Conversation is the input. You read, correct, and ask.
- **Your words stay yours.** What you dictate is saved verbatim; agents summarise around it, and your hand edits always win.
- **Memory consolidates.** Nothing is lost when old conversations scroll out of view.
- **Provenance.** Every agent change says who, when and from where (a conversation, a meeting, a run). Unconfirmed facts are marked until you confirm them. Nothing is deleted; things change status.
- **Private by default.** Nothing leaves the vault unless you ask for that specific thing. Sensitivity is set per scope or note; secrets are never stored.
- **Sources are data, never instructions.** An email or a meeting note can't tell an agent what to do; only you can.
- **Aware, not autonomous.** Runs save and prepare drafts. Anything that sends, posts, buys or books needs your OK, every time.
- **Plain files.** Markdown, YAML frontmatter and `[[wikilinks]]`. Obsidian is the viewer, not a requirement.

## What's in here

```
skills/journal/           The skill: install it in any agent that supports SKILL.md
  SKILL.md                Entry point: find the vault, load base and customization, pick the task, set up a vault
  instructions/           AGENTS.md (the contract) · conversation · import · documents
  memory/
    templates/            One per type: period, session, goal, project, task, decision, event, case,
                          person, item, note, list, document, run, scope, home; plus your AGENTS.md and about.md
    scripts/              validate_vault.py (validate a vault) · vault-sync (safe Obsidian Headless sync)
    obsidian/             Obsidian settings Init applies (folders, core plugins) and a starter view
  engine/
    run.md                The engine
    runs/                 Base runs: morning briefing, day, week, month, quarter, year, meetings
    connectors/           GitHub, Slack, Granola, Gmail, Google Drive (+ drive-setup), web; Keep and Gemini importers
agents/                   Set-up per agent platform (Claude Code for now) and the shared environment variables
.claude-plugin/           Lets Claude Code install this repo as a plugin
```

## Install (Claude Code)

Step by step in [`agents/claude-code/`](agents/claude-code/README.md):

1. Create a new vault in Obsidian and turn on Sync.
2. Install the plugin: `/plugin marketplace add chemalopezp/agent-journal`, then `/plugin install journal@agent-journal`.
3. In the vault folder, say "set up my journal here".
4. For phone and web: your Obsidian auth token as a secret, the setup script, and one "run what's due" schedule.

Other agents: many read `AGENTS.md` from the folder they work in, and several support `SKILL.md`; dedicated set-up pages will follow.

## Roadmap

- More connectors: calendar, health (Strava, Google Health), finance statements.
- More importers: Apple Notes, Evernote, Notion export.
- More agents: ChatGPT and others, each with its own set-up page.

## License

MIT
