# Отчет по тесту восстановления

Дата: 2026-03-13

## Результат
Частичный pass.

## Что восстанавливается
Новый Codex workspace может восстановить из этого public repository:
- ту же role model
- ту же route model
- ту же skill-loading model
- ту же role-profile logic
- ту же memory boundary shape
- ту же archival, checkpoint и anti-loop policy
- тот же operator workflow и bootstrap path

## Что не восстанавливается полностью
Новый Codex workspace все еще не может восстановить только из public repository:
- private vault content
- accumulated durable memory
- generated indexes
- local runtime scripts с private или machine-specific dependencies
- local secrets и credentials

## Вывод
Public repo теперь достаточен, чтобы восстановить ту же форму системы и operating discipline.
Но он не предназначен для восстановления private knowledge state или exact local runtime 1:1, и это сделано сознательно ради безопасности.
