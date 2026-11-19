# Agents

How to set up agent-journal on each agent platform. What an agent should *do* is defined once, in [`skills/journal/`](../skills/journal/SKILL.md); these pages only say how each platform does it.

## What every agent needs

| Need | Defined in |
|---|---|
| **Instructions:** the base from the skill, plus the person's customization from the vault | `instructions/AGENTS.md`, section 0 |
| **Memory:** reach the vault; read it, and write to it if the platform can | Platform-specific (each page below) |
| **Capture from conversation**, including the "📌 Save" fallback when it can't write | `instructions/conversation.md` |
| **Engine:** briefings, period runs (consolidate + review), radars | The engine `engine/run.md`; the run notes in the vault's `runs/`; sources in `engine/connectors/` |

Keep schedule prompts and custom instructions short: "run what's due", pointing at the engine and the run notes, so changing what a run does is a vault edit, never a settings edit.

| Agent | Reads the vault | Writes to it | Scheduled runs | Radars (external sources) |
|---|---|---|---|---|
| [Claude Code](claude-code/README.md) | yes | yes | yes | yes |

## Environment variables

The scripts read these, whatever agent runs them. Set them wherever your agent keeps environment settings (each page says where). **Secrets go only in the environment's secret settings**: never in the vault, this repo or a chat.

| Variable | Used by | Needed |
|---|---|---|
| `OBSIDIAN_AUTH_TOKEN` 🔒 | `vault-sync` (Obsidian Headless) | When the vault is in Obsidian Sync |
| `OBSIDIAN_VAULT_NAME` | `vault-sync` | Same |
| `OBSIDIAN_VAULT_PASSWORD` 🔒 | `vault-sync` | If the vault uses end-to-end encryption |
| `VAULT` | `vault-sync` | Optional; default `~/vault` |
| `AGENT_NAME` | Importers (how imported notes are signed) | Optional; default `Claude` |
| Drive variables | `drive-setup` | Only for document originals in Google Drive: listed in [`google-drive.md`](../skills/journal/engine/connectors/google-drive.md) |

Other connectors (GitHub, Slack, Gmail, Granola…) usually come from the agent platform's own integrations; each connector note says what it needs.

Example, as it would look in an environment settings screen (placeholders, not real values):

```
OBSIDIAN_VAULT_NAME=My vault
OBSIDIAN_AUTH_TOKEN=<secret>
OBSIDIAN_VAULT_PASSWORD=<secret>
```
