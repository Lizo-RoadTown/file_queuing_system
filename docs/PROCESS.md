# Reproducibility Review Process

*Version 1.0 — Draft for team review and sign-off. See [APPROVALS.md](../APPROVALS.md).*

---

## Roles

| Role | Person | GitHub |
|---|---|---|
| Principal Investigator | Dr. Sego | — |
| Student Lead | Liz | Lizo-RoadTown |
| Reviewer | Jamaal | Jampip |
| Reviewer | Louise | lmmaganto |

The person who curated a notebook cannot be its reviewer. This is enforced by the queue system.

---

## Pipeline

```
1. Selection          2. Curation           3. Submission         4. Second Review
─────────────         ──────────────         ─────────────         ────────────────
Paper added to   →   Curator works in   →   Notebook placed   →   Reviewer claims
queue/pending.csv    curation-dev/           in awaiting-          via queue and
                                             review-2/             approves
```

---

## Stage 1: Selection

1. Add a row to `queue/pending.csv` with the paper's name, DOI or URL, your name, the date, and the issue number.
2. Commit and push.

---

## Stage 2: Curation

See [CODESPACES_GUIDE.md](CODESPACES_GUIDE.md) for the full walkthrough.

---

## Stage 3: Submission

1. Commit and push your finished notebook.
2. Comment `/approve` on the issue. The system checks that **Notes** is filled in, then moves the files to `reviews/awaiting-review-2/`.

---

## Stage 4: Second Review

1. Find an open issue labelled `awaiting-review-2` that you did not curate.
2. Comment `/checkout`. A working copy is created and files move to `reviews/in-progress/`.
3. Open the notebook in your Codespace, run all cells, and check the output.
4. Comment `/approve`. The diff report is generated and files move to `reviews/completed/`.

To return a claimed review to the queue, comment `/release`.

---

## Annotation Conventions

| Annotation | Meaning |
|---|---|
| `#SOURCE: p.X` | Source page in the paper for a value or equation |
| `#CHANGED: reason` | Deviation from the paper |

---

## Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Curation notebook | DOI with `/` and `.` replaced by `_` | `10_1016j_chaos_2020_110381.ipynb` |
| Submission subfolder | Short paper or pathogen name | `Cholera/`, `HBV/` |
| `metadata.yml` | One per subfolder | see `reviews/awaiting-review-2/` |

---

## Process Changes

Changes to this document require a pull request reviewed and approved by the student lead and the PI.

See [APPROVALS.md](../APPROVALS.md) for the record of initial sign-off.
