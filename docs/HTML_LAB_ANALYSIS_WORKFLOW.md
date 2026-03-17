# HTML Lab Analysis Workflow

## Purpose
Prepare the workspace for a flow where the user uploads local HTML pages and expects QA-ready outputs.

## Intended use
Use this workflow for course labs, exported pages, static UI prototypes, or browser artifacts that should be converted into:
- page structure analysis
- key scenarios
- manual test cases
- automation strategy
- draft browser autotests when feasible

## Role chain
1. `researcher`
2. `qa-browser`
3. `test-strategist`
4. `test-automation-engineer` when automation should be drafted
5. `reviewer`
6. `tester`

## Skill chain
- `agent-browser` for page reading, link traversal, HTML parsing, and structured extraction
- `browser-qa-playbook` for user-flow validation
- `risk-based-test-checklists` for scenario prioritization
- `playwright-e2e-builder` if browser automation is justified

## Standard output contract
For each HTML intake, produce:
1. A page map:
   - entry page
   - reachable links
   - main sections
   - interactive elements
2. A scenario list:
   - goal
   - risk
   - dependencies or assumptions
3. Test case proposals:
   - one goal per case
   - observable expected results
   - automation mapping
4. Automation strategy:
   - what belongs to browser automation
   - what should stay manual
   - what still needs clarification
5. Draft autotests if the flow is deterministic enough

## Constraints
- Treat uploaded HTML as the source of truth for structure, not for hidden backend logic.
- Mark unsupported claims as assumptions or clarification requests.
- Avoid generating giant all-in-one scenarios.
- Prefer reusable page structure notes over one-off prose summaries.

## Smart Monitor alignment
If the HTML pages are later mapped into Smart Monitor-style manual cases, use the established regulation from main QA:
- review existing cases and autotests first
- keep one goal per test case
- store step blocks as `steps_table`
- write human-readable values in Russian
- keep expected results directly observable
