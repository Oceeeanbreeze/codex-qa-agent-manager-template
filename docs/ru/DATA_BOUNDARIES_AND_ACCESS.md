# Границы данных и доступы

## Базовая позиция
- production disabled по умолчанию
- local-first storage для чувствительной QA memory
- least privilege по ролям
- summarize/redact before archive, если это возможно

## Никогда не архивировать
- secrets, tokens, cookies, certificates
- `.env` values и private keys
- raw production exports
- HAR, traces, screenshots, logs с чувствительным контентом без redaction
- customer data и PII без отдельной необходимости и разрешения

## Approval gates
Явное подтверждение нужно для:
- destructive commands
- schema or migration changes
- writes вне workspace boundary
- sensitive external systems
- любой production access
