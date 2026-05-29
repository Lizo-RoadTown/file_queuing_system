# Codespaces System Design

The Codespaces side documents the browser-based environment offered to the curation pair as an alternative to local conda. A team member opens the repository on GitHub, clicks the Code dropdown, switches to the Codespaces tab, and clicks Create codespace on main. GitHub provisions a container, clones the repository into it, and opens a browser-based VS Code attached to the container.

The user-facing instructions are in `docs/CODESPACES_GUIDE.md`. The configuration that defines the build is in `.devcontainer/` (`devcontainer.json`, `Dockerfile`, `env.yml`).

As of the current repository state, all three files in `.devcontainer/` are zero-byte placeholders. A Codespace started today falls back to GitHub's default Universal image and presents a generic Python environment, not the `epi-sde` environment the curator workflow expects. To make Codespaces functional, the three files have to be populated with the container definition, build steps, and environment specification.

`docs/CODESPACES_GUIDE.md` also describes two automation hooks that are not implemented in any workflow under `.github/workflows/`:

- `/checkout` copying the template notebook into `curation-dev/notebooks/` automatically. Not implemented. Curators copy the template manually per `curation-dev/README`.
- `/approve` from a curation issue sending the finished notebook to the review queue. Not implemented. Curators submit by copying the finished folder into `reviews/awaiting-review-2/` and opening a PR per the curator-side methodology.

The local-setup path is at `docs/system-design/local-setup/`.
