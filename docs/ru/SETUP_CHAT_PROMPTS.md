# Набор промтов для пошаговой настройки

## Цель
Используй эти промты, чтобы вести Codex по настройке небольшими фазами, а не пытаться установить и настроить всю систему за один заход.

## Как использовать
- открой репозиторий как Codex workspace;
- сначала выполни bootstrap;
- затем отправляй по одному prompt на фазу;
- не переходи к следующей фазе, пока текущая не green или не имеет четко понятного blocker.

## Фаза 0. Понимание репозитория
```text
Используй локальные файлы этого репозитория и объясни текущую форму системы.

Прочитай:
1. AGENTS.md
2. codex/WORKFLOW.md
3. codex/SKILL_ROUTING.md
4. docs/FULL_RECONSTRUCTION_GUIDE.md
5. docs/REFERENCE_ARCHITECTURE.md
6. docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md

Затем сообщи:
- какая role model здесь определена;
- как должен работать routing;
- какие части системы восстанавливаются из git;
- что еще должно настраиваться локально.
```

## Фаза 1. Bootstrap и alignment manifest
```text
Считай это фазой 1 настройки: bootstrap и alignment manifest.

Проверь, существуют ли и согласованы ли между собой:
- memory/config.yaml
- configs/runtime-manifest.local.yaml
- configs/data-access.template.yaml
- configs/evals.template.yaml
- configs/recovery.template.yaml
- configs/role-profiles.template.yaml

Если это безопасно, обнови только локальные файлы workspace так, чтобы:
- memory/config.yaml существовал;
- configs/runtime-manifest.local.yaml существовал;
- оба файла были выровнены с задокументированной runtime shape.

После этого кратко сообщи:
- что уже настроено;
- какие локальные значения я еще должен задать вручную;
- какой файл мне открыть следующим.
```

## Фаза 2. Runtime prerequisites
```text
Считай это фазой 2 настройки: runtime prerequisites.

Используй документацию репозитория и текущее состояние workspace, чтобы понять, готова ли машина к:
- запуску Python;
- доступу к embedding provider;
- наличию embedding model;
- записи в vault и storage paths.

Используй:
- docs/ru/RUNTIME_INSTALLATION.md
- tools/install-runtime-prereqs.ps1

Если проверки уже доступны, скажи, какую команду мне запускать первой.
Если чего-то не хватает, не придумывай скрытых фиксов.
Скажи точно:
- чего не хватает;
- может ли Codex починить это из этого workspace;
- что я должен установить или настроить вручную.
Остановись после summary по фазе.
```

## Фаза 3. Готовность memory loop
```text
Считай это фазой 3 настройки: готовность memory loop.

Проверь intended path для:
- doctor
- health
- preflight
- search
- index
- finalize

По текущим файлам определи:
- какие команды уже существуют;
- какие команды только задокументированы, но еще требуют локальные wrappers;
- какой следующий минимальный шаг нужен, чтобы сделать memory loop рабочим.

Не переходи раньше времени к battle-ready.
Остановись после перечисления следующего точного действия.
```

## Фаза 4. Готовность оркестрации Codex
```text
Считай это фазой 4 настройки: готовность оркестрации Codex.

Прочитай опубликованные role и workflow files и подтверди, хватает ли этого workspace, чтобы Codex восстановил:
- ту же role model;
- ту же routing logic;
- те же memory boundaries;
- ту же operator discipline.

После этого сообщи:
- достаточно ли текущего repo для безопасной structure-level reconstruction;
- что еще мешает runtime-level parity;
- нужно ли еще обновить bootstrap prompt.
```

## Фаза 5. Battle-ready review
```text
Считай это фазой 5 настройки: battle-ready review.

Используй:
- docs/BATTLE_READY_CHECKLIST.md
- docs/HEALTH_AND_DOCTOR.md
- docs/RUNTIME_PARAMETER_MATRIX.md
- configs/runtime-manifest.local.yaml

Оцени, какие пункты чек-листа уже green, какие в статусе warning, а какие являются blocker.

Верни:
- green items;
- blockers;
- одно самое важное следующее действие.
```

## Фаза 6. Доказательство публичной воспроизводимости
```text
Считай это фазой 6 настройки: доказательство публичной воспроизводимости.

Используй:
- docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md
- docs/FULL_RECONSTRUCTION_GUIDE.md
- docs/CODEX_ASSISTED_SETUP.md

Оцени, может ли новый пользователь по Git-ссылке воспроизвести эту систему шаг за шагом без скрытых assumptions.

Верни:
- что уже воспроизводится;
- что еще зависит от недокументированного локального знания;
- какой документ или шаблон нужно улучшить следующим.
```
