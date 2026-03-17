---
name: test-hook-enabler
description: Identify and propose the smallest safe product changes that improve testability, selector stability, and automation reliability. Use when tests are blocked by avoidable product-side test debt.
---

# Test Hook Enabler

Improve testability without changing product behavior.

## Workflow
1. Confirm the current blocker:
   - missing stable selector
   - missing API seam
   - non-deterministic setup
   - unobservable result
2. Propose the smallest safe hook or selector.
3. Avoid changing business behavior or contracts.
4. Document the regression risk and why the hook is justified.

## Output expectations
- concrete hook or selector proposal
- blast radius
- verification needed after the product change
