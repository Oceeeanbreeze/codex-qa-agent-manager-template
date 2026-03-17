---
name: browser-qa-playbook
description: Drive realistic browser validation with clear repro notes, focused scenario choice, and automation-minded evidence capture. Use for UI validation, exploratory QA, and browser regressions.
---

# Browser QA Playbook

Validate what a user would actually experience.

## Workflow
1. Confirm auth, environment, and route assumptions.
2. Check one main business path first.
3. Check one failure or edge path if it is meaningful.
4. Capture exact repro details:
   - route
   - selectors used
   - visible errors
   - data or state dependencies
5. Mark strong automation candidates and selector debt.

## Output expectations
- validated path
- failure path evidence
- automation candidates
- residual browser risks
