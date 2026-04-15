# SDE Review Queue

A simple system for coordinating second reviews of research manuscripts and Jupyter notebooks. Built on GitHub — no extra software needed.

## How It Works

Each manuscript that needs a second review is tracked as a **GitHub issue**. Reviewers claim issues, do their review, and mark them done — all through comments on the issue.

```
awaiting-review-2  →  review-2-active  →  complete
       │                     │                 │
  Needs a reviewer     Someone's on it    All done
```

**That's the whole process.** Three stages, two commands.

## The Two Commands You Need

| Command | What it does |
|---|---|
| `/checkout` | Claim a review — moves the files to `in-progress` and assigns you |
| `/approve` | Finish a review — marks it complete and triggers delivery |

There's also `/release` if you need to give something back to the queue.

## Quick Start

1. **New here?** Start with the [Local Setup Guide](docs/LOCAL_SETUP_GUIDE.md) to get your computer ready
2. **Ready to review?** Follow the [Reviewer Guide](CONTRIBUTING.md) for step-by-step instructions
3. **Need the big picture?** See [How Reviewers Use This System](docs/USAGE.md)
4. **Maintainer?** See [Setup](docs/SETUP.md) for one-time configuration

## Where Files Live

```
reviews/
├── awaiting-review-2/   ← Items waiting for a second reviewer
├── in-progress/         ← Items someone is actively reviewing
└── completed/           ← Finished reviews
```

When you `/checkout` an item, the system moves its files from `awaiting-review-2/` into `in-progress/` for you. When you `/approve`, the system moves them to `completed/`.

## Adding New Items

Drop a notebook file or folder into `reviews/awaiting-review-2/`, commit, and push. The system automatically creates a tracking issue — no manual issue creation needed.

## Why GitHub?

GitHub already handles everything this system needs — file storage, change tracking, user accounts, automation, and notifications. No database, no extra server, no new accounts to create.
