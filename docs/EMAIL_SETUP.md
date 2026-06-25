# Email Notification Setup

Two workflows in this repository send email when a review is finalized: `notify-on-complete.yml` (automatic on the `complete` label) and `email-completed-reviews.yml` (manual backfill). Both rely on SMTP credentials stored as GitHub Actions secrets. This page explains what secrets are needed, how to add them, and how to wire common SMTP providers.

The values shown below are placeholders. Substitute your own.

---

## What the workflows need

Both workflows read six environment-style values, supplied as repository secrets:

| Secret name | What it holds | Example |
|---|---|---|
| `SMTP_SERVER` | The SMTP host | `smtp.gmail.com` |
| `SMTP_PORT` | The SMTP port (numeric) | `587` |
| `SMTP_LOGIN` | The SMTP login username | `your-account@example.com` |
| `SMTP_KEY` | The SMTP password or app-specific key | `xxxx-xxxx-xxxx-xxxx` |
| `FROM_EMAIL` | The address that appears in the `From:` header | `your-account@example.com` |
| `NOTIFY_TO` | The recipient address | `recipient@example.org` |

`FROM_EMAIL` and `SMTP_LOGIN` are usually the same address, but they do not have to be (some providers allow sending from any verified address).

---

## Adding the secrets to GitHub

1. On GitHub, open the repository.
2. Click **Settings** in the repo nav.
3. In the left sidebar, click **Secrets and variables** → **Actions**.
4. Click **New repository secret**.
5. Type the secret name exactly as listed in the table above. Names are case-sensitive.
6. Paste the value into the **Secret** field.
7. Click **Add secret**.
8. Repeat for all six.

The values are write-only after this point. You can update or delete them, but you cannot read them back. Keep a copy in your password manager.

---

## SMTP provider examples

Each example below shows what to put in `SMTP_SERVER`, `SMTP_PORT`, `SMTP_LOGIN`, and `SMTP_KEY` for a common provider. Most modern providers require an **app-specific password** rather than your account password, because Actions cannot complete an interactive two-factor prompt.

### Gmail (personal or Google Workspace)

| Secret | Value |
|---|---|
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_LOGIN` | your full Gmail address (`you@gmail.com`) |
| `SMTP_KEY` | a 16-character **app password**, not your Gmail password |

To create an app password:

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security).
2. Turn on **2-Step Verification** if it is not already on. Gmail will not let you create app passwords without it.
3. Search for **App passwords** in the Google Account search bar (it moves around).
4. Choose **Mail** and **Other (Custom name)**. Name it `SDE Review Queue` so you can recognize it later.
5. Copy the 16-character password Google shows. This is `SMTP_KEY`.

Gmail's sending limit is 500 messages per day for personal accounts, 2,000 for Google Workspace. Comfortably above what this queue produces.

### Outlook / Office 365

| Secret | Value |
|---|---|
| `SMTP_SERVER` | `smtp.office365.com` |
| `SMTP_PORT` | `587` |
| `SMTP_LOGIN` | your full Outlook address (`you@outlook.com` or `you@yourdomain.com`) |
| `SMTP_KEY` | account password OR an **app password** if MFA is on |

If your account has MFA, generate an app password at [account.microsoft.com/security](https://account.microsoft.com/security) → **Advanced security options** → **App passwords**.

Microsoft has been disabling basic SMTP auth on some tenant types. If sending fails with an authentication error even with the correct password, your tenant administrator may need to enable **SMTP AUTH** for the account.

### SendGrid

| Secret | Value |
|---|---|
| `SMTP_SERVER` | `smtp.sendgrid.net` |
| `SMTP_PORT` | `587` |
| `SMTP_LOGIN` | the literal string `apikey` |
| `SMTP_KEY` | a SendGrid API key with `Mail Send` permission |

Generate the API key from the SendGrid dashboard under **Settings** → **API Keys** → **Create API Key**. Choose **Restricted Access** and grant only `Mail Send`.

`FROM_EMAIL` must be a verified sender on SendGrid. Verify it under **Settings** → **Sender Authentication**.

### Mailgun

| Secret | Value |
|---|---|
| `SMTP_SERVER` | `smtp.mailgun.org` |
| `SMTP_PORT` | `587` |
| `SMTP_LOGIN` | the SMTP username from your Mailgun domain (`postmaster@yourdomain.mailgun.org`) |
| `SMTP_KEY` | the SMTP password shown in the same panel |

Find both values in the Mailgun dashboard under **Sending** → **Domains** → your domain → **SMTP credentials**.

### Generic SMTP (institutional, self-hosted)

| Secret | Value |
|---|---|
| `SMTP_SERVER` | your provider's hostname |
| `SMTP_PORT` | usually `587` for STARTTLS, sometimes `465` for SSL, rarely `25` |
| `SMTP_LOGIN` | as provided by your administrator |
| `SMTP_KEY` | as provided by your administrator |

The workflows use STARTTLS over the port specified by `SMTP_PORT`. If your provider requires a different connection method, the workflow's Python step would need to be adjusted (search for `smtplib.SMTP` in `.github/workflows/email-completed-reviews.yml` to see where).

---

## Testing the setup

Two ways:

### A: Use the manual workflow with a throwaway recipient

1. Set `NOTIFY_TO` temporarily to an address you can read (yours, or a test inbox).
2. Place a small folder under `reviews/completed/<test-name>/` (a notebook and a PDF is enough).
3. Trigger **Actions** → **Email Completed Reviews** → **Run workflow**, with `folder_name` set to your test folder.
4. The run should finish green. Check the test inbox for the zip.
5. Once confirmed, update `NOTIFY_TO` to the real recipient and remove the test folder.

### B: Send a sandbox /approve

1. Make sure you have an `awaiting-review-2` item in the queue that nobody else is reviewing.
2. Have a teammate (or a second collaborator) `/checkout`, push a trivial change, and `/approve`.
3. `notify-on-complete.yml` will fire. Check the Actions log for the email step's status.
4. If the recipient is set to a test inbox, verify the email arrived.

---

## Troubleshooting

**The Actions log shows "(530) authentication required" or "(535) authentication credentials invalid".**
The login or key is wrong, or the provider rejected basic auth. Regenerate the app password and re-add `SMTP_KEY`. For Gmail, confirm 2-Step Verification is on and you used the app password, not the account password.

**The email step times out.**
The port is probably wrong, or the provider is blocking GitHub-hosted runners. Try `587` (STARTTLS) before anything else; if that fails, contact the provider.

**The send succeeds in the log but no email arrives.**
Check the recipient's spam folder. Some providers (notably Gmail) flag mail from unfamiliar senders. Have the recipient mark a first message as Not Spam, or set up SPF/DKIM/DMARC on the sender domain.

**Sending works for some folders but not others.**
The folder probably contains a file too large for the provider's attachment limit. Gmail and Outlook cap attachments at 25 MB. Move the offending file outside the folder (or compress it heavily) and retry.

**"emailed_to_recipient_on" never gets written.**
The marker is written only after the SMTP send returns successfully. If you see the email in the recipient inbox but no marker commit, check that the workflow had `contents: write` permission and that `git push` did not fail (race with another push). Re-run the workflow; the marker write is idempotent.

---

## Rotating the credentials

When the app password is no longer in use (a teammate leaves, a token is regenerated):

1. Revoke the old app password at the provider.
2. Generate a new one.
3. Update `SMTP_KEY` in **Settings** → **Secrets and variables** → **Actions**.
4. No code change is needed.

Rotate `NOTIFY_TO` the same way when the recipient changes.

---

## Disabling email entirely

Remove the six secrets (or simply do not set them on a fork). The workflows will fail at the email step. The folder still moves into `reviews/completed/` and the issue still closes; the `emailed_to_recipient_on` marker is never written, so the next run of `email-completed-reviews.yml` would try to send again.

If a fork does not want email at all, the cleanest edit is to delete the `Email completed package` step in `notify-on-complete.yml` and to delete `email-completed-reviews.yml` and `scripts/email_completed_review.py` entirely.

---

## What the workflows send

For each completed folder, the recipient (`NOTIFY_TO`) receives one email with:

- **Subject:** `[SDE Review Complete] <folder-name>`
- **From:** `SDE Review Queue <FROM_EMAIL>`
- **To:** `NOTIFY_TO`
- **Cc:** `FROM_EMAIL`
- **Body:** a short summary listing the manuscript name, the issue URL (in the auto path), and the folder path
- **Attachment:** a zip of the completed folder

The zip contains everything inside the folder: the original notebook, the review-copy notebook, notes, metadata files, and the manuscript PDF.
