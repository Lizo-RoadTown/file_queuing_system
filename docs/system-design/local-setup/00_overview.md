# Local Setup System Design

The local-setup side documents the steps to install and configure a personal machine for working on the SDE Review Queue. The same setup serves both the curator role and the independent-reviewer role.

The user-facing instructions are in `docs/LOCAL_SETUP_GUIDE.md`. The supporting scripts are in `curation-dev/setup/` (`install-env.sh`/`.bat`, `rm-env.sh`/`.bat`, `config.sh`/`.bat`, `env.yml`) and `curation-dev/launch-code.sh`/`.bat`.

Two conda environments are referenced in the repository:

- `review-queue` (defined in `docs/LOCAL_SETUP_GUIDE.md`): `python=3.11`, `numpy`, `matplotlib`, `scipy`, `pandas`, `notebook`, `ipywidgets`, `pip`.
- `epi-sde` (defined in `curation-dev/setup/env.yml`): the `review-queue` base plus `tqdm`, `ipyevents`, `nomkl`, and pip packages `diffrax` and `jax==0.6`.

The `.devcontainer/` directory exists but the three files inside it (`devcontainer.json`, `Dockerfile`, `env.yml`) are zero-byte placeholders. The local conda path is the only active local-setup route at present.

The Codespaces path is at `docs/system-design/codespaces/`.
