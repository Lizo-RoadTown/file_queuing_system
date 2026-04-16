# Step-by-Step Workflow Guide

This guide shows you exactly how to work with Git and VS Code to do your reviews. It covers everything from pulling the latest files to pushing your work back to GitHub.

**Prerequisites:** Make sure you've already completed the [Local Setup Guide](LOCAL_SETUP_GUIDE.md).

---

## What You'll Do Each Time

Here's the pattern every time you sit down to review:

```
1. Pull (get the latest files)
       â–¼
2. Do your review work
       â–¼
3. Commit (save a snapshot)
       â–¼
4. Push (send it to GitHub)
```

---

## Part 1: Getting the Latest Files

Before you start working, always grab the latest version from GitHub. Other people may have made changes since you last worked.

### Using VS Code (preferred)

1. Open VS Code with your repository folder
2. Look at the **bottom-left corner** of the VS Code window â€” you should see the word `main` (your branch name)
3. Click the **Source Control** icon in the left sidebar (it looks like a branch/fork)
4. Click the **"..."** menu at the top of the Source Control panel
5. Click **Pull**

If there were new changes, you'll see them update in your files. If everything was already up to date, nothing will happen â€” that's fine.

### Using the terminal (backup)

```powershell
cd C:\Users\YourName\Documents\file_queuing_system
git pull
```

---

## Part 2: Doing Your Review

### Claim an issue on GitHub

1. Go to the repository on GitHub in your browser: `https://github.com/Lizo-RoadTown/file_queuing_system/issues`
2. Find an issue with the `awaiting-review-2` label
3. Click on it to open it
4. Scroll to the bottom comment box
5. Type `/checkout` and click **Comment**

The system will assign you and move the files into `reviews/in-progress/`.

### Pull the moved files to your computer

After the system moves the files, pull again so your local copy is up to date:

**VS Code:** Source Control panel â†’ **"..."** â†’ **Pull**

**Terminal:** `git pull`

### Open and review the notebook

1. In VS Code's file explorer (left sidebar), navigate to `reviews/in-progress/`
2. Find the folder or file for your issue
3. Open the `.ipynb` notebook
4. Re-run the cells and compare the results to the manuscript PDF
5. Note anything that doesn't match

> **Tip:** If VS Code asks you to select a kernel, choose "Review Queue Python" or the `review-queue` environment you set up earlier.

---

## Part 3: Saving Your Work

Git saves work in two steps: **commit** (take a snapshot) and **push** (upload to GitHub). Think of it like saving a document and then syncing it to the cloud.

### Using VS Code (preferred)

This is the easiest way and avoids typos in commands.

1. Click the **Source Control** icon in the left sidebar
2. You'll see a list of files you changed â€” review them to make sure they look right
3. In the **Message** box at the top, type a short description of what you did, like:
   - `Verified HBV notebook results`
   - `Added review notes for Cholera manuscript`
4. Click the **checkmark (âœ“)** button to commit
5. Click **Sync Changes** (or the sync icon in the bottom status bar)

That's it â€” your work is now on GitHub.

### Using the terminal (backup)

```powershell
# See what files you changed
git status

# Stage all your changes
git add .

# Save a snapshot with a message
git commit -m "Verified HBV notebook results"

# Upload to GitHub
git push
```

### What "stage, commit, push" means

If this is new to you, here's the idea:

| Step | What it does | Analogy |
|---|---|---|
| **Stage** (`git add`) | Selects which changes to include | Picking photos for an album |
| **Commit** (`git commit`) | Saves a snapshot with a label | Taking the photo and writing a caption |
| **Push** (`git push`) | Uploads to GitHub | Uploading to the cloud |

VS Code's **Sync Changes** button does both commit and push together, which is why it's easier.

---

## Part 4: Finishing Your Review

When you're happy with your review:

1. Go back to the issue on GitHub
2. Comment `/approve`

The system handles the rest:
- Moves the files to `reviews/completed/`
- Closes the issue
- Sends an email notification (if configured)

**You're done!**

---

## Common Situations

### "I need to hand something back"

If you can't finish a review, comment `/release` on the issue. The files move back to `awaiting-review-2/` and you get unassigned.

### "VS Code says I have changes I haven't saved"

The Source Control panel shows changed files. Either:
- **Commit and push them** if they're work you want to keep
- **Discard them** by right-clicking the file in Source Control â†’ **Discard Changes** (only if you're sure you don't want them)

### "My pull failed"

This usually means you have local changes that conflict with what's on GitHub. The safest approach:

1. Commit your current work first (even if it's unfinished)
2. Then pull
3. If VS Code shows a merge conflict, ask a maintainer for help

### "I want to check if I'm up to date"

Look at the bottom-left of VS Code. If you see a number next to the sync arrows, you have changes to pull or push. You can also run:

```powershell
git status
```

This tells you if you have uncommitted changes and whether you're ahead or behind GitHub.

### "Someone else pushed changes while I was working"

Just pull and then push:

**VS Code:** Click **Sync Changes** â€” it pulls and pushes in one step.

**Terminal:**

```powershell
git pull
git push
```

---

## Quick Reference

### Daily workflow

```powershell
cd C:\Users\YourName\Documents\file_queuing_system
conda activate review-queue
git pull
code .
```

### Save and upload your work

```powershell
git add .
git commit -m "Your message here"
git push
```

### VS Code equivalents

| Terminal command | VS Code action |
|---|---|
| `git pull` | Source Control â†’ **...** â†’ **Pull** |
| `git add .` | (Automatic when you commit in VS Code) |
| `git commit -m "msg"` | Type message + click **âœ“** |
| `git push` | Click **Sync Changes** |
| `git status` | Look at the Source Control panel |
