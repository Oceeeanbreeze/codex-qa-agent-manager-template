# Tester Onboarding One Pager

## Goal
Help a tester become productive with the QA agent system in the shortest safe path.

## Read first
1. `AGENTS.md`
2. `codex/WORKFLOW.md`
3. `docs/FIRST_HOUR_RUNBOOK.md`
4. `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md`
5. `docs/PLAYWRIGHT_SMART_MONITOR_STANDARDS.md`

## What this system is for
- feature analysis
- risk extraction
- manual testcase drafting
- coverage gap review
- Playwright automation design and authoring
- browser-driven validation
- regression-focused review

## Daily operator flow
1. Start from the smallest clear goal.
2. Run memory preflight before substantial work.
3. Review existing manual cases and autotests before creating new coverage.
4. Keep one testcase atomic and one automated check focused.
5. Separate product defects from stand or environment blockers.
6. Save a checkpoint at milestones or after longer sessions.

## Rules that matter most
- one testcase = one goal = one check
- one step = one user action
- expected result must be observable
- use the lightest sufficient test layer
- prefer stable selectors and explicit waits
- do not archive secrets, `.env` data, cookies, or raw sensitive artifacts

## If the system looks broken
1. Open `docs/HEALTH_AND_DOCTOR.md`
2. Run `doctor`
3. Run `health`
4. If Python is blocked by the current host, switch to the validated unsandboxed operator shell

## When to escalate to QA lead or architect
- expected behavior is unclear
- the test layer choice changes cost or risk materially
- the module needs new hooks or testability work
- the same blocker repeats without new evidence
