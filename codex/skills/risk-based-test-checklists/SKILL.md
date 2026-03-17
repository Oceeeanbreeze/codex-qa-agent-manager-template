---
name: risk-based-test-checklists
description: Produce focused risk-oriented checklists for validation, review, and exploratory work. Use when broad testing would create noise and a smaller list of high-signal checks is better.
---

# Risk Based Test Checklists

Prefer short, high-signal checks over exhaustive noise.

## Focus areas
- happy path viability
- failure path behavior
- state persistence
- permissions and access
- regressions in adjacent features
- data safety and cleanup

## Workflow
1. Start from the primary business risk.
2. Add one main path and one meaningful failure path.
3. Add regression guards only where breakage would be costly.
4. Keep each check observable and concrete.

## Output expectations
- concise validation checklist
- residual risks not covered by the checklist
