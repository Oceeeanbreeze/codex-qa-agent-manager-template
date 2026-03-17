# First Hour Runbook

## Goal
Give the operator one compact, reproducible path for turning a fresh clone into a usable QA agent workspace without guessing the next step.

## Use this when
- the repository was just cloned
- the workspace was just bootstrapped
- the device or Codex account is new
- the operator wants the shortest path to a real readiness verdict

## Step 1. Bootstrap the workspace
Run:
- `tools/bootstrap-workspace.ps1`

Expected result:
- `BOOTSTRAP_REPORT.md` exists
- `memory/config.yaml` exists
- `configs/runtime-manifest.local.yaml` exists

## Step 2. Fill local runtime truth
Open and complete:
- `configs/runtime-manifest.local.yaml`
- `memory/config.yaml`

Verify against:
- `docs/RUNTIME_PARAMETER_MATRIX.md`

Do not continue until the Python launcher, vault path, storage path, embedding endpoint, embedding model, and operator commands reflect the real machine.

## Step 3. Run runtime gates
Open:
- `docs/HEALTH_AND_DOCTOR.md`

Run:
- `doctor`
- `health`

Expected result:
- the current shell can execute Python or the blocker is diagnosed exactly
- the embedding endpoint is reachable
- the embedding model is available
- storage is writable

## Step 4. Handle constrained-host failures correctly
If `doctor` or `health` reports that Python exists but cannot execute from the current host:
- treat it as an environment restriction
- switch to the validated unsandboxed operator shell
- rerun `doctor` and `health`
- keep that blocker separate from repository architecture defects

Do not start rewriting routing, memory, or skills while the runtime gate is still red.

## Step 5. Prove the memory loop
Use:
- `preflight`
- `search`
- `index`
- `finalize`

Expected result:
- `preflight` returns role status instead of crashing
- `search` can return indexed markdown or an explicit empty-state status
- `index` builds role memory from markdown
- `finalize` archives a test interaction safely

## Step 6. Load the QA specialization docs
Read:
- `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md`
- `docs/PLAYWRIGHT_SMART_MONITOR_STANDARDS.md`
- `docs/HTML_LAB_ANALYSIS_WORKFLOW.md`

Expected result:
- the operator understands the preferred flow from feature analysis to testcase design, automation design, browser validation, and review

## Step 7. Call the system ready only after proof
Validate with:
- `docs/BATTLE_READY_CHECKLIST.md`
- `docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md`

The system is ready for daily QA work only when runtime, memory, operator, security, and parity checks are all green.
