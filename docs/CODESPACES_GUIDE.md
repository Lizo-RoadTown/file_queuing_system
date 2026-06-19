# GitHub Codespaces Guide

This guide walks you through everything you need to know to work on this project using GitHub Codespaces. You do not need to install anything on your computer. Everything runs in your web browser.

> **Heads up on the current state of the devcontainer.** The three files in `.devcontainer/` (`devcontainer.json`, `Dockerfile`, `env.yml`) are zero-byte placeholders right now. A Codespace started from this state will open, but it will not have the `epi-sde` conda environment pre-installed. You will need to run `curation-dev/setup/install-env.sh` inside the Codespace to build the environment yourself, or wait until the maintainer populates the devcontainer config. Once those files are filled in, the rest of this guide describes the expected experience.

If you are working in local desktop VS Code, follow [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md) instead and do not reopen this repository in a container.

---

## What is a Codespace?

A **Codespace** is a full coding environment that runs in the cloud and opens in your browser. When you start one, GitHub sets up a computer for you with all the software already installed, Python, the right libraries, everything. You get a version of Visual Studio Code (VS Code) running right in your browser tab.

Think of it like this: instead of setting up a lab bench yourself, you walk in and one is already set up for you.

---

## Part 1: Opening Your Codespace

### Step 1: Go to the repository on GitHub

Open your browser and go to:

```
https://github.com/Lizo-RoadTown/file_queuing_system
```

You will need to be logged in to your GitHub account. If you do not have one, go to [https://github.com](https://github.com), click **Sign up**, and follow the steps. Then ask Liz to add you to the repository.

### Step 2: Start a Codespace

1. On the repository page, click the green **`< > Code`** button near the top right.
2. A small panel will open. Click the **Codespaces** tab at the top of that panel.
3. Click **"Create codespace on main"**.

GitHub will now build your environment. This takes a few minutes the first time. You will see a loading screen that says something like "Setting up your codespace." This is normal, it is installing all the software automatically.

### Step 3: Your Codespace opens

When it is ready, a page that looks like VS Code will open in your browser. This is your workspace. You will see:

- **Left sidebar**, a file explorer showing all the files in the repository
- **Main area**, where files and notebooks open
- **Bottom panel**, a Terminal (a text interface where you can type commands)

You are now inside the project. The environment is already set up. You do not need to install Python or any libraries.

---

## Part 2: Understanding the Layout

Here is what the folders contain:

| Folder | What it is |
|---|---|
| `curation-dev/` | Your personal workspace. This is where you do your work. |
| `curation-dev/template/` | Contains the blank notebook template you copy for each paper. |
| `curation-dev/notebooks/` | Where you save your in-progress notebooks. |
| `reviews/awaiting-review-2/` | Finished notebooks waiting to be reviewed by someone else. |
| `reviews/in-progress/` | Notebooks currently being reviewed. |
| `reviews/completed/` | Notebooks that have been fully reviewed. |
| `queue/` | The list of papers to be worked on. |
| `docs/` | Guides and documentation (you are reading one now). |

---

## Part 3: Starting a New Curation

A "curation" means taking one paper, re-implementing its SDE model in a notebook, running it, and recording what happened.

### Step 1: Pick a paper with your teammate

Curation happens in teams of 2. With your teammate, choose a published epidemiological SDE model that has a DOI (or comparable identifier) and describes infection dynamics. Decide which teammate will be the implementing curator. The implementing curator's GitHub handle becomes `reviewer_1` on the resulting PR.

There is no curation-side queue or `/checkout` step at this stage. Paper selection is informal and coordinated within the team.

### Step 2: Copy the blank template

In the file explorer (left sidebar), navigate to `curation-dev/template/curation-template.ipynb`. Right-click the file and choose **Copy**, then right-click the `curation-dev/notebooks/` folder and choose **Paste**. Rename the new copy to a unique name for your paper, for example `<doi>.ipynb` or `<short-name>.ipynb`.

Anything you save inside `curation-dev/notebooks/` is gitignored. It will not appear on the repository's history until you move it into `reviews/awaiting-review-2/` in Part 5.

### Step 3: Open the notebook

Click on the notebook file to open it. The notebook will open in the main area.

A Jupyter notebook is made of **cells**. There are two kinds:
- **Text cells** (called Markdown cells), contain written notes and headings. You cannot run these.
- **Code cells**, contain Python code. You run these to execute the code.

### Step 4: Fill in the metadata header

The first cell in the notebook is the metadata header. It is a text cell that looks like a form. Fill in each field:

- **Curator**, your name
- **Title**, the full title of the paper
- **Pathogen**, the disease or organism the model is about
- **DOI**, the paper's DOI
- **Figure**, which figure in the paper you are reproducing (e.g., "Figure 3")
- **Outcome**, leave this as `Successful` for now; update it when you are done
- **Notes**, leave blank for now; fill in anything important when you are done

To edit a text cell, double-click on it. Click somewhere else (or press Escape) when you are done.

### Step 5: Implement the model


The next section of the notebook is where you write the model. It is a code cell with several variables already named for you. You fill them in based on what the paper says:

- `variable_names`, the names of the model's state variables (e.g., S, I, R)
- `parameter_names`, the names of the parameters (e.g., beta, gamma)
- `initial_values`, the starting values for each variable
- `parameter_values`, the value of each parameter
- `initial_time`, `final_time`, the start and end of the simulation
- `drift_term(t, y, p)`, the deterministic part of the model (from the paper's equations)
- `diffusion_term(t, y, p)`, the stochastic part of the model

See `curation-dev/notebooks/curation-example.ipynb` for a complete worked example of a filled-in notebook.

### Step 6: Run the notebook

Once you have filled in the model, you run it to see if it works.

**To run all cells at once:**
1. Click the **"Run All"** button at the top of the notebook (it looks like ▶▶ with the label "Run All").
2. Or go to the menu: **Run → Run All Cells**.

The cells will run from top to bottom. You will see output appear below each code cell. The last cell produces a figure.

- If a cell produces a red error message, something went wrong. Read the error, it will tell you what the problem is.
- If all cells run and you see a figure at the bottom, the model ran successfully.

### Step 7: Update Outcome and Notes

After running the notebook, go back to the metadata header cell, double-click to edit it, and:

- Set **Outcome** to `Successful` if the figure looks like the figure in the paper, or `Failed` if you could not get it to work.
- Fill in **Notes** with anything relevant, assumptions you made, things you could not find in the paper, anything that deviated from what the paper says.

---

## Part 4: Saving and Syncing Your Work

In a Codespace, your files are saved automatically as you work. But to share your work with the rest of the team, you need to **commit** and **push** your changes. This is how you send your files to GitHub.

### What "commit" and "push" mean

- **Commit**, taking a snapshot of your changes and giving it a label (like saving a version)
- **Push**, sending that snapshot to GitHub so others can see it

### How to commit and push in VS Code

1. In the left sidebar, click the **Source Control** icon. It looks like a small branching diagram (three dots connected by lines). If you have unsaved changes, it will show a number badge.
2. You will see a list of files that have changed.
3. At the top of that panel, there is a text box that says **"Message"**. Type a short description of what you did (e.g., `Add curation for 10_1016j_chaos_2020_110381`).
4. Click the **✓ Commit** button (or press Ctrl+Enter).
5. Click **Sync Changes** (or the cloud-with-arrow icon) to push to GitHub.

Your notebook is now on GitHub and the team can see it.

---

## Part 5: Submitting a Finished Notebook for Review

There is no `/approve` step on the curator side. The actual submission is a pull request. When you and your teammate agree the notebook is ready (the verifying teammate has re-run it from a clean kernel and confirmed Outcome and Notes), the implementing curator submits.

### Step 1: Create the submission folder

In the file explorer, create a folder `reviews/awaiting-review-2/<paper-id>/`. Use a short paper identifier as the folder name (for example `HBV` or `DOI_10.1016_Koufi_2022`).

### Step 2: Add the required files

Copy the finished notebook from `curation-dev/notebooks/` into the new folder. Add the manuscript PDF. Optionally add an output image (`.png` or `.svg`) showing your reproduced figure. Optionally pre-populate `metadata.yml` with the DOI.

At minimum the folder must contain one `.ipynb` and one `.pdf`. `validate-submission.yml` will block the PR if those are missing.

### Step 3: Commit, push, and open a pull request

1. Commit your work (see Part 4 above). Push to a feature branch.
2. Open a pull request against `main` from the GitHub UI.
3. Wait for `validate-submission.yml` to run. It checks the folder shape, warns on missing output image, and writes your GitHub handle into the new folder's `metadata.yml` as `reviewer_1`.
4. Merge the PR once the check is green.

### What happens after merge

The merge triggers `bootstrap-seed-issues.yml`, which creates a `[REVIEW]` issue with the `awaiting-review-2` label. The issue is your handoff point to the second-review side. An independent reviewer (not you, not your teammate) picks it up with `/checkout` from the issue and verifies your work. See `CONTRIBUTING.md` for the reviewer side.

`update-queue-csv.yml` also appends a row to `queue/review_log.csv` with the paper name, DOI, your handle, and the issue number.

---

## Part 6: Picking Up a Review from the Queue

For how to claim and complete a review, see [PROCESS.md](PROCESS.md).

---

## Part 7: The Terminal

The Terminal is the black panel at the bottom of your Codespace. It lets you type commands directly. You will not need it often, but here are a few useful ones:

| Command | What it does |
|---|---|
| `git pull` | Downloads the latest changes from GitHub |
| `git status` | Shows which files you have changed |
| `conda activate epi-sde` | Activates the project's Python environment (this happens automatically when the Codespace opens) |

To open a terminal if you do not see one: go to **Terminal → New Terminal** in the menu at the top.

---

## Part 8: Closing and Reopening Your Codespace

You can close your browser tab at any time. Your work is saved.

To reopen your Codespace:
1. Go to [https://github.com/Lizo-RoadTown/file_queuing_system](https://github.com/Lizo-RoadTown/file_queuing_system).
2. Click **`< > Code`** → **Codespaces** tab.
3. You will see your existing Codespace listed. Click on it to reopen it.

You do not need to create a new one each time.

---

## Troubleshooting

**The notebook shows an error when I run it.**
Read the error message, it usually tells you exactly what went wrong. Common causes: a variable name is misspelled, a value is missing, or the function is not returning the right thing. Check the worked example (`curation-example.ipynb`) for reference.

**I do not see my files after pulling.**
Make sure you clicked **Sync Changes** in the Source Control panel, or ran `git pull` in the terminal.

**The Codespace is taking a long time to start.**
The first time always takes a few minutes. After that it is faster. If it seems stuck, try refreshing the page.

**I cannot commit, it says my name and email are not set.**
Open the terminal and run:
```
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```
Then try committing again.

**I am not sure I did something right.**
Ask Liz. That is what she is there for.
