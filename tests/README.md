# Tests Directory

This directory contains all automated tests for the project.

## Structure

```
tests/
├── e2e/                          # End-to-End tests (Playwright)
│   ├── __init__.py
│   ├── conftest.py              # E2E-specific fixtures
│   ├── test_user_registration.py # User registration tests
│   ├── run_tests.sh             # Test runner script (Linux/Mac)
│   ├── run_tests.bat            # Test runner script (Windows)
│   └── README.md                # E2E tests documentation
│
├── unit/                         # Unit tests (future)
├── integration/                  # Integration tests (future)
└── README.md                     # This file
```

## Test Categories

### E2E Tests (`tests/e2e/`)
End-to-end tests that test the entire application flow using a real browser (Playwright).
- **Purpose**: Verify complete user workflows
- **Framework**: Playwright + Pytest
- **Target**: Django application on localhost:8000
- **Documentation**: See [tests/e2e/README.md](e2e/README.md)

### Unit Tests (`tests/unit/`) - Coming Soon
Unit tests for individual functions and classes.
- **Purpose**: Test individual components in isolation
- **Framework**: Pytest
- **Coverage**: Functions, classes, utilities

### Integration Tests (`tests/integration/`) - Coming Soon
Tests that verify interaction between multiple components.
- **Purpose**: Test component integration
- **Framework**: Pytest
- **Coverage**: Database operations, API calls, service integrations

## Quick Start

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Start Django application
python manage.py runserver
```

### Running Tests

#### All E2E Tests
```bash
# Using pytest directly
pytest tests/e2e/ -v

# Using the test runner script (Linux/Mac)
cd tests/e2e && chmod +x run_tests.sh && ./run_tests.sh -a

# Using the test runner script (Windows)
cd tests\e2e && run_tests.bat -a
```

#### Specific Test Category
```bash
# Registration tests only
pytest tests/e2e/test_user_registration.py -v

# Using markers
pytest -m registration -v
```

#### With Visual Feedback
```bash
# Headed mode (see the browser)
pytest tests/e2e/ --headed -v

# Slow motion (for debugging)
pytest tests/e2e/ --headed --slowmo 500 -v
```

## Test Markers

Tests are organized using pytest markers for easy filtering:

| Marker | Description | Usage |
|--------|-------------|-------|
| `@pytest.mark.e2e` | End-to-end tests | `pytest -m e2e` |
| `@pytest.mark.registration` | User registration tests | `pytest -m registration` |
| `@pytest.mark.login` | Login functionality tests | `pytest -m login` |
| `@pytest.mark.auth` | Tests requiring authentication | `pytest -m auth` |
| `@pytest.mark.slow` | Tests that run slowly | `pytest -m "not slow"` to skip |
| `@pytest.mark.fast` | Quick-running tests | `pytest -m fast` |
| `@pytest.mark.smoke` | Critical functionality tests | `pytest -m smoke` |

## Configuration Files

- **`pytest.ini`** (root): Global pytest configuration
- **`conftest.py`** (root): Shared fixtures across all tests
- **`tests/e2e/conftest.py`**: E2E-specific fixtures

## Writing New Tests

### E2E Test Template
```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
@pytest.mark.registration
def test_example(page: Page, unique_username, secure_password):
    """
    Test Case: Brief description of what this test verifies
    """
    # Arrange: Setup
    page.goto("http://localhost:8000")
    
    # Act: Perform actions
    page.click("text=Register")
    page.fill('input[name="username"]', unique_username)
    
    # Assert: Verify
    expect(page).to_have_url("http://localhost:8000/")
    
    print("✓ Test Passed: Description")
```

### Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Tests should clean up after themselves
3. **Naming**: Use descriptive test names that explain what's being tested
4. **Markers**: Apply appropriate markers for test categorization
5. **Documentation**: Include docstrings explaining the test purpose
6. **Assertions**: Use clear, specific assertions
7. **Fixtures**: Leverage fixtures for common setup tasks

## CI/CD Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example: GitHub Actions
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Start Django server
        run: |
          python manage.py migrate
          python manage.py runserver &
          sleep 5
      
      - name: Run E2E tests
        run: pytest tests/e2e/ -v
```

## Test Reports

### Generate HTML Report
```bash
pip install pytest-html
pytest tests/e2e/ --html=report.html --self-contained-html
```

### Generate Coverage Report
```bash
pip install pytest-cov
pytest tests/e2e/ --cov=. --cov-report=html
```

### View Test Durations
```bash
pytest tests/e2e/ --durations=10
```

## Debugging Tests

### Run Specific Test
```bash
pytest tests/e2e/test_user_registration.py::test_successful_registration_new_user -v
```

### Use Playwright Inspector
```python
def test_example(page: Page):
    page.pause()  # Opens Playwright Inspector
```

### Screenshot on Failure
```python
import pytest

@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"failure-{request.node.name}.png")
```

## Troubleshooting

### Django Server Not Running
```
Error: Connection refused to localhost:8000
Solution: Start Django with `python manage.py runserver`
```

### Browser Not Found
```
Error: Executable doesn't exist
Solution: Run `playwright install chromium`
```

### Tests Are Slow
```
Solutions:
- Run in headless mode (default)
- Skip slow tests: pytest -m "not slow"
- Enable parallel execution: pytest -n auto (requires pytest-xdist)
```

### Element Not Found
```
Solutions:
- Run with --headed to see what's happening
- Increase timeout values
- Verify selectors match your HTML
- Check if page has loaded completely
```

## Contributing

When adding new tests:
1. Place tests in the appropriate directory (e2e, unit, integration)
2. Follow the existing naming conventions
3. Add appropriate pytest markers
4. Include comprehensive docstrings
5. Update relevant README files
6. Ensure tests are isolated and repeatable

## Resources

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [E2E Tests README](e2e/README.md)

## Support

For questions or issues:
1. Check the relevant README files
2. Review existing tests for examples
3. Check Playwright/Pytest documentation
4. Create an issue with detailed information
