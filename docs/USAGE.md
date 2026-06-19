# How Reviewers Use This System

This is a quick overview of how the review queue works. For detailed step-by-step instructions, see the [Reviewer Guide](../CONTRIBUTING.md). For first-time setup, see the [Local Setup Guide](LOCAL_SETUP_GUIDE.md).

---

## The big picture

This repository keeps track of manuscripts that need a second review. Each manuscript is a GitHub issue. Labels on the issue show what stage it is in. You move things forward by typing slash commands in the issue comments.

The normal flow:

```
awaiting-review-2 --/checkout--> review-2-active --/approve--> complete
                                                            \
                                                             --/dispute--> disputed --/complete--> complete
                                                                                   \
                                                                                    --/reject--> curator-rejected
                                  --/release-->
                                  back to awaiting-review-2
```

Most reviews go straight from `awaiting-review-2` to `complete` via `/checkout` and `/approve`. The curator only enters the picture when a reviewer raises a `/dispute`.

---

## Your day-to-day

### Starting a review

1. Browse the **Issues** tab on GitHub.
2. Find one labeled `awaiting-review-2`.
3. Comment `/checkout`. The system assigns you, moves the files to `reviews/in-progress/`, and creates a `review-copy/` notebook for you to edit.

You cannot review your own submission, the system blocks this automatically.

### While reviewing

- Pull the latest files to your computer (`git pull` or VS Code's Source Control → Pull).
- Open the `_rvd.ipynb` notebook in `review-copy/`. Leave `original/` untouched.
- Re-run the notebook. Compare results to the manuscript PDF.
- Annotate any change with `#CHANGED: reason`.
- Fill in at least one section of `notes/review_notes.md` (Summary, Required Changes, or Comments).
- Commit and push your work.

### Finishing a review

Comment one of these on the issue:

- `/approve`, your review is complete and correct. The system moves files to `reviews/completed/` and closes the issue.
- `/dispute <reason>`, you found something to flag for the curator. The label changes to `disputed` and the curator is notified.
- `/release`, you cannot finish; return it to the queue.

### If you used `/dispute`

The curator will respond with either `/complete` (accept your review) or `/reject <reason>` (reject it, leave the issue open for discussion). There is no automated next step after `/reject`, the curator and the reviewer continue in issue comments.

---

## What makes this useful

- **Visible.** Anyone with repository access can see what is being reviewed, by whom, and what the outcome was.
- **Trackable.** The issue's timeline records every label change and every command, and git records every notebook change. No one has to write status updates.
- **GitHub-only.** No separate tool to install for the queue itself. You still need Git and a notebook environment on your computer to do the actual review work, see [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md).

---

## Where to go next

| Doc | Who it is for |
|---|---|
| [Reviewer Guide](../CONTRIBUTING.md) | Step-by-step walkthrough for doing a review, including the dispute path. |
| [Local Setup Guide](LOCAL_SETUP_GUIDE.md) | First-time setup: Git, VS Code, Python, repository access. |
| [Workflow Guide](WORKFLOW_GUIDE.md) | The git mechanics of pulling, committing, and pushing. |
| [Setup](SETUP.md) | Maintainer setup: labels, email, organization transfer. |
