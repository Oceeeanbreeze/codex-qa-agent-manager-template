# Playwright Smart Monitor Standards

## Goal
Use the proven Smart Monitor Playwright patterns and the current developer review requirements when creating or updating browser automation.

These standards are intentionally opinionated. They combine:
- working patterns from the existing Smart Monitor Playwright approach;
- developer comments from the current handoff;
- the review checklist expected before merge.

## Core architecture standards
- Start from one authenticated admin session and reuse it where the suite design allows it.
- Do not repeat full login inside every test body if the suite can safely share authenticated state.
- Prefer serial suites when tests intentionally share one mutable page or one prepared entity.
- Use a singleton-like page pattern only when it is explicit and justified:
  - open the target page in `beforeAll`;
  - store it in a `let page: Page`;
  - reuse that page in tests instead of fixture `page`.
- Keep tests independent in behavior and cleanup expectations even when the suite shares setup.
- Account for running under three browsers. Do not assume chromium-only timing or behavior.

## Configuration standards
- Prefer `testIdAttribute: 'data-test-subj'` in Playwright config.
- Keep `baseURL` in environment variables, not hardcoded in specs.
- Fail fast if required environment variables are missing.
- Reuse auth/session setup instead of relogging in every test.
- Enable code coverage when the task requires it and report how it was enabled.

## Naming and metadata standards
- Include the manual case number `SMTEST` in the suite title or test title.
- Prefix created mutable entities with `AT`.
- Add tags for priority, depth, and other required markers from the case.
- Keep suite and test names explicit and business-readable.

## Selector standards
- Prefer `page.getByTestId(...)` first.
- Do not use Russian text locators by heading or visible label as the main stable selector when a test id can exist.
- Prefer stable semantic selectors over CSS shape selectors.
- Use CSS selectors only as a temporary fallback when the product still has selector debt.
- If a stable selector does not exist, note that as selector debt.

Priority order:
1. `getByTestId`
2. `getByRole`
3. `getByLabel` or `getByPlaceholder`
4. Narrow CSS locator as a temporary fallback

## Spec structure standards
- Use TypeScript and `@playwright/test`.
- Group tests with `test.describe(...)`.
- Use `test.describe.configure({ mode: 'serial' })` when tests share one created entity, one shared page, or one mutable browser state.
- Open shared pages in `beforeAll` only when serial mode is intentional.
- Prefer shared helpers and utils over local duplication.
- Use `test.step` for meaningful business phases.
- Add documentation comments only for critical non-obvious behavior.

Recommended suite shape:

```ts
import { type Page, expect, test } from '@playwright/test';

test.describe.configure({ mode: 'serial', timeout: 180000 });

test.describe('SMTEST-001 | Module > Feature', () => {
  let page: Page;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
  });

  test('AT user completes one observable business check', async () => {
    await test.step('Open target page', async () => {
      // open page through helper
    });

    await test.step('Perform action', async () => {
      // interact through stable test ids
    });

    await test.step('Verify result', async () => {
      // assert user-visible outcome
    });
  });
});
```

## Navigation and waiting standards
- Do not hardcode route prefixes that may change between stands.
- Use a helper that resolves the installation prefix and then opens the app path.
- Use assertions as waits.
- Avoid `waitForTimeout()`.
- Handle optional global loaders through a dedicated helper.
- Raise timeouts only for known slow editors, first-load screens, imports, and similarly justified places.

## Assertion standards
- Add clear assertions that prove user-visible behavior.
- Add `soft` assertions for secondary checks in the same scenario when a failure should not stop the primary path immediately.
- Add explicit error messages for important expectations where the failure reason should be obvious from the report.
- After each meaningful action, verify one observable result:
  - field became visible;
  - button became enabled or disabled;
  - toast appeared;
  - row appeared in a list;
  - modal opened or closed;
  - URL or filter state changed.

## Shared helper standards
Prefer extracting and reusing helpers for:
- auth/session reuse;
- installation-prefix-aware navigation;
- loader handling;
- fatal app error detection;
- Monaco editor input;
- commonly reused page actions.

## Review checklist
- Use correct selectors with maximum preference for `testId` and no dependence on localization.
- Avoid code duplication by using shared helpers and utils.
- Add clear assertions.
- Add `soft` assertions for secondary functionality.
- Add tags for priority, depth, and other required metadata.
- Prefix created entities with `AT`.
- Include `SMTEST` in the test or group name.
- Keep the test independent from other tests.
- Add documentation for critical implementation details.
- Add code coverage measurement when required.
- Add skip reasons.
- Add clear expect failure messages where useful.
- Use `test.step`.

## What to avoid
- repeated login flow in every test body without need;
- Russian text locators as the primary stable locator;
- missing shared helper extraction for repeated behavior;
- giant monolithic specs without steps;
- browser-specific assumptions that break on multi-browser runs;
- vague names like `should work`.
