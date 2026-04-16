# Maintainer Setup

One-time configuration for the repo owner.

## 1. Create labels

The workflows depend on these labels existing:

| Label | Color |
|---|---|
| `queued` | `#cccccc` |
| `review-1-active` | `#fbca04` |
| `awaiting-review-2` | `#0e8a16` |
| `review-2-active` | `#fbca04` |
| `complete` | `#5319e7` |

With the GitHub CLI:

```bash
gh label create queued            --color cccccc
gh label create review-1-active   --color fbca04
gh label create awaiting-review-2 --color 0e8a16
gh label create review-2-active   --color fbca04
gh label create complete          --color 5319e7
```

Or click through **Issues → Labels → New label** in the browser.

## 2. Configure secrets

In **Settings → Secrets and variables → Actions**, add:

| Secret | Purpose |
|---|---|
| `NOTIFY_TO` | Recipient address for completed review packages |
| `SMTP_SERVER` | SMTP host |
| `SMTP_PORT` | SMTP port |
| `SMTP_USER` | Sender address used to authenticate |
| `SMTP_PASS` | Sender password or app-specific token |

Use a test recipient in `NOTIFY_TO` while verifying the workflow end-to-end, then update the secret to the production recipient.

## 3. Seed existing reviews

The **Bootstrap Seed Issues** workflow now runs automatically on pushes to `main` that add or change review items under `reviews/awaiting-review-2/` or `reviews/in-progress/`. It supports both review folders and standalone files placed directly in those stage directories. It creates tracking issues only for items that do not already have one, so it is idempotent and safe to re-run.

If needed, you can still run **Bootstrap Seed Issues** manually from the Actions tab to backfill or re-check the repository.

## 4. Test end-to-end

1. Pick one of the seeded `awaiting-review-2` issues.
2. From a second account (different from the recorded `reviewer_1`), comment `/checkout`.
3. Comment `/approve`.
4. Verify the folder moves to `reviews/completed/<name>/`, the issue closes, and the test recipient receives the zipped package.

If anything fails, check the workflow logs in the Actions tab.

## Authorization model

- **Currently:** any repo collaborator can run slash commands.
- **After org transfer:** any member of the designated GitHub team can run slash commands.

To add or remove reviewers, change collaborator/team membership — no code changes required.

## Transferring ownership

1. **Settings → General → Danger Zone → Transfer ownership.** Type the destination org. Everything moves: code, issues, labels, PRs, secrets, Actions history.
2. **Switch from collaborator-check to team-check.** In `.github/workflows/manage-queue.yml`, find the line marked `// TODO: switch to team check after transfer to org.` and replace the `checkCollaborator` block with the `teams.getMembershipForUserInOrg` block shown directly above it. Set the team slug.
3. **Update the `NOTIFY_TO` secret** to the production recipient.
4. **Update `.github/ISSUE_TEMPLATE/config.yml`** so the contributor-guide link points at the new org URL.

## Design notes

- **No servers, no database.** GitHub provides storage, auth, audit log, notifications, and compute (Actions).
- **All state lives in two places** — the issue (current stage) and `metadata.yml` (reviewer identities). Easy to read, easy to repair by hand.
