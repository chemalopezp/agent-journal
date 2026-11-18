# GitHub

- **Access:** the `gh` CLI (or the GitHub connector), read-only. Never comment, review, approve or merge without the human's explicit OK for that action.
- **What's new:** PRs authored by the human, PRs where they're directly requested as reviewer (`user-review-requested:<handle>`, not team requests), and PRs touching paths listed in the radar. Compare `updatedAt` with the radar's `last_run`.
- **Live:** where the environment supports PR activity subscriptions, subscribe to each open PR the radar tracks and unsubscribe when it merges or closes.
- **Keep:** one record per PR in `<scope>/records/prs/<repo>#<number> <title>.md` (AGENTS.md, Records). Store summaries and the human's take, not diffs.
- **Limits:** read code from the default branch fetched fresh (`git fetch origin main`), not a stale checkout.
