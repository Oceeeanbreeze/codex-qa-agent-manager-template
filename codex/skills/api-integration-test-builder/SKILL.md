---
name: api-integration-test-builder
description: Design and write API or integration tests for behavior that does not require full browser rendering. Use when service contracts, persistence, or backend integration are the main risk.
---

# API Integration Test Builder

Keep browser tests for browser problems.

## Workflow
1. Identify the contract under test.
2. Define setup, request, assertion, and cleanup.
3. Prefer deterministic data and idempotent cleanup.
4. Verify response shape, side effects, and error handling.
5. Escalate to browser only if UI integration is the actual risk.

## Output expectations
- target endpoint or integration surface
- deterministic test shape
- cleanup and residual risk notes
