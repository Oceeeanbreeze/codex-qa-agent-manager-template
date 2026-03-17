---
name: playwright-smart-monitor-writer
description: Write or refactor Smart Monitor Playwright tests using the established project standards. Use when Codex needs to create browser autotests for Smart Monitor flows, translate manual cases into Playwright, apply shared-auth and singleton-page patterns, enforce test id selectors, or satisfy the Smart Monitor code review checklist.
---

# Playwright Smart Monitor Writer

Use the local standards before writing code.

## Required reference
- Read [../../docs/PLAYWRIGHT_SMART_MONITOR_STANDARDS.md](../../docs/PLAYWRIGHT_SMART_MONITOR_STANDARDS.md) first.

## Workflow
1. Map the manual case goal to one observable Playwright scenario.
2. Choose whether the suite should reuse authenticated state and a shared page.
3. Prefer existing helpers for login, route opening, loader handling, and Monaco input.
4. Use `getByTestId` first and note selector debt if stable ids are missing.
5. Add `SMTEST` naming, `AT` test data prefixes, `test.step`, clear assertions, and secondary `soft` assertions where useful.
6. Check the result against the Smart Monitor review checklist before finishing.

## Output expectations
- one focused spec or spec update
- clear mapping to the manual case
- stable selectors
- minimal duplication
- notes about coverage, skip rationale, or selector debt when relevant
