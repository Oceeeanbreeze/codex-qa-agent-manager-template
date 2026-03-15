# Health And Doctor

## Goal
Define the minimum runtime checks required to consider the reconstructed agent system usable and safe.

## Doctor
Use `doctor` when the environment is newly created, unstable, or partially broken.

Suggested generic entrypoint in this template:
`tools/doctor-workspace.ps1`

Doctor should verify:
- core workspace files exist
- `configs/runtime-manifest.local.yaml` is present and readable
- `memory/config.yaml` is present and readable
- vault root exists
- storage root exists and is writable
- Python can actually execute
- local embedding endpoint is reachable
- the configured embedding model is available
- SQLite can create or open the lexical store
- vector storage location can be created or opened
- required role profiles and config templates are present

## Health
Use `health` when the system is already bootstrapped and you want a focused readiness check.

Suggested generic entrypoint in this template:
`tools/health-memory.ps1`

Health should verify:
- config loads without parse errors
- runtime manifest exists and reflects the intended local commands
- vault path is correct
- storage path is writable
- markdown roots expected by the roles exist
- embedding provider is reachable
- indexes can be updated
- archival command can run

## Minimum pass criteria
The system is not considered battle-ready until all of these are true:
- bootstrap completed
- local parity manifest is complete
- config is filled with safe local values
- doctor passes
- health passes
- preflight works for at least `archivist` and `router`
- finalize works on a test note
- search returns results from indexed markdown

## Operator rule
If `doctor` fails, stop expanding the architecture discussion and fix the runtime first.
