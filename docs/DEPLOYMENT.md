# Deployment

## Goal
Deploy the public template so it reproduces the same system shape as the internal setup and gets as close as possible to battle-ready operation without leaking private data.

For the full end-to-end route, start with `docs/FULL_RECONSTRUCTION_GUIDE.md`.

## Step 1. Create the repository
- create a new empty GitHub repository
- copy this template into it
- review `.gitignore` and `SECURITY.md`
- keep the repository docs-first and public-safe

## Step 2. Define runtime prerequisites
Before first use, decide and document:
- Python version and launcher strategy
- local embedding provider endpoint
- embedding model name
- vault path
- storage path
- writable directories
- whether the system will run only locally or also in a shared QA environment

Record all of these in `configs/runtime-manifest.local.yaml`.

## Step 3. Keep one operator entrypoint
Add or keep these operator docs:
- `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
- `docs/MEMORY_OPERATIONS_RUNBOOK.md`
- `docs/REFERENCE_ARCHITECTURE.md`
- `docs/INSTANT_SETUP.md`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/HEALTH_AND_DOCTOR.md`
- `docs/BATTLE_READY_CHECKLIST.md`
- `docs/CODEX_BOOTSTRAP_PROMPT.md`

The dashboard should be the first place an operator opens when the blocker is still unclear.

## Step 4. Prepare config templates locally
Fill these templates with your own safe local values:
- `memory/config.template.yaml`
- `configs/runtime-manifest.template.yaml`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`
- `configs/role-profiles.template.yaml`

Keep the real values out of git if they reveal local paths, secrets, or private environments.

## Step 5. Add the bootstrap layer
Include:
- `tools/bootstrap-workspace.ps1`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/CODEX_BOOTSTRAP_PROMPT.md`

This gives a repeatable new-device and new-Codex-account flow.

It should also create a local parity manifest so a new operator does not have to guess which runtime parameters matter.

## Step 6. Add local scripts or launchers
Add your own local scripts or wrappers for:
- doctor workflow
- health check
- memory-tool launcher
- indexing memory
- searching memory
- archival
- checkpointing
- optional watcher lifecycle

Publish only generic versions if needed.
This template already includes safe generic starters:
- `tools/doctor-workspace.ps1`
- `tools/health-memory.ps1`

## Step 7. Verify runtime readiness
Before active use, run a doctor or health workflow that verifies:
- core workspace files exist
- runtime manifest is present
- config file loads
- vault path exists
- storage path is writable
- SQLite works
- Python runtime is executable
- the embedding endpoint is reachable
- the embedding model is present
- finalize can archive a test note
- preflight can read active role memory

## Step 8. Enforce data and access boundaries
Use `docs/DATA_BOUNDARIES_AND_ACCESS.md` and `configs/data-access.template.yaml` to define:
- environment tiers
- never-archive classes
- role memory scopes
- approval gates
- local versus shared storage rules

## Step 9. Add workflow discipline
At minimum, support:
- route selection
- memory preflight
- implementation or generation
- review
- validation
- archival
- recovery from runtime failure

## Step 10. Add evaluation before scale
Use `docs/EVALUATION_AND_OBSERVABILITY.md` and `configs/evals.template.yaml` to define:
- small golden datasets
- quality thresholds
- scale-up gates
- where reports are stored

## Step 11. Add recovery discipline
Use `docs/BACKUP_AND_RECOVERY.md` and `configs/recovery.template.yaml` to define:
- source-of-truth assets
- backup frequency
- restore order
- rebuild-from-markdown policy
- what to do when runtime dependencies are present but unhealthy

## Step 12. Validate battle readiness
Do not call the system battle-ready until `docs/BATTLE_READY_CHECKLIST.md` is fully green.

## Step 13. Verify before push
Search the repository for:
- old product names
- local paths
- usernames
- hostnames
- secrets
- copied logs or screenshots

Then run `docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md` on a clean clone.
