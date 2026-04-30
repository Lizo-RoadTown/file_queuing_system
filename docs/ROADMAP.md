# Project Roadmap

*Current as of April 23, 2026.*

## What Is Working

The queue is live. `/checkout`, `/release`, and `/approve` all work. Files move automatically between stages. The reviewer integrity check (you cannot review your own submission) is enforced. There are open issues for active papers.

## Active Work

Two forks are in progress. One adds a structured working copy and review notes on `/checkout`, with a check that notes are filled in before `/approve` succeeds. The other builds on that by auto-generating a diff report on approval, using `#SOURCE:` and `#CHANGED:` inline annotations from the notebook.

## Merge Order

1. Reviewer copy + notes fork → main
2. Diff report fork → main (after #1 is merged)

## Next Steps

| Phase | Work |
|---|---|
| 1 | Confirm annotation conventions (`#SOURCE:`, `#CHANGED:`); agree on folder structure standard |
| 2 | Merge reviewer copy + notes + pre-approve validation |
| 3 | Merge diff report script (only after Phase 2) |

## Codespaces

GitHub Codespaces is set up and confirmed working. Reviewers open a Codespace from the repository page and get a fully configured environment with no local installation required. See [CODESPACES_GUIDE.md](CODESPACES_GUIDE.md).
