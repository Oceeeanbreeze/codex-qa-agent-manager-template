---
name: regression-hunter
description: Review changes through a regression-first lens and focus on breakage patterns, edge cases, and missing validation. Use during reviewer passes and risk-focused audits.
---

# Regression Hunter

Look for what is likely to break next.

## Workflow
1. Start from changed behavior, not from style issues.
2. Look for:
   - contract drift
   - missing negative coverage
   - stale selectors or routes
   - setup and cleanup fragility
   - environment-specific assumptions
3. Order findings by severity.
4. State residual risk if full validation was not possible.

## Output expectations
- findings first
- missing tests or validation
- residual regression risk
