---
name: atomic-testcase-writer
description: Write atomic QA test cases with one goal per case and one user action per step. Use when generating or refining manual cases, especially for Smart Monitor-style QA KB workflows.
---

# Atomic Testcase Writer

Write cases that are easy to review, automate, and trace.

## Rules
- one testcase = one goal = one check
- one step = one user action
- expected results must be observable and testable
- mark unknown behavior as `requires clarification` or `assumption`
- review existing cases and autotests before writing a new one

## Smart Monitor alignment
When the target workflow is Smart Monitor:
- write manual cases in Russian
- prefer `steps_table`
- keep names readable and business-specific
- map each case to an automation candidate and target layer

## Output expectations
- concise case goal
- preconditions
- atomic steps
- observable expected results
- automation candidacy
