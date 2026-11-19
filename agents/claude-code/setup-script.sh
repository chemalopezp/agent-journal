#!/bin/bash
# Cloud environment setup for agent-journal. Runs before every fresh session and stays fast:
# it downloads one tagged release, installs the journal skill (the base: instructions, context,
# awareness) and its two scripts (vault-sync, drive-setup), then writes the Claude instructions.
# The session itself syncs the vault in the background with `vault-sync`.
#
# Needs network access to codeload.github.com (release tarball) or github.com (git clone fallback).
# Optional: AGENT_JOURNAL_REPO (default below) and AGENT_JOURNAL_VERSION (a tag).
REPO="${AGENT_JOURNAL_REPO:-chemalopezp/agent-journal}"
VERSION="${AGENT_JOURNAL_VERSION:-v0.1.0}"
SKILL="$HOME/.claude/skills/journal"
log() { echo "[setup] $*"; }

log "journal skill"
TMP="$(mktemp -d)"
# The release tarball first; if the network blocks codeload.github.com, a shallow git clone of the tag.
if curl -fsSL "https://codeload.github.com/$REPO/tar.gz/refs/tags/$VERSION" 2>/dev/null | tar -xz -C "$TMP" 2>/dev/null \
   && [ -f "$TMP"/*/skills/journal/SKILL.md ]; then SRC="$(echo "$TMP"/*)"; HOW="tarball"
elif rm -rf "$TMP" && mkdir -p "$TMP" \
   && git clone -q --depth 1 --branch "$VERSION" "https://github.com/$REPO.git" "$TMP/repo" 2>/dev/null \
   && [ -f "$TMP/repo/skills/journal/SKILL.md" ]; then SRC="$TMP/repo"; HOW="git clone"
fi
if [ -n "$SRC" ]; then
  mkdir -p "$HOME/.claude/skills" && rm -rf "$SKILL" && cp -r "$SRC/skills/journal" "$SKILL" && log "skill ok ($VERSION, $HOW)"
else log "skill FAILED to download ($REPO $VERSION): allow codeload.github.com or github.com in the network settings"; fi
rm -rf "$TMP"

for s in memory/scripts/vault-sync engine/connectors/drive-setup; do
  name="$(basename "$s")"
  if [ -f "$SKILL/$s" ]; then install -m 755 "$SKILL/$s" "/usr/local/bin/$name" && log "$name ok"
  else log "$name missing from the skill"; fi
done

log "Claude instructions (~/.claude/CLAUDE.md)"
mkdir -p "$HOME/.claude"
cat > "$HOME/.claude/CLAUDE.md" <<'MD'
# My personal agent

My notes are an Obsidian vault at `~/vault`, synced with Obsidian Sync.

**Don't make me wait for it.** At the start of every conversation, run `vault-sync` in the background (it installs `ob` if needed, links `~/vault` the first time, and syncs). Don't wait for it:
- If the request doesn't need my notes, answer right away.
- When you need context (my plans, work, people, past decisions, or something to save), check `vault-sync --status`; once it says ready, use the journal skill: its base, plus my rules in `~/vault/AGENTS.md` and my runs in `~/vault/runs/`, which win on a conflict.

Rules for syncing: only ever use `vault-sync` (never run `ob sync` directly, never a second local copy, never kill a running sync: a sync cut off halfway can push deletions). Run `vault-sync` again after writing to the vault.

Need my document originals in Google Drive (read-only)? Run `drive-setup` once, then use `rclone ... pdrive:`.
MD
log "instructions ok"
exit 0
