# GitHub

- **Access:** the `gh` CLI (or the GitHub connector), read-only. Never comment, review, approve or merge without the person's explicit OK for that action.
- **What's new:** PRs authored by the person, PRs where they're directly requested as reviewer (`user-review-requested:<handle>`, not team requests), and PRs touching paths listed in the radar. Compare `updatedAt` with the run's `last_run`.
- **Live:** where the environment supports PR activity subscriptions, subscribe to each open PR the run tracks and unsubscribe when it merges or closes.
- **Keep:** one case per PR in `<scope>/cases/<repo>#<number> <title>.md` (`kind: pr`; AGENTS.md, Cases). Store summaries and the person's take, not diffs.
- **Limits:** read code from the default branch fetched fresh (`git fetch origin main`), not a stale checkout.
