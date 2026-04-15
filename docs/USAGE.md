# How Reviewers Use This System

This is a quick overview of how the review queue works. For detailed step-by-step instructions, see the [Reviewer Guide](../CONTRIBUTING.md).

---

## The Big Picture

This repository keeps track of manuscripts that need a second review. Think of it as a shared to-do list where:

- Each manuscript is a **GitHub issue**
- Labels on the issue show what stage it's in
- You move things forward by typing simple commands in the issue comments

```
┌──────────────────┐     /checkout     ┌──────────────────┐     /approve     ┌──────────────────┐
│ awaiting-review-2 │ ───────────────► │  review-2-active  │ ──────────────► │     complete      │
│                    │                  │                    │                 │                    │
│ "Needs a reviewer" │ ◄─────────────── │ "Someone's on it" │                 │   "All done"       │
└──────────────────┘     /release      └──────────────────┘                 └──────────────────┘
```

## Your Day-to-Day

### Starting a review

1. Browse the **Issues** tab on GitHub
2. Find one labeled `awaiting-review-2`
3. Comment `/checkout` — the system assigns you and moves the files to `reviews/in-progress/`

### While reviewing

- Pull the latest files to your computer
- Re-run the Jupyter notebook
- Compare the results to the manuscript PDF
- Push your changes back to GitHub
- Comment on the issue with questions, notes, or tags — whatever helps

### Finishing a review

- Comment `/approve` on the issue
- The system marks it complete and moves files to `reviews/completed/`

### Can't finish?

- Comment `/release` to hand it back to the queue

## What Makes This Useful

- **Visible:** Anyone can see what's being reviewed and by whom
- **Simple:** Just two commands to learn (`/checkout` and `/approve`)
- **Trackable:** Git keeps a full history of every change
- **Familiar:** It all happens in GitHub and VS Code — tools you're already learning

## Where To Go Next

| Doc | Who it's for |
|---|---|
| [Reviewer Guide](../CONTRIBUTING.md) | Step-by-step walkthrough for doing a review |
| [Local Setup Guide](LOCAL_SETUP_GUIDE.md) | First-time computer setup |
| [Workflow Guide](WORKFLOW_GUIDE.md) | Detailed Git and VS Code instructions |
| [Setup](SETUP.md) | Maintainers configuring the system |
