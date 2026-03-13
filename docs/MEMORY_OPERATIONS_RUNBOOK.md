# Memory Operations Runbook

## Purpose
This runbook describes the minimum operational workflow for a local memory stack used by a multi-agent QA system.
Start from `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md` when the blocker is still unclear, then use this runbook for memory-specific diagnosis and operations.
Use it to diagnose environment issues, run retrieval, update indexes, archive results, and recover from constrained runtime environments.

## Command order
Use commands in this order:
1. `doctor`
2. `health`
3. `preflight`
4. `search`
5. `index`
6. `finalize`
7. `watch`

## Doctor
Use this first when the environment looks unstable.
It should verify:
- core workspace files
- vault structure
- storage write access
- Python runtime access
- health workflow access
- self-test access

## Health
Use for a focused environment check.
It should verify:
- config loads
- vault exists
- storage is writable
- SQLite works
- Python works
- embedding service is reachable
- required agent profiles exist

## Preflight
Use before substantial work to retrieve role-specific memory context.

## Search
Use during work for role-specific targeted retrieval.

## Index
Prefer changed-path incremental indexing instead of broad full rebuilds.
Support:
- full-scan incremental apply
- single-agent index
- changed-path updates

## Finalize
Run at milestone boundaries, not after every reply.
Archive durable knowledge and reindex only the needed roles.

## Watch
Use only when batch note editing makes background indexing worthwhile.
Avoid it during unstable troubleshooting.

## Constrained environment rule
If the agent host blocks direct Python execution inside the session sandbox:
- run `doctor`
- confirm runtime blockage
- use a launcher from a local unsandboxed shell
- do not confuse environment limits with architecture defects

## Operational summary
- `doctor` first when in doubt
- `health` before deep troubleshooting
- `preflight` before substantial work
- `finalize` at milestones
- `watch` only when useful
- keep a launcher fallback for constrained environments
