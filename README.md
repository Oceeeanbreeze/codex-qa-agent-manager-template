# Public QA Agent Manager Template

English: `README.md`
Русская версия: `README.ru.md`

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
- a detailed memory configuration template;
- role-tooling and role-profile templates;
- data-boundary, eval, and recovery templates;
- a bootstrap script for new devices;
- a Codex bootstrap prompt for new sessions;
- security rules to avoid leaking local data;
- setup instructions for GitHub publication in English and Russian.

## Suggested repository structure

```text
qa-agent-manager-template/
  README.md
  README.ru.md
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
    role-profiles.template.yaml
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
    SETTINGS_PARITY_AUDIT.md
    ru/
  memory/
    README.md
    ROLE_TOOLING.md
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

## Recommended docs order
- `docs/REFERENCE_ARCHITECTURE.md`
- `docs/INSTANT_SETUP.md`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/DATA_BOUNDARIES_AND_ACCESS.md`
- `docs/MEMORY_OPERATIONS_RUNBOOK.md`
- `docs/SETTINGS_PARITY_AUDIT.md`

## Reconstruction test goal
This repository should let a new Codex workspace reconstruct the same agent-system shape, role model, memory model, and operator discipline as the original setup, while intentionally excluding private vault data, local secrets, and product-specific knowledge.

## Included files
- `AGENTS.md`: orchestration rules with routing, memory, checkpoints, anti-loop rules, and escalation
- `codex/WORKFLOW.md`: route selection, heuristics, execution discipline, and response standard
- `codex/SKILL_ROUTING.md`: role-to-skill mapping template
- `memory/config.template.yaml`: detailed memory configuration template
- `memory/ROLE_TOOLING.md`: role-specific memory tooling and process guide
- `configs/role-profiles.template.yaml`: logical role-profile mapping
- `configs/*.template.yaml`: generic access, eval, and recovery templates
- `tools/bootstrap-workspace.ps1`: safe scaffold for a new device
- `docs/CODEX_BOOTSTRAP_PROMPT.md`: exact prompt for a new Codex session
- `docs/SETTINGS_PARITY_AUDIT.md`: what was added to align the public template with the internal system

## Recommended next step
Keep the public repository docs-first.
If you later add scripts, publish only generic implementations and keep all environment-specific config local.
