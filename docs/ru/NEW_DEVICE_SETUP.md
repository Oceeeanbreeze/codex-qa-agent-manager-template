# Настройка на новом устройстве

## Цель
Максимально близко восстановить форму твоей agent system на новом устройстве или в новом аккаунте Codex.

## Реалистичное ожидание
Ссылка на GitHub сама по себе не развернет среду полностью автоматически.
Надежный сценарий такой:
1. клонировать репозиторий
2. запустить bootstrap script
3. открыть repo в Codex
4. отправить bootstrap prompt

## Шаги
1. Клонируй репозиторий.
2. Выполни:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-workspace.ps1
```
3. Открой репозиторий как workspace в Codex.
4. Вставь prompt из `docs/ru/CODEX_BOOTSTRAP_PROMPT.md`.
5. Проверь локальные config files и runtime prerequisites.

## Важно
- real vault contents не публикуются
- local runtime scripts могут оставаться локальными
- secrets и credentials должны настраиваться отдельно на каждом устройстве
