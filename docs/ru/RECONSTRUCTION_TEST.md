# Тест восстановления системы

## Цель
Проверить, может ли новый Codex workspace восстановить такую же форму системы, как во внутренней настройке, используя только public repository.

## Что должно восстанавливаться
- role model
- routing model
- skill-loading model
- role-profile logic
- memory model shape
- archival policy
- checkpoint и anti-loop rules
- operator workflow
- data boundaries и approval model

## Что намеренно не восстанавливается только из public repo
- private vault content
- generated indexes
- local runtime scripts с machine-specific dependencies
- local secrets, credentials и product-specific knowledge

## Критерий успеха
Тест считается пройденным, если новый Codex workspace может восстановить:
- ту же orchestration behavior
- те же QA-specialized roles
- ту же memory boundary shape
- ту же operator discipline
- тот же public-safe bootstrap flow

## Обязательные файлы
- `AGENTS.md`
- `codex/WORKFLOW.md`
- `codex/SKILL_ROUTING.md`
- `memory/config.template.yaml`
- `memory/ROLE_TOOLING.md`
- `configs/role-profiles.template.yaml`
- `docs/CODEX_BOOTSTRAP_PROMPT.md`
- `docs/SETTINGS_PARITY_AUDIT.md`

## Ожидаемый ответ
- "Да" для system shape и operating model
- "Нет" для private knowledge, exact local runtime и accumulated durable memory
