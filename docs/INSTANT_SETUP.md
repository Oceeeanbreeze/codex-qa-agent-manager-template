# Instant Setup

## Goal
Set up the full QA agent system quickly with safe defaults.

## Fastest path
1. Run `tools/bootstrap-workspace.ps1`.
2. Fill `configs/runtime-manifest.local.yaml`.
3. Open `docs/FULL_RECONSTRUCTION_GUIDE.md`.
4. Open `docs/HEALTH_AND_DOCTOR.md`.
5. Paste `docs/CODEX_BOOTSTRAP_PROMPT.md` into a new Codex chat.
6. Validate readiness with `docs/BATTLE_READY_CHECKLIST.md`.

## Step 1. Copy the template
Copy this repository into a new local workspace.

## Step 2. Open the main docs
Read in this order:
1. `docs/FULL_RECONSTRUCTION_GUIDE.md`
2. `docs/RUNTIME_PARAMETER_MATRIX.md`
3. `docs/RUNTIME_INSTALLATION.md`
4. `docs/FIRST_HOUR_RUNBOOK.md`
5. `docs/REFERENCE_ARCHITECTURE.md`
6. `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
7. `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md`
8. `docs/DATA_BOUNDARIES_AND_ACCESS.md`
9. `docs/MEMORY_OPERATIONS_RUNBOOK.md`
10. `docs/EVALUATION_AND_OBSERVABILITY.md`
11. `docs/BACKUP_AND_RECOVERY.md`
12. `docs/SETTINGS_PARITY_AUDIT.md`

If you want Codex to help complete setup phase by phase, also read:
- `docs/CODEX_ASSISTED_SETUP.md`
- `docs/SETUP_CHAT_PROMPTS.md`

## Step 3. Fill the config templates
Prepare these files locally from the templates:
- `requirements.txt`
- `memory/config.template.yaml`
- `configs/runtime-manifest.template.yaml`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`
- `configs/role-profiles.template.yaml`

## Step 4. Configure the environment tiers
- set `local` and `qa` first
- keep `production` disabled
- document approval gates for sensitive actions
- align the same posture in `configs/runtime-manifest.local.yaml`

## Step 5. Configure durable memory
- choose the vault path
- choose the storage path
- choose the local embedding endpoint and model
- keep markdown as source of truth
- treat indexes as rebuildable caches
- keep role include-paths scoped

## Step 6. Configure the role system
- keep `router` as coordinator
- enable only the needed specialist roles
- keep role prompts small and explicit
- keep memory scopes role-specific
- keep role profiles aligned with `configs/role-profiles.template.yaml`

## Step 7. Configure the operator workflow
Make these standard operator actions:
- `doctor`
- `health`
- `preflight`
- `search`
- `index`
- `finalize`
- `evals`
- `watch`

Record the actual working commands in `configs/runtime-manifest.local.yaml`.

## Step 8. Install runtime and dependencies
Use:
- `docs/RUNTIME_INSTALLATION.md`
- `tools/install-runtime-prereqs.ps1`

## Step 9. Add evals before scale
Create small golden sets for:
- routing
- retrieval
- reviewer quality
- coverage decisions
- browser validation stability

## Step 10. Publish only the safe layer
Commit only docs, prompts, generic config templates, and safe bootstrap scripts.
Do not commit live vault content, generated indexes, logs, traces, screenshots, or secrets.

## Step 11. Call it battle-ready only after runtime proof
Do not call the reconstructed system battle-ready until:
- doctor passes
- health passes
- constrained-host blockers are resolved or explicitly isolated
- memory preflight works
- finalize works
- evals pass
- the battle-ready checklist is green
- the Git parity checklist stays green on a clean clone
