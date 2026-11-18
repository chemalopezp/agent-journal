# Granola (meeting notes)

- **Access:** the Granola connector. Free plans keep notes 30 days and have no transcripts.
- **What's new:** meetings updated since `last_run` (`updated_after`).
- **Keep:** one file per meeting in `sources/granola/YYYY-MM-DD <title>.md` with `granola-id`, `url`, `sensitive`, and the summary and private notes as-is. Update in place if it changed; match on `granola-id`. Personal meetings (therapy, coaching, family, health, money) get `sensitive: true`.
- **Then:** tasks for the human into the right scope's `tasks/`, decisions proposed in `decisions/`.
- **Limits:** save the same hour or day; anything older than the retention window is gone.
