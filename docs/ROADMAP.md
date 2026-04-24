# Project Roadmap: Review Queue System

*Assessment based on review of the main repository, both active forks, open issues, and workflow code. Current as of April 23, 2026.*

---

## What the System Currently Is

A GitHub-native queue for coordinating two-stage reproducibility reviews of research manuscripts and Jupyter notebooks. The core design principle is intentional: rely only on what GitHub already provides — no external servers, no separate accounts, no database.

### What Is Already Working in the Main Repo

| Feature | Status |
|---|---|
| 3-stage queue (`awaiting-review-2` → `in-progress` → `completed`) | Working |
| Slash commands (`/checkout`, `/release`, `/approve`) via GitHub Actions | Working |
| Auto-issue creation when files are pushed to `awaiting-review-2/` | Working |
| Reviewer integrity check (reviewer 2 ≠ reviewer 1) | Working |
| Automated file/folder movement between stages | Working |
| `metadata.yml` schema for tracking paper details | Working |
| PR structure validation (`validate-submission.yml`) | Working |
| Completion notifications (`notify-on-complete.yml`) | Working |
| Beginner-friendly documentation (LOCAL_SETUP_GUIDE, WORKFLOW_GUIDE, CONTRIBUTING) | Working |

**The system is functional and in active use.** There are 15 open tracking issues across real papers with history of completed reviews.

---

## What the Forks Are Building

There are two forks. **lmmaganto forked from Jampip**, not from main. Each fork addresses one distinct issue.

---

### Issue 1 — No reviewer working copy (Jampip)

**The problem:** When a reviewer uses `/checkout`, the original notebook is the only file in the folder. There is nothing stopping a reviewer from editing it directly. If that happens, the original is overwritten and the second reviewer has nothing reliable to compare against.

**What Jampip built:** On `/checkout`, automatically creates:
- `review-copy/<name>_rvd.ipynb` — the reviewer's working copy
- `notes/review_notes.md` — a structured template (Summary, Required Changes, Comments, Decision)
- `review_metadata.yml` — timestamps and reviewer info

Before `/approve` succeeds, validates that these files exist and that the notes are not empty (`hasReviewerContent`). Approval is blocked if the reviewer left the notes unfilled. Metadata is updated with the approval timestamp and approver username on completion.

**Status:** 26 commits ahead of main. The most recent commit message ("Fianl edit, assuming") indicates they are still debugging. There are 14 comments on a single test issue reflecting significant trial and error getting the workflow mechanics right.

---

### Issue 2 — No record of what the reviewer actually changed (lmmaganto)

**The problem:** Even with a working copy, there is no record of *what* the reviewer changed in the notebook or *why*. The curator receives a completed folder but has to manually diff the notebooks to understand what the reviewer did.

**What lmmaganto built:** On top of Jampip's fork, added `scripts/generate_diff_report.py` (~193 lines). On `/approve`, this script runs automatically:
- Parses both the original notebook and the reviewer's copy
- Extracts inline annotations: `#SOURCE: p.X` (citation links) and `#CHANGED: reason` (explanations of deviations)
- Generates `DIFF_REPORT.md` in the completed folder with a line-by-line comparison table
- Posts a summary as an issue comment tagging the curator

Also did a documentation rewrite simplifying all docs for beginners and adding a `USAGE.md` guide.

**Status:** 25 commits ahead of main (includes Jampip's work). Active development. The diff report requires reviewers to use the `#SOURCE:` and `#CHANGED:` annotation conventions — if they don't, the report generates but the output is empty.

---

## What We Actually Need

Both issues above are real and worth fixing. The two forks address them in sequence — Jampip first, lmmaganto building on top.

### Definitely needed

- **Issue 1 (reviewer copy):** Jampip's solution is the right approach. A structured `review-copy/` and `notes/` created automatically on checkout, with a pre-approve check that notes aren't empty. This is the minimum needed to know a review was done.
- **Issue 2 (diff report):** lmmaganto's `generate_diff_report.py` is useful for the curator, but it only produces meaningful output if reviewers consistently use the `#CHANGED:` and `#SOURCE:` annotation conventions. It should not gate approval — if the reviewer didn't annotate, the approve should still succeed and the report should note it could not extract content.

Also needed:

- **Simplified documentation** — lmmaganto's rewrite should be carried forward.

### Useful, but conditional

- **The automated diff report (lmmaganto):** This is a reasonable tool for the curator, but it only produces meaningful output if reviewers consistently use `#SOURCE:` and `#CHANGED:` inline annotations in their notebooks. If those annotation conventions are not confirmed as part of the official reviewer protocol, the diff output will be empty or misleading. Worth including once the annotation standard is settled.

### Not needed at this stage

- **Org team-based authentication** (Jampip's TODO): Only relevant if and when the repository is transferred to a GitHub organization. Not actionable now.
- **A web interface or dashboard:** The GitHub Issues view already provides this.
- **Automated result analysis or grading:** Out of scope for a queue coordination system.
- **Email delivery configuration:** The notify workflow exists; email setup is an external environment concern for a maintainer, not something to build into the repo.
- **PR-based submission for second reviews:** The current slash command + folder approach is simpler and is already working.

---

## Conservative Roadmap

### Phase 1 — Consolidate what exists *(immediate)*

The two forks are diverging. Before either grows further, the useful parts should be identified and reconciled.

- Compare the folder structure conventions between the two forks (they differ slightly in layout) and pick one standard.
- Confirm whether the `#SOURCE:` / `#CHANGED:` annotation convention is the intended reviewer protocol.
- Ensure `/checkout` → `/approve` works reliably for both folder-based items and loose file items before adding anything new.
- Keep documentation in sync with what the automation actually does. If the workflow creates a `review-copy/` folder, the docs should say so.

**Deliverable:** A clear decision on the folder structure standard and annotation protocol, documented.

---

### Phase 2 — Review quality baseline *(near-term, once Phase 1 is settled)*

- Adopt the review notes template and structure validation from Jampip's fork.
  - This is the minimum needed to know a review was actually done.
  - It does not change the external workflow for reviewers — it just adds a notes file they need to fill in.
- Merge the simplified documentation from lmmaganto's fork.
- Test the full checkout-to-approve cycle end-to-end in a fork before merging to main.

**Deliverable:** A PR to main that adds the review structure, notes template, and pre-approve validation.

---

### Phase 3 — Diff reporting *(only after Phase 2, and only if the annotation standard is confirmed)*

- Incorporate lmmaganto's `generate_diff_report.py` script.
- Wire it into the `/approve` command as lmmaganto has done.
- This should be a fallback — if the script fails (e.g. reviewer didn't annotate), the approval should still succeed, and the diff step should note it could not run.

**Deliverable:** A PR adding the diff script and its integration, with clear documentation of the annotation conventions required for it to produce output.

---

### Out of scope (for now and the foreseeable future)

- Org migration or team-based authentication
- Any tooling beyond coordinating who is reviewing what
- Integration with external systems (submission portals, databases, email servers)
- Automated scientific validation of the notebooks themselves

---

## Summary Assessment

Both forks are working on genuine gaps in the current system. Neither is building anything unreasonable. The main risk is divergence: if both forks continue independently without reconciling, merging them later becomes harder.

**lmmaganto** is building the output side — what the curator sees when a review finishes.  
**Jampip** is building the input side — structure and quality checks during the review.

Both are needed. The order matters: getting the review structure right (Phase 2) is a prerequisite for the diff output to be meaningful (Phase 3). The system is already doing its core job; improvements should be merged deliberately and tested on a fork first.
