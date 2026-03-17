# Team Usage Guide

## Goal
Define a common operating model for a team using this QA agent system in daily Smart Monitor work.

## Standard route by work type
- feature analysis: `archivist -> researcher -> test-strategist`
- manual testcase work: `archivist -> researcher -> test-strategist -> reviewer`
- automation design or authoring: `archivist -> researcher -> test-strategist -> test-automation-engineer -> reviewer -> tester`
- browser validation: `archivist -> researcher -> qa-browser -> reviewer -> tester`
- mixed feature and automation work: `archivist -> researcher -> test-strategist -> test-automation-engineer -> qa-browser -> reviewer -> tester`

## Shared discipline
- start from existing docs, manual cases, autotests, and durable memory
- load only the smallest useful skill set
- keep one editor of record per file
- checkpoint after each major milestone
- archive durable outcomes, not raw sensitive artifacts

## Output expectations by stage
- analysis: confirmed facts, assumptions, risks, candidate checks
- testcase stage: Russian manual cases with atomic scope
- automation stage: layer choice, helper reuse plan, selector plan, cleanup plan
- review stage: findings first, residual risks second
- validation stage: exact evidence, clear blocker labeling, no vague pass claims

## Smart Monitor-specific references
- `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md`
- `docs/PLAYWRIGHT_SMART_MONITOR_STANDARDS.md`
- `docs/HTML_LAB_ANALYSIS_WORKFLOW.md`

## Failure handling
- after two identical failures, stop retrying
- after three steps with no new evidence, checkpoint and narrow scope
- keep environment blockers separate from repository or product defects

## Definition of done
- goal is explicitly answered
- at least one verification step ran when possible
- review happened for behavior-changing work
- durable knowledge was archived when useful
