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

## Battle-ready operator order
When running the system on a fresh or unstable machine, use this order:
1. `doctor`
2. `health`
3. `preflight`
4. `search`
5. `index`
6. `finalize`
7. `watch` only if needed

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
- do not call the system battle-ready until doctor and health both pass

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

## Day-2 operations
At minimum, the operator should know how to:
- rerun bootstrap safely
- update local config without publishing secrets
- reindex memory after note changes
- archive milestone notes
- recover after Python or embedding runtime failure
- rebuild indexes from markdown instead of copying stale storage state
