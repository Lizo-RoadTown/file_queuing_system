# Step-by-Step Workflow Guide

**This guide shows you exactly how to:**
1. Clone (download) this repository to your computer
2. Do your review work
3. Add your finished files
4. Create a pull request (not merge directly!)

**Follow this every time you work on a review.**

---

## Prerequisites

Before you start, make sure you've completed:
- ✅ [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md) - First-time setup
- ✅ You've been added as a collaborator to the repository
- ✅ You have a Personal Access Token saved

---

## Part 1: Clone the Repository (First Time Only)

You only need to do this **once** when you first start working on reviews.

### Step 1: Open PowerShell

1. Press the **Windows key**
2. Type `PowerShell`
3. Press **Enter**

### Step 2: Choose Where to Save the Repository

Pick a location on your computer. We recommend:
```powershell
cd C:\Users\YourName\Documents
```
Replace `YourName` with your actual Windows username.

**⚠️ Important:** Don't use a folder that syncs with OneDrive, Dropbox, or Google Drive. Git handles syncing for you.

### Step 3: Clone the Repository

Copy and paste this command:

```powershell
git clone https://github.com/Lizo-RoadTown/file_queuing_system.git
```

Press **Enter**.

**You'll be asked for:**
- **Username:** Type your GitHub username and press Enter
- **Password:** **Paste your Personal Access Token** (NOT your GitHub password!) and press Enter

> **Note:** When you paste the token, you won't see any characters appear. This is normal! Just paste and press Enter.

**You'll see:**
```
Cloning into 'file_queuing_system'...
remote: Enumerating objects: ...
remote: Counting objects: 100% ...
Receiving objects: 100% ...
done
```

✅ **Success!** The repository is now on your computer.

### Step 4: Navigate Into the Repository

```powershell
cd file_queuing_system
```

### Step 5: Set Up Your Python Environment (First Time Only)

Follow the instructions in [LOCAL_SETUP_GUIDE.md - Step 4](LOCAL_SETUP_GUIDE.md#step-4-set-up-your-python-environment) to create your conda environment.

---

## Part 2: Daily Workflow - Starting Your Work

**Do this every time you sit down to work on a review.**

### Step 1: Open PowerShell and Navigate to the Repository

```powershell
cd C:\Users\YourName\Documents\file_queuing_system
```

### Step 2: Get the Latest Changes from GitHub

Before you start working, always pull the latest changes:

```powershell
git pull
```

**What this does:** Downloads any changes other people made since you last worked.

**You'll see:**
```
Already up to date.
```
or
```
Updating abc1234..def5678
Fast-forward
 reviews/... | 10 +++
 1 file changed, 10 insertions(+)
```

### Step 3: Activate Your Python Environment

```powershell
conda activate review-queue
```

Your prompt will change to show `(review-queue)` at the beginning.

### Step 4: Open VS Code

```powershell
code .
```

VS Code will open with the repository loaded.

✅ **You're ready to work!**

---

## Part 3: Doing Your Review Work

This is where you actually do your review. The specific steps depend on whether you're doing a first review or second review (see [CONTRIBUTING.md](../CONTRIBUTING.md) for details).

### Claim an Issue

1. **Go to GitHub** in your web browser:
   ```
   https://github.com/Lizo-RoadTown/file_queuing_system/issues
   ```

2. **Find an issue** labeled `queued` (for first review) or `awaiting-review-2` (for second review)

3. **Click on the issue** to open it

4. **Scroll to the bottom** and type a comment: `/checkout`

5. **Click "Comment"**

The issue will automatically update and assign you. ✅

### Create Your Review Folder

In VS Code:

1. **Right-click** on the `reviews/in-progress/` folder in the left sidebar
2. **Select "New Folder"**
3. **Name it** something descriptive (e.g., `ManuscriptName`)
4. Press **Enter**

### Add Your Files

Add all your review files to this folder:
- Your Jupyter notebook (`.ipynb` file)
- The manuscript PDF
- Output images (PNG files)
- A `metadata.yml` file (see template in [CONTRIBUTING.md](../CONTRIBUTING.md))

**Example folder structure:**
```
reviews/in-progress/MyReview/
├── manuscript.pdf
├── 10.1234.example.ipynb
├── output.png
└── metadata.yml
```

---

## Part 4: Saving Your Work to Git

Now you need to save your work and send it to GitHub. This is a **3-step process**: Stage → Commit → Push.

### Understanding Git Saves

Think of Git like taking a photo:
1. **Stage** = Arrange what you want in the photo
2. **Commit** = Take the photo and write a caption
3. **Push** = Upload the photo to the cloud (GitHub)

### Step 1: Check What Changed

In PowerShell (or VS Code's terminal - press `` Ctrl+` ``):

```powershell
git status
```

**You'll see** something like:
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        reviews/in-progress/MyReview/

nothing added to commit but untracked files present
```

This shows what files you've added or changed (in red).

### Step 2: Stage Your Files

This tells Git which files to save.

**To add everything you've changed:**
```powershell
git add .
```

The `.` means "add everything."

**Or to add specific files only:**
```powershell
git add reviews/in-progress/MyReview/
```

**Check it worked:**
```powershell
git status
```

Now the files should be in green under "Changes to be committed."

### Step 3: Commit Your Changes (Take the Photo)

This saves your changes **locally** on your computer with a description.

```powershell
git commit -m "Add first review for MyReview"
```

**The text in quotes** is your commit message. Make it descriptive:
- ✅ `"Add first review for Hepatitis B manuscript"`
- ✅ `"Fix typo in metadata.yml"`
- ✅ `"Add output images for SIR model"`
- ❌ `"stuff"` (too vague)
- ❌ `"update"` (doesn't say what was updated)

**You'll see:**
```
[main abc1234] Add first review for MyReview
 4 files changed, 250 insertions(+)
 create mode 100644 reviews/in-progress/MyReview/manuscript.pdf
 ...
```

### Step 4: Push to GitHub (Upload to the Cloud)

This uploads your changes to GitHub so others can see them.

```powershell
git push
```

**You'll see:**
```
Enumerating objects: ...
Counting objects: 100% ...
Writing objects: 100% ...
To https://github.com/Lizo-RoadTown/file_queuing_system.git
   abc1234..def5678  main -> main
```

✅ **Your changes are now on GitHub!**

---

## Part 5: Creating a Pull Request

**Important:** You create a **Pull Request**, not a direct merge. A pull request lets others review your work before it's added to the main repository.

### What's a Pull Request?

A pull request (PR) is like saying: *"Hey, I've finished some work. Can you review it and add it to the main repository?"*

**You do NOT merge directly.** Ever. Always create a pull request.

### Step 1: Go to GitHub

Open your web browser and go to:
```
https://github.com/Lizo-RoadTown/file_queuing_system
```

### Step 2: You'll See a Yellow Banner

After you push, GitHub usually shows a yellow banner at the top:

```
[branch icon] main had recent pushes less than a minute ago
                                     [Compare & pull request]
```

**Click the "Compare & pull request" button.**

If you don't see the banner:
1. Click the **"Pull requests"** tab at the top
2. Click the green **"New pull request"** button
3. Make sure it says `base: main` ← `compare: main`
4. Click **"Create pull request"**

### Step 3: Fill Out the Pull Request

You'll see a form:

**Title:** GitHub auto-fills this with your commit message. You can change it if needed.
- Example: `Add first review for MyReview`

**Description:** Add details about what you did:
```
- Added Jupyter notebook reproducing the model
- Included manuscript PDF
- Generated output plots
- Created metadata.yml

Closes #5
```

> **Tip:** If your PR completes an issue, add `Closes #X` where X is the issue number. This automatically closes the issue when the PR is merged.

**Reviewers (optional):** You can request someone review your PR by clicking the gear icon next to "Reviewers" and selecting them.

### Step 4: Create the Pull Request

Click the green **"Create pull request"** button.

✅ **Done!** Your pull request is now created.

### What Happens Next?

1. **Automated checks run** - GitHub Actions will validate your submission
   - Check if you have all required files
   - Verify the folder structure is correct
   - Usually takes 1-2 minutes

2. **You'll see check marks or X's** next to the checks:
   - ✅ Green check = passed
   - ❌ Red X = failed (click "Details" to see why)

3. **If checks fail:**
   - Read the error message
   - Fix the issue in your files
   - Save and push again (repeat Part 4, Steps 2-4)
   - The PR automatically updates with your new changes

4. **Reviewers or maintainers will review your PR**
   - They might request changes
   - They might approve it

5. **Once approved, someone will merge it**
   - NOT you! A maintainer merges it
   - The PR will close automatically
   - Your changes are now part of the main repository

---

## Part 6: If You Need to Make Changes to Your Pull Request

If the automated checks fail or someone requests changes:

### Step 1: Make the Changes

Edit your files in VS Code to fix the issues.

### Step 2: Save to Git Again

```powershell
git add .
git commit -m "Fix metadata.yml format"
git push
```

✅ **Your pull request automatically updates** with the new changes! You don't need to create a new PR.

---

## Part 7: After Your PR is Merged

Once a maintainer merges your pull request:

### Step 1: Pull the Latest Changes

```powershell
git pull
```

This downloads the merged changes back to your computer.

### Step 2: Update the Issue (If Doing First Review)

If you just completed a **first review**:

1. Go to the issue on GitHub
2. The folder should now be moved to `reviews/awaiting-review-2/` by a maintainer OR
3. You can update the issue label to `awaiting-review-2`

If you just completed a **second review**:
- Comment `/approve` on the issue
- The system will automatically close it and email the package

---

## Quick Reference: Complete Workflow

### Every Time You Start Working

```powershell
# Navigate to repository
cd C:\Users\YourName\Documents\file_queuing_system

# Get latest changes
git pull

# Activate environment
conda activate review-queue

# Open VS Code
code .
```

### When You're Done Working

```powershell
# Check what changed
git status

# Stage all changes
git add .

# Commit with a message
git commit -m "Describe what you did"

# Push to GitHub
git push
```

### Then on GitHub (web browser)

1. Click **"Compare & pull request"**
2. Fill out title and description
3. Click **"Create pull request"**
4. Wait for checks and approval
5. A maintainer will merge it (not you!)

---

## Common Questions

### Do I merge my own pull request?

**NO.** Always let a maintainer merge it. Creating a pull request is asking for permission to add your changes. Merging is granting that permission.

### What if I have more work to do after creating a PR?

Just edit your files, then:
```powershell
git add .
git commit -m "Add more changes"
git push
```

The PR updates automatically!

### What if someone else merged changes while I was working?

Before pushing:
```powershell
git pull
```

If there are conflicts (you both edited the same file), Git will tell you. Ask a maintainer for help resolving conflicts.

### Can I work on multiple reviews at once?

Yes, but it's easier to use **branches** for this. That's an advanced topic - ask a maintainer for guidance.

### I pushed to the wrong place / made a mistake!

Don't panic! Git can undo almost anything. Contact a maintainer and explain what happened.

---

## Troubleshooting

### "Git push rejected" or "Updates were rejected"

**Cause:** Someone else pushed changes before you.

**Fix:**
```powershell
git pull
git push
```

### "Your branch is behind origin/main"

**Cause:** GitHub has newer changes than your computer.

**Fix:**
```powershell
git pull
```

### "There isn't anything to compare" when creating PR

**Cause:** You didn't push your changes yet.

**Fix:** Go back to Part 4 and push your changes.

### "Please tell me who you are" error

**Cause:** Git doesn't know your name/email.

**Fix:**
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Then try committing again.

### Can't push - asks for password every time

**Fix:** Use your Personal Access Token, not your GitHub password. If you lost it, generate a new one (see [LOCAL_SETUP_GUIDE.md - Step 2.3](LOCAL_SETUP_GUIDE.md#step-2-get-access-to-the-repository)).

---

## Getting Help

If you're stuck:

1. **Check this guide's Troubleshooting section** (above)
2. **Check** [LOCAL_SETUP_GUIDE.md - Troubleshooting](LOCAL_SETUP_GUIDE.md#troubleshooting)
3. **Ask a maintainer or teammate** - share:
   - What you were trying to do
   - The exact error message
   - What you've already tried
4. **Open an issue** on GitHub labeled "help wanted"

**Remember:** Everyone learns this eventually. Don't be afraid to ask questions!

---

## Summary

1. **Clone once** (first time only)
2. **Pull** every time you start working
3. **Do your review work** in `reviews/in-progress/`
4. **Stage, commit, push** your changes
5. **Create a pull request** on GitHub (don't merge!)
6. **Wait for approval** and let a maintainer merge

That's it! Follow these steps and you'll be contributing successfully. 🎉
