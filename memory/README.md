# Memory Setup

Use a durable memory layer so important QA decisions do not live only inside the chat window.
Start from `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`, then move into `docs/MEMORY_OPERATIONS_RUNBOOK.md` for memory-specific operations.

## Recommended components
- markdown vault or notes folder
- local embeddings provider
- vector store
- lexical search store

## Operational rules
- search memory before substantial work
- archive at milestones
- preserve exact wording for explicit memory requests
- keep checkpoint notes short and reusable
- prefer task-scoped conversation archives over broad daily logs
- preserve immutable metadata such as original `created_at`
- strip YAML frontmatter before indexing content
- verify runtime dependencies by execution, not path existence

## Do not publish
- live vault contents
- generated indexes
- archived conversations from real work
- logs or traces from internal systems
