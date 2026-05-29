# Merge Plan (obsolete)

This document described a two-fork merge plan used during early development of the queue system. **It no longer matches how the system works.**

The previous plan had reviewers work on two parallel forks, one carrying the annotated reproduction notebook, one carrying an auto-generated diff report, and merged them to main in order. That structure was replaced on May 22, 2026 by a simpler model:

- Reviewers submit a single folder via a direct pull request against `reviews/awaiting-review-2/`.
- Reviewer 2 claims the resulting issue via `/checkout`, edits the `review-copy/` notebook in place, and finalizes with `/approve` (or escalates with `/dispute`).
- No automated diff report is generated. The reviewer's `#CHANGED:` annotations and the git diff between `original/` and `review-copy/` serve as the record.

For current submission and review procedures, see:

- [CONTRIBUTING.md](../CONTRIBUTING.md), full reviewer walkthrough.
- [README.md](../README.md), system overview and command reference.
- [docs/PROCESS.md](PROCESS.md), the process the team agreed on.

`scripts/generate_diff_report.py` remains in the repository but is not invoked by any current workflow. It is preserved in case the team decides to re-integrate auto-generated diff artifacts in the future.
