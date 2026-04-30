# Local Setup Guide: Getting Started with the Review Queue

This guide walks you through setting up this repository on your local computer and working with it in Visual Studio Code. **No prior experience with Git, GitHub, or VS Code is required** — we'll explain everything step by step.

---

## Table of Contents

1. [What You'll Install](#what-youll-install)
2. [Step 1: Install Required Software](#step-1-install-required-software)
3. [Step 2: Get Access to the Repository](#step-2-get-access-to-the-repository)
4. [Step 3: Clone the Repository](#step-3-clone-the-repository)
5. [Step 4: Set Up Your Python Environment](#step-4-set-up-your-python-environment)
6. [Step 5: Open in VS Code](#step-5-open-in-vs-code)
7. [Understanding the Repository](#understanding-the-repository)
8. [Optional: GitHub Copilot](#optional-github-copilot)
9. [Daily Workflow](#daily-workflow)
10. [Troubleshooting](#troubleshooting)

---

## What You'll Install

You need four things on your computer:

1. **Git** - Software that tracks changes to files
2. **Visual Studio Code (VS Code)** - A text/code editor (like fancy Notepad)
3. **Python** - Programming language needed for Jupyter notebooks
4. **GitHub Account** - Your online identity for collaborating

Don't worry if you don't know what these are — we'll install and set up everything together.

---

## Step 1: Install Required Software

### 1.1: Install Git

Git is a tool that helps you download and sync files from GitHub.

**Windows:**
1. Go to [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. Click **"Download for Windows"**
3. Run the downloaded installer
4. **Important:** During installation, when asked about default editor, select **"Use Visual Studio Code as Git's default editor"**
5. For all other options, accept the defaults (just keep clicking "Next")
6. Click "Install" and then "Finish"

**To verify it installed:**
1. Open PowerShell (search "PowerShell" in Windows Start menu)
2. Type: `git --version`
3. You should see something like `git version 2.x.x`

### 1.2: Install Visual Studio Code

VS Code is where you'll view and edit files.

1. Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Click the big **"Download for Windows"** button
3. Run the installer
4. **Important:** Check the box that says **"Add to PATH"** during installation
5. Accept all other defaults
6. Click "Install"

### 1.3: Install Python (via Miniconda)

Python is needed to run Jupyter notebooks. We'll use Miniconda, which is a lightweight Python installer.

1. Go to [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. Under Windows installers, download **Miniconda3 Windows 64-bit**
3. Run the installer
4. **Important:** Check **"Add Miniconda3 to my PATH environment variable"** (even if it says "Not recommended")
5. Accept all other defaults
6. Click "Install"

**To verify it installed:**
1. **Close and reopen PowerShell** (important!)
2. Type: `conda --version`
3. You should see something like `conda 24.x.x`

### 1.4: Create a GitHub Account

If you don't have a GitHub account yet:

1. Go to [https://github.com/](https://github.com/)
2. Click **"Sign up"**
3. Follow the prompts to create a free account
4. **Remember your username and password** — you'll need them later

---

## Step 2: Get Access to the Repository

A repository is like a shared folder on GitHub. You need permission to access this private repository.

### Request Access

**Send the repository owner:**
- Your GitHub username (e.g., "john_doe123")
- They will add you as a collaborator

**You'll know you have access when:**
- You receive an email invitation to collaborate
- Click the link in the email and accept the invitation

### Create a Personal Access Token (PAT)

GitHub no longer accepts passwords when downloading repositories. You need a special token instead.

**Creating a PAT:**

1. Log into GitHub in your web browser
2. Click your profile picture (top-right) → **Settings**
3. Scroll down the left sidebar → Click **Developer settings** (near the bottom)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a note like "Review Queue Access"
7. Set expiration to **90 days** (or longer if available)
8. **Important:** Check the box next to **`repo`** (this selects all repo permissions)
9. Scroll down and click **Generate token**
10. **CRITICAL:** Copy the token immediately! It looks like `ghp_xxxxxxxxxxxx`
11. **Save it somewhere safe** — you cannot see it again! (Notepad, password manager, etc.)

---

## Step 3: Clone the Repository

"Cloning" means downloading a copy of the repository to your computer.

### Choose Where to Save It

First, decide where on your computer you want to keep this repository. Good locations:
- `C:\Users\YourName\Documents\review-queue`
- `C:\Users\YourName\Projects\review-queue`

**NOT recommended:**
- Desktop (gets cluttered)
- OneDrive-synced folders (can cause conflicts with Git)

### Clone Using PowerShell

1. **Open PowerShell** (search for it in Windows Start menu)

2. **Navigate to where you want to save the repository:**
   ```powershell
   cd C:\Users\YourName\Documents
   ```
   Replace `YourName` with your actual Windows username.

3. **Clone the repository:**
   ```powershell
   git clone https://github.com/Lizo-RoadTown/file_queuing_system.git
   ```

4. **You'll be asked for credentials:**
   - **Username:** Your GitHub username
   - **Password:** **Paste your Personal Access Token** (NOT your GitHub password!)

5. **Wait for it to download.** You'll see:
   ```
   Cloning into 'file_queuing_system'...
   remote: Enumerating objects: ...
   remote: Counting objects: ...
   Receiving objects: 100% ...
   ```

6. **Navigate into the repository:**
   ```powershell
   cd file_queuing_system
   ```

✅ **Success!** You now have a local copy of the repository.

---

## Step 4: Set Up Your Python Environment

The repository requires specific Python libraries. We'll create an isolated environment so these don't conflict with anything else on your computer.

### 4.1: Create an Environment Configuration File

We need to tell Python what libraries to install.

1. **While still in PowerShell, navigate to the repository:**
   ```powershell
   cd C:\Users\YourName\Documents\file_queuing_system
   ```

2. **Create a `setup` folder:**
   ```powershell
   mkdir setup
   ```

3. **Open VS Code to create a file:**
   ```powershell
   code setup/env.yml
   ```
   
   This will open VS Code with a new empty file.

4. **Copy and paste this EXACTLY into the file:**
   ```yaml
   name: review-queue
   channels:
     - conda-forge
   dependencies:
     - python=3.11
     - numpy
     - matplotlib
     - scipy
     - pandas
     - notebook
     - ipywidgets
     - pip
   ```

5. **Save the file:**
   - Press `Ctrl+S`
   - Close the tab

### 4.2: Create the Environment

Back in PowerShell:

```powershell
conda env create -f setup/env.yml
```

This will take 2-5 minutes. You'll see lots of text scrolling by — that's normal!

**When it's done, you'll see:**
```
done
#
# To activate this environment, use
#
#     $ conda activate review-queue
```

### 4.3: Activate the Environment

Every time you work on this repository, you must activate the environment first:

```powershell
conda activate review-queue
```

Your PowerShell prompt will change to show `(review-queue)` at the beginning:
```
(review-queue) C:\Users\YourName\Documents\file_queuing_system>
```

✅ **You're ready!** The environment is active.

### 4.4: Install Jupyter Kernel (One-Time Setup)

This lets Jupyter notebooks use your environment:

```powershell
python -m ipykernel install --user --name review-queue --display-name "Review Queue Python"
```

---

## Step 5: Open in VS Code

Now let's open the repository in VS Code for editing.

### Important: Do Not Reopen This Repo in a Container Locally

This project's devcontainer is for GitHub Codespaces only.

- If you are using local VS Code on your own computer, stay in your normal local window.
- If VS Code prompts you to **Reopen in Container**, click **No** or close the prompt.
- Local work for this repository should use your local conda environment from Step 4.

This is expected behavior and prevents accidental container boot on local machines.

### Method 1: From PowerShell (Easiest)

If you're still in PowerShell in the repository folder:

```powershell
code .
```

The `.` means "this folder". VS Code will open.

### Method 2: From VS Code

1. Open VS Code (search for it in Windows Start menu)
2. Click **File → Open Folder**
3. Navigate to `C:\Users\YourName\Documents\file_queuing_system`
4. Click **Select Folder**

### First Time Setup in VS Code

#### Install VS Code Extensions

When you first open the repository, VS Code might show a popup suggesting extensions. If so, click **Install All**. If not:

1. Click the **Extensions** icon in the left sidebar (it looks like four squares)
2. Search for and install these (click the blue "Install" button for each):
   - **Python** (by Microsoft)
   - **Jupyter** (by Microsoft)
   - **GitHub Pull Requests and Issues** (by GitHub)

#### Select Python Interpreter

1. Press `Ctrl+Shift+P` to open the **Command Palette** (a search box at the top)
2. Type: `Python: Select Interpreter`
3. Click on it
4. Choose **`review-queue`** or **`Review Queue Python`**

✅ **VS Code is now set up!**

---

## Understanding the Repository

Now that you've set everything up, let's understand what's in this repository and how it's organized.

### What is a Repository?

Think of a repository as a **shared project folder** that multiple people can work on together. Every file and change is tracked.

### Folder Structure

When you open the repository in VS Code, you'll see these folders in the left sidebar:

```
file_queuing_system/
├── .github/           # Automation scripts (you won't edit these)
├── docs/              # Documentation (guides like this one)
├── queue/             # Queue management files
├── reviews/           # Where you'll do your work
│   ├── in-progress/       # Active reviews
│   ├── awaiting-review-2/ # Ready for second review
│   └── completed/         # Finished reviews
├── CONTRIBUTING.md    # Instructions for reviewers
├── README.md          # Project overview
└── .gitignore         # Files Git should ignore
```

**Key folders you'll use:**
- **`reviews/`** - This is where all review work happens
- **`docs/`** - Documentation and guides

### Read the Project Documentation

Before starting work, read these files (click them in VS Code to open):

1. **`README.md`** - Overview of how the queue system works
2. **`CONTRIBUTING.md`** - Detailed instructions for reviewers

---

## Optional: GitHub Copilot

GitHub Copilot is an AI assistant that can help you write code faster. **It costs money** (~$10/month) and is **completely optional**. Everything in this repository can be done without it.

### What Copilot Does

- Suggests code as you type (like autocomplete on your phone)
- Can explain code if you don't understand it
- Answers questions about programming

### Should You Get It?

**Get Copilot if:**
- You code regularly and want to work faster
- You're learning and want AI help
- Your organization pays for it

**Skip Copilot if:**
- You're only doing occasional reviews
- You prefer to learn by researching yourself
- You don't want to pay for it

### If You Want Copilot

1. Subscribe at [https://github.com/copilot](https://github.com/copilot)
2. In VS Code, install these extensions:
   - **GitHub Copilot**
   - **GitHub Copilot Chat**
3. Sign in when prompted

### Using Copilot (Brief Basics)

**Inline suggestions:**
- As you type, gray text suggestions appear
- Press `Tab` to accept, `Esc` to reject

**Copilot Chat:**
- Press `Ctrl+Shift+I` to open chat
- Ask questions like "How do I create a plot in Python?"
- It will suggest code

**⚠️ Important:** Always review Copilot's suggestions! Don't blindly copy code you don't understand.

---

## Daily Workflow

Here's how to work with the repository on a daily basis.

### Starting Your Work Session

Every time you sit down to work:

1. **Open PowerShell**

2. **Navigate to the repository:**
   ```powershell
   cd C:\Users\YourName\Documents\file_queuing_system
   ```

3. **Activate the Python environment:**
   ```powershell
   conda activate review-queue
   ```
   You'll see `(review-queue)` appear before your prompt.

4. **Get the latest changes from GitHub:**
   ```powershell
   git pull
   ```
   This downloads any changes other people made.

5. **Open VS Code:**
   ```powershell
   code .
   ```

✅ **You're ready to work!**

### Working on a Review

This is covered in detail in [`CONTRIBUTING.md`](../CONTRIBUTING.md), but the quick version:

1. **Find an issue** labeled `awaiting-review-2` on GitHub
2. **Comment `/checkout`** to claim it (the system moves the files for you)
3. **Pull** the latest files so the moved files appear on your computer
4. **Do your review work** (re-run notebooks, compare to the manuscript)
5. **Save your changes to Git** (see below)
6. **Comment `/approve`** on the issue when you're done

### Saving Changes to Git

#### Using VS Code (preferred)

1. Click the **Source Control** icon in the left sidebar
2. Review the changed files — make sure they look right
3. Type a short message in the **Message** box, like:
   - `Verified HBV notebook results`
   - `Added review notes for Cholera manuscript`
4. Click the **checkmark (✓)** to commit
5. Click **Sync Changes**

That's it — your work is on GitHub.

#### Using the terminal (backup)

```powershell
git add .
git commit -m "Verified HBV notebook results"
git push
```

### Syncing Changes from Others

If someone else made changes:

**VS Code:** Source Control panel → **"..."** → **Pull**

**Terminal:** `git pull`

**Do this:**
- At the start of each work session
- Whenever VS Code shows a number on the sync arrows in the bottom status bar

### Ending Your Work Session

1. **Check the Source Control panel** — if files appear there, commit and sync them
2. **Close VS Code**
3. **Deactivate the environment (optional):** `conda deactivate`

Done! Your work is saved both locally and on GitHub.

---

## Troubleshooting

### Git Says "Permission Denied" or "Repository Not Found"

**Possible causes:**
- You haven't been added as a collaborator yet
- Your Personal Access Token expired or is wrong

**Solutions:**
1. Ask the repository owner to add you as a collaborator
2. Generate a new Personal Access Token (see Step 2)
3. When Git asks for a password, paste your PAT, not your GitHub password

### "conda: command not found" or "conda is not recognized"

**Cause:** PowerShell doesn't know where conda is installed.

**Solutions:**
1. **Close and reopen PowerShell** (this often fixes it)
2. Manually add conda to PATH:
   - Search "Environment Variables" in Windows Start
   - Click "Environment Variables"
   - Under "User variables", find "Path"
   - Click "Edit" → "New"
   - Add: `C:\Users\YourName\miniconda3\Scripts`
   - Click OK
   - Restart PowerShell

### "No module named 'xyz'" When Running Notebooks

**Cause:** The Python environment isn't active or the package isn't installed.

**Solutions:**
1. Make sure you activated the environment: `conda activate review-queue`
2. Check your Jupyter kernel (top-right of notebook) is set to "Review Queue Python"
3. If still failing, reinstall the environment:
   ```powershell
   conda env remove -n review-queue
   conda env create -f setup/env.yml
   ```

### VS Code Can't Find Python

**Solutions:**
1. Press `Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose `review-queue` or `Review Queue Python`
4. Reload the VS Code window: `Ctrl+Shift+P` → `Developer: Reload Window`

### VS Code Keeps Asking to Reopen in Container

**Cause:** The repository includes a devcontainer for Codespaces users.

**What to do locally:**
1. Click **No** when prompted to reopen in container.
2. Continue in the current local VS Code window.
3. Use your local Python/conda environment (`review-queue`) from Step 4.

If you accidentally reopen in container locally, it will fail intentionally. Reopen the folder normally and continue.

### Git Says "Your Branch is Behind"

**Cause:** Someone else made changes you don't have yet.

**Solution:**
```powershell
git pull
```

If this fails with conflicts, ask a maintainer for help.

### Git Push Fails with "Updates Were Rejected"

**Cause:** Someone else pushed changes before you did.

**Solution:**
1. Pull the changes: `git pull`
2. If it says "merge failed", you have conflicts (ask a maintainer for help)
3. If it succeeds, then push: `git push`

### "Git is Not Recognized as a Command"

**Cause:** Git isn't installed or isn't in your PATH.

**Solutions:**
1. Reinstall Git (see Step 1.1)
2. During installation, choose "Add Git to PATH"
3. Restart PowerShell

### VS Code Shows Lots of Red Squiggly Lines

**Possible causes:**
- Python isn't selected
- Python environment isn't active
- A file has actual errors

**Solutions:**
1. Select the correct Python interpreter (see "VS Code Can't Find Python" above)
2. If it's a `.ipynb` file, ignore most red squiggles (they're often false positives)
3. If it's a `.py` file, read the error and fix it

### OneDrive Sync Conflicts

**Cause:** If you're syncing the repository folder with OneDrive, Git and OneDrive can fight over files.

**Solution:**
**Don't put the repository in an OneDrive-synced folder**. Instead:
- Put it in `C:\Users\YourName\Projects\` (not synced)
- Use Git to sync changes, not OneDrive
- If you must sync, exclude the `.git` folder from OneDrive

### Forgot My Personal Access Token

**Solution:**
1. Generate a new one (see Step 2.3)
2. Save it somewhere safe this time (password manager, secure note)
3. Next time Git asks for a password, use the new token

---

## Additional Resources

### Learning More About Git

- **Git Basics:** [https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- **GitHub Guides:** [https://guides.github.com/](https://guides.github.com/)
- **Git Cheat Sheet:** [https://education.github.com/git-cheat-sheet-education.pdf](https://education.github.com/git-cheat-sheet-education.pdf)

### Learning More About VS Code

- **VS Code Basics:** [https://code.visualstudio.com/docs/getstarted/userinterface](https://code.visualstudio.com/docs/getstarted/userinterface)
- **Jupyter in VS Code:** [https://code.visualstudio.com/docs/datascience/jupyter-notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)

### Learning More About Python/Conda

- **Conda Basics:** [https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
- **Conda Cheat Sheet:** [https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)

### Project-Specific Help

- **README:** [`../README.md`](../README.md) - How the queue system works
- **CONTRIBUTING:** [`../CONTRIBUTING.md`](../CONTRIBUTING.md) - How to do reviews  
- **SETUP:** [`SETUP.md`](SETUP.md) - For maintainers only

---

## Getting Help

If you're stuck:

1. **Check this guide's Troubleshooting section** (above)
2. **Read the error message carefully** - Google it if unclear
3. **Ask a teammate or maintainer** - include:
   - What you were trying to do
   - The error message (exact text or screenshot)
   - What you've already tried
4. **Open an issue on GitHub** for documentation improvements

Remember: **Everyone was a beginner once!** Don't hesitate to ask questions.

---

## Quick Reference Commands

### Daily Workflow
```powershell
# Navigate to repository
cd C:\Users\YourName\Documents\file_queuing_system

# Activate environment
conda activate review-queue

# Get latest changes
git pull

# Open VS Code
code .
```

### Saving Changes

**VS Code:** Type a message in Source Control → click **✓** → click **Sync Changes**

**Terminal:**
```powershell
git add .
git commit -m "Your message here"
git push
```

### Environment Management
```powershell
# Activate environment
conda activate review-queue

# Deactivate environment
conda deactivate

# List all environments
conda env list

# Delete and recreate environment
conda env remove -n review-queue
conda env create -f setup/env.yml
```

---

**You're all set!** Return to [`CONTRIBUTING.md`](../CONTRIBUTING.md) to learn how to do reviews. Good luck! 🎉
