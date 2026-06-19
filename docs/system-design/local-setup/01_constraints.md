# Constraints

## Who uses this

### Operator setting up a machine

The person setting up the machine is a team member who has been added as a GitHub collaborator and now needs a working local checkout. The operator may be on Windows, macOS, or Linux; the user-facing guide is written for Windows and PowerShell, and the shell scripts in `curation-dev/setup/` cover macOS and Linux through `install-env.sh`, `rm-env.sh`, `config.sh`, and `launch-code.sh`. The Windows path uses the corresponding `.bat` files.

The operator installs four pieces of software: Git, Visual Studio Code, Miniconda, and a GitHub account. The operator requests collaborator access from the repository owner, accepts the email invitation, and generates a Personal Access Token with `repo` scope. The operator clones the repository over HTTPS, using their GitHub username and the PAT in place of a password. The operator builds the Python environment from a conda `env.yml` file, activates it, installs the Jupyter kernel with `python -m ipykernel install --user --name <env> --display-name "<label>"`, opens the working tree in Visual Studio Code, installs the Python, Jupyter, and GitHub Pull Requests and Issues extensions, and selects the conda environment as the Python interpreter. The setup ends when the operator can pull from `main`, activate the environment, and open a notebook with the registered kernel.

### Maintainer supporting setup issues

The maintainer is the repository owner or a delegate who answers questions when the setup path fails. The Troubleshooting section of `docs/LOCAL_SETUP_GUIDE.md` is the maintainer's first line of support: it enumerates the failure modes that recur (conda not on PATH, PAT missing or expired, environment not active, interpreter not selected, "Reopen in Container" prompt, "Your branch is behind", "Updates were rejected", Git not on PATH, OneDrive conflicts with `.git`, forgotten PAT) and gives the resolution for each. The maintainer is also the actor who issues collaborator invitations and approves access requests.

### Future contributor

The future contributor joins the project after the current cohort. They arrive without the team's tribal knowledge, without a maintainer walking them through the steps, and often without a Windows machine. Their interaction with the local-setup side is the user-facing guide and the setup scripts in `curation-dev/setup/`. The guide is the only documentation they have; the scripts are the only automation. The local-setup side serves this user when the guide is self-sufficient end to end and when the scripts produce the same environment they did for earlier operators.

### Downstream Bridge layer

The beneficiary on this side is the downstream Bridge layer, which packages completed reviews into hashable artifacts for cross-organizational handoff. The Bridge depends on the operator having a clean local checkout: a working tree free of merge conflicts, an environment that can re-run the notebook from a clean kernel, and a commit history that has not been corrupted by OneDrive sync or interrupted clones. The local-setup side contributes to the Bridge by ensuring the operator's checkout is the same shape and produces the same notebook outputs that the Bridge will hash downstream.

---

### Primary operator (machine-setup) requirements

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| A complete software inventory | The operator may have none of Git, Visual Studio Code, Miniconda, or a GitHub account installed | `docs/LOCAL_SETUP_GUIDE.md` lists the four items, links to the official download for each, and gives a verification command per install | Operator has install rights on their own machine |
| Step-by-step instructions for Windows + PowerShell | The first cohort is on Windows | The guide is written for PowerShell with paste-ready commands. Each step has a verification cue (`git --version`, `conda --version`, `code .`) | Operator can copy commands from the guide |
| Cross-platform parity for environment build | macOS and Linux operators need the same environment as Windows operators | Shell-script counterparts in `curation-dev/setup/`: `install-env.sh`, `rm-env.sh`, `config.sh`, `launch-code.sh`. Each batch file has a matching `.sh` | Operator's shell can execute the `.sh` scripts |
| Reproducible Python environment | Every operator needs the same packages so notebooks run the same way | `env.yml` in `curation-dev/setup/` pins the channel to `conda-forge` and lists `python`, `numpy<2`, `matplotlib`, `scipy`, `pandas`, `tqdm`, `notebook`, `ipywidgets`, `ipyevents`, `nomkl`, `pip`, plus `diffrax` and `jax==0.6` via pip. The user-facing guide describes a simpler `review-queue` env on `python=3.11` for reviewers who do not need the SDE stack | Operator follows the path that matches their role |
| Jupyter kernel registration | The environment must be selectable as a kernel inside Visual Studio Code notebooks | The guide gives `python -m ipykernel install --user --name review-queue --display-name "Review Queue Python"` as a one-time step | Operator runs the command while the environment is active |
| One-step Visual Studio Code launcher | Operators forget to activate the environment before opening the editor | `curation-dev/launch-code.sh` and `curation-dev/launch-code.bat` source `config.*`, activate `epi-sde`, then run `code .` | Operator uses the launcher rather than opening Visual Studio Code from the Start menu |
| HTTPS clone with PAT authentication | GitHub no longer accepts passwords for git operations | The guide walks through PAT generation with `repo` scope, 90-day expiry, and instructs the operator to paste the PAT when prompted for a password | Operator saves the PAT immediately after generation |
| Selectable interpreter in Visual Studio Code | The editor must point at the conda environment, not a system Python | The guide gives `Ctrl+Shift+P` → `Python: Select Interpreter` → choose `review-queue` or `Review Queue Python` | Operator has installed the Python extension |

### Maintainer (setup-support) requirements

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| A documented failure-mode catalog | The maintainer fields the same questions repeatedly | The Troubleshooting section of `docs/LOCAL_SETUP_GUIDE.md` enumerates nine recurring failure modes with resolution steps | Operators read the Troubleshooting section before asking |
| A path to grant collaborator access | The maintainer must respond to access requests | The guide tells the operator to send their GitHub username and the maintainer adds them as a collaborator via GitHub admin | Maintainer has admin access on the repository |
| A re-runnable environment build | When an operator's environment is broken, the maintainer can recommend a clean rebuild | The scripts `rm-env.*` followed by `install-env.*` produce a fresh `epi-sde`. The guide's Quick Reference covers `conda env remove -n review-queue` followed by `conda env create -f setup/env.yml` for the simpler env | Operator can run the scripts on their own machine |
| Clear signal when the devcontainer is not the right path | Local operators see a "Reopen in Container" prompt | The guide's Step 5 and the Troubleshooting section direct local operators to dismiss the prompt and stay in their local window. The `.devcontainer/` files are currently empty, which is consistent with the local-only path being the only working route | Operator follows the guide's direction |

### Future contributor (self-sufficiency) requirements

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Guide reads end to end without prior context | The future contributor may have no prior contact with the team | The guide opens with "No prior experience with Git, GitHub, or VS Code is required" and explains each tool before installing it. The Table of Contents lists ten sections in execution order | Operator reads top to bottom |
| Cross-platform script availability | Future contributors may be on macOS or Linux | `curation-dev/setup/` carries `.sh` and `.bat` variants for install, removal, and config. `launch-code.sh` and `launch-code.bat` cover the editor launcher | Future contributor's platform matches one of Windows, macOS, or Linux |
| Source for the conda environment definition | The `env.yml` is the source of truth for package versions | `curation-dev/setup/env.yml` is checked into the repository. The user-facing guide instructs the operator to create a separate `setup/env.yml` with a smaller package list for the `review-queue` env | Future contributor picks the file that matches their role |
| A worked launcher script | Future contributors should not have to assemble activate + `code .` themselves | `launch-code.sh` and `launch-code.bat` do both in one command | Future contributor finds the launcher in `curation-dev/` |
| A maintained troubleshooting section | The guide remains useful when the toolchain shifts | Troubleshooting captures conda PATH, PAT, environment activation, interpreter selection, devcontainer prompt, branch-behind, push-rejected, Git PATH, OneDrive, and forgotten-PAT failure modes | Maintainer keeps Troubleshooting current as new failure modes surface |

### Beneficiary (Bridge layer) requirements from the local-setup side

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Operator's working tree is uncorrupted | The Bridge will hash files from the operator's commits | The guide warns against placing the repository inside an OneDrive-synced folder, since OneDrive and `.git` conflict | Operator uses `C:\Users\<name>\Documents\` or `C:\Users\<name>\Projects\` |
| Operator can re-run the notebook from a clean kernel | The Bridge implicitly trusts that notebooks were executed in the documented environment | Both `review-queue` and `epi-sde` are built from a checked-in `env.yml`. Kernel registration ties Jupyter to that environment | Operator selected the registered kernel before running cells |
| Operator's commits use a real GitHub identity | The Bridge attributes work by GitHub handle | The HTTPS + PAT flow ensures every push goes through the operator's authenticated GitHub identity | Operator generated the PAT under their own account |
| Operator can pull and push without help | Routine state transitions must not stall waiting for the maintainer | The Daily Workflow section covers `git pull`, edit, `git commit`, `git push` with both Visual Studio Code Source Control and terminal variants | Operator follows the Daily Workflow each session |

---

## When and where it runs

Local setup runs once per machine for the heavy steps (install Git, Visual Studio Code, Miniconda, generate PAT, clone, build env, register kernel) and once per session for the daily-workflow steps (activate, pull, edit, commit, push). The heavy steps require install rights and network access to the upstream download servers (git-scm.com, code.visualstudio.com, docs.conda.io, conda-forge, github.com). The daily steps require an active conda environment, a network path to GitHub, and a valid PAT.

### System operating constraints

| Constraint | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Operator may be on Windows, macOS, or Linux | The team is not standardized on a single OS | Windows path: PowerShell + `.bat` scripts. macOS and Linux path: shell + `.sh` scripts. Both share the `env.yml` package list | Operator's OS is supported by Git, Visual Studio Code, and Miniconda upstream |
| Operator has install rights on their own machine | Miniconda and Git both write to user space, but PATH edits require account-level rights | The guide's Miniconda step instructs the operator to check "Add Miniconda3 to my PATH environment variable" during install | Operator's account permits PATH edits |
| Network access to GitHub and conda-forge is available | Clone, pull, push, and env build all require network | Clone over HTTPS through `github.com`. Env build downloads packages from `conda-forge` channel pinned in `env.yml` | Operator's network does not block these hosts |
| GitHub no longer accepts passwords for git over HTTPS | The PAT replaces the password at git authentication time | The guide includes PAT generation with `repo` scope and 90-day expiry, and instructs the operator to paste the PAT when git prompts for a password | Operator has saved the PAT outside the terminal scrollback |
| Operator may have other Python installations on the same machine | System Python or other conda envs can confuse interpreter selection | The guide instructs the operator to select the registered `Review Queue Python` kernel in notebooks and to run `Python: Select Interpreter` in Visual Studio Code to point at the conda env explicitly | Operator follows the interpreter-selection step |
| Operator may use OneDrive or similar sync for `Documents/` | OneDrive and `.git` corrupt each other when both touch the same files | The guide names OneDrive-synced folders as a "NOT recommended" clone location and gives `C:\Users\<name>\Documents\` and `C:\Users\<name>\Projects\` as preferred locations | Operator picks a non-synced path |
| `.devcontainer/` is currently empty | The container files in the repository hold one blank line each | The user-facing guide instructs local operators to dismiss the "Reopen in Container" prompt, which is consistent with the empty state of the container files | Operator stays in the local Visual Studio Code window |
| Setup is one operator at a time | The guide is run on the operator's own machine | No coordination across operators is required during setup. Each operator's environment is independent | Operator's setup does not need to interlock with anyone else's |

---

## What the system can’t do on its own

The local-setup side carries known gaps that the user-facing guide names directly in its Troubleshooting section, plus structural gaps that surface from reading the setup scripts alongside the guide.

### Acknowledged limitations

| Limitation | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| `conda` not on PATH after Miniconda install | Miniconda's installer warns against PATH integration, but the guide requires it | Troubleshooting tells the operator to close and reopen PowerShell and, if that fails, to edit User PATH manually to add `C:\Users\<name>\miniconda3\Scripts` | Operator can edit Environment Variables in Windows |
| Permission denied or repository not found on clone | The operator may not have accepted the collaborator invitation, or the PAT is missing or expired | Troubleshooting names both causes and tells the operator to confirm collaborator status and to generate a new PAT if needed | Operator can re-request collaborator access |
| "No module named X" when running notebooks | The environment is not active or the wrong kernel is selected | Troubleshooting tells the operator to run `conda activate review-queue` and to set the kernel to "Review Queue Python". As a last resort, the operator removes and recreates the env | Operator has the `env.yml` available to rebuild from |
| Visual Studio Code cannot find Python | The Python extension defaults to a system Python that may not exist | Troubleshooting gives `Ctrl+Shift+P` → `Python: Select Interpreter` and a reload-window step | Operator has installed the Python extension |
| "Reopen in Container" prompt appears for local operators | Visual Studio Code reads `.devcontainer/` and offers the container, even when the files are empty | The guide's Step 5 and Troubleshooting both say to dismiss the prompt. The empty `.devcontainer/` files reinforce that no local container path exists | Operator notices the prompt and dismisses it |
| "Your branch is behind" on pull | A teammate pushed while the operator was offline | Troubleshooting tells the operator to run `git pull` and to ask for help if a conflict is reported | Operator has not made local commits that conflict |
| "Updates were rejected" on push | Someone else pushed before the operator did | Troubleshooting tells the operator to `git pull` and then `git push`, and to ask for help on merge conflicts | Operator pulls before re-attempting the push |
| "Git is not recognized" | Git is missing from PATH | Troubleshooting tells the operator to reinstall Git with the "Add Git to PATH" option and restart PowerShell | Operator can reinstall Git |
| OneDrive sync corrupts `.git` | OneDrive renames files mid-operation that git is also writing | Troubleshooting tells the operator not to clone into an OneDrive folder and gives the preferred locations | Operator can choose where to clone |
| Forgotten PAT | The PAT cannot be recovered after generation | Troubleshooting tells the operator to generate a new PAT and save it in a password manager | Operator generates a replacement PAT |
| Two environment definitions exist in parallel | `docs/LOCAL_SETUP_GUIDE.md` builds `review-queue` (Python 3.11 + basic stack); `curation-dev/setup/env.yml` builds `epi-sde` (full SDE stack with `diffrax` and `jax==0.6`) | Both are checked-in and reproducible. The role determines which one the operator builds | Operator picks the env that matches their role |
| `.devcontainer/` files are empty | `.devcontainer/devcontainer.json`, `.devcontainer/Dockerfile`, and `.devcontainer/env.yml` each contain one blank line | There is no container fallback at present. The local conda path is the only working route on a local machine | Operator does not need a container path |
| Guide is Windows-first | The prose, paste-ready commands, and screenshots all assume PowerShell | `curation-dev/setup/` has `.sh` script counterparts that produce the same environment on macOS and Linux | Operator on macOS or Linux maps the guide's PowerShell commands to their shell |
