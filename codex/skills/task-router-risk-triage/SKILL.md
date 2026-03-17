---
name: task-router-risk-triage
description: Triage a request into the smallest safe route and identify which specialist roles are actually needed. Use before substantial work when the route, blast radius, or risk profile is not obvious.
---

# Task Router Risk Triage

Pick the smallest safe route without under-scoping risky work.

## Workflow
1. Extract the user goal, requested output, and implied constraints.
2. Classify the request as `research-only`, `bugfix`, `feature`, `refactor`, `review-only`, or `ui-validation`.
3. Identify the minimum specialist roles needed.
4. Call out risk drivers:
   - behavior change
   - cross-file impact
   - browser or auth impact
   - unclear test layer
   - sensitive data or access concerns
5. Prefer a narrower route unless the risk profile clearly requires more roles.

## Output expectations
- chosen route
- active roles
- top assumptions
- top risks
- first verification layer
