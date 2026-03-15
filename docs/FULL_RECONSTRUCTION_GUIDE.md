# Full Reconstruction Guide

## Goal
Use this repository as a public-safe bootstrap layer that lets a new operator recreate the same agent-system shape, runtime contracts, memory layout, operator workflow, and validation discipline as the original internal setup.

## Important expectation
Git alone can reconstruct the full system shape and all governed configuration surfaces, but it cannot safely contain private vault data, secrets, generated indexes, or machine-specific state.

This guide is therefore split into:
- what is reconstructed directly from the repository;
- what must be filled locally to reach parity on a real machine;
- what must stay outside git by design.

## Two supported setup modes

### Mode A. Operator-led setup
Use this when the operator reads the docs and runs the commands directly.

### Mode B. Codex-assisted setup
Use this when the operator wants Codex to guide the installation phase by phase.

In Codex-assisted mode, the docs remain the source of truth, but Codex is used to:
- inspect the current workspace state;
- explain blockers;
- update safe local files;
- stop after each phase with the next exact action.

Use:
- `docs/CODEX_ASSISTED_SETUP.md`
- `docs/SETUP_CHAT_PROMPTS.md`
- `docs/RUNTIME_INSTALLATION.md`

## What this repository should reproduce
- role model and routing model;
- role prompts and skill-routing logic;
- memory layout and role-scoped retrieval boundaries;
- operator workflow for `doctor`, `health`, `preflight`, `search`, `index`, `finalize`, and optional `watch`;
- approval and access boundaries;
- evaluation, observability, backup, and recovery discipline;
- battle-ready validation gates;
- Git publication hygiene for future updates.

## What must be provided locally
- Python launcher and runtime;
- local embedding provider and embedding model;
- writable local storage paths;
- local vault root;
- local credentials and environment-specific boundaries;
- local launchers for memory scripts if they are not committed publicly.

## What must remain outside git
- private vault contents;
- generated vector indexes and SQLite stores;
- `.env` files, tokens, credentials, cookies, certificates;
- screenshots, traces, HAR files, logs with internal data;
- company-specific product notes and operator secrets.

## Recommended operator path

### Step 1. Clone into a clean workspace
```powershell
git clone https://github.com/<your-account>/<repo-name>.git
cd <repo-name>
```

### Step 2. Bootstrap the workspace
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-workspace.ps1
```

Bootstrap should create:
- `BOOTSTRAP_REPORT.md`;
- `memory/config.yaml`;
- `configs/runtime-manifest.local.yaml`;
- `obsidian-vault/`;
- `memory/data/`;
- `configs/`.

### Step 3. Fill the parity manifest
Open `configs/runtime-manifest.local.yaml` and make it your single local source of truth for:
- workspace and shell assumptions;
- Python launcher choice;
- embedding provider URL and model;
- vault path and storage path;
- command entrypoints;
- environment tiers and approval posture;
- observability and backup rules.

Use `docs/RUNTIME_PARAMETER_MATRIX.md` as the field-by-field guide.

### Step 4. Review and align the config surfaces
Verify these files together:
- `memory/config.yaml`
- `configs/runtime-manifest.local.yaml`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`
- `configs/role-profiles.template.yaml`

The parity rule is simple:
- `runtime-manifest.local.yaml` explains the intended local operating model;
- `memory/config.yaml` reflects the live memory runtime;
- the other templates define policy, evaluation, and recovery contracts.

### Step 5. Install runtime prerequisites
Required minimum runtime:
- PowerShell;
- Git;
- a Python launcher available from the operator shell;
- a reachable local embedding provider such as Ollama;
- the selected embedding model already pulled locally;
- write access to the workspace, vault, and storage paths.

Use:
- `docs/RUNTIME_INSTALLATION.md`
- `tools/install-runtime-prereqs.ps1`

### Step 6. Validate structure before behavior
Run:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\doctor-workspace.ps1
powershell -ExecutionPolicy Bypass -File .\tools\health-memory.ps1
```

You should not move to higher-level orchestration until both gates are green or the remaining warnings are understood and accepted.

### Step 7. Validate the memory loop
The system is only operationally useful when the full memory loop works:
- `preflight` can search role-scoped memory;
- `search` returns indexed markdown results;
- `index` can rebuild caches from markdown;
- `finalize` can archive a safe test interaction.

Safe generic scripts for these commands are shipped in `memory/scripts/`.
If you need wrappers, define them in `configs/runtime-manifest.local.yaml`.

### Step 8. Open the workspace in Codex
Use the cloned repository as the active Codex workspace.

Then paste `docs/CODEX_BOOTSTRAP_PROMPT.md` into a new chat so the routed role model initializes from the published files instead of relying on hidden context.

If you want a guided installation instead of a single bootstrap review, continue with:
- `docs/CODEX_ASSISTED_SETUP.md`
- `docs/SETUP_CHAT_PROMPTS.md`

### Step 9. Confirm battle-ready status
Use all of these together:
- `docs/HEALTH_AND_DOCTOR.md`
- `docs/BATTLE_READY_CHECKLIST.md`
- `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
- `docs/RUNTIME_PARAMETER_MATRIX.md`

The system should be called battle-ready only when bootstrap, runtime, memory, operator, security, and parity sections are green.

### Step 10. Validate public reproducibility
Before publishing or updating the repo:
1. clone it into a second clean folder;
2. repeat bootstrap and runtime checks;
3. verify that the same docs lead a new operator to the same result;
4. confirm that no private data was required from git.

Use `docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md`.

## Parity targets

### Required for "works like my system"
- same role set;
- same routing order and role activation rules;
- same memory directory model and role-scoped include-paths;
- same operator command vocabulary;
- same health and doctor gates;
- same approval posture and production restrictions;
- same recovery and observability expectations.

### Optional local variation
- exact file-system paths;
- exact Python install method;
- exact Ollama URL host;
- exact machine-specific launcher wrappers;
- exact vault contents.

## Final rule
This repository should make the system reproducible by configuration, workflow, and operator behavior.
Private state must still be injected locally, never copied into git.
