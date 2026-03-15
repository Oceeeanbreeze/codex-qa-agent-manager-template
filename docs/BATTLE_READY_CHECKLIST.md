# Battle Ready Checklist

## Goal
Use this checklist to decide whether the reconstructed system is ready for real daily work instead of only a structure-level reconstruction test.

## 1. Bootstrap and repository shape
- [ ] Repository is cloned into a clean workspace.
- [ ] `tools/bootstrap-workspace.ps1` completed without errors.
- [ ] `BOOTSTRAP_REPORT.md` was created.
- [ ] `memory/config.yaml` exists and contains local safe values.
- [ ] `configs/runtime-manifest.local.yaml` exists and reflects the real local runtime.
- [ ] Required folders exist: `obsidian-vault`, `memory/data`, `configs`.

## 2. Runtime prerequisites
- [ ] Python can execute from the operator shell.
- [ ] Ollama is installed and reachable.
- [ ] The embedding model is present locally.
- [ ] Storage directories are writable.
- [ ] The selected vault path is valid.

## 3. Memory readiness
- [ ] `doctor` passes.
- [ ] `health` passes.
- [ ] `preflight` works for at least `archivist` and `router`.
- [ ] `search` returns indexed content from markdown.
- [ ] `finalize` can archive a test interaction.

## 4. Operator readiness
- [ ] The operator knows the startup order of the docs.
- [ ] The operator knows when to use `doctor`, `health`, `preflight`, `search`, `index`, `finalize`, and `watch`.
- [ ] The operator keeps the actual command entrypoints in `configs/runtime-manifest.local.yaml`.
- [ ] Recovery and backup docs are reviewed.
- [ ] Approval gates are understood.

## 5. Security readiness
- [ ] Production remains disabled by default.
- [ ] Secrets are not stored in git or durable memory.
- [ ] `.env`, live vault content, generated indexes, logs, screenshots, and traces stay outside public git.
- [ ] Local access boundaries are reviewed before first real use.

## 6. Behavior parity readiness
- [ ] `AGENTS.md` is present.
- [ ] `codex/WORKFLOW.md` is present.
- [ ] `codex/SKILL_ROUTING.md` is present.
- [ ] Role profiles are reviewed.
- [ ] Reconstruction behavior matches the expected route and role model.
- [ ] The runtime parameter matrix is fully covered by the local manifest.

## 7. Public reproducibility readiness
- [ ] A second clean clone can follow the same docs successfully.
- [ ] The Git release and parity checklist stays green.

## Final rule
The system should be called battle-ready only when bootstrap, runtime, memory, operator, security, parity, and public reproducibility sections are all green.
