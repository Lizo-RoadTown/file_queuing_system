# Archive

This folder holds scripts that were once part of the live system but are no longer wired into any workflow. They are preserved here, with a header comment explaining their history, in case the team decides to re-integrate them.

## Why archive instead of delete

Archived scripts are kept because:

- They document a design path the team has already validated and may revisit.
- They preserve the work that went into them, so a future re-integration does not start from scratch.
- They make the deprecation visible. An empty `scripts/` folder hides the history; an `archive/` folder names it.

## What lives here

| File | Archived on | Was wired in by | Was removed by | Replaced with |
|---|---|---|---|---|
| `generate_diff_report.py` | 2026-05-29 | `672efca` (2026-04-21): "feat: wire diff report into /approve workflow" | `4c6a8a9` (2026-05-22): "added a new command /dispute and got rid of the extra copy" | Reviewer `#CHANGED:` annotations + git diff between `original/` and `review-copy/` + issue comments via `/dispute` |

## How to re-integrate something from this folder

If the team decides to restore a script:

1. Read the script's header comment to understand why it was archived and what replaced it.
2. Check `manage-queue.yml` (or the relevant workflow) to see where the original invocation sat. The git commit named in the header is a useful starting point: `git show <sha>` shows the wiring as it existed.
3. Move the file out of `archive/` back to `scripts/` and remove the header comment block.
4. Re-wire the workflow.

## How to delete something from this folder

If the team decides to drop a script entirely:

1. Update the table above to remove the row.
2. `git rm` the file.
3. Note the deletion in the commit message so the history is searchable.
