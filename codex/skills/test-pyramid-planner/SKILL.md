---
name: test-pyramid-planner
description: Decide the cheapest sufficient test layer and split coverage between unit, integration, API, browser, and exploratory validation. Use for design, refactor, and test strategy work.
---

# Test Pyramid Planner

Choose the right layer before writing tests.

## Workflow
1. Define the behavior under change.
2. Decide what can be proven at unit, integration, API, or browser level.
3. Prefer the cheapest layer that proves the risk.
4. Escalate to browser only when UI, auth, navigation, rendering, or cross-layer integration matter.
5. Call out what should stay manual or exploratory.

## Output expectations
- target layers
- why those layers are sufficient
- what would be redundant
