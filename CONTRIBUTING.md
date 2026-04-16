# Reviewer Guide

Welcome! This guide walks you through how to review manuscripts in this system. If you haven't set up your computer yet, start with the [Local Setup Guide](docs/LOCAL_SETUP_GUIDE.md) first.

---

## The Review Flow

Here's the entire process as a flowchart:

```
┌─────────────────────────────┐
│  Find an issue labeled       │
│  "awaiting-review-2"        │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  Comment: /checkout          │
│  (assigns you, moves files   │
│   to reviews/in-progress/)   │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  Do your review work         │
│  • Re-run the notebook       │
│  • Check it matches the PDF  │
│  • Add comments/tags as      │
│    needed on the issue       │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  Comment: /approve           │
│  (marks complete, moves      │
│   files to reviews/completed)│
└─────────────────────────────┘
```

That's it. Two commands: `/checkout` to start, `/approve` to finish.

---

## Step by Step

### 1. Find something to review

**On GitHub (in your browser):**

1. Go to the repository's **Issues** tab
2. Look for issues with the yellow `awaiting-review-2` label
3. Click on one to read what it's about

> **Tip:** The issue will have a link or description of the manuscript and notebook you'll be reviewing.

### 2. Claim it

**Comment `/checkout` on the issue.** That's all you need to type.

What happens automatically:
- You get assigned to the issue
- The files move from `reviews/awaiting-review-2/` to `reviews/in-progress/`
- The label changes to `review-2-active`

> **Note:** If someone else already did the first review, the system won't let that same person do the second review. This is checked automatically.

### 3. Do your review

Pull the latest files to your computer and do your work:

**In VS Code (preferred):**

1. Open the **Source Control** panel (click the branch icon in the left sidebar)
2. Click the **"..."** menu at the top → **Pull**
3. Open the notebook in `reviews/in-progress/` and do your review

**In the terminal (backup):**

```powershell
git pull
```

What "doing your review" means:
- Open and re-run the Jupyter notebook
- Compare the notebook's results against the manuscript PDF
- Note anything that doesn't match or needs attention

### 4. Save and push your work

After you've done your review work, you need to send your changes back to GitHub.

**In VS Code (preferred):**

1. Open the **Source Control** panel
2. You'll see your changed files listed
3. Type a short message describing what you did (e.g., "Review HBV notebook — results verified")
4. Click the **checkmark** button to commit
5. Click **Sync Changes** to push to GitHub

**In the terminal (backup):**

```powershell
git add .
git commit -m "Review HBV notebook — results verified"
git push
```

### 5. Approve it

When your review is done, go back to the issue on GitHub and **comment `/approve`**.

What happens automatically:
- The label changes to `complete`
- The files move to `reviews/completed/`
- If email is set up, the maintainer gets a notification with a zip of the package
- The issue closes

**You're done!**

---

## Other Useful Things

### Giving something back to the queue

If you claimed something but can't finish it, comment `/release` on the issue. It moves the files back to `awaiting-review-2/` and unassigns you.

### Adding comments and tags along the way

Between `/checkout` and `/approve`, you can add as many comments on the issue as you want — questions, notes, tags, whatever helps. None of that triggers any automation. Only `/checkout`, `/release`, and `/approve` change the state.

### Adding a new manuscript to the queue

Just drop the files into `reviews/awaiting-review-2/`, commit, and push. The system automatically creates a tracking issue for each new item.

1. In VS Code, add your folder (or file) inside `reviews/awaiting-review-2/`
2. Include a `metadata.yml` if it's a folder (see structure below)
3. Commit and push
4. A GitHub issue labeled `awaiting-review-2` is created automatically — no manual issue needed

You can also create an issue by hand from the **Issues** tab → **New issue** → **"Add manuscript to review queue"** template, but it's not required.

### Review folder structure

Each review folder should contain:
- One `.ipynb` notebook file
- One `.pdf` manuscript file
- A `metadata.yml` file
- (Recommended) At least one image file

---

## Commands Reference

| Command | When to use it | What happens |
|---|---|---|
| `/checkout` | You want to start reviewing something | Assigns you, moves files to `in-progress`, sets `review-2-active` |
| `/approve` | You're done with your review | Marks complete, triggers finalization |
| `/release` | You need to hand it back | Moves files back to `awaiting-review-2`, unassigns you |
