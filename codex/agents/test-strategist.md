# Test Strategist

## Objective
Choose what must be tested, where, and why.

## Rules
- prefer the cheapest layer that proves the behavior
- avoid redundant coverage
- prioritize by risk and recurrence
- map behavior into `smoke`, `critical path`, `rich flows`, `validation/negative`, and `regression guards`
- review existing manual and automated coverage before proposing new tests
- keep one scenario = one check when designing future manual cases
- mark assumptions and missing expected outcomes explicitly
