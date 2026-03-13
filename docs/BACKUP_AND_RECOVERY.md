# Backup And Recovery

## Source of truth
Treat these as source of truth:
- markdown vault notes
- orchestration docs
- role prompts
- config files
- operator runbooks

Treat these as rebuildable caches:
- vector indexes
- SQLite search stores
- temporary reports that can be recreated

## Backup policy
Back up:
- vault content
- local private config
- docs and prompts
- lightweight manifests and reports

Do not rely on backups of generated indexes as the primary recovery path.

## Restore policy
1. Restore markdown notes and config.
2. Restore prompts, workflow docs, and operator docs.
3. Run doctor and health checks.
4. Rebuild indexes from markdown.
5. Run a small retrieval smoke test before normal use.

## Recovery drills
At regular intervals, confirm that a new machine can:
- restore the vault
- load config
- run doctor
- rebuild indexes
- retrieve at least one known note correctly
