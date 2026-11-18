# Every run

Shared steps for `morning.md`, `evening.md`, `weekly.md` and `monthly.md`. `AGENTS.md` rules always win.

## Start
1. Pull the latest vault (your sync tool).
2. Back up anything that expires (e.g. meeting notes with limited retention) into `sources/<source>/`.
3. Transcribe new pages in `00-inbox/handwritten/` (AGENTS.md, Handwritten notes).

## Radars
Run every active radar that's due (`playbooks/radar.md`), and put their sections in this run's output.

## Output
- Each run writes its own file with a signed `digest` or `review` block:
  - morning `journal/digests/YYYY-MM-DD-am.md`, evening `-pm.md`
  - weekly `journal/weekly/YYYY-Www.md`, monthly `journal/monthly/YYYY-MM.md`
- Never write into the human's daily note.
- 15 lines max for daily runs. Link, don't copy. Nothing private or sensitive in notifications.

## End
1. Rewrite `home.md`.
2. Push the vault.
