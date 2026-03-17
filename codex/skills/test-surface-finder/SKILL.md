---
name: test-surface-finder
description: Find the real feature surface, affected files, user flows, and likely regression areas before testing or automation work starts. Use during research for QA-oriented tracing.
---

# Test Surface Finder

Map what can change and what should be checked.

## Workflow
1. Locate entrypoints, routes, modules, and supporting helpers.
2. Identify user-visible surfaces:
   - pages
   - forms
   - API boundaries
   - background jobs
   - config surfaces
3. Mark dependencies and likely regression neighbors.
4. Distinguish confirmed surfaces from inferred ones.
5. Point to the lightest useful test layer for each surface.

## Output expectations
- affected surface map
- likely regression list
- suggested verification layers
