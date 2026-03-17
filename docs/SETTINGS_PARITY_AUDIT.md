# Settings Parity Audit

## Goal
Track which settings from the internal agent system are already mirrored in the public template and which were added to improve parity.

## Added for parity
- coordinator responsibilities for `router`
- richer role definitions, including QA-specific roles
- routing add-on rules for `test-strategist`, `test-automation-engineer`, and `qa-browser`
- local route starter packs and smallest-useful-skill loading guidance
- local Smart Monitor QA skills for feature analysis, atomic testcase writing, Playwright authoring, browser QA, and review
- memory search and memory capture policy
- milestone archival policy
- checkpoint and anti-loop rules
- model escalation and role profiles
- richer route heuristics and final-response rules
- role-scoped memory include paths and richer query hints
- retrieval exclusions and lower-noise retrieval diagnostics
- capture-kind tagging for archived notes
- public `memory/ROLE_TOOLING.md`
- public `configs/role-profiles.template.yaml`
- Smart Monitor QA operator playbook and standards docs
- first-hour reproducibility runbook and team enablement docs
- lightweight eval harness, golden datasets, and eval runbook
- battle-ready and parity docs updated for constrained-host fallback and eval readiness

## Still intentionally excluded from the public template
- live vault content
- generated indexes and search databases
- private runtime scripts with local operational dependencies
- local absolute paths
- internal incidents, screenshots, and logs
- private credentials and environment-specific secrets

## Reconstruction test question
Can a new Codex workspace rebuild the same system shape from this repo?

Answer:
- yes for orchestration rules, role model, memory model shape, route logic, checkpoints, anti-loop behavior, operator discipline, Smart Monitor QA specialization, and lightweight eval readiness flow
- no for private knowledge, accumulated vault memory, generated indexes, local runtime dependencies, or secrets

## Practical result
The public template is now much closer to the internal system in behavior and configuration shape, while still staying safe for GitHub publication.
