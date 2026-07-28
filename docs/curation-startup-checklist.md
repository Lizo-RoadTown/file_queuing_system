# Curation Process — Needs at the Start

A running list of things that need to be in place before the curation process can run at scale. Used to track open items at meetings.

---

## 1. DOI duplicate-check database

*Added: 2026-05-28 · Status: planning*

**Why**: Curators doing academic literature reviews need to check whether a paper has already been curated — or is currently being curated by someone else — before they start work. Otherwise two curators can independently start on the same paper and waste hours.

**What's needed**:
- A queryable list of every DOI ever entered into the curation queue, at any stage (`awaiting-review-2`, `in-progress`, `awaiting-pi`, `archived`, `rejected`, etc.).
- Easily accessible to curators during their literature-review work — they should be able to paste or type a DOI and get an immediate answer.
- Auto-populated whenever a new submission lands in the queue (so no curator has to remember to update it manually).
- Each DOI's current status visible (in queue vs. in progress vs. done vs. rejected).
- Ideally also a way to claim a DOI as "intended for upcoming curation" so two curators don't both start a paper neither has officially submitted yet.

**Open questions** (for meetings):
- Where does the database live? Options: a CSV in this repo, a Google Sheet, a Supabase table, a small static webpage backed by the queue, the GitHub Issues search itself.
- Who is responsible for keeping it accurate?
- Does it include rejected / failed submissions too, so curators can see what's already been tried and ruled out?
- Should curators be able to "claim" a DOI in advance? If so, with what TTL before the claim expires?
- What does "DOI" cover here — just the primary paper, or also any companion papers / supplements that share an extended DOI?

---

*(Add new items below as they come up at meetings.)*
