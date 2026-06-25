"""Send one completed review folder by email from a local machine.

Manual fallback for when the GitHub Actions workflows cannot run. Reads
SMTP credentials from environment variables (same names as the workflow
secrets), zips the named folder, sends the zip, and writes the
`emailed_to_recipient_on` marker into the folder's review_metadata.yml.

Usage:

    export SMTP_SERVER=smtp.example.com
    export SMTP_PORT=587
    export SMTP_LOGIN=your-login
    export SMTP_KEY='your-app-password'
    export FROM_EMAIL=from@example.com
    export NOTIFY_TO=to@example.com

    python3 scripts/email_completed_review.py reviews/completed/HBV

Exits non-zero on argument or send errors. After a successful send,
commit and push the marker so the workflows do not re-send the same
folder later.
"""

import os
import re
import smtplib
import sys
import zipfile
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path


REQUIRED_ENV = [
    "SMTP_SERVER",
    "SMTP_PORT",
    "SMTP_LOGIN",
    "SMTP_KEY",
    "FROM_EMAIL",
    "NOTIFY_TO",
]


def has_email_marker(rmeta_path: Path) -> bool:
    if not rmeta_path.exists():
        return False
    for line in rmeta_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("emailed_to_recipient_on:"):
            value = line.split(":", 1)[1].strip().strip("'\"")
            if value and value.lower() not in ("null", "none", ""):
                return True
    return False


def write_email_marker(rmeta_path: Path, today: str) -> None:
    line = f"emailed_to_recipient_on: {today}\n"
    if rmeta_path.exists():
        content = rmeta_path.read_text(encoding="utf-8")
        if re.search(r"^emailed_to_recipient_on:.*$", content, flags=re.M):
            content = re.sub(
                r"^emailed_to_recipient_on:.*$",
                f"emailed_to_recipient_on: {today}",
                content,
                flags=re.M,
            )
        else:
            if content and not content.endswith("\n"):
                content += "\n"
            content += line
    else:
        content = line
    rmeta_path.write_text(content, encoding="utf-8")


def zip_folder(folder: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder):
            for name in files:
                file_path = Path(root) / name
                arcname = file_path.relative_to(folder.parent)
                zf.write(file_path, arcname)


def send(folder: Path, zip_path: Path) -> None:
    msg = EmailMessage()
    msg["Subject"] = f"[SDE Review Complete] {folder.name}"
    msg["From"] = formataddr(("SDE Review Queue", os.environ["FROM_EMAIL"]))
    msg["To"] = os.environ["NOTIFY_TO"]
    msg["Cc"] = os.environ["FROM_EMAIL"]
    msg.set_content(
        f"A review package has been finalized.\n\n"
        f"Manuscript: {folder.name}\n"
        f"Location:   {folder.as_posix()}\n\n"
        f"The complete review package is attached as a zip file.\n"
    )
    msg.add_attachment(
        zip_path.read_bytes(),
        maintype="application",
        subtype="zip",
        filename=f"{folder.name}.zip",
    )
    with smtplib.SMTP(os.environ["SMTP_SERVER"], int(os.environ["SMTP_PORT"])) as s:
        s.starttls()
        s.login(os.environ["SMTP_LOGIN"], os.environ["SMTP_KEY"])
        s.send_message(msg)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <path/to/reviews/completed/folder>", file=sys.stderr)
        return 2

    missing = [k for k in REQUIRED_ENV if not os.environ.get(k)]
    if missing:
        print(f"missing env vars: {', '.join(missing)}", file=sys.stderr)
        return 2

    folder = Path(argv[1]).resolve()
    if not folder.is_dir():
        print(f"not a directory: {folder}", file=sys.stderr)
        return 2

    rmeta_path = folder / "review_metadata.yml"
    if has_email_marker(rmeta_path):
        print(f"already emailed: {folder.name}")
        return 0

    zip_path = Path(f"/tmp/{folder.name}.zip")
    print(f"zipping {folder} -> {zip_path}")
    zip_folder(folder, zip_path)

    print(f"sending {folder.name} to {os.environ['NOTIFY_TO']}")
    send(folder, zip_path)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    write_email_marker(rmeta_path, today)
    print(f"marker written: {rmeta_path} (emailed_to_recipient_on: {today})")
    print("commit and push the marker so future runs do not re-send this folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
