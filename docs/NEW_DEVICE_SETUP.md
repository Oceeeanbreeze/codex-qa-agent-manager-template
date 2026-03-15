# New Device Setup

## Goal
Use this repository to recreate the same agent-system shape on a new device or in a new Codex account with minimal manual work and explicit runtime validation.

## Reality check
A GitHub link alone does not fully auto-deploy the system.
The closest reliable flow is:
1. clone the repository
2. open the folder in Codex
3. run the bootstrap script
4. fill the local runtime manifest
5. send the prepared bootstrap prompt to Codex

That reproduces the same orchestration model, role model, memory model shape, and operator discipline while keeping secrets, local paths, private vault data, and product knowledge out of the public repo.

## Prerequisites
Before starting, make sure you have:
- Git
- PowerShell
- Python available from the operator shell
- a local embedding provider such as Ollama
- the required embedding model already pulled locally
- write access to the target workspace location

## Step 1. Clone the repository
```powershell
git clone https://github.com/<your-account>/<repo-name>.git
cd <repo-name>
```

## Step 2. Run the bootstrap script
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-workspace.ps1
```

## Step 3. Fill the local runtime manifest
Open `configs/runtime-manifest.local.yaml` and make sure it matches:
- your actual Python launcher;
- your actual embedding endpoint and model;
- your actual vault and storage paths;
- your actual operator commands.

Use `docs/RUNTIME_PARAMETER_MATRIX.md` to fill it completely.

## Step 4. Open the workspace in Codex
Open the cloned folder as the active workspace.

## Step 5. Paste the bootstrap prompt into Codex
Use the prompt from `docs/CODEX_BOOTSTRAP_PROMPT.md`.

If you want Codex to guide the remaining installation in phases, continue with:
- `docs/CODEX_ASSISTED_SETUP.md`
- `docs/SETUP_CHAT_PROMPTS.md`

## Step 6. Verify the local config
Check:
- `memory/config.yaml`
- `configs/runtime-manifest.local.yaml`
- `memory/ROLE_TOOLING.md`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`
- `configs/role-profiles.template.yaml`

## Step 7. Run doctor and health
Use `docs/HEALTH_AND_DOCTOR.md` as the runtime gate.

At minimum verify:
- Python can execute
- config loads
- runtime manifest is present
- vault exists
- storage is writable
- the embedding endpoint is reachable
- the embedding model is available
- preflight can run
- finalize can archive a test note

Suggested generic commands:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\doctor-workspace.ps1
powershell -ExecutionPolicy Bypass -File .\tools\health-memory.ps1
```

## Step 8. Keep the safe boundaries
- keep production disabled
- keep local/private memory out of git
- keep generated indexes out of git
- do not store secrets in durable memory

## Step 9. Confirm battle-ready status
Use `docs/BATTLE_READY_CHECKLIST.md`.

The system is battle-ready only when:
- bootstrap is complete
- runtime prerequisites are green
- memory operations work
- operator workflow is understood
- security boundaries are confirmed
- parity manifest is complete

## What this process reconstructs
- role model
- route model
- skill-loading logic
- memory boundary shape
- archival and checkpoint discipline

## What it does not reconstruct by itself
- private vault content
- generated indexes
- local secrets
- internal screenshots, logs, or traces
- machine-specific runtime scripts that were never published
