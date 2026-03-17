# Evals

## Goal
Store small golden datasets used to keep routing, retrieval, coverage, review, and browser-validation quality measurable.

## Rules
- keep datasets small, explicit, and reviewable
- prefer representative cases over large noisy collections
- update golden sets when the operating model changes materially
- treat these files as safe reference data, not as private vault content

## Dataset files
- `routing-cases.yaml`
- `retrieval-cases.yaml`
- `reviewer-cases.yaml`
- `coverage-cases.yaml`
- `browser-validation-cases.yaml`

## Operator entrypoint
Use:
- `tools/run-evals.ps1`

This validates dataset readiness and writes markdown and json reports under `reports/evals/`.
