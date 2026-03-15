# Codex-Assisted Setup

## Goal
Use Codex as a guided operator assistant so the system can be reproduced step by step even when the full setup cannot be completed in a single command or a single prompt.

## Why this mode exists
Real setup usually has two classes of work:
- deterministic repository bootstrap that can be documented and partially scripted;
- local runtime finishing steps that depend on the machine, installed tools, shell behavior, permissions, and safe local values.

This document defines a staged setup model where the operator and Codex work together until the installation matches the intended system shape and runtime behavior.

## Core rule
The setup should proceed in phases.
Codex should not try to "finish everything at once".
Each phase ends with one of these outcomes:
- green and ready to continue;
- blocked with a concrete next fix;
- waiting for a local value that only the operator can safely provide.

## Who does what

### Operator responsibilities
- clone the repository;
- run local commands when execution is required;
- install local prerequisites such as Python or Ollama;
- provide safe local values for runtime paths and credentials;
- approve sensitive actions;
- confirm when a phase is complete.

### Codex responsibilities
- read the published system files and preserve the intended role model;
- inspect current workspace state;
- explain what is already configured and what is missing;
- guide the operator phase by phase;
- update safe local files inside the workspace when asked;
- stop and surface blockers instead of hiding them;
- validate that the resulting setup still matches the documented system shape.

## Phase model

### Phase 0. Repository understanding
Goal:
- verify that Codex can read the published agent-system files and explain the architecture back.

Done when:
- Codex identifies the role model, routing model, memory model, and operator docs.

### Phase 1. Bootstrap and manifest alignment
Goal:
- create the local workspace skeleton;
- create `memory/config.yaml`;
- create `configs/runtime-manifest.local.yaml`;
- align manifest values with the local machine.

Done when:
- bootstrap succeeds;
- the operator has filled the manifest enough for runtime checks.

### Phase 2. Runtime prerequisites
Goal:
- verify that required local tools are installed and callable from the operator shell.

Typical checks:
- Git;
- PowerShell;
- Python launcher;
- Ollama or the chosen embedding provider;
- embedding model presence;
- writable vault and storage paths.

Done when:
- `doctor` is green or only leaves understood warnings.

### Phase 3. Memory loop readiness
Goal:
- confirm the system can do more than hold files;
- it must be able to read, index, search, and archive.

Typical checks:
- `health`;
- `preflight`;
- `search`;
- `index`;
- `finalize`.

Done when:
- the memory loop is operational or the only missing pieces are explicitly documented local scripts.

### Phase 4. Codex orchestration readiness
Goal:
- confirm that Codex initializes from the repository itself rather than hidden prior context.

Done when:
- the bootstrap prompt works;
- Codex explains the same routed role model and operating rules as the published docs.

### Phase 5. Battle-ready review
Goal:
- confirm runtime, operator, security, and parity readiness together.

Done when:
- `docs/BATTLE_READY_CHECKLIST.md` is green.

### Phase 6. Public reproducibility proof
Goal:
- prove that the same repository can drive the same setup on a fresh clean clone.

Done when:
- `docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md` is green.

## Recommended working pattern in chat

### Pattern A. Codex drives the phase
Use this when you want Codex to inspect the workspace and tell you the next exact step.

Codex should:
- check the current phase status;
- make only the smallest safe changes;
- tell you the exact command to run next if local execution is required;
- stop after each phase summary.

### Pattern B. Operator drives the phase
Use this when you already know which command you want to run and want Codex to validate the result afterward.

Codex should:
- interpret the command output;
- explain pass, warn, or fail;
- propose the next narrow fix.

## How to avoid setup drift
- keep `configs/runtime-manifest.local.yaml` as the local source of truth for runtime choices;
- keep `memory/config.yaml` aligned with the manifest;
- do not let Codex invent hidden defaults that are not reflected in files;
- after each meaningful phase, update the manifest or the relevant config file.

## When Codex should stop and ask
Codex should pause when:
- a secret, token, or credential is required;
- a path cannot be inferred safely;
- a tool must be installed outside the repo;
- a destructive or approval-gated action is needed;
- production or another sensitive environment would be touched.

## Required outcomes for "reproduce the system like mine"
By the end of the staged setup, the installation should match:
- the same role chain and routing rules;
- the same memory shape and role-scoped boundaries;
- the same operator command vocabulary;
- the same health and doctor gates;
- the same production-disabled-by-default posture;
- the same battle-ready and release parity discipline.

## Use with prompt pack
Use `docs/SETUP_CHAT_PROMPTS.md` to drive each phase with a ready-made Codex prompt.
