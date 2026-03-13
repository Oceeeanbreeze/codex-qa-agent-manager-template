# Evaluation And Observability

## Goal
Make the system measurable, debuggable, and teachable.

## Evaluate four layers separately
1. Routing
2. Retrieval
3. Generation
4. Verification

## Recommended golden sets
- route selection cases
- memory retrieval relevance cases
- reviewer bug-finding cases
- QA coverage decision cases
- browser validation stability cases

## Minimum metrics
- route accuracy
- retrieval precision at top-k
- reviewer finding quality
- percentage of changes with the correct test layer selected
- percentage of tasks with explicit verification or explicit residual risk
- percentage of milestones archived successfully

## Observability artifacts
- doctor report
- health report
- self-test report
- per-task checkpoint note
- final archived outcome
- optional eval summary report

## Operational rule
Do not debug by intuition alone.
When a failure repeats, capture the subsystem, the command, the blocker, and the next fallback.

## Recommended review loop
- generator or implementer produces output
- reviewer challenges it
- tester or qa-browser validates it
- archivist preserves what should survive the thread
