# UF Curation Database — schema

This document defines the tables, columns, relationships, and access policies for the UF Curation Database (Stage 3 of the pipeline). The schema implements the append-only, public-readable, signature-verified model from [Inspiration/sde-pipeline-overview.svg](../Inspiration/sde-pipeline-overview.svg).

Visual layout: [Inspiration/sde-database-schema.svg](../Inspiration/sde-database-schema.svg).

## Design principles

1. **Append-only everywhere it matters.** Every content-bearing table allows `INSERT` only. `UPDATE` and `DELETE` are blocked by Row-Level Security at the database engine level — application code cannot bypass them. Corrections are new rows with `supersedes_*_id` references; the old rows remain forever.

2. **Per-row checksums.** Content-bearing tables include `*_sha256` columns for every artifact. Anyone with `SELECT` access can recompute and compare.

3. **Per-handoff signatures.** Handoff tables (`arrivals`, `signoffs`) carry Ed25519 signatures from the producing party. Anyone with the published public key can verify.

4. **Audit log fires automatically on every INSERT.** Postgres triggers append to `audit_log`. The audit log is itself append-only and public-readable.

5. **The substrate is also versioned in-band.** `substrate_versions` records every change to the system itself (Terraform, workflow YAMLs, schema migrations). Each archive deposit bundles a snapshot of the substrate at deposit time — so the rules of the system are audited alongside the data the rules produced.

6. **Public read access at the database level, not the UI level.** The `anon` Postgres role can `SELECT` from every table. The Public Dashboard (Stage 6) is just a friendlier face on the same public REST endpoint anyone else can query.

## Tables

### `arrivals`
One row per submission entering from the Auto-Transfer Bridge (Stage 2).

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid (PK) | Row identifier |
| arrival_timestamp | timestamptz | When the row was inserted |
| manifest_sha256 | text | SHA-256 of the signed manifest |
| manifest_signature | text | Ed25519 signature from Bridge |
| bridge_sha256 | text | Which Bridge version produced this manifest |
| github_commit_sha | text | Repo commit at `/approve` |
| github_issue_url | text | Source issue in the queue repo |
| github_issue_comments_sha256 | text | Hash of the discussion thread at `/approve` |
| curator_github | text | Curator's GitHub login |
| curator_orcid | text | Curator's ORCID (nullable until adopted) |
| reviewer_github | text | Reviewer's GitHub login |
| reviewer_orcid | text | Reviewer's ORCID (nullable until adopted) |
| paper_doi | text | DOI of the paper being reproduced |
| paper_pdf_sha256 | text | SHA-256 of the paper PDF |
| notebook_sha256 | text | SHA-256 of the entire curation notebook |
| notebook_curation_sha256 | text | SHA-256 of cells above `# End Curation` |
| notebook_testing_sha256 | text | SHA-256 of cells below `# Begin Testing` |
| env_lockfile_sha256 | text | SHA-256 of the conda lockfile at curation |
| verification_status | enum | `verified` / `failed_signature` / `failed_checksum` |
| receipt_signature | text | Ed25519 signature of the receipt by UF DB |

### `compute_runs`
One row per PI Verification Engine run against an arrival.

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid (PK) | Row identifier |
| arrival_id | uuid (FK → arrivals.id) | Which arrival this run verifies |
| engine_sha256 | text | Which engine version ran |
| engine_version_tag | text | Human-readable version tag |
| container_image_sha | text | Docker image SHA used |
| lockfile_sha256 | text | Conda lockfile at execution time |
| hardware_info | jsonb | CPU model, RAM, GPU model (matters for stochastic results) |
| seeds_used | jsonb | Array of random seeds used in this run |
| started_at | timestamptz | When run began |
| completed_at | timestamptz | When run finished |
| duration_seconds | numeric | Total wall-clock duration |
| results | jsonb | Structured results payload |
| results_sha256 | text | SHA-256 of results |
| verdict | enum | `reproducible` / `partial` / `failed` / `inconclusive` |
| error_log | jsonb | Array of errors encountered |

### `signoffs`
One row per PI sign-off on a verified arrival.

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid (PK) | Row identifier |
| arrival_id | uuid (FK → arrivals.id) | Which arrival this sign-off applies to |
| compute_run_ids | uuid[] (FK → compute_runs.id) | Which runs informed this sign-off |
| pi_github | text | PI's GitHub login |
| pi_orcid | text | PI's ORCID |
| pi_signature | text | Ed25519 signature of the sign-off payload |
| signoff_timestamp | timestamptz | When the sign-off was recorded |
| verdict | enum | `reproducible` / `partial` / `failed` / `inconclusive` / `needs_more_data` |
| pi_notes | text | Free-form PI commentary (public) |
| supersedes_signoff_id | uuid (FK → signoffs.id) | If the PI changes their mind later |

### `audit_log`
Append-only log of every `INSERT` across the system. Populated by Postgres triggers, not by application code.

| Column | Type | Purpose |
|--------|------|---------|
| id | bigserial (PK) | Row identifier |
| timestamp | timestamptz | When the trigger fired |
| table_name | text | Which table received the INSERT |
| row_id | uuid | Which row was inserted |
| action | text | Always `INSERT` |
| actor_role | text | Which Postgres role did the insert |
| payload | jsonb | The full row that was inserted |

### `archive_receipts`
One row per weekly Zenodo deposit (the "DOI dump"). See [What's in each DOI dump](#whats-in-each-doi-dump) below.

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid (PK) | Row identifier |
| period_start | timestamptz | Start of the period this deposit covers |
| period_end | timestamptz | End of the period |
| deposit_timestamp | timestamptz | When the deposit was sent to Zenodo |
| zenodo_concept_doi | text | Stable concept DOI (same across versions) |
| zenodo_version_doi | text | This-specific-version DOI |
| zenodo_returned_checksum | text | Zenodo's own checksum, reconciled against ours |
| arrivals_included | int | Count of new arrival rows |
| compute_runs_included | int | Count of new compute_run rows |
| signoffs_included | int | Count of new signoff rows |
| audit_entries_included | int | Count of new audit_log rows |
| substrate_version_id | uuid (FK → substrate_versions.id) | Substrate version at deposit time |
| substrate_snapshot_sha256 | text | Hash of the Terraform/workflow snapshot included |
| bundle_sha256 | text | Hash of the entire deposit bundle |

### `substrate_versions`
One row per change to the system itself (Terraform, workflow YAMLs, schema migrations). The "version control wrapper around the whole thing."

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid (PK) | Row identifier |
| timestamp | timestamptz | When the change was applied |
| changed_by_github | text | Who proposed the change |
| changed_by_orcid | text | Their ORCID |
| approved_by | text[] | GitHub logins of reviewers |
| pull_request_url | text | Link to the PR that made the change |
| terraform_state_sha256 | text | SHA-256 of the Terraform state after this change |
| workflow_yamls_sha256 | text | SHA-256 of the `.github/workflows/` tree |
| schema_migration_sha256 | text | SHA-256 of any schema migration applied |
| description | text | Human-readable summary |

## Relationships

```
arrivals  ─1:N→  compute_runs  ─N:M→  signoffs
arrivals  ─1:N───────────────────────→ signoffs   (arrival_id FK on signoffs)
signoffs  ─self─→  signoffs              (supersedes_signoff_id)

archive_receipts  ─N:1→  substrate_versions  (the substrate snapshot included)

audit_log  ←(INSERT trigger from every other table)
```

## Access policy (RLS sketch)

```sql
-- Default: SELECT for anon, no UPDATE, no DELETE anywhere
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon;

-- One role per write-capable actor
CREATE ROLE bridge_writer;
GRANT INSERT ON arrivals TO bridge_writer;

CREATE ROLE compute_writer;
GRANT INSERT ON compute_runs TO compute_writer;

CREATE ROLE pi;
GRANT INSERT ON signoffs TO pi;

CREATE ROLE archive_writer;
GRANT INSERT ON archive_receipts TO archive_writer;

CREATE ROLE substrate_admin;
GRANT INSERT ON substrate_versions TO substrate_admin;

-- No role has UPDATE or DELETE on any table.

-- Audit triggers on each main table
CREATE TRIGGER audit_arrivals AFTER INSERT ON arrivals
  FOR EACH ROW EXECUTE FUNCTION write_audit_log();
-- (one per table)
```

## What's in each DOI dump

Each weekly `archive_receipts` row corresponds to a Zenodo deposit. The deposit bundle contains:

1. **All new arrival rows** since the last deposit (with their manifests and signatures)
2. **All new compute_run rows** (with their seeds, hardware info, results)
3. **All new signoff rows** (with PI signatures and verdicts)
4. **All new audit_log entries** since the last deposit
5. **A snapshot of `substrate_versions`** as of the deposit moment — meaning the Terraform files, workflow YAMLs, and schema migrations that defined the system when this data was generated
6. **A top-level manifest** with SHA-256 of every file in the bundle, signed by the archive_writer key
7. **Zenodo's returned checksum** stored in the `archive_receipts.zenodo_returned_checksum` column

This is the recursive transparency commitment: not just *what was reproduced* gets archived, but the *rules of the system that produced it*. Future researchers can audit both the data and the policies that governed the data.

## Notes on naming

- `bridge_*` columns are for things produced by Stage 2 (Auto-Transfer Bridge)
- `pi_*` columns are for things produced by Stage 4 / Stage 5a
- `*_sha256` columns are content hashes; `*_signature` columns are Ed25519 signatures
- `_id` columns ending in `_id` are foreign keys; arrays of FKs are written `_ids`
