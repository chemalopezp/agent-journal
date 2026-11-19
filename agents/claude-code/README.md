# Claude Code

Full support: conversation capture, scheduled runs, radars, imports, documents. Works on desktop, web and phone (cloud sessions). What agents do is defined in `skills/journal/` (see [agents/README.md](../README.md)); this page only covers the Claude Code side.

These steps assume a new vault. Already have one? See [Using an existing vault](#using-an-existing-vault).

## 1. Create the vault

1. In the Obsidian app, create a new, empty vault.
2. Turn on **Sync** (Settings → Sync) and create a remote vault for it. Note its name; if you choose end-to-end encryption, note the password too. Cloud sessions need both.
3. In Settings → Sync, turn on syncing of **main settings** and **core plugin settings** on each device, so the settings Init applies reach your phone.

Obsidian Sync is what lets cloud sessions (phone and web) reach the vault. On your computer alone, any folder works.

## 2. Install the plugin

```
/plugin marketplace add chemalopezp/agent-journal
/plugin install journal@agent-journal
```

Or copy `skills/journal/` to `~/.claude/skills/journal/`. The plugin files (`.claude-plugin/`) live at the root of this repo, not in this folder, because Claude Code looks for them there and the plugin has to contain `skills/`.

## 3. Set up the journal

Start Claude Code in the vault folder and say "set up my journal here". It creates your scope, settings, `about.md` and the runs you want, sets Obsidian's folders and core plugins (attachments, daily notes, templates, Bases) and adds a starter view in `views/` (`SKILL.md`, Init); nothing else from the base is copied. Reopen the vault afterwards so Obsidian reads the new settings. Add a `CLAUDE.md` in the vault root containing `@AGENTS.md`, so your own rules load in every session there. Obsidian syncs it all.

## 4. Cloud sessions and schedules (phone and web)

1. **Get your Obsidian auth token**, on your computer:
   ```
   npm install -g obsidian-headless
   ob login
   ```
   Then copy the token from `~/.obsidian-headless/auth_token`. Obsidian's docs only say to set `OBSIDIAN_AUTH_TOKEN` for non-interactive use; the file location is what users report, and may change between versions. Don't run `ob logout` afterwards: it invalidates the token.
2. **Set the environment variables** in the cloud environment: `OBSIDIAN_AUTH_TOKEN` and `OBSIDIAN_VAULT_PASSWORD` (if encrypted) as **secrets**, and `OBSIDIAN_VAULT_NAME`. The full list is in [agents/README.md](../README.md#environment-variables). Never paste the token into a chat, the vault or this repo.
3. **Allow** `codeload.github.com` in the environment's network settings. If you can't, the script falls back to a `git clone` from `github.com`, which most environments allow.
4. **Paste [`setup-script.sh`](setup-script.sh)** into the environment's setup script. It runs before every fresh session and stays fast. It installs:
   - **The journal skill** (`instructions/`, `memory/`, `engine/`) into `~/.claude/skills/journal/`, from a tagged release. Optional variables: `AGENT_JOURNAL_REPO` (a fork) and `AGENT_JOURNAL_VERSION` (a tag).
   - **`vault-sync`** (from `memory/scripts/`): installs Obsidian Headless if missing, links `~/vault` the first time, and syncs. One sync at a time. If the **first** sync in a container fails partway, it wipes the partial copy and starts fresh (up to 3 tries): a half-downloaded copy must never sync, because it would push the missing files as deletions.
   - **`drive-setup`** (optional): on-demand read-only access to document originals in Google Drive (`engine/connectors/google-drive.md`).
   - **`~/.claude/CLAUDE.md`**: tells every session to start `vault-sync` in the background, answer right away when the vault isn't needed, and use the journal skill plus the vault's `AGENTS.md` once it's ready.

**Safety rules agents follow:** only ever sync with `vault-sync`; never put a timeout on a sync or kill one; never keep a second local copy of the vault.

## 5. Runs

Runs are notes in the vault's `runs/` (briefings, period runs, radars), each with its own cadence; the engine is `engine/run.md`; a run note with `base: Day` turns on the base Day run. So schedules don't need to know what each run does:

```
Hourly   "Run what's due: the journal skill's engine/run.md with the run notes in ~/vault/runs/, following ~/vault/AGENTS.md. Sync only with vault-sync."
```

One hourly schedule is enough: at each tick it runs whatever is due (the morning briefing at the first tick after 7:00, the week run on Friday at noon…). Add a separate schedule only if a run must post into a specific conversation, e.g. the briefings you read on your phone.

Give the schedule the connectors your runs' sources need (e.g. Granola, Slack, Gmail). A schedule's prompt can usually only be changed from the conversation it posts into, which is one more reason to keep it to one line.

**Live events:** for runs with `cadence: live` (e.g. pull requests), subscribe the conversation that receives your briefings to the relevant activity; the hourly tick picks up new items.

## 6. Conversation, imports and documents

Nothing extra to set up: conversations follow `instructions/conversation.md`, imports `instructions/import.md`, documents `instructions/documents.md` (set `documents_root` in your vault `AGENTS.md` settings).

## Using an existing vault

Point Claude Code at it (start in its folder, or link `~/vault` to it) and say "set up my journal here": Init only adds what's missing and never overwrites a note. If the vault has its own folder layout, ask the agent first to propose how it maps to this one, as a dry run you review before anything moves.
