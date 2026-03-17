# Evals Runbook

## Goal
Run the lightweight eval harness that proves the golden datasets are present, structurally valid, and ready to be used as a quality gate.

## Inputs
- `configs/evals.local.yaml`
- `evals/*.yaml`

## Operator command
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run-evals.ps1 -ConfigPath .\configs\evals.local.yaml -Strict
```

## What this checks
- required eval datasets exist
- each dataset has the required fields for each case
- each dataset meets the minimum case count
- reports can be written to `reports/evals/`

## Outputs
- `reports/evals/evals-report-<timestamp>.json`
- `reports/evals/evals-report-<timestamp>.md`

## Gate meaning
- `pass`: dataset readiness is green and scale-up can continue
- `fail`: missing, empty, degraded, or invalid datasets must be fixed before relying on evals as a quality gate

## Constrained-host note
If the current shell cannot execute Python:
- switch to the validated unsandboxed operator shell
- rerun `tools/run-evals.ps1`
- keep that blocker separate from dataset defects
