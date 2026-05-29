# Constraints

## Who uses this

### Implementing curator (Reviewer 1)

The implementing curator selects the paper with their teammate, copies the template, fills in the parameters and equations, runs the notebook, and documents the outcome. After the teammate verifies the result, the implementing curator opens the PR. The system records them as `reviewer_1` in the folder's `metadata.yml`, written automatically by `validate-submission.yml` on merge. From that point forward, `manage-queue.yml` rejects `/checkout`, `/release`, and `/approve` from the implementing curator on their own item. The only commands available to them on their own item are `/complete`, `/reject`, or `/reopen` (after a `/reject`), and only when the second reviewer has raised `/dispute`.

### Verifying teammate (first reviewer)

The verifying teammate is the other person in the curation pair. They verify the implementing curator's outcome before submission. The system does not track this person separately; their work is part of the team's internal process. In practice the verifying teammate reads the notebook, re-runs it, checks the equations and parameters against the paper, and confirms or pushes back on the implementing curator's documented outcome. The first-review stage ends when the verifying teammate agrees that the documented outcome is faithful to what the team observed.

### Independent second reviewer

The second reviewer is an operator from a different team who will receive the curator pair's submission through the queue and verify it independently. The curator pair never directly interacts with the second reviewer during the curation stage. Their contribution to the second reviewer is the integrity of the submission: a complete folder shape, a stable DOI, a notebook that re-runs cleanly, and parameter values that the second reviewer can cross-check against the paper.

### Beneficiary

The beneficiary is the downstream consumer of completed reviews: the Bridge layer that packages folders for cross-organizational handoff, the receiving institution and PI who run verification engines, and external researchers who consume public observability surfaces. The curator pair's contribution to the beneficiary is the integrity of the submission's content: complete folder shape, stable DOI in metadata, and a notebook whose values can be cited back to the paper.

### Science community

The broader scientific community includes external researchers. Their interaction is mediated through the planned browser extension that queries `queue/review_log.csv` by DOI and through public observability surfaces downstream. The curator pair contributes here by accurately recording the DOI at submission, which is what makes DOI-based discoverability work.

---

### Implementing curator requirements

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| A reliable, reproducible Python environment | Curators may be on Windows, macOS, or Linux | Two interchangeable paths: GitHub Codespaces using `.devcontainer/devcontainer.json`, or local conda using `curation-dev/setup/install-env.*`. Both build the same `epi-sde` environment | Each curator has Codespace quota or local install permissions |
| A blank notebook template | Each curation starts from a known shape so submissions are uniform | `curation-dev/template/curation-template.ipynb` provides a metadata header and named code cells for `variable_names`, `parameter_names`, `initial_values`, `parameter_values`, `initial_time`, `final_time`, `drift_term`, `diffusion_term` | The template covers the SDE models the team curates |
| A worked example | New curators need to see what a finished notebook looks like | `curation-dev/notebooks/curation-example.ipynb` is a complete worked example | The example is kept up to date as the template evolves |
| A draft workspace that does not pollute the repository | Failed attempts and intermediate work should not appear in public history | `curation-dev/` is gitignored. Only finished folders moved to `reviews/awaiting-review-2/` reach the repository | Curators understand the boundary between `curation-dev` and `reviews` |
| Authorship recorded on submission | The implementing curator should not need to manually claim Reviewer 1 status | `validate-submission.yml` writes `reviewer_1: <PR author>` into `metadata.yml` on merge | The PR author is the implementing curator |
| A submission gate that catches missing pieces | Discovering missing files post-merge is expensive | `validate-submission.yml` requires `.ipynb` + `.pdf` per folder, warns on missing image, blocks merge on failure | Curators see the PR check status before merging |

### Verifying teammate (first-reviewer) requirements

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Access to the same environment as the implementing curator | Verification depends on running the same notebook from a clean kernel | Both teammates use the same `epi-sde` environment (Codespace or local) | The teammates coordinate environment choice |
| Visibility into the implementing curator's work in progress | The verifying teammate needs to read the notebook and the documented outcome before submission | The team shares the work through the gitignored `curation-dev/` workspace (e.g., via the same Codespace or a shared branch) and via direct conversation | The teammates have an out-of-band channel to coordinate |
| A clear documented outcome to verify against | Without a documented outcome the first review has nothing to confirm or push back on | The notebook metadata header has Outcome (Successful or Failed) and Notes fields that the implementing curator fills in before verification | The implementing curator documents honestly |
| A way to push back without ambiguity | The first review must allow the verifying teammate to refuse a flawed submission | The team's convention is direct conversation. The verifying teammate refuses by declining to participate in the PR until concerns are addressed | The team has agreed that the verifying teammate's refusal blocks submission |

### Independent second reviewer requirements (from the curator pair's perspective)

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| The notebook re-runs cleanly | The second reviewer will run it from a clean kernel as part of `/checkout` and verification | The first-review stage ends with a clean-kernel run check by the verifying teammate | The `epi-sde` environment is stable across reviewers |
| Values are sourced | The second reviewer needs to confirm each value against the paper without guessing | The team's convention is `#SOURCE: p.X eq.(Y)` annotations. The first review is the opportunity to ensure each value has one | The team made notes about source pages during implementation |
| Metadata is filled in | The second reviewer needs paper title, DOI, curator name, figure, and Outcome | The notebook template includes a metadata header with these fields. The first-review stage confirms they are filled | The implementing curator filled in the metadata header |
| Folder shape is intact | The second reviewer's `/checkout` depends on finding a single `.ipynb` to copy | The submission folder contains exactly one notebook and one manuscript PDF | `validate-submission.yml` enforces this on PR |

### Beneficiary requirements

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Stable DOI on submission | The downstream index keys on DOI | The implementing curator enters the DOI in the metadata header and in the issue body. `update-queue-csv.yml` reads it into `review_log.csv` | The paper has a DOI or comparable identifier (per selection criteria) |
| Hashable folder content | The downstream Bridge will compute per-file SHA-256 hashes | The submission folder contains text files (`.ipynb`, `.md`, `.yml`) plus a `.pdf` binary, all stable across reads | The curator does not include transient artifacts |
| Recorded authorship | The Bridge attributes the work by GitHub handle | `metadata.yml.reviewer_1` is written by `validate-submission.yml` on merge | The PR author is the implementing curator |

### Science community requirements (from the curator pair's perspective)

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Accurate DOI on submission | DOI-based discoverability depends on the DOI being correct | The implementing curator enters the DOI in the issue body or the queue issue template, where `update-queue-csv.yml` reads it | The implementing curator copies the DOI accurately from the paper |
| Plausible notebook outcome | External researchers care whether the reproduction succeeded | The Outcome field in the metadata header records the team's documented outcome | The team updated Outcome to reflect reality |
| Documented failure is preserved | The community is interested in failed reproductions, not only successful ones | The team's "no guessing or approximating" rule means that a `Failed` outcome with a clear reason is a valid and valued artifact | The team submits failed reproductions rather than abandoning them |

---

## Selection criteria

The curation pair selects a paper that satisfies two criteria:

- The paper is **published with a DOI or comparable identifier**. Preprints with stable URLs count.
- The paper **describes infection dynamics** at any pathogen scale or biological scale.

Reproducibility-testing criteria the team applies during implementation:

- Are the equations used to produce the figure described in the paper?
- Are all model parameters available in the publication?
- Are all initial conditions available in the publication?

The summary the team reports for each curated paper:

- Can the team implement the model to reproduce the figure?
- If not, then why not?

---

## When and where it runs

The curation pair works in either a GitHub Codespace or a local devcontainer, both producing the same `epi-sde` Python environment. Drafts live in `curation-dev/`, which is gitignored, so curation-in-progress does not pollute the repository. The team's convention is that the verifying teammate confirms the documented outcome before the implementing curator opens the submission PR.

### System operating constraints

| Constraint | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Curation work happens in teams of 2 | Each paper is the responsibility of a pair, not a single curator | The team coordinates internally; the system tracks only the implementing curator (`reviewer_1`) | The two teammates can communicate directly outside the system |
| No guessing or approximating | If a parameter or equation is not in the publication, the team must not invent one | The notebook records the absence and the consequence. `Failed` is a valid Outcome with a documented reason | The team follows this rule honestly |
| First review is informal | The system does not enforce any specific check before submission | The team's convention is teammate verification. The PR review process serves as an additional informal check | The team performs the verification in good faith |
| Codespaces config is per-repo | The devcontainer is configured for Codespaces and is intentionally restricted from running on local desktop VS Code | If a local user opens the repo and chooses "Reopen in Container", container startup is designed to fail. Local curators should use `curation-dev/setup/install-env.*` | Curators read LOCAL_SETUP_GUIDE and CODESPACES_GUIDE before starting |
| `curation-dev/` is gitignored | Drafts must not contaminate public history | The `.gitignore` excludes `/curation-dev/`. The team moves finished folders to `reviews/awaiting-review-2/` and submits via PR | Curators understand which folder is for drafts and which is for submissions |
| Fork submissions cannot have metadata written back | The bot cannot push to a fork branch | `validate-submission.yml` checks `head.repo.full_name === base.repo.full_name` and short-circuits the `reviewer_1` write on forks | External fork-based curators are currently not supported |

---

## What the system can’t do on its own

The curator side has known gaps where the system does not provide as much support as it could.

### Acknowledged limitations

| Limitation | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| No curation queue enforcement | The system has no `awaiting-curation` label and no workflow that creates a curation issue when a paper is added to the team's list | The pair self-selects based on selection criteria. `CODESPACES_GUIDE.md` documents a curation-queue workflow that does not match current code | The team can manage paper assignment out of band |
| First review is not separately recorded | The system records only `reviewer_1` (the PR author). The verifying teammate's contribution is not captured by the system | The team's pair-work convention is documented here. Future iterations could record both teammates if there is value in formalizing it | The team trusts the pair convention |
| Cannot verify the notebook ran in a clean environment | A team could submit a notebook that only runs in their specific setup | Both the Codespace and the local devcontainer build the same `epi-sde` environment. A team that tests in both has higher confidence | The team tests in at least the environment they submit from |
| No automated metadata-consistency check | The metadata header in the notebook and the `metadata.yml` file in the folder could disagree | `validate-submission.yml` checks file shape but does not parse the notebook to verify metadata consistency | The team keeps both metadata sources in sync manually |
| Cannot prevent submission of a Failed outcome | An Outcome of `Failed` is still a valid submission. The system does not block it | The team's "no guessing" rule means failed reproductions are submitted on purpose, with documented reasons | Downstream consumers can read the Outcome field to filter |
| `CODESPACES_GUIDE.md` describes an aspirational workflow | The guide references an `awaiting-curation` label, a `/checkout`-creates-template-copy automation, and a curator-side `/approve` step that do not exist in the current workflow code | The current curator workflow is: copy the template manually, build the notebook, then PR-submit the finished folder | Curators read the guide critically and follow the actual code path |
