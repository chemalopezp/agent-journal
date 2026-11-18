# Adapter: Claude Code

Full support: read, signed writes, digests, imports.

## Setup

1. Put the vault on disk where Claude Code runs, synced however you like (e.g. Obsidian Sync with Obsidian Headless, or a synced folder).
2. Install the skill (see the main README), or copy `skills/journal/AGENTS.md` and `skills/journal/playbooks/` into the vault root.
3. Add `CLAUDE.md` in the vault root so Claude Code loads the contract:

   ```markdown
   @AGENTS.md
   ```

4. Start Claude Code in the vault folder.

## Scheduled runs

One schedule per run. Keep each prompt to one line, so changing what a run does is a vault edit, never a schedule edit:

```
Morning (weekdays 7:00):   "Run playbooks/morning.md from the vault, following AGENTS.md."
Evening (weekdays 19:00):  "Run playbooks/evening.md from the vault, following AGENTS.md."
Weekly (Fridays 12:00):    "Run playbooks/weekly.md from the vault, following AGENTS.md."
Monthly (1st, 00:00):      "Run playbooks/monthly.md from the vault, following AGENTS.md."
```

## Cloud sessions (phone and web)

Paste `setup-script.sh` into the cloud environment's setup script. It downloads nothing at startup, so sessions open instantly. It installs:

- **`vault-sync`**: installs Obsidian Headless if missing, links `~/vault` the first time, and syncs. One sync at a time. If the **first** sync in a container fails partway, it wipes the partial copy and starts fresh (up to 3 tries): a half-downloaded copy must never sync again, because it would push the missing files as deletions.
- **`drive-setup`** (optional): on-demand rclone + 1Password CLI for read-only access to your document originals. Set `OP_DRIVE_KEY_ITEM` to the 1Password document holding the key.
- **`~/.claude/CLAUDE.md`**: tells every session to start `vault-sync` in the background, answer right away when the vault isn't needed, and follow the vault's `AGENTS.md` once it's ready.

Environment variables: `OBSIDIAN_AUTH_TOKEN`, `OBSIDIAN_VAULT_NAME`, `OBSIDIAN_VAULT_PASSWORD` (end-to-end encryption), and for Drive `OP_SERVICE_ACCOUNT_TOKEN` and the `RCLONE_CONFIG_PDRIVE_*` settings. Secrets belong in the environment's secret settings, never in the vault or this repo.

Safety rules agents follow: only ever sync with `vault-sync`; never put a timeout on a sync or kill one; never keep a second local copy of the vault.

## Originals storage (document catalog)

Originals live outside the vault (see `playbooks/documents.md`); set `documents_root` in `AGENTS.md → Settings`. Claude Code reaches them as files, so **no claude.ai connector is needed** — and a work account's connectors stay untouched.

- **On your computer:** Google Drive for Desktop (or Dropbox/iCloud) signed in to your **personal** account. It can run alongside a work account; each shows as its own folder. Point `documents_root` there.
- **Cloud sessions:** use a sync tool such as rclone with your personal account. Put its credential in the cloud environment's secrets, never in the repo or the vault.

## Imports

Drop files or paste notes in the conversation and say "import this", or put them in `00-inbox/_import/` and say "process imports". Follows `playbooks/import.md`.
