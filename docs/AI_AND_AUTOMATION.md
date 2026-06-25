# AI and Automation in the SDE Review Queue

The system has two kinds of non-human work happening inside it: scripted automation that runs the queue, and AI tooling the author uses while designing and maintaining it.

Scripted automation runs inside GitHub Actions, executed by the `github-actions[bot]` service account. The bot has the permissions granted by each workflow's `permissions:` block and runs the JavaScript and YAML checked into `.github/workflows/`.

AI tooling runs in the author's editor, on triggers from the author. Its outputs are drafted code, drafted prose, and search results. The author corrects hallucinations and validates output before accepting it into the repository.

---

## 1 Scripted automation

Slash commands are dispatched by `manage-queue.yml`, an Actions workflow whose body is JavaScript embedded in `actions/github-script@v7`. The `github-actions[bot]` service account is the actor that runs that JavaScript.

### What runs in this layer

| Workflow | Triggered by | What the script does |
|---|---|---|
| `manage-queue.yml` | Issue comments matching `/checkout`, `/release`, `/approve`, `/dispute`, `/complete`, `/reject`, `/reopen` | Runs the collaborator check; runs the reviewer-exclusion check (`commenter == reviewer_1`); moves folders between `reviews/awaiting-review-2/`, `reviews/in-progress/`, and `reviews/completed/`; updates `review_metadata.yml`; changes the issue label; posts a confirmation comment; closes the issue when finalized |
| `validate-submission.yml` | Pull request touching `reviews/**` | Diffs the PR; checks each touched folder for `.ipynb` + `.pdf`; warns on missing image; writes `reviewer_1: <PR author>` into `metadata.yml` on same-repo PRs |
| `bootstrap-seed-issues.yml` | Push to `main` touching `reviews/awaiting-review-2/**`, or manual `workflow_dispatch` | Scans `reviews/awaiting-review-2/` for folders without an existing tracking issue; reads each folder's `metadata.yml`; creates a `[REVIEW]` issue with the `awaiting-review-2` label and a `<!-- folder: ... -->` marker |
| `update-queue-csv.yml` | Issue opened | Parses the issue title and body for paper name and DOI; appends a row to `queue/review_log.csv`; commits and pushes |
| `notify-on-complete.yml` | Issue gains the `complete` label | Moves the folder to `reviews/completed/` if not already there; writes `reviewer_2` to `metadata.yml`; zips the folder; sends the package via SMTP; writes `emailed_to_recipient_on` into `review_metadata.yml`; posts a final comment naming both reviewers; closes the issue |
| `auto-label-completed.yml` | Push to `main` on `reviews/completed/**` by a non-bot actor | Finds the matching issue, updates its folder marker, reopens if closed, and applies the `complete` label so `notify-on-complete.yml` handles the rest |
| `email-completed-reviews.yml` | `workflow_dispatch` (optional `folder_name` input) | Backfill: emails any completed folder without the `emailed_to_recipient_on` marker, or only the named folder. Idempotent on re-runs |
| `void-issue.yml` | Issue gains the `void` label | Closes the issue without moving files or sending notifications |

### Boundaries of this layer

The bot enforces shape, runs the slash-command dispatcher, and propagates state changes. Semantic judgments live in the head of a human reviewer or curator: reading the manuscript PDF, judging whether a `#CHANGED:` reason is sensible, deciding whether a notebook reproduces a paper.

The system's central integrity claim, that no one can review their own past curation, is enforced by a string comparison (`commenter == reviewer_1`) inside checked-in JavaScript.

---

## 2 AI tooling

The author uses LLM-based assistants at design time.

### Tools in use

| Tool | Where it runs | What the author uses it for |
|---|---|---|
| **Claude Code** (Anthropic's CLI/VS Code agent) | Inside the author's local VS Code, operating on the repository filesystem | Reading workflow YAML and inline JavaScript; drafting code, documentation, and Mermaid diagrams from specifications the author provides; performing search-and-replace; maintaining the persistent memory directory |
| **Claude Desktop** (Anthropic's desktop application) | Outside the code editor, on the author's machine | Running the author's personal writing skill on doc drafts before publication |
| **GitHub Copilot** (optional, per `docs/LOCAL_SETUP_GUIDE.md`) | Inside a reviewer's VS Code, if subscribed | Optional inline code suggestions for reviewers editing notebooks |

### Steps where AI is used in the development workflow

The author originates the design decisions, provides the source material, and writes the specifications. In every step below, the author corrects hallucinations and validates the AI's output before accepting it into the repository.

| Step | What AI does | What the author does |
|---|---|---|
| Searching the repo for information | Greps the codebase for symbols or patterns; reads named files; traces references across workflows; pulls history from git log | Tells the AI what to look for. Corrects hallucinations and validates output |
| Reading and explaining workflow code | Reads named YAML and inline JavaScript; produces a plain-language summary of what happens on a given event | Specifies what to explain. Corrects hallucinations and validates output against running behavior |
| Drafting documentation skeletons | After the author has designed the structure and created specifications, produces a skeleton with headings and table column structure | Designs the structure and creates the specifications. Corrects hallucinations and validates output |
| Drawing up diagrams after structure is designed and specifications are created | After the author has designed what the diagram should show and specified the type (state machine, sequence, hierarchy, layered architecture), produces the Mermaid source | Designs the structure and specifies the diagram type. Corrects hallucinations and validates output |
| Writing code per specification | After the author has scoped a workflow change and specified the behavior, implements the handler in JavaScript or YAML | Scopes the change and writes the specification. Corrects hallucinations and validates output before commit |
| Performing search-and-replace across files | Finds every occurrence of a string or pattern; produces the corrected version | Specifies what to find and what to replace it with. Corrects hallucinations and validates output |
| Filling in tables from repo content | After the author has designed the table structure, populates the rows from the actual workflow code, configuration files, and existing data | Designs the table structure. Corrects hallucinations and validates output |
| Maintaining persistent memory of author preferences | Saves typed memory files in the author's local Claude Code memory directory (under `~/.claude/projects/<project>/memory/`) so subsequent sessions do not re-derive context | Decides what is remembered. Corrects hallucinations and validates output, prunes stale entries |
| Debugging workflow failures | Reads the Actions log, identifies the failure point, proposes a fix | Specifies the failure being debugged. Corrects hallucinations and validates whether the fix addresses the root cause |
