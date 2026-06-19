# Reviewer System Design

The reviewer side of the SDE Review Queue handles the second review of each curated reproduction notebook. An independent reviewer (Reviewer 2) browses open issues, claims one with `/checkout`, re-runs the notebook, annotates changes with `#CHANGED:`, and finalizes with `/approve`. If they disagree with something, they escalate to the curator with `/dispute`. If they cannot finish, they return the item with `/release`.

The mechanism: a label-state machine over GitHub issues, a slash-command actor model implemented in `manage-queue.yml`, and a dispute-resolution branch that involves the curator only when Reviewer 2 raises `/dispute`. The audit trail is the GitHub issue timeline.

The full review process has three stages: curation, first review (the verifying teammate inside the curation pair), and second review (this document). The curator side is at `docs/system-design/curator/`.
