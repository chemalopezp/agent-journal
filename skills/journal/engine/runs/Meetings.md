---
type: run
cadence: hourly
sources: ["granola: meetings created or updated since last_run"]
actions: [save, prepare]
alert: a decision, or a request to me
---
# Meetings

A radar. Turn it on once a meeting-notes connector (e.g. Granola) is attached to your scheduler; see `engine/connectors/granola.md`.

## Lens
- Save every meeting to `sources/granola/` the same hour (notes may expire), then file what matters into the right scope: a work meeting, a therapy session and a school meeting go to different scopes.
- Tasks assigned to me → tasks; decisions → decision notes, for me to confirm.
- Personal meetings (therapy, coaching, family, health, money) are `sensitive: true`.
