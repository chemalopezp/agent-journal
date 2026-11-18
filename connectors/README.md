# Connectors

How agents read each source a radar can watch. Generic: no accounts, IDs or personal choices here. Your vault's radar notes say which connectors to use (`sources:`) and what to look for.

Every connector note answers the same questions:
- **Access:** how the agent reaches it (claude.ai connector, CLI, API token) and where credentials live (environment secrets, never the vault or this repo).
- **What's new:** how to collect only items since the radar's `last_run` or `cursor`.
- **Keep:** what to save in the vault and where.
- **Limits:** rate limits, retention, what's read-only.

| Connector | Status |
|---|---|
| [GitHub](github.md) | ready |
| [Slack](slack.md) | ready |
| [Granola](granola.md) | ready |
| [Gmail](gmail.md) | ready |
| [Google Drive](google-drive.md) | ready (read-only originals) |
| [Web and news](web.md) | ready |
| [Strava / Google Health](health.md) | planned |
