# SDE Review Queue: Curator System Design

This document describes the curator side of the SDE Review Queue. The work supported here is part of AT3 Remote Research in Systems Medicine, a research project investigating the reproducibility of published epidemiological SDE models. The full review process has three stages: curation (a team of 2 implements the model in a notebook), first review (the teammate within the pair verifies the curated outcomes), and second review (an independent reviewer outside the pair verifies the work through the GitHub queue). The reviewer side of the queue is documented under `docs/system-design/reviewer/`. This document covers the curation and first-review stages.

---

## Abstract

The curator side of the SDE Review Queue produces the reviewable artifact. Curation work happens in teams of 2. Each team selects a published epidemiological SDE model (criteria: published with a DOI or comparable identifier, describes infection dynamics at any pathogen or biological scale), copies the blank notebook template from `curation-dev/template/curation-template.ipynb` into a working notebook, attempts to implement the model in code, documents the outcome (whether the figure was reproduced and, if not, why not), and verifies the outcome with the other teammate (the first-review stage). The team's working environment is either a GitHub Codespace (using `.devcontainer/devcontainer.json`) or a local conda environment (using `curation-dev/setup/install-env.*`); both build the same `epi-sde` Python environment. Once the teammate has verified the result, the implementing teammate copies the finished folder into `reviews/awaiting-review-2/`, opens a pull request, and the system automatically records them as `reviewer_1`, creates a `[REVIEW]` tracking issue, and appends an entry to `queue/review_log.csv`. This document covers the curator pair's workflow up to and including PR merge. The second-review stage is documented under `docs/system-design/reviewer/`.

---

## 1 Introduction

The AT3 Remote Research in Systems Medicine project investigates the reproducibility of published epidemiological SDE models. Earlier work in the same line examined 6 HBV SDE models and 6 COVID-19 SDE models; 5 of the 12 figures (41.7%) could be reproduced from what the publications provided. The questions the project is investigating include whether published sample sizes are sufficient and whether parameters are identifiable.

The curator side of the SDE Review Queue exists to record the answers. A team of 2 chooses a model, attempts to implement it, documents what happened, and verifies the result internally before handing the work to an independent reviewer. The curator's procedure is short and explicit: choose a model and figure, implement, document, verify with teammate, report findings.

The team's working environment is provided in two interchangeable forms. The `.devcontainer/` configuration starts the same environment in a GitHub Codespace (browser-based, no local installation). The local alternative lives in `curation-dev/setup/` with shell and batch scripts that build a conda environment on the curator's own machine. Both build the same `epi-sde` environment with `numpy`, `scipy`, `matplotlib`, `pandas`, `notebook`, `diffrax`, and `jax==0.6`. The team chooses between Codespace and local by preference.

One rule applies across the whole curation stage: **no guessing or approximating**. If a parameter, an equation, or an initial condition is not in the publication, the team documents the absence and records the consequence in the notebook. Documented failure is a valid outcome; invented values are not.

This document covers the curator pair's process up to PR merge. The second-review stage is documented under `docs/system-design/reviewer/`.
