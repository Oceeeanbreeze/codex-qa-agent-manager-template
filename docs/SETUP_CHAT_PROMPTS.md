# Setup Chat Prompts

## Goal
Use these prompts to drive Codex through setup in small phases instead of trying to install and configure everything in one turn.

## How to use
- open the repository as a Codex workspace;
- run bootstrap first;
- then send one prompt at a time;
- do not skip to the next phase until the current one is green or clearly blocked.

## Phase 0. Repository understanding
```text
Use the local files in this repository and explain the current system shape.

Read:
1. AGENTS.md
2. codex/WORKFLOW.md
3. codex/SKILL_ROUTING.md
4. docs/FULL_RECONSTRUCTION_GUIDE.md
5. docs/REFERENCE_ARCHITECTURE.md
6. docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md

Then tell me:
- which role model is defined here;
- how routing is supposed to work;
- what parts of the system are reconstructed from git;
- what still must be configured locally.
```

## Phase 1. Bootstrap and manifest alignment
```text
Treat this as setup phase 1: bootstrap and manifest alignment.

Check whether these files exist and are aligned:
- memory/config.yaml
- configs/runtime-manifest.local.yaml
- configs/data-access.template.yaml
- configs/evals.template.yaml
- configs/recovery.template.yaml
- configs/role-profiles.template.yaml

If safe, update only local workspace files so that:
- memory/config.yaml exists;
- configs/runtime-manifest.local.yaml exists;
- both are aligned with the documented runtime shape.

Then summarize:
- what is already configured;
- what local values I still must provide manually;
- what exact file I should open next.
```

## Phase 2. Runtime prerequisites
```text
Treat this as setup phase 2: runtime prerequisites.

Use the repository docs and current workspace state to verify whether the machine is ready for:
- Python execution;
- embedding provider access;
- embedding model presence;
- writable vault and storage paths.

Use:
- docs/RUNTIME_INSTALLATION.md
- tools/install-runtime-prereqs.ps1

If checks are available, tell me which command to run first.
If something is missing, do not guess hidden fixes.
Tell me exactly:
- what is missing;
- whether Codex can fix it from this workspace;
- what I must install or configure manually.
Stop after the phase summary.
```

## Phase 3. Memory loop readiness
```text
Treat this as setup phase 3: memory loop readiness.

Verify the intended path for:
- doctor
- health
- preflight
- search
- index
- finalize

Use the current files to decide:
- which commands already exist;
- which commands are only documented but still require local wrappers;
- what the next smallest step is to make the memory loop operational.

Do not jump ahead to battle-ready.
Stop after listing the next exact action.
```

## Phase 4. Codex orchestration readiness
```text
Treat this as setup phase 4: Codex orchestration readiness.

Read the published role and workflow files and confirm whether this workspace is enough for Codex to reconstruct:
- the same role model;
- the same routing logic;
- the same memory boundaries;
- the same operator discipline.

Then tell me:
- whether the current repo is sufficient for safe structure-level reconstruction;
- what still prevents runtime-level parity;
- whether the bootstrap prompt should be updated further.
```

## Phase 5. Battle-ready review
```text
Treat this as setup phase 5: battle-ready review.

Use:
- docs/BATTLE_READY_CHECKLIST.md
- docs/HEALTH_AND_DOCTOR.md
- docs/RUNTIME_PARAMETER_MATRIX.md
- configs/runtime-manifest.local.yaml

Evaluate which checklist items are already green, which are warnings, and which are blockers.

Return:
- green items;
- blockers;
- the single most important next action.
```

## Phase 6. Public reproducibility proof
```text
Treat this as setup phase 6: public reproducibility proof.

Use:
- docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md
- docs/FULL_RECONSTRUCTION_GUIDE.md
- docs/CODEX_ASSISTED_SETUP.md

Assess whether a new user from the Git link can reproduce this system step by step without hidden assumptions.

Return:
- what is already reproducible;
- what still depends on undocumented local knowledge;
- what document or template should be improved next.
```
