# Deployment

## Goal
Deploy a docs-first QA agent manager without leaking local project data.

## Step 1. Create the repository
- create a new empty GitHub repository
- copy this template into it
- review `.gitignore` and `SECURITY.md`

## Step 2. Keep one operator entrypoint
Add or keep these operator docs:
- `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
- `docs/MEMORY_OPERATIONS_RUNBOOK.md`
- `docs/REFERENCE_ARCHITECTURE.md`
- `docs/INSTANT_SETUP.md`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/CODEX_BOOTSTRAP_PROMPT.md`

The dashboard should be the first place an operator opens when the blocker is still unclear.

## Step 3. Prepare config templates locally
Fill these templates with your own safe local values:
- `memory/config.template.yaml`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`

Keep the real values out of git if they reveal local paths, secrets, or private environments.

## Step 4. Add the bootstrap layer
Include:
- `tools/bootstrap-workspace.ps1`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/CODEX_BOOTSTRAP_PROMPT.md`

This gives a repeatable new-device and new-Codex-account flow.

## Step 5. Add local scripts
Add your own local scripts for:
- doctor workflow
- memory-tool launcher
- health check
- indexing memory
- searching memory
- archival
- checkpointing

Publish only generic versions if needed.

## Step 6. Verify local readiness
Before active use, run a doctor or health workflow that verifies:
- core workspace files exist
- config file loads
- vault path exists
- storage path is writable
- SQLite works
- Python runtime is executable
- Ollama is reachable and the embedding model is present
- full self-test result is available when needed

## Step 7. Enforce data and access boundaries
Use `docs/DATA_BOUNDARIES_AND_ACCESS.md` and `configs/data-access.template.yaml` to define:
- environment tiers
- never-archive classes
- role memory scopes
- approval gates

## Step 8. Add workflow discipline
At minimum, support:
- route selection
- memory preflight
- implementation or generation
- review
- validation
- archival

## Step 9. Add evaluation before scale
Use `docs/EVALUATION_AND_OBSERVABILITY.md` and `configs/evals.template.yaml` to define:
- small golden datasets
- quality thresholds
- scale-up gates
- where reports are stored

## Step 10. Add recovery discipline
Use `docs/BACKUP_AND_RECOVERY.md` and `configs/recovery.template.yaml` to define:
- source-of-truth assets
- backup frequency
- restore order
- rebuild-from-markdown policy

## Step 11. Verify before push
Search the repository for:
- old product names
- local paths
- usernames
- hostnames
- secrets
- copied logs or screenshots
