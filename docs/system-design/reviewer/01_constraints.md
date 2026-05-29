# Constraints

## Who uses this

### Reviewer 1 (the curator)

The curator is the team member who originally selected the paper from the literature, built the reproduction notebook, and submitted the folder via pull request. The system records them as `reviewer_1` in the folder's `metadata.yml`, written automatically by `validate-submission.yml` on PR merge. Reviewer 1 and "the curator" are the same actor under different names. The curator role is not a separate person who reviews someone else's submission, it is the person whose submission gets reviewed.

The curator's authority on their own item is limited and conditional. `manage-queue.yml` rejects `/checkout`, `/release`, and `/approve` from the recorded `reviewer_1`. The only commands available to the curator on their own item are `/complete`, `/reject`, and `/reopen`. `/complete` and `/reject` are valid only after Reviewer 2 has raised `/dispute`. `/reopen` is valid only after the curator has used `/reject` and both parties have agreed on a path forward. In the normal happy path, the curator has no further interaction with the item after submission. The curator's authority is a fallback for the dispute branch, not a primary gate.

### Reviewer 2

Reviewer 2 is any other team member with collaborator access on the repository, anyone except the recorded Reviewer 1 for this particular paper. The exclusion is per-item, not per-person. The same individual may play Reviewer 2 on one paper and Reviewer 1 on another.

Reviewer 2 owns the decision in the normal flow. They can `/checkout` (claim), `/release` (return without decision), `/approve` (finalize as accepted), or `/dispute <reason>` (escalate to the curator). After a curator `/reject`, the reviewer can also `/reopen` to return the item to active review. `/approve` does not require curator agreement; it moves the item to `reviews/completed/` and closes the issue directly. This is the design choice that distinguishes the SDE Review Queue from review systems requiring two-sign-off on every item: most reviews complete with one signoff (Reviewer 2's), and only contested reviews invoke the second authority.

### The downstream beneficiary

The beneficiary is whatever consumes the queue's output downstream. The most direct consumer is the Bridge layer that packages each completed review folder with per-file SHA-256 hashes for handoff to another organization. After that comes the receiving institution (a database or a signed handoff chain) and the Principal Investigator who runs verification engines against the package. Eventually an external researcher might query the index by DOI to find out whether a given paper has been reproduced.

The beneficiary is a system, not a person. The system needs durable hash inputs, a complete audit trail, and stable identifiers. The beneficiary does not perform reviews and does not interact with the queue directly.

### The science community

The broader scientific community includes external researchers reading the paper online, peer reviewers of related work, modelers reusing the reproduced code, and anyone asking "has this paper's model been independently reproduced, and what happened when someone tried?" Their access to the queue happens through the planned browser extension that queries `queue/review_log.csv` by DOI, and through whatever public surfaces the receiving institution chooses to expose (Zenodo, OSF, RSS, ORCID notifications).

The science community does not perform reviews and does not interact with the GitHub layer directly. Their interest is that verified reproductions exist, are findable, and outlast any single project.

---

### What Reviewer 1 (the curator) needs

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Authorship of the original notebook is recorded automatically | Curators are not asked to manually claim Reviewer 1 status; the system infers it from PR authorship | `validate-submission.yml` writes `reviewer_1: <PR author>` into `metadata.yml` on merge | The PR author is the actual curator, not a delegate pushing on someone else's behalf |
| Not asked to participate in routine reviews | Curators have other technical work and cannot be on call for every second review | The happy path skips the curator entirely. `/approve` by Reviewer 2 finalizes without curator action | Most reviews are uncontested |
| Notified when their work is disputed | The curator must learn about a dispute without polling the queue | `/dispute` posts a comment with an @-mention resolved from `metadata.yml`'s `reviewer_1` field | GitHub notifications reach the curator within their normal monitoring cadence |
| Submission shape is validated before merge | Curators may forget required files; finding out post-merge is expensive | `validate-submission.yml` runs on PR and requires `.ipynb` + `.pdf` per folder; warns on missing image | The curator is the PR author and the PR is from the same repo, not a fork |
| Mechanical exclusion from reviewing their own past curation | The system's central integrity claim must not depend on the curator's self-discipline | `/checkout` and `/approve` reject `commenter == reviewer_1` | The curator cannot trivially control two collaborator accounts |

### What Reviewer 2 needs

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Browseable queue of unclaimed items | Reviewers cannot remember which items are available; they need to scan | GitHub Issues filtered by the `awaiting-review-2` label. `review_log.csv` provides a machine-readable index | The reviewer has collaborator access and can view issues |
| One-step claim with no prep | Reviewers will not invest setup time before deciding whether the work is feasible | `/checkout` triggers everything: assignment, folder move, structure creation, label change | The reviewer has pulled at least once before claiming, so the bot's commit can fast-forward locally |
| Clean working copy that will not conflict with the original | Reviewers must be able to re-execute the notebook freely without contaminating the canonical version | `manage-queue.yml` moves the original into `original/` and copies it into `review-copy/<name>_rvd.ipynb`. Both are committed by the bot | The curator's notebook is well-formed enough to copy without error |
| Cannot review own past curation | The integrity claim must apply symmetrically to the reviewer side | Both `/checkout` and `/approve` reject `commenter == reviewer_1` | `metadata.yml` is present and parseable for the item |
| Finalize in one comment when the review is uncontested | Routine reviews must complete in one action to avoid queue stalls | `/approve` validates folder shape, moves the folder to `completed/`, updates metadata, applies `complete`, closes the issue, triggers email notification | Folder shape is intact and notes have content under at least one heading |
| Escalate without committing to a finalization | Reviewers may find issues they cannot resolve unilaterally | `/dispute <reason>` flags the item for curator review without closing it. The reviewer stays assigned | The reviewer can articulate a clear reason for the dispute |
| Abandon and return to queue | Reviewers may misjudge feasibility after starting | `/release` moves the folder back to `awaiting-review-2/` and unassigns the reviewer | No partial work needs to be preserved across abandonment |
| Return to active review after a `/reject` | A rejection may turn into a workable path once the parties talk | `/reopen` returns the item to `review-2-active` so the reviewer can update and re-`/approve` or re-`/dispute` | The reviewer and curator have agreed on a resolution path |

### What the beneficiary needs

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Complete folder structure at finalization | The downstream Bridge requires a hashable artifact | At `/approve` or `/complete`, the folder contains `original/`, `review-copy/`, `notes/`, `metadata.yml`, `review_metadata.yml`. Validation runs before the move | The reviewer pushed all working files before commenting `/approve` |
| Stable identifier | Bridge and downstream consumers index by DOI | `metadata.yml` carries `doi:`. `review_log.csv` records DOI per issue | The curator filled in the DOI at submission or through the queue template |
| Queryable index | A browser extension and any downstream consumer needs a flat data source | `update-queue-csv.yml` appends a row per opened issue to `queue/review_log.csv`. Columns are `name,doi_or_url,added_by,added_on,issue_number` | The CSV does not need outcome columns at this stage |
| Recorded reviewer identities | The Bridge needs to attribute the work without consulting external systems | `metadata.yml.reviewer_1` (from `validate-submission.yml`), `review_metadata.yml.approved_by` (from `manage-queue.yml`). `notify-on-complete.yml` writes `reviewer_2` | All actors used their canonical GitHub handle |
| Recorded timestamps | Downstream audit requires temporal ordering | `review_metadata.yml.checkout_timestamp` (on `/checkout`), `.approval_timestamp` (on `/approve`). `notify-on-complete.yml` writes `reviewer_2_completed` (ISO date) | The Actions runner clock is trustworthy |
| No silent re-edit of completed work | The Bridge must hash a stable artifact | Once moved to `completed/`, the folder is not edited by any workflow. Further changes leave a git commit trail | Reviewers do not force-push to main. Admins do not silently edit completed folders |

### What the science community needs

| What's needed | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Public verifiability of which papers have been reproduced | External researchers want to know reproduction status before relying on a paper's results | `queue/review_log.csv` is committed in the public repository. Any reader can fetch and parse it | The repository is public or at least readable by the intended audience |
| Findable index by DOI | The natural query is "has paper X been reproduced?" | `review_log.csv` includes a DOI column. The planned browser extension reads this column to answer DOI lookups | DOI is the canonical identifier the community uses |
| Outcome information attached to each entry | "Curated" alone is insufficient; the community needs to know whether the reproduction succeeded | Current gap: the CSV records the issue number but not the outcome. Outcome lives in the issue label and the completed folder's metadata | Outcome can be derived by following the issue link in a future iteration |
| Long-term durability | Verification records must survive personnel turnover and project transitions | Git history preserves all state. The CSV is replayable from issue events. The downstream Bridge produces signed artifacts in the larger system | The repository remains hosted and accessible |
| Open and inspectable process | Trust in verifications depends on the verification process being inspectable | Workflow YAMLs, scripts, and the issue timeline are all public artifacts | Public scrutiny of the workflow code is acceptable to the team |

---

## When and where it runs

Reviewers are spread across timezones and work whenever they have time. There is no shared workstation and no separate login system, just GitHub collaborator status. Every slash command runs a collaborator check before doing anything. The queue does not need anyone to be online at any particular moment; slash commands queue as comments and process in order.

### Constraints on how it runs

| Constraint | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Reviewers geographically and temporally distributed | No team standup or shared review window. Reviewers are in different timezones | All state is durable in GitHub. Any reviewer can see the queue at any time without coordination | GitHub remains available |
| Asynchronous and unscheduled work | Reviews happen when reviewers have time. The queue has no service-level agreement | The label and metadata are sufficient state for any reviewer to pick up an item without context handoff | Stale items are visible by their unchanged label and can be re-prioritized by the team out of band |
| No additional software for the queue itself | Installing tools is friction reviewers will not absorb | Slash commands run in the browser via the GitHub website. No local tooling is required to use the queue | Reviewers have Git and a notebook environment installed separately for the actual review work, per LOCAL_SETUP_GUIDE |
| Only collaborators can run commands | The single authorization layer is GitHub repo collaborator status | `manage-queue.yml` calls `github.rest.repos.checkCollaborator` before any state change. Non-collaborators get a polite refusal comment | The repository owner manages collaborator membership through normal GitHub admin |
| Fork PRs cannot be augmented by the bot | Bot accounts cannot push to a contributor's fork branch | `validate-submission.yml` short-circuits on fork PRs without writing `reviewer_1` | External contributors via fork are currently not supported as curators |
| Reviewers may not know Git deeply | Some reviewers come from scientific backgrounds with limited prior Git exposure | LOCAL_SETUP_GUIDE and WORKFLOW_GUIDE document the Git mechanics in step-by-step form. The VS Code Source Control panel is the recommended path | A reviewer can learn enough Git in one session to do a review |

---

## What the system can't do on its own

The queue cannot check whether a review's reasoning is correct, and it cannot guarantee what happens after the package leaves for the downstream Bridge. It maximizes what it can check mechanically (folder shape, reviewer identity, label transitions, timestamps) and leaves the meaning-of-the-work judgment to the human reviewer.

### Limits we accept

| Limitation | Why it matters | How it's handled | What we assume |
|---|---|---|---|
| Cannot detect the intent behind a `#CHANGED:` comment | Annotation presence is mechanical, meaning is human | The system records that an annotation exists and where. Readers must judge whether the reason is sound | Reviewers write annotations honestly |
| Cannot review changes outside notebook cells | The diff machinery, when in use, targets `.ipynb` cells only | Reviewers can edit supporting `.py` modules, but those edits are not surfaced in any automated comparison | Supporting modules are stable across review |
| Cannot prevent force-push erasure | A main-branch force-push from any collaborator would rewrite the commit-level audit trail | Branch protection rules on `main`, if enabled by the admin, prevent this | The admin has configured branch protection appropriately |
| Cannot enforce same-person rule against multiple accounts | The integrity check compares GitHub handles, not real-world identities | None at the queue layer. Downstream Bridge signing could close this gap | Collaborators do not control multiple authorized GitHub accounts |
| Cannot validate manuscript-versus-notebook agreement | The system does not read the manuscript PDF | The reviewer reads the PDF and writes `#CHANGED:` or `#SOURCE:` annotations. Their judgment is the verification | The reviewer has access to the manuscript and the technical ability to read it |
| Cannot verify the reviewer re-executed the notebook | No clean-room re-run happens automatically | `/approve` trusts the reviewer's claim that they ran it | A future notebook-execution-as-verification workflow could close this gap |
| No diff report at finalization | An earlier design generated `DIFF_REPORT.md` on `/approve`. The current design relies on `#CHANGED:` annotations and the git diff between `original/` and `review-copy/` | The diff generator script lives in `scripts/archive/` and can be re-wired if the team chooses | The curator can read the notebook diff in any git client |
