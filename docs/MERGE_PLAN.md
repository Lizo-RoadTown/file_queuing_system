# Merge Plan

## Fork Structure

| Fork | Contains |
|---|---|
| Fork 1 | Annotated reproduction notebook (`#SOURCE:`, `#CHANGED:`) |
| Fork 2 | Diff report generated from Fork 1 via `generate_diff_report.py` |

## Merge Order

1. Fork 1 → main
2. Fork 2 → main (after Fork 1 is merged)

## Before Merging

- All cells run without errors
- All `#SOURCE:` annotations have a page number
- All `#CHANGED:` annotations have a reason
- PR approved by student lead
- Do not approve your own work

## Opening a PR

Go to **Pull requests → New pull request**, set the base and compare branches, and request a review from the student lead.
