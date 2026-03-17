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
- launcher failures are reported with an actionable reason, for example `py.exe exists but no Python runtime is installed`
- shell checks may use `CODEX_PYTHON`, `PYTHON`, or `PYTHON_EXECUTABLE` as an explicit runtime override
- endpoint reachability and CLI visibility are reported separately when the embedding service is alive but its shell command is not on `PATH`

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
- archival command can run safely in smoke mode such as `finalize --dry-run`
- first-run retrieval can fail gracefully with empty results when a role index has not been created yet
- shell diagnostics distinguish `runtime missing`, `index uninitialized`, and `retrieval degraded`

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

## First-run note
On a newly bootstrapped workspace, some role memories may still be empty.
`search` and `preflight` should not be treated as architecture failures just because a role-specific index has not been created yet.
They should either return results from existing markdown or return an explicit empty-state diagnostic that tells the operator to run indexing for that role.

## Constrained-host note
If Python is installed but the current host still reports execution denial, treat that as an environment restriction.
Use an unsandboxed operator shell for the memory commands and keep that blocker separate from architecture defects in the repository itself.

## Retrieval maturity note
Healthy retrieval does not only mean "returns something".
It should also:
- return explicit status when a role is uninitialized
- expose lexical, embedding, vector, and exclusion diagnostics
- avoid surfacing low-value operational noise ahead of milestone or decision notes
