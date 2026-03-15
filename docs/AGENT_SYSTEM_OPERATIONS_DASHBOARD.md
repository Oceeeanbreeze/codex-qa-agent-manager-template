# Agent System Operations Dashboard

## Purpose
This dashboard is the operator entrypoint for a local multi-agent QA system.
Use it to identify the current blocker, choose the right command, and jump to the correct subsystem guide.

## What it should show
- current system status
- current known blocker
- first commands to run
- which subsystem to inspect first
- links to routing, memory, skills, and automation guides

## Core subsystems
- routing layer
- role and skill layer
- memory layer
- browser and automation layer

## First commands
- `doctor`
- `health`
- `preflight`
- `index`
- `finalize`
- `watch`

## First documents
- `docs/FULL_RECONSTRUCTION_GUIDE.md`
- `docs/RUNTIME_PARAMETER_MATRIX.md`
- `docs/CODEX_ASSISTED_SETUP.md`
- `docs/HEALTH_AND_DOCTOR.md`
- `docs/BATTLE_READY_CHECKLIST.md`

## Operational rule
Start from the dashboard, then jump to the right runbook.
Do not begin by editing scripts when the blocker is still unclear.

## Constrained environment rule
If the agent host blocks direct Python execution:
- diagnose with `doctor`
- use a launcher from an unsandboxed shell
- separate environment blockers from architecture defects
