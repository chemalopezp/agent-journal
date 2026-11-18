# Playbook: radars (awareness)

A **radar** watches some sources, compares what's new with the vault, applies the human's own lens, then reports or acts. Each radar is one note in a scope's `radars/` folder (`_templates/radar.md`). The note holds everything personal: sources, cadence, context, lens, allowed actions. This playbook is only the engine.

## When a radar runs

Its `cadence` decides:

| cadence | Runs |
|---|---|
| `on request` | When the human asks ("run the dev radar") in any conversation |
| `live` | On events where a source can push them (e.g. subscribed PR activity), plus every hourly run to discover new items |
| `hourly` | In the hourly awareness run |
| `daily HH:MM` | In the first run at or after that time (morning or evening digest, or the hourly run) |
| `weekly <day> HH:MM` | Same, on that day (usually the weekly review) |
| `monthly <day>` | Same, on that day (usually the monthly review) |

A radar is **due** when its cadence time has passed since `last_run`. Every run (digests, reviews, the hourly awareness run) checks all `status: active` radars in every scope and runs the due ones. Radars with `status: draft` or `paused` never run.

## Each run of a radar

1. **Collect** what's new in each source since `last_run` (cursor). Never reprocess older items.
2. **Keep** what's worth keeping in the vault: records (`<scope>/records/<kind>/`), `sources/<source>/`, tasks. Respect the scope's sensitivity.
3. **Compare** with the `context` notes: what's new, what changed, what contradicts a plan or decision, what's overdue.
4. **Analyze** with the radar's lens (the body of its note).
5. **Report** where `output` says: a section in the current digest (`digest`), the radar's own report note (`report` → `<scope>/radars/reports/<radar> YYYY-MM-DD.md`), or both. Anything matching `alert` goes first, marked ⚠️.
6. **Act** only within `actions` (below). Then set `last_run` (and `cursor`, if the source has one) in the radar's frontmatter.

## Actions

| Level | Examples | Rule |
|---|---|---|
| `save` | records, meeting notes, transcripts, tasks from requests made to the human | allowed if listed |
| `prepare` | draft replies, meeting briefs, PR review drafts, decision notes | allowed if listed; drafts stay in the vault and are shown to the human |
| `do` | send, post, comment, buy, sell, book | **never** without the human's explicit OK for that single action |

Money and health radars give analysis and recommendations only.

## Event subscriptions (`live`)

Where the environment supports it, keep live sources subscribed (for example PR activity for each open PR in a radar's scope) and unsubscribe when the item closes. Events run only that radar's steps for that item.
