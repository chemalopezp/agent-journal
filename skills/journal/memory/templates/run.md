---
type: run
base:                    # a base run to build on (e.g. Day); leave empty for your own run. With a base, fill in only what you change
status: draft            # draft | active | paused
cadence: daily 07:00     # live | hourly | daily HH:MM | weekly <day> HH:MM | monthly <day> HH:MM | quarterly | yearly | on request
period:                  # for period runs: day | week | month | quarter | year
sources:                 # vault, or e.g. "github: owner/repo (my PRs)", "slack: #channel", "gmail: label:bills"
  - vault
actions: [save]          # save | prepare  (sending, posting, buying never happen without an OK)
alert:                   # what to put first, marked ⚠️
author: human
last_run:
cursor:
---
# {{title}}

## Lens
With a base run: what to add to its lens (or set `lens: replace` above to write your own).
Otherwise: what matters to me here, how to judge it, and what a good result looks like.
