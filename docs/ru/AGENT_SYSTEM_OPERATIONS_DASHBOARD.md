# Операционный дашборд системы агентов

## Назначение
Этот дашборд является основной operator entrypoint для локальной multi-agent QA system.
Используй его, чтобы быстро понять текущий блокер, выбрать правильную команду и перейти в нужный subsystem guide.

## Что здесь должно быть видно
- текущий статус системы;
- текущий известный блокер;
- первые команды для запуска;
- какой subsystem нужно проверять первым;
- ссылки на routing, memory, skills и automation guides.

## Ключевые подсистемы
- routing layer;
- role и skill layer;
- memory layer;
- browser и automation layer.

## Первые команды
- `doctor`;
- `health`;
- `preflight`;
- `index`;
- `finalize`;
- `watch`.

## Первые документы
- `docs/ru/FULL_RECONSTRUCTION_GUIDE.md`;
- `docs/ru/RUNTIME_PARAMETER_MATRIX.md`;
- `docs/ru/CODEX_ASSISTED_SETUP.md`;
- `docs/ru/HEALTH_AND_DOCTOR.md`;
- `docs/ru/BATTLE_READY_CHECKLIST.md`.

## Операционное правило
Начинай с dashboard, потом переходи в нужный runbook.
Не начинай с редактирования scripts, если блокер еще не локализован.

## Правило для ограниченной среды
Если agent host блокирует прямой запуск Python:
- сначала диагностируй через `doctor`;
- используй launcher из unsandboxed shell;
- не смешивай environment blockers с architecture defects.
