# Skill Routing

## Role to skill mapping
- `router`
  - `task-router-risk-triage`
  - `requirements-extractor`
- `archivist`
  - `vault-archivist`
- `researcher`
  - `test-surface-finder`
- `architect`
  - `test-pyramid-planner`
- `implementer`
  - `test-hook-enabler`
- `reviewer`
  - `regression-hunter`
  - `test-gap-audit`
- `tester`
  - `risk-based-test-checklists`
- `test-strategist`
  - `test-pyramid-planner`
  - `test-gap-audit`
- `test-automation-engineer`
  - `playwright-e2e-builder`
  - `api-integration-test-builder`
  - `test-hook-enabler`
- `qa-browser`
  - `browser-qa-playbook`
  - `playwright-e2e-builder`
  - `risk-based-test-checklists`

## Load rules
- prefer route-level skills first
- load the smallest useful set
- prefer browser QA playbook before adding automation detail
- add archival skill when durable knowledge should be preserved
