---
name: playwright-review-checklist
description: Review Playwright tests for determinism, selector quality, helper reuse, and regression-focused coverage. Use after writing or changing browser automation.
---

# Playwright Review Checklist

Review browser automation like production code.

## Focus
- one scenario per test
- stable selectors first
- helper reuse before duplication
- loader-aware waits and `expect()` instead of sleeps
- explicit assertions after meaningful actions
- cleanup and shared-state discipline
- skip rationale and environment blockers

## Smart Monitor specifics
- prefer `data-test-subj` and `getByTestId()`
- align with the local Smart Monitor Playwright standards
- note selector debt when forced onto CSS or localized text
- check whether auth/session reuse is done correctly

## Output expectations
- findings first
- severity and residual risk
- missing assertions or flaky patterns
- opportunities to reduce duplication
