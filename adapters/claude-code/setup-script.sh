#!/bin/bash
# Cloud environment setup for agent-journal. Runs before every fresh session and stays fast:
# it installs two small scripts from a tagged release of the repo and writes the Claude
# instructions. The session itself syncs the vault in the background with `vault-sync`.
#
# Needs network access to raw.githubusercontent.com.
# Optional: AGENT_JOURNAL_REPO (default below) and AGENT_JOURNAL_VERSION (a tag).
REPO="${AGENT_JOURNAL_REPO:-<github-user>/agent-journal}"
VERSION="${AGENT_JOURNAL_VERSION:-v0.1.0}"
BASE="https://raw.githubusercontent.com/$REPO/$VERSION/scripts"
log() { echo "[setup] $*"; }

for s in vault-sync drive-setup; do
  if curl -fsSL "$BASE/$s" -o "/usr/local/bin/$s.new" && head -1 "/usr/local/bin/$s.new" | grep -q '^#!/bin/bash'; then
    mv "/usr/local/bin/$s.new" "/usr/local/bin/$s" && chmod 755 "/usr/local/bin/$s" && log "$s ok ($VERSION)"
  else
    rm -f "/usr/local/bin/$s.new"; log "$s FAILED to download from $BASE"
  fi
done

log "Claude instructions (~/.claude/CLAUDE.md)"
mkdir -p "$HOME/.claude"
cat > "$HOME/.claude/CLAUDE.md" <<'MD'
# My journal

My journal and second brain is an Obsidian vault at `~/vault`, synced with Obsidian Sync.

**Don't make me wait for it.** At the start of every conversation, run `vault-sync` in the background (it installs `ob` if needed, links `~/vault` the first time, and syncs). Don't wait for it:
- If the request doesn't need my notes, answer right away.
- When you need context (my plans, work, people, past decisions, or something to save), check `vault-sync --status`; once it says ready, read `~/vault/AGENTS.md` and follow it. All instructions live there.

Rules for syncing: only ever use `vault-sync` (never run `ob sync` directly, never a second local copy, never kill a running sync: a sync cut off halfway can push deletions). Run `vault-sync` again after writing to the vault.

Need my document originals in Google Drive (read-only)? Run `drive-setup` once, then use `rclone ... pdrive:`.
MD
log "instructions ok"
exit 0
