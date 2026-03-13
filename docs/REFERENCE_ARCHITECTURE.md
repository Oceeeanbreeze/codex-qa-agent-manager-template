# Reference Architecture

## Goal
Provide a production-minded, GitHub-safe reference architecture for a QA-focused multi-agent system.

## Design principles
- smallest safe role chain
- one coordinator, several specialists
- local-first durable memory for sensitive QA work
- explicit validation and review
- markdown as source of truth, indexes as caches
- least privilege for tools and environments
- operator-friendly diagnostics

## Recommended architecture

```text
Request
v
Router
v
Archivist preflight
v
Researcher
v
Architect or Test Strategist
v
Implementer or Test Automation Engineer or QA Browser
v
Reviewer
v
Tester
v
Archivist finalize
v
Evals and reports
```

## Recommended role set
- `router`
- `archivist`
- `researcher`
- `architect`
- `implementer`
- `reviewer`
- `tester`
- `test-strategist`
- `test-automation-engineer`
- `qa-browser`

## Why this shape works
- It is simpler and more controllable than deep autonomous trees.
- It supports QA-specific work such as coverage planning, browser validation, and test automation.
- It keeps durable knowledge outside the chat window.
- It supports debugging and recovery when runtime conditions are unstable.

## Required subsystems
- orchestration and role prompts
- memory and archival
- access policy and data boundaries
- evaluation and observability
- backup and recovery
- operator dashboard and runbooks

## First documents to open
- `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
- `docs/INSTANT_SETUP.md`
- `docs/DATA_BOUNDARIES_AND_ACCESS.md`
- `docs/EVALUATION_AND_OBSERVABILITY.md`
- `docs/BACKUP_AND_RECOVERY.md`
