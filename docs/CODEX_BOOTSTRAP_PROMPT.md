# Codex Bootstrap Prompt

Paste this into a new Codex chat after opening the repository as a workspace.

```text
Use the local agent-system files in this repository.

Read in this order:
1. AGENTS.md
2. docs/REFERENCE_ARCHITECTURE.md
3. docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md
4. docs/NEW_DEVICE_SETUP.md
5. docs/DATA_BOUNDARIES_AND_ACCESS.md
6. docs/MEMORY_OPERATIONS_RUNBOOK.md
7. docs/EVALUATION_AND_OBSERVABILITY.md
8. docs/BACKUP_AND_RECOVERY.md

Then do the following:
- verify that memory/config.yaml exists
- if it does not exist, create it from memory/config.template.yaml using safe local defaults
- keep production access disabled
- preserve the existing role system and routing model
- treat markdown as source of truth and memory indexes as rebuildable caches
- use the smallest safe role chain for future work
- ask me only for values that cannot be inferred safely
- never commit private vault contents, generated memory indexes, logs, screenshots, traces, or secrets

When setup review is complete, summarize:
- what is already configured
- what still requires local installation or credentials
- what command I should run first if the memory environment looks broken
```
