---
name: smart-monitor-feature-analysis
description: Analyze Smart Monitor features, modules, and user flows so QA work starts from the real product surface instead of assumptions. Use before testcase authoring, coverage audit, or Playwright design for Smart Monitor.
---

# Smart Monitor Feature Analysis

Anchor QA work in the actual Smart Monitor module behavior.

## Workflow
1. Identify the target module, component, and route.
2. Review existing project memory, manual cases, autotests, and helper patterns first.
3. Build a short feature map:
   - user goal
   - entrypoints and routes
   - main entities and data objects
   - main path
   - failure path
   - side effects and cleanup needs
4. Mark what is:
   - confirmed by code or browser evidence
   - inferred from naming or docs
   - blocked by environment
5. Produce QA-ready outputs:
   - feature summary
   - risks
   - testcase candidates
   - automation candidates

## Output expectations
- module and component scope
- confirmed user flows
- key risks and test data needs
- candidate manual and automated checks
