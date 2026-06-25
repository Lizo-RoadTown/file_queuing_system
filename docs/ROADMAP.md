# Project Roadmap

*Current as of May 29, 2026.*

---

## What is working

The queue runs end to end on GitHub. All six slash commands are live: `/checkout`, `/release`, `/approve`, `/dispute`, `/complete`, `/reject`. Files move automatically between `awaiting-review-2/`, `in-progress/`, and `completed/`. The reviewer integrity check (you cannot second-review your own submission) is enforced by both `/checkout` and `/approve`.

Issue tracking is automatic. `bootstrap-seed-issues.yml` creates a `[REVIEW]` issue whenever a folder appears under `reviews/awaiting-review-2/` on main. `update-queue-csv.yml` appends every new issue to `queue/review_log.csv`. `validate-submission.yml` checks PR shape and records the PR author as Reviewer 1.

Completed reviews are packaged and emailed automatically by `notify-on-complete.yml` (zip + SMTP send) when an issue gains the `complete` label, provided the SMTP secrets are configured. The workflow writes `emailed_to_recipient_on: <date>` into the folder's `review_metadata.yml` after a successful send.

Hand-committed completions (folders pushed directly into `reviews/completed/` without going through `/approve` or `/complete`) are caught by `auto-label-completed.yml`, which finds the matching issue and applies the `complete` label so `notify-on-complete.yml` handles the email.

`email-completed-reviews.yml` is the manual backfill, available via the Actions tab. It skips folders that already carry the `emailed_to_recipient_on` marker and accepts an optional `folder_name` input for sending a single folder. `scripts/email_completed_review.py` is the local fallback for when Actions cannot run.

The system has run in practice. Several papers have moved through the full happy path. At least one paper (Witbooi_Malaria) went through the dispute branch and was resolved by the curator with `/complete`.

---

## What is in progress or planned

| Area | Description | Status |
|---|---|---|
| System design documentation | Formal design-case docs under `docs/system-design/` matching the depth of the UX/UI Final report. Skeleton landed; prose pass pending. | In progress |
| Diff report integration | `scripts/generate_diff_report.py` exists but is not currently called by any workflow. The April 21 wiring (`feat: wire diff report into /approve workflow`) was removed on May 22 when `/dispute` was added; the new design relies on `#CHANGED:` annotations + git diff + dispute comments instead. The script remains in the repository in case the team decides to re-integrate an auto-generated artifact. | Decided against for now |
| Bridge layer | Bridge package (per-file SHA-256, packing slip, optional Ed25519 signature) that hands the queue's completed folders to a downstream receiver. Architecture sketched; not built. | Not started |
| Browser extension | A client-side extension that reads a paper page in the browser, extracts the DOI, queries `queue/review_log.csv`, and reports curation status. The CSV is already maintained. | Not started |
| Fork-PR support | `validate-submission.yml` cannot write `reviewer_1` back to a fork PR (the bot cannot push to a fork branch). External contributors are currently unsupported. | Known gap |
| Notebook-execution-as-verification | A workflow that re-runs the `review-copy/` notebook in a clean environment to confirm Reviewer 2 actually re-executed it. | Not started |

---

## Known issues

- `update-queue-csv.yml` historically referenced the old `queue/pending.csv` path in its commit step after the file was renamed to `queue/review_log.csv`. This has been corrected.
- `docs/MERGE_PLAN.md` describes an obsolete two-fork merge plan that no longer matches the current workflow.

---

## Codespaces

GitHub Codespaces is configured and confirmed working. Reviewers can open a Codespace from the repository page and get a fully configured environment with no local installation required. See [CODESPACES_GUIDE.md](CODESPACES_GUIDE.md).
