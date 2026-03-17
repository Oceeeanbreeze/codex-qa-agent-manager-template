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
- a runtime manifest template for local parity;
- a Codex bootstrap prompt for new sessions;
- a Codex-assisted staged setup guide and prompt pack;
- security rules to avoid leaking local data;
- setup instructions for GitHub publication in English and Russian;
- a full reconstruction guide and a Git release parity checklist.

## Suggested repository structure

```text
qa-agent-manager-template/
  README.md
  README.ru.md
  requirements.txt
  .gitignore
  SECURITY.md
  AGENTS.md
  codex/
    WORKFLOW.md
    SKILL_ROUTING.md
    agents/
    skills/
  configs/
    data-access.template.yaml
    evals.template.yaml
    recovery.template.yaml
    role-profiles.template.yaml
    runtime-manifest.template.yaml
  docs/
    AGENT_SYSTEM_OPERATIONS_DASHBOARD.md
    REFERENCE_ARCHITECTURE.md
    FULL_RECONSTRUCTION_GUIDE.md
    FIRST_HOUR_RUNBOOK.md
    RUNTIME_INSTALLATION.md
    CODEX_ASSISTED_SETUP.md
    SETUP_CHAT_PROMPTS.md
    INSTANT_SETUP.md
    NEW_DEVICE_SETUP.md
    HEALTH_AND_DOCTOR.md
    BATTLE_READY_CHECKLIST.md
    BATTLE_READY_REPORT.md
    RUNTIME_PARAMETER_MATRIX.md
    GIT_RELEASE_AND_PARITY_CHECKLIST.md
    GITHUB_REPO_SNIPPETS.md
    CODEX_BOOTSTRAP_PROMPT.md
    DATA_BOUNDARIES_AND_ACCESS.md
    MEMORY_OPERATIONS_RUNBOOK.md
    EVALUATION_AND_OBSERVABILITY.md
    BACKUP_AND_RECOVERY.md
    DEPLOYMENT.md
    OPERATIONS.md
    EVALS_RUNBOOK.md
    HTML_LAB_ANALYSIS_WORKFLOW.md
    SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md
    TESTER_ONBOARDING_ONE_PAGER.md
    TEAM_USAGE_GUIDE.md
    QA_LEAD_ADOPTION_GUIDE.md
    WORKSHOP_PACK.md
    SETTINGS_PARITY_AUDIT.md
    ru/
  evals/
    README.md
    *.yaml
  memory/
    README.md
    ROLE_TOOLING.md
    config.template.yaml
    scripts/
  tools/
    bootstrap-workspace.ps1
    doctor-workspace.ps1
    health-memory.ps1
    run-evals.ps1
    install-runtime-prereqs.ps1
```

## Quick start

1. Copy these files into a new repository.
2. Read `docs/FULL_RECONSTRUCTION_GUIDE.md` first.
3. Run `tools/bootstrap-workspace.ps1` on the target device.
4. Install runtime prerequisites from `docs/RUNTIME_INSTALLATION.md` or `tools/install-runtime-prereqs.ps1`.
5. Fill `configs/runtime-manifest.local.yaml` and verify it against `docs/RUNTIME_PARAMETER_MATRIX.md`.
6. Replace placeholders in `memory/config.template.yaml` and the other templates you actually use.
7. If you want guided phase-by-phase help, use `docs/CODEX_ASSISTED_SETUP.md` and `docs/SETUP_CHAT_PROMPTS.md`.
8. Review `docs/HEALTH_AND_DOCTOR.md`, `docs/BATTLE_READY_CHECKLIST.md`, `docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md`, `SECURITY.md`, and `.gitignore`.
9. Treat the template as battle-ready only after runtime, memory, operator, and parity checks are green.

## New device or new Codex account flow

1. Clone the repo.
2. Run `tools/bootstrap-workspace.ps1`.
3. Install Python, Ollama, dependencies, and the embedding model using `docs/RUNTIME_INSTALLATION.md`.
4. Fill `configs/runtime-manifest.local.yaml`.
5. Open the repo as a workspace in Codex.
6. Paste `docs/CODEX_BOOTSTRAP_PROMPT.md` into a new chat.
7. If you want guided setup, continue with `docs/SETUP_CHAT_PROMPTS.md` one phase at a time.
8. Run the doctor and health checks described in `docs/HEALTH_AND_DOCTOR.md`.
9. Validate readiness using `docs/BATTLE_READY_CHECKLIST.md`.
10. Let Codex finish local review and tell you what still depends on local runtime or credentials.

## Recommended docs order
- `docs/REFERENCE_ARCHITECTURE.md`
- `docs/FULL_RECONSTRUCTION_GUIDE.md`
- `docs/FIRST_HOUR_RUNBOOK.md`
- `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md`
- `docs/RUNTIME_INSTALLATION.md`
- `docs/CODEX_ASSISTED_SETUP.md`
- `docs/INSTANT_SETUP.md`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/HEALTH_AND_DOCTOR.md`
- `docs/BATTLE_READY_CHECKLIST.md`
- `docs/EVALS_RUNBOOK.md`
- `docs/RUNTIME_PARAMETER_MATRIX.md`
- `docs/DATA_BOUNDARIES_AND_ACCESS.md`
- `docs/MEMORY_OPERATIONS_RUNBOOK.md`
- `docs/SETTINGS_PARITY_AUDIT.md`

## Reconstruction test goal
This repository should let a new Codex workspace reconstruct the same agent-system shape, role model, memory model, and operator discipline as the original setup, while intentionally excluding private vault data, local secrets, and product-specific knowledge.

## Included files
- `AGENTS.md`: orchestration rules with routing, memory, checkpoints, anti-loop rules, and escalation
- `codex/WORKFLOW.md`: route selection, heuristics, execution discipline, and response standard
- `codex/SKILL_ROUTING.md`: role-to-skill mapping template
- `codex/skills/agent-browser/`: local skill for page navigation, HTML parsing, structured extraction, and QA automation handoff
- `memory/config.template.yaml`: detailed memory configuration template
- `memory/scripts/`: safe generic entrypoints for preflight, search, index, finalize, archive, and watch
- `memory/scripts/run_evals.py`: lightweight executable eval harness for golden datasets and readiness reports
- `memory/ROLE_TOOLING.md`: role-specific memory tooling and process guide
- `configs/role-profiles.template.yaml`: logical role-profile mapping
- `configs/*.template.yaml`: generic access, eval, and recovery templates
- `evals/`: small golden datasets for routing, retrieval, review, coverage, and browser validation
- `tools/bootstrap-workspace.ps1`: safe scaffold for a new device
- `tools/run-evals.ps1`: operator entrypoint for eval readiness checks and report generation
- `configs/runtime-manifest.template.yaml`: single local parity manifest template
- `docs/CODEX_BOOTSTRAP_PROMPT.md`: exact prompt for a new Codex session
- `docs/SETUP_CHAT_PROMPTS.md`: staged prompts for Codex-assisted setup
- `docs/FIRST_HOUR_RUNBOOK.md`: shortest reproducible path from fresh clone to runtime and memory readiness
- `docs/HTML_LAB_ANALYSIS_WORKFLOW.md`: intake workflow for uploaded HTML pages and QA output generation
- `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md`: recommended Smart Monitor flow for feature analysis, testcase design, automation design, browser validation, and review
- `docs/EVALS_RUNBOOK.md`: operator flow for validating golden datasets and writing eval readiness reports
- `docs/TESTER_ONBOARDING_ONE_PAGER.md`: compact onboarding for testers using the agent system safely
- `docs/TEAM_USAGE_GUIDE.md`: shared operating model for teams using the QA agent system
- `docs/QA_LEAD_ADOPTION_GUIDE.md`: governance and rollout guidance for QA leads
- `docs/WORKSHOP_PACK.md`: short workshop outline for team enablement
- `docs/SETTINGS_PARITY_AUDIT.md`: what was added to align the public template with the internal system
- `docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md`: what to verify before each public update

## Recommended next step
Keep the public repository docs-first.
If you later add scripts, publish only generic implementations and keep all environment-specific config local.

## What still must be added locally for a truly battle-ready installation
- local secrets and access boundaries configured outside git
- a completed local parity manifest
