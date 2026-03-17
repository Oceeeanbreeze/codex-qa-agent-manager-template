# Local Skills

This folder contains the local skill layer used by `codex/SKILL_ROUTING.md`.

Rules:
- keep skills small and composable
- prefer one concrete capability per skill
- use the smallest useful set for a task
- route-level skills should help decide and scope work before deeper specialist skills are loaded

Core groups:
- routing: `task-router-risk-triage`, `requirements-extractor`
- memory: `vault-archivist`
- analysis and strategy: `test-surface-finder`, `test-pyramid-planner`, `test-gap-audit`, `risk-based-test-checklists`, `regression-hunter`
- browser and automation: `agent-browser`, `browser-qa-playbook`, `playwright-e2e-builder`, `playwright-smart-monitor-writer`, `api-integration-test-builder`
- implementation support: `test-hook-enabler`
