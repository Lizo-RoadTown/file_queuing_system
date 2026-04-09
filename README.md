# Reproducibility Review Queuing System

**University of Florida Laboratory of Systems Medicine**

A transparent, version-controlled system for managing two-stage reproducibility reviews of computational research manuscripts.

---

## System Documentation

This document describes the technical methodology behind the review queue system, including how GitHub features are used to create transparency, enforce review integrity, and maintain a complete audit trail.

---

## Table of Contents

1. [What is This System?](#what-is-this-system)
2. [Core Components](#core-components)
3. [How Transparency is Achieved](#how-transparency-is-achieved)
4. [The Queuing System Mechanism](#the-queuing-system-mechanism)
5. [How Self-Review is Prevented](#how-self-review-is-prevented)
6. [Version Control and Audit Trail](#version-control-and-audit-trail)
7. [Automated Workflows](#automated-workflows)
8. [For Reviewers](#for-reviewers)
9. [For Maintainers](#for-maintainers)

---

## What is This System?

This repository manages a queue of manuscripts awaiting reproducibility verification. Each manuscript goes through two independent reviews where reviewers attempt to reproduce computational results from published or submitted research papers.

The system uses GitHub's built-in features to:
- Track which manuscripts are in the queue
- Assign reviewers automatically
- Enforce two-stage independent review (different reviewers)
- Validate submissions automatically
- Maintain a complete history of all activities
- Provide public transparency (or private within collaborator group)

**Key Design Goal:** Everything is visible, traceable, and verifiable. No hidden decisions, no black-box automation.

---

## Core Components

The system is built entirely on standard GitHub features:

### 1. GitHub Issues

**What they are:** Issues are discussion threads attached to a repository. Originally designed for bug tracking, we repurpose them to track manuscripts in the review queue.

**How we use them:**
- **One issue = one manuscript** being reviewed
- **Issue title** = manuscript name
- **Issue body** = manuscript details (DOI, URL, description)
- **Issue labels** = current workflow state (`queued`, `review-1-active`, etc.)
- **Issue assignees** = who is currently reviewing it
- **Issue comments** = reviewer commands and automation responses
- **Issue timeline** = complete history of label changes, assignments, state transitions

**Why this creates transparency:**
- Anyone with repository access can see all manuscripts in the queue
- Anyone can see who is assigned to what
- Anyone can see how long a review has been active
- Complete history is preserved (when was it claimed? by whom? when did it advance?)

**Example:** Issue #5 titled "Hepatitis B Viral Dynamics Model"
- Label: `review-1-active`
- Assigned to: `@reviewer-jane`
- Comment history shows: `/checkout` command by reviewer-jane on April 1, 2026

### 2. GitHub Pull Requests

**What they are:** Pull requests (PRs) are proposed changes to the repository. They show exactly what files will be added/modified, allow discussion, and require approval before merging.

**How we use them:**
- Reviewers submit their work (notebooks, PDFs, metadata) via pull request
- Automated checks validate the submission structure
- Other reviewers or maintainers can see exactly what's being added
- Changes aren't added to the repository until the PR is approved and merged

**Why this creates transparency:**
- **Before merging:** Everyone can see what a reviewer is submitting
- **Diff view:** GitHub shows exactly what files are being added and their contents
- **Validation:** Automated checks run publicly—everyone sees if checks pass or fail
- **Discussion:** Anyone can comment on the PR to ask questions or request changes
- **Approval required:** Changes don't automatically enter the repository; a maintainer must approve

**Example:** PR #12 titled "Add first review for HBV manuscript"
- Shows: 4 files added (notebook.ipynb, manuscript.pdf, output.png, metadata.yml)
- Automated check: ✅ All required files present
- Automated check: ✅ YAML structure valid
- Maintainer reviews and clicks "Merge pull request"

### 3. GitHub Labels

**What they are:** Colored tags attached to issues to categorize them.

**How we use them:** Each label represents a state in the review workflow:

| Label | Color | Meaning |
|-------|-------|---------|
| `queued` | Gray | Manuscript entered, awaiting first reviewer |
| `review-1-active` | Yellow | First reviewer currently working |
| `awaiting-review-2` | Green | First review complete, ready for second reviewer |
| `review-2-active` | Yellow | Second reviewer currently working |
| `complete` | Purple | Both reviews done, package archived |

**Why this creates transparency:**
- Visual status at a glance (filter issues by label to see all manuscripts in a specific state)
- Label changes are logged in issue timeline with timestamps
- No way to skip states—automation enforces the state machine
- Color coding makes queue status obvious

### 4. GitHub Actions (Workflows)

**What they are:** Automated scripts that run when specific events happen (e.g., issue comment posted, pull request opened).

**How we use them:**
- **Workflow 1:** When someone comments on an issue, check if it's a slash command (`/checkout`, `/release`, `/approve`) and execute it
- **Workflow 2:** When a pull request is opened, validate that required files are present and structured correctly
- **Workflow 3:** When a review is approved, zip files, email them, close the issue

**Why this creates transparency:**
- All workflow code is visible in `.github/workflows/` folder (anyone can read the automation logic)
- Every workflow run is logged publicly in the **Actions** tab with timestamped execution records
- If a workflow fails, the error log is visible (no silent failures)
- Workflows run on GitHub's servers (no hidden server running somewhere)

### 5. Git Version Control

**What it is:** Git tracks every change to every file, who made it, and when.

**How we use it:**
- Every review submission creates Git commits (snapshots of changes)
- Commits are attributed to the reviewer's GitHub account
- Complete history of all changes is preserved forever
- Any version of any file can be retrieved from history

**Why this creates transparency:**
- **Attribution:** Every change has an author and timestamp
- **Reversibility:** Mistakes can be undone by reverting to previous versions
- **Inspection:** Anyone can see what changed between versions
- **Immutability:** Once committed, history cannot be secretly altered (commits are cryptographically hashed)

---

## How Transparency is Achieved

Every action in this system is visible and verifiable:

### What You Can See:

**Issue List:**
- All manuscripts currently in queue
- Which state each manuscript is in
- Who is assigned to each manuscript
- How long they've been assigned

**Issue Timeline:**
- When the manuscript was added (issue created)
- When first reviewer claimed it (label changed to `review-1-active`)
- When first review was completed (label changed to `awaiting-review-2`)
- When second reviewer claimed it (label changed to `review-2-active`)
- When review was finalized (label changed to `complete`, issue closed)

**Pull Request History:**
- All review submissions
- What files were added
- Whether automated checks passed
- Discussion/feedback on submissions
- Who approved and merged the submission

**Git Commit History:**
- Every file change
- Who made each change
- When they made it
- What the change was (diff view)

**Workflow Execution Logs:**
- Every time automation ran
- What it did
- Whether it succeeded or failed
- Complete console output

### What You Cannot Do (Enforced by GitHub):

- ❌ Change issue labels without leaving a trace in the timeline
- ❌ Assign yourself without GitHub logging it
- ❌ Merge a pull request without automated checks passing (if configured as required)
- ❌ Modify Git history without creating "force push" warnings
- ❌ Delete workflow execution logs (GitHub retains them)
- ❌ Run slash commands unless you're a repository collaborator (permission check)

---

## The Queuing System Mechanism

### How Manuscripts Enter the Queue

1. **Issue is created** using the "Add manuscript to review queue" template
2. **Initial label is set** to `queued`
3. **Manuscript appears in queue** (visible to all reviewers)

### How Reviewers Claim Work

Instead of being assigned by a coordinator, reviewers **self-select** work:

1. **Reviewer browses issues** and finds one labeled `queued` (or `awaiting-review-2` for second reviews)
2. **Reviewer comments** `/checkout` on the issue
3. **GitHub Action workflow triggers:**
   - Detects the `/checkout` command in the comment
   - Verifies commenter is a repository collaborator (permission check)
   - Assigns the issue to the commenter
   - Changes label to next state (`review-1-active` or `review-2-active`)
   - Posts automated confirmation comment

**Example workflow execution:**
```
User @reviewer-jane comments: "/checkout"
Workflow runs:
  ✓ User is collaborator
  ✓ Issue is in 'queued' state
  → Assign issue to @reviewer-jane
  → Change label from 'queued' to 'review-1-active'
  → Post comment: "Assigned to @reviewer-jane. State: review-1-active"
```

**Why this is transparent:**
- The `/checkout` comment is visible to everyone
- The workflow execution is logged in Actions tab
- The label change appears in issue timeline
- The assignment appears in issue sidebar and timeline

### How Reviews Progress

**First Review:**
1. Reviewer creates folder in `reviews/in-progress/<name>/`
2. Adds Jupyter notebook reproducing manuscript results
3. Adds manuscript PDF, output images, metadata file
4. Opens pull request
5. Automated validation checks structure
6. Maintainer reviews and merges PR
7. Reviewer or maintainer moves folder to `reviews/awaiting-review-2/`
8. Issue label changed to `awaiting-review-2`

**Second Review:**
1. Different reviewer comments `/checkout` on `awaiting-review-2` issue
2. Workflow assigns them, changes label to `review-2-active`
3. Reviewer independently runs the first reviewer's notebook
4. Reviewer verifies results match manuscript claims
5. (Optional) Reviewer adds `review2.md` notes via pull request
6. Reviewer comments `/approve` on issue
7. Workflow triggers completion:
   - Moves folder to `reviews/completed/`
   - Zips all files
   - Emails zip to designated recipient
   - Changes label to `complete`
   - Closes issue

### State Transitions (Enforced by Automation)

The workflow enforces valid state transitions:

```
Valid transitions:
  queued → review-1-active (via /checkout)
  review-1-active → queued (via /release)
  review-1-active → awaiting-review-2 (via PR merge)
  awaiting-review-2 → review-2-active (via /checkout)
  review-2-active → awaiting-review-2 (via /release)
  review-2-active → complete (via /approve)

Invalid transitions are rejected:
  queued → complete ❌ (cannot skip reviews)
  review-1-active → review-2-active ❌ (must complete first review)
```

If someone tries to run `/checkout` on an issue in the wrong state, the workflow rejects it and posts an error comment.

---

## How Self-Review is Prevented

**The Problem:** A reviewer could theoretically review their own first submission as the second reviewer, defeating the purpose of independent verification.

**The Solution:** The workflow enforces reviewer separation.

### Mechanism:

1. **When first review completes**, the reviewer's GitHub username is recorded in `metadata.yml`:
   ```yaml
   reviewer_1: jane-smith
   reviewer_1_completed: 2026-04-01
   reviewer_2: null
   state: awaiting-review-2
   ```

2. **When someone comments `/checkout` on an `awaiting-review-2` issue**, the workflow:
   - Reads the `metadata.yml` file
   - Extracts `reviewer_1` value
   - Compares it to the GitHub username of the person commenting
   - **If they match:** Reject the command, post error comment
   - **If they differ:** Proceed with assignment

**Example workflow logic (pseudocode):**
```python
def handle_checkout(issue, commenter):
    if issue.label == "awaiting-review-2":
        metadata = read_yaml(f"reviews/awaiting-review-2/{issue.name}/metadata.yml")
        if metadata['reviewer_1'] == commenter:
            post_comment("❌ You cannot review your own first submission.")
            return
    # Proceed with assignment...
```

**Why this is transparent:**
- The rejection is posted as a public comment on the issue
- The metadata file is visible in the repository
- The workflow code is visible in `.github/workflows/manage-queue.yml`
- Anyone can verify the logic

**Edge case handling:**
- If `metadata.yml` is missing → validation check fails during PR submission
- If `metadata.yml` has wrong format → validation check fails
- If someone manually edits Git history to change metadata → Git log shows the manual edit (not normal workflow)

---

## Version Control and Audit Trail

### Every Action Leaves a Trace

**Issue Comments:**
- **What:** Every slash command, every discussion
- **Who:** GitHub username (authenticated)
- **When:** Timestamp (UTC)
- **Preserved:** Forever (unless issue is deleted, which is rare and logged)

**Label Changes:**
- **Visible in:** Issue timeline, issue events API
- **Shows:** Old label → new label, who made the change, when
- **Preserved:** Forever

**Pull Requests:**
- **Shows:** Exactly what files changed
- **Diff view:** Line-by-line comparison of changes
- **Preserved:** Forever (even after merge)

**Git Commits:**
- **Contains:** Author, timestamp, commit message, full file snapshot
- **Verified by:** Cryptographic hash (SHA-1 or SHA-256)
- **Immutable:** Cannot be secretly changed (would change hash, visible to all)

**Workflow Runs:**
- **Logs:** Complete console output of every automation execution
- **Preserved:** 90 days (GitHub default), can be extended
- **Shows:** What triggered the workflow, what it did, success/failure

### How Reviewers Can Verify History

**To see what happened to a manuscript:**
1. Open the issue
2. Scroll through comments and timeline
3. See all state transitions, assignments, commands

**To see what a reviewer submitted:**
1. Find their pull request (linked from issue or in PR list)
2. Click "Files changed" tab
3. See every file they added and the contents

**To see if automation worked correctly:**
1. Go to "Actions" tab
2. Filter by workflow name
3. Click a workflow run to see full execution log

**To see when files were modified:**
1. Browse to the file in GitHub
2. Click "History" button
3. See all commits that modified the file

**To see who did what in the repository:**
1. Go to "Insights" → "Contributors"
2. See commit counts, lines added/removed per person
3. Click a person to see their commit history

---

## Automated Workflows

All automation is defined in `.github/workflows/` and runs on GitHub's servers.

### 1. Queue Management Workflow (`manage-queue.yml`)

**Triggers:** When a comment is posted on an issue

**Execution Steps:**
1. Parse comment for slash commands: `/checkout`, `/release`, `/approve`
2. Check if commenter is a repository collaborator (permission verification)
3. Read current issue state (labels)
4. Execute command:

   **For `/checkout`:**
   - Verify issue is in `queued` or `awaiting-review-2` state
   - If `awaiting-review-2`: check commenter ≠ first reviewer (read `metadata.yml`)
   - Assign issue to commenter
   - Update label to `review-1-active` or `review-2-active`
   - Post confirmation comment

   **For `/release`:**
   - Verify issue is in `review-1-active` or `review-2-active` state
   - Verify commenter is currently assigned
   - Unassign issue
   - Update label back to `queued` or `awaiting-review-2`
   - Post confirmation comment

   **For `/approve`:**
   - Verify issue is in `review-2-active` state
   - Verify commenter is the second reviewer
   - Trigger completion workflow (zip, email, close)

**Why this is transparent:**
- Code is visible in repository
- Execution log shows each step
- Comments posted by workflow are visible to all

### 2. Submission Validation Workflow (`validate-submission.yml`)

**Triggers:** When a pull request is opened or updated

**Execution Steps:**
1. Find folders added/modified in the PR
2. For each folder in `reviews/in-progress/` or `reviews/awaiting-review-2/`:
   - Check for exactly 1 `.ipynb` file
   - Check for exactly 1 `.pdf` file
   - Check for `metadata.yml` file
   - Validate YAML structure (required fields, correct types)
   - Check that files referenced in YAML exist
   - Check for at least 1 image file (`.png`, `.jpg`, `.svg`) [warning, not error]
3. If all checks pass: mark check as ✅
4. If any check fails: mark check as ❌ with error message

**Why this is transparent:**
- Check status visible on PR page (green checkmark or red X)
- Click "Details" to see full validation log
- Prevents incomplete submissions from being merged
- Forces reviewers to follow structure

### 3. Completion Notification Workflow (`notify-on-complete.yml`)

**Triggers:** When `/approve` command is executed on `review-2-active` issue

**Execution Steps:**
1. Find the review folder in `reviews/awaiting-review-2/`
2. Move folder to `reviews/completed/`
3. Create `.zip` archive of the folder
4. Send email via SMTP with attachment:
   - **To:** Configured recipient (from `NOTIFY_TO` secret)
   - **From:** Configured sender (from `SMTP_USER` secret)
   - **Subject:** "Review complete: [manuscript name]"
   - **Attachment:** Zipped review package
5. Update issue label to `complete`
6. Close issue with automated comment

**Why this is transparent:**
- Workflow execution logged in Actions tab
- Folder move visible in Git commit history
- Issue closure visible in issue timeline
- (Email recipient is configured in repository secrets, visible to maintainers)

---

## For Reviewers

**New reviewers:** Follow this learning path:
1. [LOCAL_SETUP_GUIDE.md](docs/LOCAL_SETUP_GUIDE.md) - Install software and set up environment
2. [WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) - Learn Git workflow (clone, commit, pull request)
3. [CONTRIBUTING.md](CONTRIBUTING.md) - Learn what to do in a review

**To claim a manuscript:** Comment `/checkout` on a `queued` or `awaiting-review-2` issue

**To release a manuscript:** Comment `/release` if you need to return it to the queue

**To finalize a review:** (Second reviewer only) Comment `/approve` when verification is complete

---

## For Maintainers

**Setup instructions:** See [docs/SETUP.md](docs/SETUP.md) for:
- Creating required labels
- Configuring repository secrets (SMTP credentials)
- Setting up branch protection rules
- Managing collaborator access

**Merging pull requests:** Review submitted files, verify automated checks pass, then merge

**Handling edge cases:** If workflows fail or issues get stuck, manually update labels and post explanatory comments (all actions still logged)

---

## Why This Design?

**No Custom Servers:**
- GitHub provides all infrastructure (hosting, compute, authentication)
- No server maintenance, no uptime monitoring
- No security patching of custom code

**Complete Transparency:**
- Everything is visible in issues, PRs, commits, and workflow logs
- No "black box" decisions
- Audit trail for accountability

**Decentralized Collaboration:**
- Reviewers work independently
- No coordinator bottleneck
- Self-service assignment

**Automated Integrity:**
- Reviewer separation enforced by code, not policy
- Validation automated, not manual
- State transitions enforced, not trusted

**Familiar Tools:**
- Researchers already use Git and GitHub
- Jupyter notebooks already standard in computational research
- No specialized software to learn

---

## Summary

This system uses standard GitHub features (issues, pull requests, labels, actions, version control) to create a transparent, auditable, and automated review queue. Every action is logged, every decision is visible, and integrity rules (like reviewer separation) are enforced by code rather than policy.

**Transparency mechanisms:**
- Issues show queue status and assignments
- Pull requests show exactly what reviewers submit
- Git commits preserve complete change history
- Workflows automate repetitive tasks with visible logs
- Labels enforce state machine transitions

**Result:** A review queue where nothing happens in secret, everything is traceable, and anyone with access can verify that the process followed the rules.
