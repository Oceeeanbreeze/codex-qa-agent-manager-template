# Security Rules For Public Publication

## Never commit

- real vault contents
- generated vector indexes
- SQLite memory databases
- screenshots from internal systems
- traces, HAR files, logs, or exports with product data
- `.env` files or secrets
- customer data, credentials, tokens, cookies, certificates
- local absolute paths that reveal workstation structure

## Safe to publish

- generic workflow docs
- generic role prompts
- generic memory config templates with placeholders
- generic setup instructions
- example commands with placeholders

## Sanitization checklist

Before publishing, search for:
- company names
- product names
- employee names
- local usernames
- hostnames
- IPs that should remain private
- real repository paths
- copied incident text

## Placeholder policy

Use placeholders like:
- `<YOUR_VAULT_PATH>`
- `<YOUR_STORAGE_PATH>`
- `<YOUR_OLLAMA_URL>`
- `<YOUR_MODEL_NAME>`
- `<REPO_NAME>`

## Git discipline

- review `git diff --cached` before every commit
- keep the first public commit docs-only if possible
- enable branch protection after the initial push
- prefer pull-request review even for personal maintenance
