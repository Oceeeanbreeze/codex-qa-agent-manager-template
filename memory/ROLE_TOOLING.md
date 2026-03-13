# Role Tooling

## Global memory process
- Before substantial work, run preflight retrieval for the active roles.
- After substantive work, archive the interaction and reindex only the needed memories.
- Preserve exact wording when the user explicitly asks to remember something.

## Archivist
Memory profile:
- `archivist`
Tools:
- `search_memory.py --agent archivist`
- `preflight_memory.py`
- `finalize_task.py`
- `archive_interaction.py`
Process:
- search existing durable notes first
- archive the conversation and exact remembered statements
- enforce note structure and metadata

## Router
Memory profile:
- `router`
Tools:
- `search_memory.py --agent router`
- `preflight_memory.py`
Process:
- search similar prior tasks before choosing a route
- pull requirement and risk notes before assigning roles

## Researcher
Memory profile:
- `researcher`
Tools:
- `search_memory.py --agent researcher`
- `preflight_memory.py`
Process:
- retrieve related investigations, prior bugs, and architectural context
- feed exact file and decision notes into handoff

## Architect
Memory profile:
- `architect`
Tools:
- `search_memory.py --agent architect`
- `preflight_memory.py`
Process:
- look up past tradeoffs and invariants before proposing structure
- create new decision notes for important changes

## Implementer
Memory profile:
- `implementer`
Tools:
- `search_memory.py --agent implementer`
- `preflight_memory.py`
Process:
- search for seams, selectors, and reusable implementation patterns
- write back concise implementation notes when a new pattern emerges

## Reviewer
Memory profile:
- `reviewer`
Tools:
- `search_memory.py --agent reviewer`
- `preflight_memory.py`
Process:
- search for similar failures, edge cases, and prior regressions
- compare current change against known failure patterns

## Tester
Memory profile:
- `tester`
Tools:
- `search_memory.py --agent tester`
- `preflight_memory.py`
Process:
- retrieve checklists and prior repro steps before validation
- store new repro steps and observed risks for later reuse

## Test Strategist
Memory profile:
- `test-strategist`
Tools:
- `search_memory.py --agent test-strategist`
- `preflight_memory.py`
Process:
- search what already exists before proposing new coverage
- record why behavior belongs to unit, integration, API, or browser layers

## Test Automation Engineer
Memory profile:
- `test-automation-engineer`
Tools:
- `search_memory.py --agent test-automation-engineer`
- `preflight_memory.py`
Process:
- search for existing helpers, fixtures, and stable selectors
- write back patterns that reduce flakiness or setup cost

## QA Browser
Memory profile:
- `qa-browser`
Tools:
- `search_memory.py --agent qa-browser`
- `preflight_memory.py`
- browser tools or Playwright
Process:
- retrieve prior flow notes before exploratory QA
- save reproducible browser findings into markdown for future retrieval
