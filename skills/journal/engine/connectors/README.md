# Connectors

How agents read each source a run can watch. Generic: no accounts, IDs or personal choices here. Your vault's run notes say which connectors to use (`sources:`) and what to look for.

Every connector note answers the same questions:
- **Access:** how the agent reaches it (claude.ai connector, CLI, API token), the environment variables it needs, and where credentials live (environment secrets, never the vault or this repo).
- **What's new:** how to collect only items since the run's `last_run` or `cursor`.
- **Keep:** what to save in the vault and where.
- **Limits:** rate limits, retention, what's read-only.

| Connector | Status |
|---|---|
| [GitHub](github.md) | ready |
| [Slack](slack.md) | ready |
| [Granola](granola.md) | ready |
| [Gmail](gmail.md) | ready |
| [Google Drive](google-drive.md) | ready (read-only originals; `drive-setup` installs access) |
| [Web and news](web.md) | ready |
| Google Keep, Gemini (one-off imports from Google Takeout) | ready: `import_keep.py`, `import_gemini.py`, run as `instructions/import.md` describes |
| [Strava / Google Health](health.md) | planned |
