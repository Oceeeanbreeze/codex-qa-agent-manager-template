---
name: playwright-e2e-builder
description: Translate focused user-visible scenarios into maintainable Playwright tests with stable selectors, shared helpers, and explicit assertions. Use for browser automation work across products.
---

# Playwright E2E Builder

Build focused browser checks, not monoliths.

## Workflow
1. Map one observable scenario to one test.
2. Reuse auth, navigation, loader, and setup helpers first.
3. Prefer stable selectors and explicit assertions.
4. Avoid sleep-based timing.
5. Keep test data and cleanup deterministic.
6. Note selector debt and environment blockers explicitly.

## Output expectations
- one focused spec or spec update
- helper reuse
- explicit verification steps
