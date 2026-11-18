---
type: radar
status: draft            # draft | active | paused
cadence: daily 07:00     # on request | live | hourly | daily HH:MM | weekly <day> HH:MM | monthly <day>
sources:                 # where to look, e.g. "github: owner/repo (my PRs)", "slack: #channel", "gmail: label:bills", "web: news on X"
  -
context:                 # vault notes or folders to compare against
  -
actions: [save]          # save | prepare  (do is never automatic)
output: digest           # digest | report | both
alert:                   # when to put it first, marked ⚠️
last_run:
cursor:
---
# {{title}}

## Lens
What matters to me here, how to judge it, and what a good result looks like.

## Notes
