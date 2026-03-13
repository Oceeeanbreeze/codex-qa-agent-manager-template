# Публикация и деплой

## Цель
Опубликовать docs-first QA agent manager без утечки локальных данных.

## Что должно быть в публичном repo
- docs
- prompts
- generic config templates
- safe bootstrap script

## Что должно оставаться локально
- real vault
- generated indexes
- local runtime scripts с приватными зависимостями
- secrets и credentials

## Перед push
Проверь:
- нет локальных путей
- нет product-specific names
- не трекаются `obsidian-vault/` и `memory/data/`
- нет screenshots, logs, traces и `.env`
