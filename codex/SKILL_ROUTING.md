# Skill Routing

## Role to skill mapping
- `router`
  - `task-router-risk-triage`
  - `requirements-extractor`
- `archivist`
  - `vault-archivist`
- `researcher`
  - `test-surface-finder`
  - `agent-browser`
  - `smart-monitor-feature-analysis` for Smart Monitor module work
- `architect`
  - `test-pyramid-planner`
- `implementer`
  - `test-hook-enabler`
- `reviewer`
  - `regression-hunter`
  - `test-gap-audit`
  - `playwright-review-checklist` for browser automation review
- `tester`
  - `risk-based-test-checklists`
- `test-strategist`
  - `test-pyramid-planner`
  - `test-gap-audit`
  - `atomic-testcase-writer`
- `test-automation-engineer`
  - `smart-monitor-feature-analysis`
  - `atomic-testcase-writer`
  - `playwright-e2e-builder`
  - `playwright-smart-monitor-writer`
  - `playwright-review-checklist`
  - `api-integration-test-builder`
  - `test-hook-enabler`
  - `agent-browser`
- `qa-browser`
  - `browser-qa-playbook`
  - `smart-monitor-feature-analysis`
  - `playwright-e2e-builder`
  - `playwright-smart-monitor-writer`
  - `risk-based-test-checklists`
  - `agent-browser`

## Load rules
- prefer route-level skills first
- load the smallest useful set
- prefer browser QA playbook before adding automation detail
- add `playwright-smart-monitor-writer` for Smart Monitor browser automation work
- add `agent-browser` when the task starts from live pages or local HTML artifacts
- add archival skill when durable knowledge should be preserved

## Route starter packs
- `research-only`
  - `requirements-extractor`
  - `test-surface-finder`
- `bugfix`
  - `task-router-risk-triage`
  - `requirements-extractor`
  - `regression-hunter`
  - `test-pyramid-planner` when the test layer is unclear
- `feature`
  - `task-router-risk-triage`
  - `requirements-extractor`
  - `test-pyramid-planner`
  - `test-gap-audit`
- `refactor`
  - `task-router-risk-triage`
  - `test-pyramid-planner`
  - `regression-hunter`
- `review-only`
  - `regression-hunter`
  - `test-gap-audit`
- `ui-validation`
  - `browser-qa-playbook`
  - `agent-browser`
  - `smart-monitor-feature-analysis` for Smart Monitor product work
  - `risk-based-test-checklists`
  - `playwright-e2e-builder` only when automation output is requested

## Practical rule
Do not load every skill mapped to every active role.
Start from one route starter pack, then add one specialist skill at a time only when the current evidence shows it is needed.
