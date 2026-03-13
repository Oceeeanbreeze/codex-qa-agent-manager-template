# Reconstruction Test

## Goal
Verify whether a new Codex workspace can reconstruct the same system shape as the internal setup from the public repository.

## What must be reproducible
- role model
- routing model
- skill-loading model
- role-profile logic
- memory model shape
- archival policy
- checkpoint and anti-loop rules
- operator workflow
- data boundaries and approval model

## What is intentionally not reproducible from the public repo alone
- private vault content
- generated indexes
- local runtime scripts with machine-specific dependencies
- local secrets, credentials, and product-specific knowledge

## Pass criteria
The reconstruction test passes if a new Codex workspace can recover:
- the same orchestration behavior
- the same QA-specialized roles
- the same memory boundary shape
- the same operator discipline
- the same public-safe bootstrap flow

## Required files for the test
- `AGENTS.md`
- `codex/WORKFLOW.md`
- `codex/SKILL_ROUTING.md`
- `memory/config.template.yaml`
- `memory/ROLE_TOOLING.md`
- `configs/role-profiles.template.yaml`
- `docs/CODEX_BOOTSTRAP_PROMPT.md`
- `docs/SETTINGS_PARITY_AUDIT.md`

## Expected answer
- "Yes" for system shape and operating model
- "No" for private knowledge, exact local runtime, and accumulated durable memory
