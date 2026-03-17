---
name: test-gap-audit
description: Compare requested coverage with existing manual and automated checks, then identify what is missing or redundant. Use during review, strategy, and QA planning.
---

# Test Gap Audit

Find gaps before adding more tests.

## Workflow
1. Review existing cases, specs, smoke checks, and project memory first.
2. Map each required behavior to current coverage.
3. Mark each item as:
   - covered
   - partially covered
   - uncovered
   - duplicated
4. Prioritize gaps by business risk and recurrence.
5. Recommend the next minimal useful additions.

## Output expectations
- coverage map
- prioritized gaps
- duplicate or weak coverage warnings
