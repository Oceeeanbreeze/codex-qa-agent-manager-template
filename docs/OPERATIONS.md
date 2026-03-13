# Operations

## Default operating routine
1. Route the task.
2. Load only the needed skills.
3. Search memory for active roles.
4. Gather evidence.
5. Design the smallest safe change.
6. Implement or generate.
7. Review for regressions.
8. Validate at the right layer.
9. Archive reusable knowledge.

## Archival rules
- archive at milestones, not after every turn
- prefer task-scoped conversation captures over daily catch-all files
- preserve immutable metadata such as original `created_at` on append
- update `updated_at` only for the latest write

## Memory indexing rules
- strip YAML frontmatter before chunking and embedding
- treat metadata as metadata, not semantic content
- inspect retrieval results for metadata noise after index changes

## Runtime health rules
- verify Python and other runtime dependencies by successful execution, not by path existence alone
- add an explicit environment check before deeper memory tests
- keep shell-based and Python-based runtime resolution consistent

## Checkpoint rule
Create or update one compact checkpoint when:
- the task lasts more than 20-30 minutes
- the thread becomes crowded
- tool runs become flaky
- the next step may require a fresh conversation

## Retry rule
- if the same failure happens twice, stop retrying automatically
- if three steps produce no new evidence, checkpoint and narrow scope

## QA-specific rule
Do not default every check to browser automation.
Prefer the lightest layer that proves the behavior with confidence.
