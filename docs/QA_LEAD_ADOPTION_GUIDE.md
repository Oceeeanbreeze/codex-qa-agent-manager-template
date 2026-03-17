# QA Lead Adoption Guide

## Goal
Help a QA lead adopt the agent system as a controlled quality multiplier instead of an uncontrolled content generator.

## Where the system adds value
- faster feature decomposition
- consistent atomic testcase drafting
- coverage gap audits
- Playwright design and review support
- browser-assisted validation with clearer evidence capture

## Governance model
- keep one human owner per workstream
- require findings-first review for behavior-changing work
- require a named blocker for environment issues
- require durable checkpoints for long-running tasks
- keep production disabled by default

## Recommended team guardrails
- review the route choice for new work types
- keep a canonical testcase regulation
- keep Playwright standards explicit and versioned
- evaluate routing, retrieval, review quality, and coverage decisions separately
- prefer small golden datasets over broad subjective scoring

## Suggested adoption path
1. Start with feature analysis and testcase drafting.
2. Add coverage audit and review support.
3. Add automation design and selected Playwright authoring.
4. Add browser-driven validation where evidence quality matters.
5. Expand only after runtime and memory gates stay healthy.

## Signals to monitor
- repeated route confusion
- noisy retrieval
- testcase duplication
- flaky automation output
- browser validation findings that never feed back into standards

## Decision rule
Treat the system as mature only when it improves speed without reducing evidence quality, review quality, or operational safety.
