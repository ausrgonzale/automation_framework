# Issue: PytestCollectionWarning for Non-Test Classes Named with Test* Prefix

## Problem

Pytest attempts to collect any class whose name starts with `Test` as a test class. If such a class is not an actual test (e.g., a Pydantic model or service class with a custom `__init__`), pytest emits a `PytestCollectionWarning` like:

    PytestCollectionWarning: cannot collect test class 'TestcaseGenerationRequest' because it has a __init__ constructor

This can cause confusion and unnecessary warnings during test runs.

## Solution

Suppress pytest collection for these non-test classes by adding the following line inside each affected class:

```python
__test__ = False
```

## Work Performed

- Added `__test__ = False` to the following classes:
  - `TestcaseGenerationService` (services/testcase_generation_service.py)
  - `TestcaseGenerationRequest` (ai/schemas/testcase_generation_request.py)
  - `TestCase` (ai/schemas/testcase.py)
  - `TestCaseSet` (ai/schemas/testcase.py)
  - `TestcaseRepository` (repositories/testcase_repository.py)

## Regression Risk

- Minimal: This change only affects pytest’s test collection and does not impact runtime behavior or class usage.
- No code outside of these class definitions is affected.


## Recommendation (Updated Naming Convention)

- For all future non-test classes, use the `Check*` prefix instead of `Test*` to avoid confusion and prevent pytest from collecting non-test classes as tests.
- Begin refactoring existing non-test classes to use the `Check*` prefix (e.g., `CheckcaseGenerationRequest`, `CheckCase`, `CheckCaseSet`, `CheckcaseRepository`, `CheckcaseGenerationService`).
- Only use the `Test*` prefix for actual test classes intended for pytest discovery.
- If renaming is not immediately possible, continue to add `__test__ = False` to non-test classes with the `Test*` prefix to suppress warnings.

**Team Standard:**
> The `Check*` prefix is the official convention for non-test classes in this codebase. The `Test*` prefix is reserved for actual test cases only.
