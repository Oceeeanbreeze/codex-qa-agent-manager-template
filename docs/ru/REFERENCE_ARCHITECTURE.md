# Референсная архитектура

## Цель
Дать production-minded, GitHub-safe архитектуру QA-focused multi-agent system.

## Принципы
- smallest safe role chain
- один coordinator и несколько specialists
- local-first durable memory для чувствительных QA-задач
- явные review и validation
- markdown как source of truth
- indexes как caches
- least privilege
- operator-friendly diagnostics

## Рекомендуемая цепочка
Request -> Router -> Archivist preflight -> Researcher -> Architect/Test Strategist -> Implementer/Test Automation Engineer/QA Browser -> Reviewer -> Tester -> Archivist finalize -> Evals

## Обязательные подсистемы
- orchestration and role prompts
- memory and archival
- data boundaries and access
- evaluation and observability
- backup and recovery
- operator dashboard and runbooks
