# Methodology

## What the steps are

The operator's procedure has six tasks: install the required software, obtain repository access, clone the repository, set up the Python environment, open the working tree in Visual Studio Code, and run the daily workflow. The first five are one-time. The sixth repeats every session.

### Local-setup hierarchical task analysis

```mermaid
flowchart TD
    G[Goal: a local checkout that serves<br/>both the curator role and the<br/>independent-reviewer role]
    G --> T1[Task 1<br/>Install required software]
    G --> T2[Task 2<br/>Obtain repository access]
    G --> T3[Task 3<br/>Clone the repository]
    G --> T4[Task 4<br/>Set up the Python environment]
    G --> T5[Task 5<br/>Open in Visual Studio Code]
    G --> T6[Task 6<br/>Run the daily workflow]

    T1 --> T1a[1a. Install Git from git-scm.com<br/>verify with git --version]
    T1 --> T1b[1b. Install Visual Studio Code<br/>check "Add to PATH"]
    T1 --> T1c[1c. Install Miniconda<br/>check "Add Miniconda3 to PATH"<br/>verify with conda --version]
    T1 --> T1d[1d. Create a GitHub account<br/>save username and password]

    T2 --> T2a[2a. Send GitHub username<br/>to the repository owner]
    T2 --> T2b[2b. Accept the collaborator<br/>email invitation]
    T2 --> T2c[2c. Generate a Personal Access Token<br/>Settings > Developer settings ><br/>Tokens (classic) > repo scope]
    T2 --> T2d[2d. Save the PAT in a password<br/>manager or secure note]

    T3 --> T3a[3a. Open PowerShell, cd into<br/>Documents or Projects<br/>(not a OneDrive-synced folder)]
    T3 --> T3b[3b. git clone https://github.com/<br/>Lizo-RoadTown/file_queuing_system.git]
    T3 --> T3c[3c. Enter GitHub username<br/>paste PAT as password]
    T3 --> T3d[3d. cd file_queuing_system]

    T4 --> T4a[4a. Write env.yml<br/>(review-queue + python=3.11 + basic stack)<br/>or use curation-dev/setup/env.yml<br/>(epi-sde + diffrax + jax==0.6)]
    T4 --> T4b[4b. conda env create -f env.yml<br/>or run curation-dev/setup/install-env.*]
    T4 --> T4c[4c. conda activate <env>]
    T4 --> T4d[4d. python -m ipykernel install --user<br/>--name <env> --display-name "<label>"]

    T5 --> T5a[5a. code . from PowerShell<br/>or launch-code.* from curation-dev/]
    T5 --> T5b[5b. Dismiss "Reopen in Container" prompt]
    T5 --> T5c[5c. Install extensions:<br/>Python, Jupyter,<br/>GitHub Pull Requests and Issues]
    T5 --> T5d[5d. Ctrl+Shift+P > Python: Select Interpreter<br/>choose review-queue or Review Queue Python]

    T6 --> T6a[6a. cd into the repository]
    T6 --> T6b[6b. conda activate <env>]
    T6 --> T6c[6c. git pull]
    T6 --> T6d[6d. code . and do work]
    T6 --> T6e[6e. git add, git commit, git push<br/>or Source Control > commit > sync]
```

### Task 1: Install required software

The operator installs four items: Git, Visual Studio Code, Miniconda, and a GitHub account. Each install has a verification cue: `git --version` returns a version string, `code .` opens the editor, `conda --version` returns a version string, and the GitHub account is verified by logging in to github.com. Miniconda's installer warns against adding itself to PATH; the guide overrides that warning because the rest of the workflow depends on `conda` being callable from PowerShell.

**Steps in detail:**

| Step | What happens | What you see | How you know it's done |
|---|---|---|---|
| Install Git | Operator downloads installer from git-scm.com; accepts defaults; sets Visual Studio Code as default editor | Installer reports success | `git --version` returns a version string |
| Install Visual Studio Code | Operator downloads installer from code.visualstudio.com; checks "Add to PATH" | Installer reports success | `code .` opens the editor from PowerShell |
| Install Miniconda | Operator downloads Miniconda3 64-bit; checks "Add Miniconda3 to my PATH environment variable" | Installer reports success | `conda --version` returns a version string after PowerShell restart |
| Create GitHub account | Operator signs up at github.com | GitHub confirms account creation by email | Operator can log in |

### Task 2: Obtain repository access

The operator sends their GitHub username to the maintainer, accepts the collaborator invitation, and generates a Personal Access Token. The PAT replaces the password for git operations because GitHub no longer accepts passwords over HTTPS. The PAT carries `repo` scope and a 90-day expiry. The operator saves the PAT outside the terminal scrollback because GitHub does not show the token after the generation screen closes.

**Steps in detail:**

| Step | What happens | What you see | How you know it's done |
|---|---|---|---|
| Send GitHub username | Operator sends username to maintainer | Maintainer adds the operator as a collaborator | Operator receives collaborator invitation email |
| Accept invitation | Operator clicks the link in the email | GitHub confirms collaborator status | Operator sees the repository in their account |
| Generate PAT | Operator navigates to Settings > Developer settings > Tokens (classic) > Generate new token (classic); selects `repo` scope; sets 90-day expiry | GitHub displays the token once on the result page | Token string starting `ghp_` is shown |
| Save PAT | Operator copies the token into a password manager or secure note | None | Token is stored outside the browser session |

### Task 3: Clone the repository

The operator opens PowerShell, navigates to a non-synced folder (`Documents/` or `Projects/`, never an OneDrive-synced folder), and runs `git clone https://github.com/Lizo-RoadTown/file_queuing_system.git`. Git prompts for credentials; the operator enters their GitHub username and pastes the PAT in place of a password. The clone produces a `file_queuing_system/` directory with the full repository history. The operator changes into the directory to prepare for the environment build.

**Steps in detail:**

| Step | What happens | What you see | How you know it's done |
|---|---|---|---|
| Choose location | Operator picks `Documents/` or `Projects/`; avoids OneDrive-synced folders | None | Operator is in a non-synced directory |
| Run `git clone` | Git contacts github.com over HTTPS | Git asks for username | Prompt appears |
| Authenticate | Operator enters GitHub username and pastes PAT as password | Git accepts the credentials and begins downloading | Object counts increase on screen |
| Download completes | Git writes objects to `file_queuing_system/.git/` and the working tree | Git reports "Cloning into 'file_queuing_system'..." then exits | Operator can `cd file_queuing_system` |

### Task 4: Set up the Python environment

The operator picks the environment definition that matches their role. The user-facing guide describes a `review-queue` environment built from a hand-written `setup/env.yml` with `python=3.11`, `numpy`, `matplotlib`, `scipy`, `pandas`, `notebook`, `ipywidgets`, and `pip`. The curator-side scripts in `curation-dev/setup/` build an `epi-sde` environment from `curation-dev/setup/env.yml` with the same numerical stack plus `tqdm`, `ipyevents`, `nomkl`, `diffrax`, and `jax==0.6`. The operator runs either `conda env create -f setup/env.yml` directly or the wrapper script `curation-dev/setup/install-env.sh` (`.bat` on Windows), which calls `conda env remove` followed by `conda env create` to guarantee a clean rebuild. The operator activates the environment with `conda activate <env>` and registers the Jupyter kernel with `python -m ipykernel install --user --name <env> --display-name "<label>"`.

**Steps in detail:**

| Step | What happens | What you see | How you know it's done |
|---|---|---|---|
| Write or select `env.yml` | Operator either creates `setup/env.yml` per the guide (review-queue) or uses `curation-dev/setup/env.yml` (epi-sde) | None | File exists on disk |
| Create the environment | `conda env create -f <env.yml>` reads channels and dependencies; downloads packages from conda-forge | conda prints download progress, then "done" | Final message points at `conda activate <env>` |
| Activate the environment | `conda activate <env>` modifies the shell so `python` resolves to the env's interpreter | Prompt prefix changes to `(<env>)` | Operator sees the prefix |
| Register Jupyter kernel | `python -m ipykernel install --user --name <env> --display-name "<label>"` writes a kernel spec under the user's Jupyter config | ipykernel prints the install location | Kernel appears in Jupyter kernel picker |

### Task 5: Open in Visual Studio Code

The operator opens Visual Studio Code with the repository as the workspace root, either by running `code .` from PowerShell while the environment is active, or by running `curation-dev/launch-code.sh` (`.bat` on Windows), which activates `epi-sde` and runs `code .` in one step. Visual Studio Code may show a "Reopen in Container" prompt; the operator dismisses it because the `.devcontainer/` files are empty and the local path is the working route. The operator installs three extensions (Python, Jupyter, GitHub Pull Requests and Issues) and selects the conda environment as the Python interpreter via the Command Palette.

**Steps in detail:**

| Step | What happens | What you see | How you know it's done |
|---|---|---|---|
| Launch the editor | `code .` from the activated environment, or `launch-code.*` from `curation-dev/` | Visual Studio Code opens with the repository as the workspace root | Editor window is visible |
| Dismiss container prompt | Operator clicks "No" or closes the prompt | Prompt disappears; editor stays in the local window | Workspace stays local |
| Install extensions | Operator installs Python, Jupyter, and GitHub Pull Requests and Issues from the Extensions panel | Each extension reports "Installed" | All three appear under Installed |
| Select interpreter | `Ctrl+Shift+P` > `Python: Select Interpreter` > pick `review-queue` or `Review Queue Python` | The status bar shows the selected interpreter | Operator sees the env name in the status bar |

### Task 6: Run the daily workflow

The operator runs the daily workflow every session. The pattern is: change into the repository, activate the environment, pull from `origin/main`, open the editor, do work, and commit + push the changes. The Source Control panel in Visual Studio Code is the preferred way to commit and sync because it surfaces the staged file list and the diff before the commit. The terminal path (`git add`, `git commit -m`, `git push`) is the backup. Pulling at the start of each session avoids the "Your branch is behind" and "Updates were rejected" failures that appear when the operator's local branch has drifted from `main`.

**Steps in detail:**

| Step | What happens | What you see | How you know it's done |
|---|---|---|---|
| Navigate to the repository | `cd C:\Users\<name>\Documents\file_queuing_system` (or the chosen path) | Prompt shows the current directory | Operator is at the repository root |
| Activate the environment | `conda activate review-queue` (or `epi-sde`) | Prompt prefix changes to the env name | Operator sees the prefix |
| Pull from `origin/main` | `git pull` contacts GitHub over HTTPS using cached PAT | Git reports fast-forward or no-op | Working tree is up to date |
| Open the editor | `code .` from the same shell | Visual Studio Code opens with the workspace | Editor window appears |
| Edit and run | Operator edits files and runs notebooks against the registered kernel | Cell outputs appear in notebooks | Operator's work is complete |
| Commit and sync | Operator stages files in Source Control, types a commit message, clicks the checkmark, clicks Sync Changes; or runs `git add`, `git commit -m`, `git push` | Visual Studio Code shows the push completion; Git prints the push result | Changes appear on `origin/main` |

---

## Sequence diagram

The first-time setup involves the operator, PowerShell, Git, conda, the GitHub web UI, and Visual Studio Code. The sequence below traces the interactions from a fresh machine to a working checkout with the environment built and the editor configured.

### First-time setup sequence

```mermaid
sequenceDiagram
    actor User as Operator
    participant PS as PowerShell
    participant Git as Git
    participant Conda as Conda
    participant GH as GitHub web
    participant VSC as Visual Studio Code

    User->>GH: open github.com, sign up
    GH-->>User: account created
    User->>GH: send username to maintainer (out of band)
    GH-->>User: collaborator invitation by email
    User->>GH: accept invitation
    User->>GH: Settings > Developer settings ><br/>Tokens (classic) > Generate new (classic)
    GH-->>User: PAT shown once (ghp_...)
    User->>User: save PAT in password manager

    User->>PS: open PowerShell
    User->>PS: cd C:\Users\<name>\Documents
    User->>PS: git clone https://github.com/<br/>Lizo-RoadTown/file_queuing_system.git
    PS->>Git: git clone
    Git->>GH: HTTPS request for repository
    GH-->>Git: ask for credentials
    Git-->>User: prompt for username + password
    User->>Git: enter username + paste PAT
    Git->>GH: authenticate with PAT
    GH-->>Git: send repository objects
    Git-->>PS: working tree at file_queuing_system/
    User->>PS: cd file_queuing_system

    User->>PS: write setup/env.yml (review-queue)<br/>or use curation-dev/setup/env.yml (epi-sde)
    User->>PS: conda env create -f <env.yml><br/>or curation-dev/setup/install-env.*
    PS->>Conda: env create
    Conda->>Conda: resolve dependencies from conda-forge
    Conda-->>PS: "done" + activate instruction
    User->>PS: conda activate <env>
    PS-->>User: prompt prefix shows (<env>)
    User->>PS: python -m ipykernel install --user<br/>--name <env> --display-name "<label>"
    PS-->>User: kernel spec installed

    User->>PS: code .
    PS->>VSC: launch with workspace
    VSC-->>User: open editor; prompt "Reopen in Container"?
    User->>VSC: dismiss prompt
    User->>VSC: install Python, Jupyter,<br/>GitHub Pull Requests and Issues extensions
    User->>VSC: Ctrl+Shift+P > Python: Select Interpreter
    VSC-->>User: list of interpreters
    User->>VSC: choose <env>
    VSC-->>User: status bar shows <env> as interpreter
```

---

## Layered architecture

The local-setup side separates into four layers. The hardware and operating system layer provides the machine, the user account, and the PATH the operator edits during the Git and Miniconda installs. The installed-tools layer is Git, Visual Studio Code, and Miniconda, plus optional GitHub CLI. The workspace layer is the conda environment (`review-queue` or `epi-sde`) and the Jupyter kernel registered against it. The repository layer is the cloned working tree under the operator's chosen folder and the `.git/` directory that holds the commit history. Each layer is replaceable without disturbing the layer above or below.

### Local-setup layered architecture

```mermaid
flowchart TB
    subgraph OS["Hardware and operating system layer"]
        H1[Windows, macOS, or Linux]
        H2[User account with install rights]
        H3[PATH: Git, code, conda]
    end

    subgraph TOOLS["Installed-tools layer"]
        T1[Git<br/>git-scm.com installer]
        T2[Visual Studio Code<br/>code.visualstudio.com installer<br/>extensions: Python, Jupyter,<br/>GitHub Pull Requests and Issues]
        T3[Miniconda<br/>docs.conda.io installer<br/>conda command on PATH]
        T4[Optional: GitHub CLI<br/>for authenticated git over HTTPS]
    end

    subgraph WS["Workspace layer"]
        W1[Conda environment<br/>review-queue (python=3.11 + basic stack)<br/>or epi-sde (full SDE stack<br/>with diffrax + jax==0.6)]
        W2[Jupyter kernel spec<br/>python -m ipykernel install --user<br/>--name <env> --display-name "<label>"]
        W3[Personal Access Token<br/>cached by git credential manager]
    end

    subgraph REPO["Repository layer"]
        R1[Cloned working tree<br/>under Documents/ or Projects/<br/>not OneDrive-synced]
        R2[.git/ commit history<br/>HTTPS remote: github.com/<br/>Lizo-RoadTown/file_queuing_system]
        R3[curation-dev/setup/<br/>install-env.*, rm-env.*,<br/>config.*, env.yml]
        R4[curation-dev/launch-code.*<br/>activate epi-sde + code .]
        R5[docs/LOCAL_SETUP_GUIDE.md<br/>user-facing setup guide]
        R6[.devcontainer/<br/>currently empty<br/>(no local container path)]
    end

    OS --> TOOLS
    TOOLS --> WS
    WS --> REPO
    REPO -.daily workflow.-> WS
```

---

## Tools

### Tools

| Tool | What it does | Where it fits |
|---|---|---|
| Windows, macOS, or Linux | Host operating system for the operator's machine | Hardware and OS |
| PowerShell (Windows) or bash/zsh (macOS, Linux) | Shell for running install commands, git operations, and conda commands | Hardware and OS |
| Git | Version control client; clones the repository, pulls and pushes, holds the local commit history | Installed tools |
| Visual Studio Code | Editor for source files and notebooks; hosts the Python, Jupyter, and GitHub Pull Requests and Issues extensions | Installed tools |
| Miniconda | Conda installer; provides the `conda` command on PATH | Installed tools |
| GitHub Personal Access Token | Replaces the password for git over HTTPS; carries `repo` scope and a 90-day expiry | Installed tools |
| GitHub web UI | Account creation, collaborator invitation acceptance, PAT generation | Installed tools (out of band) |
| `docs/LOCAL_SETUP_GUIDE.md` | User-facing step-by-step setup guide, written for Windows + PowerShell, with a Troubleshooting section that catalogs recurring failure modes | Repository |
| `curation-dev/setup/env.yml` | Conda environment definition for `epi-sde`: `python`, `numpy<2`, `matplotlib`, `scipy`, `pandas`, `tqdm`, `notebook`, `ipywidgets`, `ipyevents`, `nomkl`, `pip`, plus `diffrax` and `jax==0.6` | Repository |
| `curation-dev/setup/install-env.sh` and `.bat` | Wrapper scripts that source `config.*`, run `conda env remove`, and run `conda env create -f env.yml`. Guarantees a clean rebuild on each invocation | Repository |
| `curation-dev/setup/rm-env.sh` and `.bat` | Wrapper scripts that source `config.*` and run `conda env remove`. Used when the operator wants to discard the environment | Repository |
| `curation-dev/setup/config.sh` and `.bat` | Set `EPISDE_ENVNAME=epi-sde`. The `.sh` variant also sets `EPISDE_CONDADIR=${HOME}/miniconda3`. Sourced by the install, removal, and launcher scripts | Repository |
| `curation-dev/launch-code.sh` and `.bat` | One-step launcher: source `config.*`, activate `epi-sde`, run `code .` | Repository |
| Conda environment (`review-queue` or `epi-sde`) | Isolated Python environment selected as the Visual Studio Code interpreter and as the Jupyter kernel | Workspace |
| `python -m ipykernel install --user --name <env> --display-name "<label>"` | Registers the conda environment as a Jupyter kernel so notebooks can pick it up by display name | Workspace |
| `.devcontainer/devcontainer.json`, `.devcontainer/Dockerfile`, `.devcontainer/env.yml` | Currently empty (one blank line each). No local container path is available; local setup uses the conda environment | Repository (inactive) |
