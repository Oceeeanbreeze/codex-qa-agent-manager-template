# Data Boundaries And Access

## Goal
Keep the QA agent system useful without turning durable memory into a privacy or leakage risk.

## Default posture
- production access disabled by default
- local-first storage for sensitive QA memory
- least privilege by role
- summarize or redact before archival when possible

## Never archive
- secrets, tokens, cookies, certificates
- `.env` values and private keys
- raw production data exports
- HAR files, traces, screenshots, or logs with sensitive content unless redacted and explicitly approved
- customer data or personally identifying information unless there is a legal and operational reason to retain it

## Role-based memory boundaries
- `archivist`: broad but governed access to reusable notes and safe conversation captures
- `researcher`: investigations, logs, decisions, project notes
- `architect`: decisions, contracts, invariants, playbooks
- `implementer`: implementation patterns and reusable helpers
- `reviewer`: failure patterns, regressions, postmortems
- `tester` and `qa-browser`: repro steps, verification notes, checklists

## Environment tiers
- `local`: safe for private experimentation and local scripts
- `qa`: preferred environment for browser and automation validation
- `staging`: only when needed and with team approval
- `production`: disabled for routine agent operation

## Approval gates
Require explicit operator approval for:
- destructive commands
- schema or migration changes
- writes outside the workspace boundary
- access to sensitive external systems
- any production interaction

## Publishing rule
Public repositories should contain only:
- generic docs
- generic prompts
- generic config templates
- example commands with placeholders

Keep live vaults, indexes, secrets, logs, traces, and screenshots out of git.
