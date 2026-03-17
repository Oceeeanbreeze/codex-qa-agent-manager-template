# HTML Lab Analysis

Use this reference when the input is a set of local HTML pages, course labs, or exported browser pages.

## Goal
Convert static browser artifacts into reusable QA outputs without inventing missing runtime behavior.

## Intake checklist
- Identify the entry HTML file.
- Identify whether linked assets are local, missing, or remote.
- Note whether the page is static content, a mockup, or an interactive artifact with scripts.
- Record the language used in visible UI text.

## Structure extraction
Capture only what can be observed:
- page title and main sections
- navigation menu, breadcrumbs, and outbound links
- cards, tables, accordions, tabs, dialogs, and banners
- forms, fields, defaults, placeholders, hints, and visible validation text
- buttons, links, toggles, and other interactive controls

## Scenario derivation
Derive scenarios from user goals and interaction surfaces:
- entry and navigation scenarios
- content discovery scenarios
- form completion and validation scenarios
- cancel, reset, back, and close scenarios
- empty-state, error-state, and unavailable-path scenarios when visible

Keep scenarios atomic. If one scenario bundles multiple goals, split it.

## Test case output
When producing manual test cases for Smart Monitor style work, use the working regulation from main QA:
- Russian human-readable content
- one goal per case
- one user action per step
- observable expected result
- `steps_table`
- explicit automation block

## Automation strategy
Recommend automation only when the artifact provides enough stability:
- `ui-e2e` for route, visibility, form, and navigation behavior that is user-visible
- `integration` or `api` only if the artifact is paired with known request contracts elsewhere
- keep purely presentational or content-only checks lightweight

## Safe assumptions policy
Mark as assumptions instead of facts when the HTML does not prove:
- server-side persistence
- authorization or role gates
- async backend success or failure
- database state
- cross-page saved state after reload

## Useful output shape
Prefer this sequence:
1. Page map
2. Key scenarios
3. Manual test case candidates
4. Automation strategy
5. Draft autotest candidates when selectors and flow are stable
