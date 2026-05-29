# Maintainer Setup

This guide is for the person who owns or manages the repository. Reviewers don't need this, they should follow the [Local Setup Guide](LOCAL_SETUP_GUIDE.md) instead.

Everything here only needs to be done **once** when you first set up the system.

---

## 1. Create the Required Labels

The automation uses labels on issues to track progress. You need five:

| Label | Color | Meaning |
|---|---|---|
| `awaiting-review-2` | green (`#0e8a16`) | Ready for a reviewer to claim. |
| `review-2-active` | yellow (`#fbca04`) | Someone is working on it. |
| `disputed` | orange (`#d93f0b`) | The reviewer flagged a disagreement; waiting on the curator. |
| `complete` | purple (`#5319e7`) | Review is finished. |
| `curator-rejected` | dark red (`#b60205`) | Curator rejected the dispute; issue stays open for discussion. |

The label `void` is also used by `void-issue.yml` to close duplicate or admin-action issues without moving files or sending notifications. You can create it with any color (a neutral gray works).

### Using the GitHub website (preferred)

1. Go to your repository on GitHub.
2. Click **Issues** in the top menu.
3. Click **Labels** (on the right side).
4. Click **New label**.
5. Type the label name, pick the color, and click **Create label**.
6. Repeat for all five labels (plus `void` if you want voiding to work).

### Using the terminal (backup)

If you have the [GitHub CLI](https://cli.github.com/) installed:

```bash
gh label create awaiting-review-2  --color 0e8a16
gh label create review-2-active    --color fbca04
gh label create disputed           --color d93f0b
gh label create complete           --color 5319e7
gh label create curator-rejected   --color b60205
gh label create void               --color cccccc
```

---

## 2. Set Up Email Notifications (Optional)

If you want the system to email people when a review is completed, you need to add some secrets. If you skip this, everything else still works, you just won't get emails.

### Where to add secrets

1. Go to your repository on GitHub.
2. Click **Settings** → **Secrets and variables** → **Actions**.
3. Click **New repository secret** for each one below.

### What to add

| Secret name | What to put in it |
|---|---|
| `NOTIFY_TO` | The email address that should receive completed review packages. |
| `SMTP_SERVER` | Your email provider's SMTP server (e.g., `smtp.gmail.com`). |
| `SMTP_PORT` | The SMTP port (usually `587`). |
| `SMTP_LOGIN` | The SMTP login username (often your email address). |
| `SMTP_KEY` | The password or app-specific password for that account. |
| `FROM_EMAIL` | The address that appears in the "From" header on outgoing emails. |

> **Tip:** Start with a test email address in `NOTIFY_TO`. Once you've confirmed it works, change it to the real recipient.
>
> The secret names above are the exact strings the workflows look for in `.github/workflows/notify-on-complete.yml` and `.github/workflows/email-completed-reviews.yml`. If you use different names, the workflows will not pick them up.

---

## 3. Seed Existing Reviews

If you already have notebooks in `reviews/awaiting-review-2/`, the system can automatically create tracking issues for them.

The **Bootstrap Seed Issues** workflow runs automatically when you push new items to that folder. It's safe to run multiple times, it won't create duplicate issues (it checks for existing issues by their path marker).

You can also trigger it manually:

1. Go to **Actions** in your repository.
2. Find **Bootstrap Seed Issues** in the left sidebar.
3. Click **Run workflow**.

---

## 4. Test Everything

Walk through the full cycle once to make sure it works:

1. Pick one of the `awaiting-review-2` issues.
2. Comment `/checkout`, the files should move to `reviews/in-progress/` and the label should change to `review-2-active`.
3. Edit the `review-copy/_rvd.ipynb` notebook, fill in `notes/review_notes.md`, commit, and push.
4. Comment `/approve`, the files should move to `reviews/completed/`, the issue should close, and you should get an email (if configured).

To test the dispute path, pick another item, `/checkout`, then `/dispute test reason`. The label should change to `disputed` and you should see an @-mention of the recorded curator. The curator can then comment `/complete` or `/reject test reason`.

If something doesn't work, check the **Actions** tab for the failing workflow's run log.

---

## Who Can Run Commands

Any repository collaborator can use the slash commands. The full set is `/checkout`, `/release`, `/approve`, `/dispute`, `/complete`, `/reject`. The `manage-queue.yml` workflow checks `checkCollaborator` on the GitHub API for each comment and rejects non-collaborators with a comment.

To add or remove reviewers, just add or remove them as collaborators on the repository, no code changes needed. If you want to recognize reviewers by their full name in notebook content, add them to `team_members.yml`.

---

## Transferring to an Organization

If you move this repository to a GitHub organization later:

1. **Settings → General → Danger Zone → Transfer ownership**, type the destination organization.
2. In `.github/workflows/manage-queue.yml`, switch from the collaborator check to a team check. The relevant call is `github.rest.repos.checkCollaborator`; replace it with `github.rest.teams.getMembershipForUserInOrg` against your reviewer team.
3. Update the `NOTIFY_TO` secret to the production email recipient.
4. Update `.github/ISSUE_TEMPLATE/config.yml` if it references the previous repository URL.

---

## How It Works (Design Notes)

- **No servers or databases.** Everything runs on GitHub: storage, authentication, and automation (via GitHub Actions).
- **State lives in two places.** The issue label is the source of truth for "what stage this paper is in." The folder's `metadata.yml` is the source of truth for "who curated this paper" and `review_metadata.yml` is the source of truth for "who reviewed it and when."
- **Six commands drive five states.** See [README.md](../README.md) for the command and state reference, and [docs/system-design/02_methodology.md](system-design/02_methodology.md) for the formal state machine.
- **The queue index lives in `queue/review_log.csv`.** Every new issue is appended to it by `update-queue-csv.yml`. This file is intended to be machine-readable for downstream consumers (e.g., a planned browser extension that checks whether a given paper has been curated).
