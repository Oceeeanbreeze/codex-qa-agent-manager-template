# Settings Parity Audit

## Goal
Track which settings from the internal agent system are already mirrored in the public template and which were added to improve parity.

## Added for parity
- coordinator responsibilities for `router`
- richer role definitions, including QA-specific roles
- routing add-on rules for `test-strategist`, `test-automation-engineer`, and `qa-browser`
- memory search and memory capture policy
- milestone archival policy
- checkpoint and anti-loop rules
- model escalation and role profiles
- richer route heuristics and final-response rules
- role-scoped memory include paths and richer query hints
- public `memory/ROLE_TOOLING.md`
- public `configs/role-profiles.template.yaml`

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
- yes for orchestration rules, role model, memory model shape, route logic, checkpoints, anti-loop behavior, and operator discipline
- no for private knowledge, accumulated vault memory, generated indexes, local runtime dependencies, or secrets

## Practical result
The public template is now much closer to the internal system in behavior and configuration shape, while still staying safe for GitHub publication.
