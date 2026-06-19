# Reproducibility Review Process

This describes the process the team agreed on. The code in `.github/workflows/` enforces most of it; the rest is convention.

---

## Roles

| Role | Person | GitHub |
|---|---|---|
| Principal Investigator | Dr. Sego |, |
| Student Lead | Liz | Lizo-RoadTown |
| Reviewer | Jamaal | Jampip |
| Reviewer | Louise | lmmaganto |

Per-paper, the team divides into two operator roles:

- **Reviewer 1 (curator).** The person who selected the paper, built the reproduction notebook, and submitted the folder via pull request. The system records them as `reviewer_1` in the folder's `metadata.yml`.
- **Reviewer 2.** Any other team member. Claims the issue, re-runs the notebook, decides whether the review is complete or flags a dispute.

The same person can be Reviewer 1 on one paper and Reviewer 2 on another. The system enforces that they cannot be both roles on the same paper, `/checkout` and `/approve` are blocked if the commenter is also Reviewer 1.

---

## Pipeline

```
1. Selection             2. Curation              3. Submission           4. Second review
─────────────            ──────────────           ─────────────           ────────────────
Paper chosen for     →   Notebook built       →   PR opens; folder    →   Reviewer 2 claims
reproduction.            offline (typically       lands in awaiting-      via /checkout, runs
                         in curation-dev/         review-2/. Validate-    notebook, decides
                         locally).                submission.yml          /approve or /dispute.
                                                  records reviewer_1.
                                                  Issue auto-created.
```

---

## Stage 1: Selection

Pick a paper that needs reproduction. There is no separate sign-off step, selection happens informally. The team's working list of candidate papers is tracked in `queue/review_log.csv`, which is appended to automatically whenever a tracking issue is opened (by PR merge or by the queue issue template).

---

## Stage 2: Curation

Build the reproduction notebook locally. Working in `curation-dev/` is the team's convention, but the system does not enforce a particular workspace. The output of this stage is a folder containing at minimum:

- One `.ipynb` notebook that reproduces the paper's model.
- One `.pdf` of the manuscript.
- (Recommended) At least one output image.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the required folder shape.

---

## Stage 3: Submission

1. Place the curated folder under `reviews/awaiting-review-2/`.
2. Commit, push, and open a pull request.
3. The `validate-submission.yml` workflow checks the folder shape and refuses to merge if anything is missing.
4. On merge, `validate-submission.yml` writes the PR author's username into the folder's `metadata.yml` as `reviewer_1`. `bootstrap-seed-issues.yml` creates a `[REVIEW]` tracking issue with the `awaiting-review-2` label. `update-queue-csv.yml` appends a row to `queue/review_log.csv`.

There is no `/approve` step at submission, that command is reserved for Reviewer 2 at the end of the second review. The submission is "approved" by the PR review process itself.

---

## Stage 4: Second review

1. Reviewer 2 finds the issue under the `awaiting-review-2` label, confirms they are not Reviewer 1, and comments `/checkout`. The system assigns them, moves the folder to `reviews/in-progress/`, creates the `original/` and `review-copy/` structure, and changes the label to `review-2-active`.
2. Reviewer 2 pulls the files, opens the `_rvd.ipynb` copy, re-runs cells, annotates changes with `#CHANGED:` comments, fills in `notes/review_notes.md`, commits, and pushes.
3. Reviewer 2 comments one of:
   - `/approve`, the system validates the folder shape, moves it to `reviews/completed/`, updates `review_metadata.yml`, sets the label to `complete`, and closes the issue. `notify-on-complete.yml` zips and emails the package.
   - `/dispute <reason>`, the system sets the label to `disputed` and notifies the curator (Reviewer 1).
   - `/release`, the system returns the folder to `reviews/awaiting-review-2/` and unassigns Reviewer 2.

If Reviewer 2 used `/dispute`, the curator inspects the changes and comments:

- `/complete`, the system finalizes as above, with the curator recorded as the resolver.
- `/reject <reason>`, the system sets the label to `curator-rejected`. The issue stays open for discussion in comments. There is no automated next step.

---

## Annotation conventions

| Annotation | Meaning |
|---|---|
| `#SOURCE: p.X eq.(Y)` | Where this value came from in the paper. Optional but strongly encouraged. |
| `#CHANGED: reason` | Why this line was changed from the curator's original. Required if a value was changed. |

Both work with or without a space after `#`. Capitalization does not matter.

---

## Naming conventions

| Item | Convention | Example |
|---|---|---|
| Submission folder | Short name for the paper, often based on DOI or pathogen | `HBV/`, `DOI_10.1016_Koufi_2022_F43/` |
| Notebook inside the folder | Matches or relates to the folder name | `HBV.ipynb` |
| `metadata.yml` | One per submission folder | `doi:`, `reviewer_1:` |

---

## Process changes

Changes to the *enforced* part of this process require changes to `.github/workflows/manage-queue.yml` and related workflow files. Changes to the *conventional* part (selection process, naming, where curation work happens locally) are agreed by the team in PR review.
