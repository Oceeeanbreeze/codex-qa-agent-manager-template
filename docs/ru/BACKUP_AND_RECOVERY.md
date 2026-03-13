# Backup и Recovery

## Source of truth
Считай source of truth:
- markdown vault notes
- orchestration docs
- role prompts
- config files
- operator runbooks

Считай rebuildable caches:
- vector indexes
- SQLite search stores
- временные отчеты

## Restore policy
1. Восстанови markdown notes и config.
2. Восстанови prompts и workflow docs.
3. Запусти doctor и health checks.
4. Пересобери indexes из markdown.
5. Сделай retrieval smoke test.
