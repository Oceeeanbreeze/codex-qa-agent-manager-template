# Instant Setup

## Goal
Set up the full QA agent system quickly with safe defaults.

## Fastest path
1. Run `tools/bootstrap-workspace.ps1`.
2. Open `docs/NEW_DEVICE_SETUP.md`.
3. Paste `docs/CODEX_BOOTSTRAP_PROMPT.md` into a new Codex chat.

## Step 1. Copy the template
Copy this repository into a new local workspace.

## Step 2. Open the main docs
Read in this order:
1. `docs/REFERENCE_ARCHITECTURE.md`
2. `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
3. `docs/DATA_BOUNDARIES_AND_ACCESS.md`
4. `docs/MEMORY_OPERATIONS_RUNBOOK.md`
5. `docs/EVALUATION_AND_OBSERVABILITY.md`
6. `docs/BACKUP_AND_RECOVERY.md`

## Step 3. Fill the config templates
Prepare these files locally from the templates:
- `memory/config.template.yaml`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`

Keep the real values out of git if they reveal local paths, secrets, or private environments.

## Step 4. Configure the environment tiers
- set `local` and `qa` first
- keep `production` disabled
- document approval gates for sensitive actions

## Step 5. Configure durable memory
- choose the vault path
- choose the storage path
- choose the local embedding endpoint and model
- keep markdown as source of truth
- treat indexes as rebuildable caches

## Step 6. Configure the role system
- keep `router` as coordinator
- enable only the needed specialist roles
- keep role prompts small and explicit
- keep memory scopes role-specific

## Step 7. Configure the operator workflow
Make these standard operator actions:
- `doctor`
- `health`
- `preflight`
- `search`
- `index`
- `finalize`
- `watch`

## Step 8. Add evals before scale
Create small golden sets for:
- routing
- retrieval
- reviewer quality
- coverage decisions
- browser validation stability

## Step 9. Publish only the safe layer
Commit only docs, prompts, generic config templates, and safe bootstrap scripts.
Do not commit live vault content, generated indexes, logs, traces, screenshots, or secrets.
