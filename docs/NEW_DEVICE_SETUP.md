# New Device Setup

## Goal
Use this repository to recreate the same agent-system shape on a new device or in a new Codex account with minimal manual work.

## Reality check
A GitHub link alone does not fully auto-deploy the system.
The closest reliable flow is:
1. clone the repository
2. open the folder in Codex
3. run the bootstrap script
4. send the prepared bootstrap prompt to Codex

That reproduces the same orchestration model, role model, memory model shape, and operator discipline while keeping secrets, local paths, private vault data, and product knowledge out of the public repo.

## Step 1. Clone the repository
```powershell
git clone https://github.com/<your-account>/<repo-name>.git
cd <repo-name>
```

## Step 2. Run the bootstrap script
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-workspace.ps1
```

## Step 3. Open the workspace in Codex
Open the cloned folder as the active workspace.

## Step 4. Paste the bootstrap prompt into Codex
Use the prompt from `docs/CODEX_BOOTSTRAP_PROMPT.md`.

## Step 5. Verify the local config
Check:
- `memory/config.yaml`
- `memory/ROLE_TOOLING.md`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`
- `configs/role-profiles.template.yaml`

## Step 6. Keep the safe boundaries
- keep production disabled
- keep local/private memory out of git
- keep generated indexes out of git
- do not store secrets in durable memory
