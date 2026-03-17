---
name: agent-browser
description: Navigate web pages and local HTML artifacts, inspect and parse HTML, follow links, extract structured data, and turn browser evidence into QA assets. Use when Codex needs to analyze page structure, derive scenarios, prepare manual test cases, plan automation, or generate browser-facing tests from real pages.
---

# Agent Browser

Analyze browser-facing artifacts in a way that stays reusable for QA and automation.

## Favor
- browser navigation when user flows matter
- HTML and DOM inspection when structure matters
- structured extraction when the output will become scenarios, cases, or tests
- explicit assumptions when a static page does not prove runtime behavior

## Workflow
1. Open the page or local HTML entry point.
2. Record the visible structure: navigation, sections, forms, tables, calls to action, and repeated UI patterns.
3. Follow meaningful links and map the reachable flow, but stop when the path becomes repetitive.
4. Extract structured data for later reuse:
   - page inventory
   - routes or reachable links
   - interactive elements
   - form fields and validation cues
   - tables, cards, tabs, dialogs, and status messages
5. Separate confirmed behavior from assumptions. If HTML alone cannot prove backend logic, auth, persistence, or data rules, mark that explicitly.
6. Turn the extracted structure into QA outputs:
   - key user scenarios
   - atomic manual test cases
   - automation candidates
   - browser or Playwright checks

## Output expectations
When using this skill, prefer producing:
- a short page map
- a list of key scenarios with goal and risk
- a list of reusable selectors or stable DOM anchors when visible
- a clear automation recommendation per scenario

## For HTML lab intake
When the user uploads static HTML pages such as course labs:
- read [references/html-lab-analysis.md](references/html-lab-analysis.md)
- treat the pages as the source of truth for UI structure
- do not invent dynamic behavior that is not evidenced by the artifact
- mark anything backend-dependent as `assumption` or `requires clarification`

## Pair well with
- `browser-qa-playbook` for exploratory user-flow validation
- `playwright-e2e-builder` when scenarios should become browser automation
- `risk-based-test-checklists` when extracting regression-focused checks
