# Curator System Design

The curator side of the SDE Review Queue is where the reviewable artifact is produced. Curation happens in teams of 2. The pair selects a published epidemiological SDE model (DOI or comparable identifier; describes infection dynamics), copies `curation-dev/template/curation-template.ipynb` into a working notebook, implements the model, documents the outcome (Successful or Failed with reasons), and verifies the result internally (the first-review stage). One teammate is the implementing curator (becomes `reviewer_1` on PR merge); the other is the verifying teammate.

The team's working environment is one of two interchangeable forms: GitHub Codespaces (`.devcontainer/`) or a local conda install (`curation-dev/setup/`). Both build the `epi-sde` environment.

After teammate verification, the implementing curator copies the finished folder into `reviews/awaiting-review-2/`, opens a PR, and the system records them as `reviewer_1`, creates a `[REVIEW]` issue, and appends a row to `queue/review_log.csv`.

One rule applies across the whole stage: **no guessing or approximating**. If a parameter, equation, or initial condition is not in the publication, the team documents the absence. Documented failure is a valid outcome; invented values are not.

The reviewer side is at `docs/system-design/reviewer/`.
