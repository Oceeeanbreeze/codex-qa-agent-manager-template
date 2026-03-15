# System Comparison Guide

## Goal
Use this guide to compare two QA agent-system installations and decide whether they match in system shape, operating model, memory boundaries, and operator discipline.

## What should match
- role model
- routing model
- skill-loading logic
- role profile logic
- memory model shape
- archival policy
- checkpoint and anti-loop behavior
- operator workflow
- data boundaries and approval rules

## What does not need to match
- local absolute paths
- live vault contents
- generated indexes
- machine-specific runtime details
- private product knowledge
- secrets, tokens, credentials, and internal artifacts

## Comparison layers

### 1. Role model
Compare:
- coordinator role
- full role list
- when optional roles are added
- editor-of-record rule

Primary files:
- `AGENTS.md`
- `configs/role-profiles.template.yaml`

### 2. Routing
Compare:
- route list
- route triggers
- default role chains
- escalation rules
- checkpoint and anti-loop rules

Primary files:
- `codex/WORKFLOW.md`
- `docs/SETTINGS_PARITY_AUDIT.md`

### 3. Skills
Compare:
- role to skill mapping
- route-level presets
- minimal skill-loading rules

Primary files:
- `codex/SKILL_ROUTING.md`

### 4. Memory architecture
Compare:
- markdown source of truth
- storage paths and topology
- embedding provider and model
- vector and lexical retrieval
- chunking settings
- search limits
- per-agent include paths and query hints

Primary files:
- `memory/config.yaml` or `memory/config.template.yaml`
- `memory/ROLE_TOOLING.md`
- `docs/MEMORY_OPERATIONS_RUNBOOK.md`

### 5. Operator workflow
Compare:
- bootstrap flow
- health, preflight, search, finalize, watch entrypoints
- archival milestones
- recovery workflow

Primary files:
- `docs/INSTANT_SETUP.md`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/OPERATIONS.md`
- `docs/BACKUP_AND_RECOVERY.md`

### 6. Security and access boundaries
Compare:
- redaction rules
- approval gates
- environment tiers
- publication boundaries
- what must never enter durable memory

Primary files:
- `docs/DATA_BOUNDARIES_AND_ACCESS.md`
- `SECURITY.md`

## Recommended audit flow
1. Compare role and routing documents.
2. Compare skill routing.
3. Compare memory configuration and role tooling.
4. Compare operational docs and bootstrap flow.
5. Compare security and access boundaries.
6. Mark each layer as `Match`, `Partial`, or `Mismatch`.
7. Summarize what is intentionally excluded.

## Suggested result table

| Layer | System A | System B | Status | Notes |
|---|---|---|---|---|
| Role model |  |  |  |  |
| Routing |  |  |  |  |
| Skills |  |  |  |  |
| Memory architecture |  |  |  |  |
| Operator workflow |  |  |  |  |
| Security boundaries |  |  |  |  |

## PowerShell comparison helpers

### Compare AGENTS files
```powershell
Compare-Object \
  (Get-Content .\AGENTS.md) \
  (Get-Content .\other-system\AGENTS.md)
```

### Compare workflow files
```powershell
Compare-Object \
  (Get-Content .\codex\WORKFLOW.md) \
  (Get-Content .\other-system\codex\WORKFLOW.md)
```

### Compare memory configs
```powershell
Compare-Object \
  (Get-Content .\memory\config.yaml) \
  (Get-Content .\other-system\memory\config.yaml)
```

## Pass criteria
A comparison passes if the second system reproduces:
- the same orchestration behavior
- the same QA-specialized role model
- the same memory boundary shape
- the same operator discipline
- the same public-safe bootstrap and recovery model

## Interpretation rule
- `Match`: same behavior and same configuration shape.
- `Partial`: same system intent, but one side is richer or more detailed.
- `Mismatch`: material difference that changes how the system behaves or is operated.
