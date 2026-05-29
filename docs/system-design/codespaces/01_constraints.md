# Constraints

## Who uses this

### Team member opening a Codespace

The team member opening a Codespace is the same actor as the implementing curator on the curator side. They are working on a paper, they want a Python environment with the curation libraries available, and they have chosen the browser path over the local conda path. Their interaction with the Codespaces layer is short: open the Code dropdown on the repo, switch to the Codespaces tab, click Create codespace on main, wait for the build, work in the resulting browser VS Code, and reopen the same Codespace from the Codespaces tab on later sessions. The team member trusts that the build will produce the environment described in `docs/CODESPACES_GUIDE.md`.

### Maintainer authoring the devcontainer config

The maintainer is the person responsible for the three files under `.devcontainer/`. They decide which base image the container starts from, which features are added (for example a Python toolchain), how the `epi-sde` conda environment is built into the image, how the environment is activated for the curator's shell and notebook kernel, and what post-create commands run after the container starts. The maintainer's edits to these files determine what every curator who opens a Codespace from that point forward will see inside the container. The maintainer is not necessarily the same person as any individual curator.

### GitHub Codespaces (platform)

GitHub Codespaces is the platform that hosts the container. It allocates compute quota against the GitHub account opening the Codespace, schedules the build on its infrastructure, runs the container, hosts the persistent volume that backs the curator's home directory, mediates network access between the container and the GitHub repository, and provides the browser-based VS Code client. Codespaces reads `.devcontainer/devcontainer.json` as the entry point of the build. If that file is absent or empty, Codespaces falls back to a default Universal image and presents a generic environment. The platform also enforces inactivity timeouts and storage quotas that govern how long a Codespace persists between sessions.

---

### Team member (implementing curator) requirements

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| A working environment available from a browser | The curator may be on Windows, macOS, Linux, or a managed machine without admin rights | Codespaces runs in the browser; nothing is installed on the local machine | The curator has a modern browser and a stable internet connection |
| The same environment regardless of the curator's host OS | Team members must produce notebooks that re-run on a teammate's machine | The container is the same image for every curator who opens a Codespace from the repo | The `.devcontainer/` files define the image |
| The repository is checked out automatically | The curator should not have to clone or configure git remotes | Codespaces clones the repository into `/workspaces/<repo>` on container start | Repository access is granted by collaborator or read role |
| The `epi-sde` Python environment is ready on container open | The curator should not need to run install steps before working | `devcontainer.json` can declare a `postCreateCommand` or `postStartCommand` that activates `epi-sde`; the `Dockerfile` can build the env into the image from `env.yml` | The three `.devcontainer/` files are populated |
| Work persists across browser-tab close | The curator should not have to restart from scratch each session | The Codespace VM and its volume persist on GitHub infrastructure until the curator deletes the Codespace or the inactivity policy expires it | The curator stays inside their account quota |
| Commit and push reach GitHub directly | The curator must be able to share work and submit PRs | The container has `git` available and is authenticated to GitHub via the Codespaces session | The curator uses the Source Control panel or the terminal to commit and push |
| A predictable cost in terms of GitHub quota | The curator should not be surprised by quota burn | Codespaces meters compute by core-hour and storage by GB-month per GitHub account | The curator stops or deletes Codespaces they are no longer using |

### Maintainer requirements

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| A single canonical location for the container definition | Curators should not be asked to install per-machine prerequisites | `.devcontainer/devcontainer.json` is the entry point Codespaces reads | The maintainer keeps the config under that path |
| A reproducible image build | Each Codespace built from `main` should produce the same environment | `.devcontainer/Dockerfile` is the build recipe; `.devcontainer/env.yml` is the conda env specification | The Dockerfile pins versions where reproducibility matters |
| The same library set as the local path | The Codespace and the local conda install are described as interchangeable | `env.yml` carries the same package list as `curation-dev/setup/env.yml`, producing the `epi-sde` env in both paths | The two `env.yml` files are kept in sync |
| Edits to the config propagate to new Codespaces | Maintainer updates should reach curators without manual action on the curator side | New Codespaces built from `main` after the edit pick up the new config | Curators create fresh Codespaces or rebuild existing ones to pick up changes |
| Codespaces-only scope for the devcontainer | The repository documents that the devcontainer is for Codespaces, not for local Reopen in Container | `CODESPACES_GUIDE.md` directs local users to `LOCAL_SETUP_GUIDE.md` and to `curation-dev/setup/install-env.*` | Local users follow the local guide |

### GitHub Codespaces platform requirements (from the user's perspective)

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| A devcontainer entry point | Codespaces reads `.devcontainer/devcontainer.json` to determine what to build | A populated `devcontainer.json` references a Dockerfile or image, declares features, and sets `postCreateCommand` | The file is non-empty and valid JSON |
| A build recipe when the entry point references one | `devcontainer.json` may delegate the image build to a Dockerfile | A populated `Dockerfile` provides the layered build, including conda install and `env.yml` consumption | The file is non-empty and references `env.yml` correctly |
| Repository read or write access | The platform clones the repo into the container; pushes from the container need write access | The curator's GitHub session carries collaborator status into the Codespace | The curator is a collaborator on the repository |
| Available quota | The platform meters compute and storage per account | The curator's account has the standard free or paid Codespaces allocation | The curator's organization or account has not exhausted quota |
| A fallback path when the devcontainer is empty | Codespaces must produce some environment even when the config is missing | The platform's default Universal image runs when the devcontainer files are absent or empty | A generic environment is acceptable as a fallback signal that the config is unpopulated |

---

## When and where it runs

The Codespaces path runs entirely on GitHub infrastructure. The curator's local machine contributes only a browser. The Codespace persists across browser-tab close and is reopenable from the Codespaces tab. The first build of a Codespace takes a few minutes; subsequent starts of the same Codespace skip the build and resume in seconds. Codespaces quota is finite per GitHub account, and long-running Codespaces continue to consume storage quota even when stopped.

### System operating constraints

| Constraint | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Browser-based, no local installation required | The curator's local machine needs only a browser and a stable connection | Nothing is installed on the curator's machine. Cross-OS uniformity is automatic | The curator's browser supports the GitHub web app and VS Code in the browser |
| Requires GitHub login and repository access | The Codespace is created against the curator's GitHub identity | The Codespace inherits the curator's collaborator role for git operations | The curator has been added as a collaborator |
| First-time build takes a few minutes | The Dockerfile build, the conda env build, and the post-create commands all run on first start | The build is one-time per Codespace. Reopens skip it. The curator sees a "Setting up your codespace" screen during build | The maintainer's Dockerfile is functional |
| Codespace persists across browser-tab close | Work is saved to the Codespace volume, not the browser | The curator can close the tab and reopen the same Codespace from the Codespaces tab later | The curator stays within the inactivity policy window |
| Codespaces quota is finite per GitHub account | Compute is metered by core-hour, storage by GB-month | Curators stop Codespaces when not in active use; curators delete Codespaces when finished | The curator monitors their quota dashboard |
| A Codespace started with empty devcontainer files falls back to a default base image | Codespaces does not error on empty config; it uses the Universal image | The curator can still log in, see the repository, and open a terminal, but the `epi-sde` environment is not present | The maintainer authors the devcontainer files for the intended environment to appear |
| Pushes from the container reach GitHub over the platform's internal path | The curator does not need to configure SSH keys or credentials | Source Control panel commits and pushes work out of the box | The curator's identity (`user.name`, `user.email`) is set, either by the platform or by the curator running `git config` once |

---

## What the system can’t do on its own

The Codespaces layer has known gaps where the configuration, the documentation, and the platform constraints diverge from the intended behavior described in `docs/CODESPACES_GUIDE.md`. The most consequential gap is that the three `.devcontainer/` files are present as zero-byte placeholders. This is a fact about the current repository state and is surfaced first.

### Acknowledged limitations

| Limitation | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| `.devcontainer/devcontainer.json` is currently a zero-byte file | The file exists at the path Codespaces expects, but contains no content | A Codespace started from `main` today falls back to the GitHub default Universal image. The `epi-sde` environment is not built. The curator lands in a generic Python container | The maintainer will populate this file when the configuration is authored |
| `.devcontainer/Dockerfile` is currently a zero-byte file | The image build recipe has not been written | No custom image is built. The fallback Universal image is used | The Dockerfile will be authored to install conda and build the env from `env.yml` |
| `.devcontainer/env.yml` is currently a zero-byte file | The conda env specification has not been written | No `epi-sde` conda env is built into the image. The curator would need to install packages manually inside the running Codespace | The env spec will be authored to match `curation-dev/setup/env.yml` |
| `CODESPACES_GUIDE.md` describes a `/checkout` automation that copies the template | The guide states that commenting `/checkout` on an `awaiting-curation` issue causes the system to copy `curation-template.ipynb` into `curation-dev/notebooks/` | No workflow under `.github/workflows/` implements this. The curator copies the template manually per the curator-side methodology | The guide is aspirational ahead of the workflow code |
| `CODESPACES_GUIDE.md` describes a curator-side `/approve` automation that submits the finished notebook to the review queue | The guide states that commenting `/approve` checks that notes are filled in, then moves files to the review queue automatically | No workflow under `.github/workflows/` implements this. The curator copies the finished folder into `reviews/awaiting-review-2/` and opens a PR per the curator-side methodology | The guide is aspirational ahead of the workflow code |
| Codespaces quota is finite per GitHub account | Long curation sessions burn core-hours; idle Codespaces continue to burn storage | The curator stops or deletes Codespaces when not in use. The maintainer keeps the build small enough to fit within typical free-tier allowances | The curator's account or organization has Codespaces enabled |
| A Codespace runs on GitHub infrastructure | The path requires network connectivity to GitHub | Curators on intermittent connections may prefer the local conda path, which works offline once installed | The curator chooses the path that fits their working conditions |
| The Codespace's git identity may not be preconfigured | First-time commits may fail with "your name and email are not set" | The curator runs `git config --global user.name` and `git config --global user.email` once, as documented in `CODESPACES_GUIDE.md` troubleshooting | The curator follows the guide when prompted |
