# E2E Tests for Django Application

This directory contains End-to-End (E2E) tests for the Django application running on `localhost:8000` using Playwright.

## Test Files

### `test_user_registration.py`
Comprehensive test suite for user registration functionality covering:
- ✅ Registration page accessibility
- ✅ Successful user registration
- ✅ Duplicate username validation
- ✅ Password mismatch validation
- ✅ Empty field validation
- ✅ Weak password validation
- ✅ Password similarity to username validation
- ✅ Common password validation
- ✅ Numeric-only password validation
- ✅ Form field structure verification
- ✅ Post-registration navigation
- ✅ Sequential multiple user registration
- ✅ Username case sensitivity

## Prerequisites

1. **Django Application Running**
   ```bash
   # Make sure your Django app is running on localhost:8000
   python manage.py runserver
   ```

2. **Python Dependencies**
   ```bash
   pip install pytest playwright pytest-playwright
   ```

3. **Playwright Browsers**
   ```bash
   playwright install chromium
   ```

## Running the Tests

### Run All E2E Tests
```bash
# From project root
pytest tests/e2e/

# With verbose output
pytest tests/e2e/ -v

# With detailed output including print statements
pytest tests/e2e/ -v -s
```

### Run Only Registration Tests
```bash
pytest tests/e2e/test_user_registration.py -v

# Or using marker
pytest -m registration -v
```

### Run Specific Test Cases
```bash
# Run a single test
pytest tests/e2e/test_user_registration.py::test_successful_registration_new_user -v

# Run tests matching a pattern
pytest tests/e2e/ -k "password" -v
```

### Run Tests in Headed Mode (See Browser)
```bash
pytest tests/e2e/ --headed -v
```

### Run Tests in Slow Motion (For Debugging)
```bash
pytest tests/e2e/ --headed --slowmo 500 -v
```

### Skip Slow Tests
```bash
pytest tests/e2e/ -m "not slow" -v
```

### Run Only Fast Tests
```bash
pytest tests/e2e/ -m "fast" -v
```

## Test Markers

Tests are organized with markers for easy filtering:

- `@pytest.mark.registration` - User registration tests
- `@pytest.mark.login` - Login functionality tests
- `@pytest.mark.auth` - Tests requiring authentication
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.fast` - Quick-running tests
- `@pytest.mark.e2e` - End-to-end tests

### Using Markers
```bash
# Run only registration tests
pytest -m registration

# Run all except slow tests
pytest -m "not slow"

# Run registration tests that are fast
pytest -m "registration and fast"
```

## Test Structure

### Fixtures (in conftest.py)
- `base_url` - Provides BASE_URL for tests
- `navigate_to_register` - Helper to navigate to registration page
- `navigate_to_login` - Helper to navigate to login page
- `unique_username` - Generates unique usernames
- `secure_password` - Provides a secure password
- `register_user` - Function to register a user
- `logout_user` - Function to logout current user

### Using Fixtures in Tests
```python
def test_example(page: Page, navigate_to_register, unique_username, secure_password):
    # navigate_to_register already navigates to the page
    page.fill('input[name="username"]', unique_username)
    page.fill('input[name="password1"]', secure_password)
    page.fill('input[name="password2"]', secure_password)
    page.click('button[type="submit"]')
```

## Configuration

Test configuration is managed in:
- `pytest.ini` (root directory) - Global pytest configuration
- `tests/e2e/conftest.py` - E2E-specific fixtures
- `conftest.py` (root) - Shared fixtures across all tests

## Debugging Failed Tests

### 1. Run in Headed Mode
```bash
pytest tests/e2e/test_user_registration.py::test_name --headed -v -s
```

### 2. Add Breakpoints
```python
def test_example(page: Page):
    page.goto("http://localhost:8000")
    page.pause()  # This will pause execution and open Playwright Inspector
```

### 3. Take Screenshots on Failure
Add to your test:
```python
try:
    # test code
except Exception as e:
    page.screenshot(path="failure.png")
    raise
```

### 4. Check Test Durations
```bash
pytest tests/e2e/ --durations=10
```

## Common Issues

### Issue: Connection Refused
**Solution**: Make sure Django development server is running:
```bash
python manage.py runserver
```

### Issue: Element Not Found
**Solution**: 
- Run in headed mode to see what's happening
- Check if selectors match your Django templates
- Increase timeout values if needed

### Issue: Tests Are Slow
**Solution**:
- Run in headless mode (default)
- Skip slow tests with `-m "not slow"`
- Enable parallel execution with `pytest-xdist`:
  ```bash
  pip install pytest-xdist
  pytest tests/e2e/ -n auto
  ```

## Best Practices

1. **Use Unique Usernames**: Always generate unique usernames using timestamps to avoid conflicts
2. **Cleanup After Tests**: Tests should be independent and not rely on previous test state
3. **Use Fixtures**: Leverage fixtures for common setup tasks
4. **Mark Tests Appropriately**: Use markers to categorize tests
5. **Keep Tests Fast**: Mock external services, use database transactions when possible
6. **Explicit Waits**: Use Playwright's built-in waiting mechanisms instead of time.sleep()

## CI/CD Integration

To run tests in CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
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
  run: pytest tests/e2e/ -v --headed=false
```

## Writing New Tests

Template for new test:
```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.registration  # Add appropriate markers
def test_your_test_name(page: Page, unique_username, secure_password):
    """
    Test Case: Description of what you're testing
    """
    # Arrange: Setup test data and navigate
    page.goto("http://localhost:8000")
    
    # Act: Perform actions
    page.click("text=Register")
    page.fill('input[name="username"]', unique_username)
    
    # Assert: Verify results
    expect(page).to_have_url("http://localhost:8000/")
    
    print("✓ Test Passed: Description")
```

## Contributing

When adding new tests:
1. Follow existing naming conventions
2. Add appropriate markers
3. Include descriptive docstrings
4. Add print statements for success messages
5. Update this README if adding new test categories

## Support

For issues or questions:
- Check Playwright documentation: https://playwright.dev/python/
- Check pytest documentation: https://docs.pytest.org/
- Review existing tests for examples
