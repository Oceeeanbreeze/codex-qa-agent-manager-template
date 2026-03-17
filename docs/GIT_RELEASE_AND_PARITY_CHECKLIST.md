# Git Release And Parity Checklist

## Goal
Use this checklist before each public push so the repository remains safe to publish and still capable of reconstructing the intended agent system on a clean machine.

## 1. Documentation completeness
- [ ] `README.md` explains the public-safe purpose of the repository.
- [ ] `README.ru.md` explains the same flow for Russian-speaking operators.
- [ ] `docs/FULL_RECONSTRUCTION_GUIDE.md` reflects the current deployment path.
- [ ] `docs/FIRST_HOUR_RUNBOOK.md` reflects the shortest reproducible setup path from fresh clone to runtime and memory proof.
- [ ] `docs/RUNTIME_INSTALLATION.md` reflects the real runtime setup path.
- [ ] `docs/RUNTIME_PARAMETER_MATRIX.md` matches the current required local parameters.
- [ ] `docs/HEALTH_AND_DOCTOR.md` matches the actual runtime gates.
- [ ] `docs/BATTLE_READY_CHECKLIST.md` matches the actual readiness criteria.
- [ ] `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md` reflects the current Smart Monitor QA workflow.
- [ ] `docs/EVALS_RUNBOOK.md` reflects the current evals entrypoint and report flow.
- [ ] Team enablement docs are current:
  - `docs/TESTER_ONBOARDING_ONE_PAGER.md`
  - `docs/TEAM_USAGE_GUIDE.md`
  - `docs/QA_LEAD_ADOPTION_GUIDE.md`
  - `docs/WORKSHOP_PACK.md`

## 2. Configuration completeness
- [ ] `memory/config.template.yaml` is current.
- [ ] `requirements.txt` is current.
- [ ] `configs/runtime-manifest.template.yaml` is current.
- [ ] `configs/data-access.template.yaml` is current.
- [ ] `configs/evals.template.yaml` is current.
- [ ] `configs/recovery.template.yaml` is current.
- [ ] `configs/role-profiles.template.yaml` is current.
- [ ] `configs/runtime-manifest.template.yaml` includes the documented `doctor`, `health`, `preflight`, `search`, `index`, `finalize`, `watch`, and `evals` entrypoints.

## 3. Public safety
- [ ] No live vault content is committed.
- [ ] No generated indexes or SQLite caches are committed.
- [ ] No `.env`, secrets, tokens, cookies, or certificates are committed.
- [ ] No company-specific screenshots, logs, traces, or HAR files are committed.
- [ ] No internal URLs, hostnames, usernames, or workstation-specific paths leaked into the docs.
- [ ] Generated eval reports under `reports/` are not committed.

## 4. Reproducibility
- [ ] The repository was cloned into a clean folder.
- [ ] `tools/bootstrap-workspace.ps1` completed on the clean clone.
- [ ] `tools/doctor-workspace.ps1` passes or leaves only understood warnings.
- [ ] `tools/health-memory.ps1` passes or leaves only understood warnings.
- [ ] `tools/run-evals.ps1` runs and writes a report or leaves only understood warnings.
- [ ] `memory/scripts/` contains the documented generic memory entrypoints.
- [ ] `memory/scripts/run_evals.py` is present if `docs/EVALS_RUNBOOK.md` is published.
- [ ] `BOOTSTRAP_REPORT.md` is created in the clean clone.
- [ ] `configs/runtime-manifest.local.yaml` is created in the clean clone.
- [ ] `configs/evals.local.yaml` can be created or copied locally without hidden knowledge.
- [ ] Constrained-host fallback is documented clearly enough for a new operator to separate environment restrictions from repository defects.

## 5. Parity proof
- [ ] A new operator can identify the role model from the published files.
- [ ] A new operator can identify the routing model from the published files.
- [ ] A new operator can identify the memory model from the published files.
- [ ] A new operator can identify the operator commands from the published files.
- [ ] A new operator can identify the Smart Monitor QA specialization from the published files.
- [ ] A new operator can identify the evals and observability layer from the published files.
- [ ] `codex/SKILL_ROUTING.md` does not reference missing local skills.
- [ ] The published `codex/skills/` tree contains the skills referenced by the public routing model.
- [ ] The repository clearly explains what still must be configured locally.

## 6. Final push gate
- [ ] `git diff --cached` was reviewed.
- [ ] New docs are linked from at least one operator-facing entrypoint when they change the startup path.
- [ ] Public-safe generated artifacts stay ignored after the update.
- [ ] The repository description and README snippets are still accurate.
- [ ] The repo can honestly be described as a public-safe reconstruction layer for the internal system.

## Final rule
Do not push a documentation update that improves wording but breaks reproducibility.
