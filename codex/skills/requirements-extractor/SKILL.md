---
name: requirements-extractor
description: Extract explicit requirements, hidden constraints, acceptance criteria, and missing inputs from user requests and workspace evidence. Use before design or implementation when scope needs to be pinned down.
---

# Requirements Extractor

Turn a request into a short, testable contract.

## Workflow
1. Separate explicit asks from inferred expectations.
2. List observable outcomes, not implementation wishes.
3. Identify boundaries:
   - what must not be changed
   - sensitive data rules
   - environment or host limitations
4. Mark unknowns as `requires clarification` or `assumption`.
5. Convert the result into acceptance criteria the reviewer and tester can use later.

## Output expectations
- goal
- constraints
- acceptance criteria
- open questions or assumptions
