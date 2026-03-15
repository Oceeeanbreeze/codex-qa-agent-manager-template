# Чек-лист боевой готовности

## Цель
Используй этот чек-лист, чтобы понять, готова ли reconstructed система к ежедневной работе, а не только к structure-level reconstruction test.

## 1. Bootstrap и форма репозитория
- [ ] Репозиторий клонирован в чистый workspace.
- [ ] `tools/bootstrap-workspace.ps1` завершился без ошибок.
- [ ] Создан `BOOTSTRAP_REPORT.md`.
- [ ] `memory/config.yaml` существует и содержит безопасные локальные значения.
- [ ] `configs/runtime-manifest.local.yaml` существует и отражает реальный локальный runtime.
- [ ] Существуют обязательные папки: `obsidian-vault`, `memory/data`, `configs`.

## 2. Runtime prerequisites
- [ ] Python запускается из operator shell.
- [ ] Ollama установлен и доступен.
- [ ] embedding model присутствует локально.
- [ ] storage directories доступны на запись.
- [ ] выбранный vault path корректен.

## 3. Готовность памяти
- [ ] `doctor` проходит.
- [ ] `health` проходит.
- [ ] `preflight` работает как минимум для `archivist` и `router`.
- [ ] `search` возвращает indexed content из markdown.
- [ ] `finalize` умеет архивировать тестовую interaction.

## 4. Готовность оператора
- [ ] Оператор знает порядок чтения документов.
- [ ] Оператор понимает, когда использовать `doctor`, `health`, `preflight`, `search`, `index`, `finalize` и `watch`.
- [ ] Реальные command entrypoints зафиксированы в `configs/runtime-manifest.local.yaml`.
- [ ] Документы по recovery и backup изучены.
- [ ] Approval gates понятны.

## 5. Готовность по безопасности
- [ ] Production остается disabled по умолчанию.
- [ ] Secrets не хранятся в git и durable memory.
- [ ] `.env`, live vault content, generated indexes, logs, screenshots и traces остаются вне публичного git.
- [ ] Локальные access boundaries проверены до первого реального использования.

## 6. Готовность по parity
- [ ] Есть `AGENTS.md`.
- [ ] Есть `codex/WORKFLOW.md`.
- [ ] Есть `codex/SKILL_ROUTING.md`.
- [ ] Role profiles проверены.
- [ ] Reconstruction behavior совпадает с ожидаемыми route и role model.
- [ ] Матрица runtime-параметров полностью покрыта локальным manifest.

## 7. Готовность по публичной воспроизводимости
- [ ] Второй clean clone успешно проходит по тем же документам.
- [ ] Чек-лист релиза в Git и parity остается зеленым.

## Финальное правило
Систему можно называть battle-ready только когда зеленые bootstrap, runtime, memory, operator, security, parity и public reproducibility sections.
