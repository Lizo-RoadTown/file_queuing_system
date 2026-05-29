# SDE Review Queue: Reviewer System Design

This document describes the reviewer side of the SDE Review Queue. The full system is a transparent GitHub-based repository for the curation and two-review of computational models from academic literature. The process has three stages: curation (a team of 2 reproduces the model in a notebook), first review (the teammate within the pair verifies the curated outcomes), and second review (an independent reviewer outside the pair verifies the work). The curator side is documented under `docs/system-design/curator/`. This document covers the second-review stage.

---

## Abstract

The SDE Review Queue coordinates independent verification of scientific manuscripts and the Jupyter notebooks that reproduce their models. Each manuscript is tracked as a GitHub issue, and the queue's lifecycle is encoded entirely in the issue's label set. Reviewers drive the system by commenting slash commands. The system handles file movement between three folders (`awaiting-review-2`, `in-progress`, `completed`), records reviewer identities in metadata files, mechanically prevents anyone from reviewing their own past curation, and emits a packaged email at completion. This document describes the second-review stage: the role of Reviewer 2 as the operator, the state machine that governs the queue, the sequence of slash-command interactions across actors, and the layered architecture that separates GitHub's UI from the orchestration workflows and the data layer. The system runs on GitHub-native primitives. The curation and first-review stages are documented under `docs/system-design/curator/`.

---

## 1 Introduction

The reviewer side of the SDE Review Queue handles the second review of each curated reproduction notebook. The curator (Reviewer 1) submits a finished folder through a pull request. The reviewer side picks up from there: an independent reviewer (Reviewer 2) browses open issues, claims one with `/checkout`, re-runs the notebook locally, annotates any changes with `#CHANGED:` comments, and finalizes with `/approve`, escalates to the curator with `/dispute`, or returns the item to the queue with `/release`.

The mechanism is a label-state machine over GitHub issues, a slash-command actor model implemented in GitHub Actions workflows, and a dispute-resolution branch that escalates to the curator only when Reviewer 2 disagrees with the curator's work. The system runs on GitHub-native primitives. Reviewers need Git and a Jupyter notebook environment locally to do the review work; the queue itself runs in the browser through issue comments.
