# Maintainer Setup

This guide is for the person who owns or manages the repository. Reviewers don't need this — they should follow the [Local Setup Guide](LOCAL_SETUP_GUIDE.md) instead.

Everything here only needs to be done **once** when you first set up the system.

---

## 1. Create the Required Labels

The automation uses labels on issues to track progress. You need three:

| Label | Color | Meaning |
|---|---|---|
| `awaiting-review-2` | green (`#0e8a16`) | Ready for a reviewer to claim |
| `review-2-active` | yellow (`#fbca04`) | Someone is working on it |
| `complete` | purple (`#5319e7`) | Review is finished |

### Using the GitHub website (preferred)

1. Go to your repository on GitHub
2. Click **Issues** in the top menu
3. Click **Labels** (on the right side)
4. Click **New label**
5. Type the label name, pick the color, and click **Create label**
6. Repeat for all three labels

### Using the terminal (backup)

If you have the [GitHub CLI](https://cli.github.com/) installed:

```bash
gh label create awaiting-review-2 --color 0e8a16
gh label create review-2-active   --color fbca04
gh label create complete          --color 5319e7
```

---

## 2. Set Up Email Notifications (Optional)

If you want the system to email people when a review is completed, you need to add some secrets. If you skip this, everything else still works — you just won't get emails.

### Where to add secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each one below

### What to add

| Secret name | What to put in it |
|---|---|
| `NOTIFY_TO` | The email address that should receive completed review packages |
| `SMTP_SERVER` | Your email provider's SMTP server (e.g., `smtp.gmail.com`) |
| `SMTP_PORT` | The SMTP port (usually `587`) |
| `SMTP_USER` | The "from" email address |
| `SMTP_PASS` | The password or app-specific password for that email |

> **Tip:** Start with a test email address in `NOTIFY_TO`. Once you've confirmed it works, change it to the real recipient.

---

## 3. Seed Existing Reviews

If you already have notebooks in `reviews/awaiting-review-2/`, the system can automatically create tracking issues for them.

The **Bootstrap Seed Issues** workflow runs automatically when you push new items to that folder. It's safe to run multiple times — it won't create duplicate issues.

You can also trigger it manually:

1. Go to **Actions** in your repository
2. Find **Bootstrap Seed Issues** in the left sidebar
3. Click **Run workflow**

---

## 4. Test Everything

Walk through the full cycle once to make sure it works:

1. Pick one of the `awaiting-review-2` issues
2. Comment `/checkout` — the files should move to `reviews/in-progress/` and the label should change to `review-2-active`
3. Comment `/approve` — the files should move to `reviews/completed/`, the issue should close, and you should get an email (if configured)

If something doesn't work, check the **Actions** tab for error logs.

---

## Who Can Run Commands

Right now, any repository collaborator can use the slash commands (`/checkout`, `/approve`, `/release`).

To add or remove reviewers, just add or remove them as collaborators on the repository — no code changes needed.

---

## Transferring to an Organization

If you move this repository to a GitHub organization later:

1. **Settings → General → Danger Zone → Transfer ownership** — type the destination org
2. In `.github/workflows/manage-queue.yml`, switch from the collaborator check to the team check (there's a comment in the code marking where)
3. Update the `NOTIFY_TO` secret to the production email
4. Update `.github/ISSUE_TEMPLATE/config.yml` with the new org URL

---

## How It Works (Design Notes)

- **No servers or databases.** Everything runs on GitHub: storage, authentication, and automation (via GitHub Actions).
- **State lives in two places:** the issue labels (current stage) and `metadata.yml` files (reviewer identities). Both are easy to read and fix by hand if needed.
