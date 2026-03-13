# Public QA Agent Manager Template

This package is safe to publish as a public GitHub repository.
It contains generic instructions and configuration templates for a quality-first agent system used to automate QA workflows.

It does not include:
- product-specific notes;
- private vault contents;
- local absolute paths;
- project incidents or screenshots;
- customer or company data.

## What this template gives you

- a routed multi-agent QA workflow;
- generic role definitions;
- generic workflow and skill-routing files;
- a template memory configuration;
- data-boundary, eval, and recovery templates;
- a bootstrap script for new devices;
- a Codex bootstrap prompt for new sessions;
- security rules to avoid leaking local data;
- setup instructions for GitHub publication.

## Suggested repository structure

```text
qa-agent-manager-template/
  README.md
  .gitignore
  SECURITY.md
  AGENTS.md
  codex/
    WORKFLOW.md
    SKILL_ROUTING.md
    agents/
  configs/
    data-access.template.yaml
    evals.template.yaml
    recovery.template.yaml
  docs/
    AGENT_SYSTEM_OPERATIONS_DASHBOARD.md
    REFERENCE_ARCHITECTURE.md
    INSTANT_SETUP.md
    NEW_DEVICE_SETUP.md
    CODEX_BOOTSTRAP_PROMPT.md
    DATA_BOUNDARIES_AND_ACCESS.md
    MEMORY_OPERATIONS_RUNBOOK.md
    EVALUATION_AND_OBSERVABILITY.md
    BACKUP_AND_RECOVERY.md
    DEPLOYMENT.md
    OPERATIONS.md
  memory/
    README.md
    config.template.yaml
  tools/
    bootstrap-workspace.ps1
```

## Quick start

1. Copy these files into a new repository.
2. Read `docs/REFERENCE_ARCHITECTURE.md`, `docs/INSTANT_SETUP.md`, and `docs/NEW_DEVICE_SETUP.md`.
3. Run `tools/bootstrap-workspace.ps1` on the target device.
4. Replace placeholders in `memory/config.template.yaml` and `configs/*.template.yaml`.
5. Review `SECURITY.md` and `.gitignore` before the first commit.
6. Add your local scripts or implementation later, but never commit live vault data or generated indexes.

## New device or new Codex account flow

1. Clone the repo.
2. Run `tools/bootstrap-workspace.ps1`.
3. Open the repo as a workspace in Codex.
4. Paste `docs/CODEX_BOOTSTRAP_PROMPT.md` into a new chat.
5. Let Codex finish local review and tell you what still depends on local runtime or credentials.

## Publish to GitHub

1. Create a new empty repository in your account.
2. Initialize git locally in the folder.
3. Commit only the template files.
4. Push to GitHub.

Example commands:

```powershell
git init
git add .
git commit -m "Add public QA agent manager template"
git branch -M main
git remote add origin https://github.com/<your-account>/<repo-name>.git
git push -u origin main
```

## Before every push

Run these checks:
- no local absolute paths remain;
- no product names remain if the repo must stay generic;
- no `obsidian-vault/` content is tracked;
- no `memory/data/` content is tracked;
- no screenshots, traces, logs, or exports with sensitive context are tracked;
- no secrets or `.env` files are tracked.

## Included files

- `AGENTS.md`: generic orchestration rules
- `codex/WORKFLOW.md`: route selection and execution discipline
- `codex/SKILL_ROUTING.md`: role-to-skill mapping template
- `memory/config.template.yaml`: generic memory configuration template
- `configs/*.template.yaml`: generic access, eval, and recovery templates
- `tools/bootstrap-workspace.ps1`: safe scaffold for a new device
- `docs/CODEX_BOOTSTRAP_PROMPT.md`: exact prompt for a new Codex session
- `docs/REFERENCE_ARCHITECTURE.md`: target system design
- `docs/INSTANT_SETUP.md`: step-by-step setup
- `docs/NEW_DEVICE_SETUP.md`: new-device playbook
- `docs/DATA_BOUNDARIES_AND_ACCESS.md`: memory and environment boundaries
- `docs/EVALUATION_AND_OBSERVABILITY.md`: measurement model
- `docs/BACKUP_AND_RECOVERY.md`: restore and recovery model
- `docs/DEPLOYMENT.md`: setup instructions
- `docs/OPERATIONS.md`: operational rules
- `SECURITY.md`: public publishing safety checklist

## Recommended next step

Keep the public repository docs-first.
If you later add scripts, publish only generic implementations and keep all environment-specific config local.
