# Smart Monitor QA Automation Playbook

## Goal
Define the recommended end-to-end flow for Smart Monitor QA work inside this agent system.

## Primary capability chain
1. Feature analysis
2. Risk extraction
3. Coverage audit
4. Atomic manual testcase design
5. Test layer decision
6. Playwright or API automation design
7. Browser validation
8. Review and residual risk reporting

## Recommended role chain
1. `archivist`
2. `researcher`
3. `test-strategist`
4. `test-automation-engineer` when automation is needed
5. `qa-browser` when browser evidence matters
6. `reviewer`
7. `tester`
8. `archivist`

## Recommended skill chain
- `smart-monitor-feature-analysis`
- `test-surface-finder`
- `test-gap-audit`
- `atomic-testcase-writer`
- `test-pyramid-planner`
- `browser-qa-playbook`
- `playwright-e2e-builder`
- `playwright-smart-monitor-writer`
- `playwright-review-checklist`

Load only the minimum subset needed for the current step.

## Operating rules
- do not start from automation if feature understanding is still weak
- review existing manual cases and autotests before adding new ones
- keep one testcase atomic and one automated check focused
- separate product defects from stand or environment blockers
- preserve Smart Monitor selector and helper standards

## Output ladder
### 1. Feature analysis
- module or route
- user goal
- entities and side effects
- confirmed flows
- assumptions

### 2. Coverage audit
- already covered
- partially covered
- missing
- duplicated

### 3. Manual testcase design
- one goal per case
- one user action per step
- observable expected results
- Russian language for Smart Monitor-style QA KB flows

### 4. Automation design
- target layer
- helper reuse plan
- selector plan
- data and cleanup plan
- skip or blocker rationale

### 5. Browser validation and review
- main path evidence
- failure path evidence
- automation candidate quality
- reviewer findings
- residual risks

## Preferred layer decisions
- use browser automation for auth, navigation, rendering, route integration, and user-visible workflows
- use API or integration tests for contract and persistence behavior that does not require rendering
- keep exploratory validation for unstable or poorly instrumented surfaces until testability improves

## Smart Monitor standards link
Use [PLAYWRIGHT_SMART_MONITOR_STANDARDS.md](C:/Users/ocean/agent-system-reconstruction-test/codex-qa-agent-manager-template/docs/PLAYWRIGHT_SMART_MONITOR_STANDARDS.md) before authoring or reviewing Smart Monitor browser automation.
