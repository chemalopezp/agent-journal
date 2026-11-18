# Slack

- **Access:** the Slack connector. Read-only unless the human asks to post a specific message.
- **What's new:** messages in the radar's channels since `last_run`, **including new replies on older threads** (check threads whose latest reply is newer than the last run). Mentions and DMs: search for the human's user ID.
- **Keep:** people and org changes as event records (`<scope>/records/events/`), requests to the human as tasks. Never copy whole threads; link them.
- **Limits:** surface only what the radar's lens asks for; never summarize a whole channel.
