# Conversation (capture)

The main way things get into the vault: the person talks to an agent, by voice or text, in any conversation. The agent's job is to answer, and to quietly keep the vault current with what was said.

## Answer first

- Start the vault sync in the background; don't make the person wait for it.
- If the request needs context, read only what it needs (AGENTS.md, section 1).

## What to capture

Capture only what's worth remembering next week. Where each thing goes is in AGENTS.md, section 4; the most common:

| They say… | Capture as |
|---|---|
| How their day went, how they feel, what they think | `🗣️` entry in today's day note, **verbatim** |
| "I need to…", "remind me…" | `task` in the right scope's `plans/` |
| "Every Monday I…", "I want to swim 3 times a week" | `task` with `cadence` |
| "I did it", "went to the gym" | Log line on that task (and `status: done` if it was one-off) |
| An appointment, a birthday, a deadline | `event` |
| A choice and why | `decision`, with their reasons in their words |
| News about a person | That person's record: update the facts, add a `## Log` line |
| A change in a project or goal | Update it; `## Log` line |
| Something bought, owned, broken | `item`; a repair or claim is a `case` linked to it |
| A preference, routine, value | Propose it for `about.md`; write it once they confirm |
| A lesson or idea | `note` (only if it's distilled; otherwise the day note) |

Not sure which scope, or whether it's worth keeping? Ask in one short question, or create it in the best-guess scope with `status: triage` and a ❓.

## How to write it

- AGENTS.md section 5: their words verbatim under `🗣️`, agent text signed, facts updated with a `## Log` line, nothing deleted.
- Link everything captured to the session note (`source: "[[<session>]]"`).
- Voice transcripts mangle names: check against existing person records and `about.md`; mark uncertain names ❓ and facts `verified: false` rather than guess.
- Sensitive things (health, family, relationships, money) get `sensitive: true`, or go in a sensitive scope.

## Say what you saved

After capturing, tell the person in one line, e.g. *"Saved: task 'Renew passport' (family), and Ana's new job."* That's their chance to correct it. Group small updates; don't list every one.

## End of the conversation

If anything was captured or decided, write the session note (template `session`) and sync.

## Without file access

If this agent can't write to the vault (e.g. a chat app without a connector), don't pretend to save. End with a "📌 Save" block: date, the person's words or one line, and the suggested scope and type. The person pastes it into `sources/saves/`, and the next run files it.
