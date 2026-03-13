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

That produces a setup that is intentionally very close to your current one, but still keeps secrets, local paths, and private data under your control.

## Step 1. Clone the repository
```powershell
git clone https://github.com/<your-account>/<repo-name>.git
cd <repo-name>
```

## Step 2. Run the bootstrap script
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-workspace.ps1
```

Optional custom values:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-workspace.ps1 -VaultDir 'D:\qa-agent-vault' -StorageDir 'D:\qa-agent-memory-data' -OllamaUrl 'http://127.0.0.1:11434' -ModelName 'nomic-embed-text-v2-moe'
```

## Step 3. Open the workspace in Codex
Open the cloned folder as the active workspace.

## Step 4. Paste the bootstrap prompt into Codex
Use the prompt from `docs/CODEX_BOOTSTRAP_PROMPT.md`.
It tells Codex exactly which files to read and how to continue setup.

## Step 5. Verify the local config
Check:
- `memory/config.yaml`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`

Keep real private values local and out of git.

## Step 6. Keep the safe boundaries
- keep production disabled
- keep local/private memory out of git
- keep generated indexes out of git
- do not store secrets in durable memory
