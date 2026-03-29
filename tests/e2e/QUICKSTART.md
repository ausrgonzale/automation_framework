# Quick Start Guide - E2E Registration Tests

Get up and running with E2E tests in 5 minutes!

## 1. Prerequisites Check

```bash
# ✓ Python 3.8+ installed
python --version

# ✓ Django app code available
# ✓ Project dependencies installed
pip install -r requirements.txt

# ✓ Playwright installed
pip install playwright pytest-playwright
playwright install chromium
```

## 2. Start Django Application

```bash
# Terminal 1: Start Django server
python manage.py runserver

# You should see:
# Starting development server at http://127.0.0.1:8000/
```

## 3. Run the Tests

### Option A: Quick Run (Simple)
```bash
# From project root directory
pytest tests/e2e/test_user_registration.py -v
```

### Option B: Using Test Runner Script
```bash
# Linux/Mac
cd tests/e2e
chmod +x run_tests.sh
./run_tests.sh -r -v

# Windows
cd tests\e2e
run_tests.bat -r -v
```

### Option C: See It in Action (Headed Mode)
```bash
# Watch the browser perform the tests
pytest tests/e2e/test_user_registration.py --headed -v -s
```

## 4. Expected Output

You should see output like:
```
tests/e2e/test_user_registration.py::test_registration_page_accessibility PASSED
tests/e2e/test_user_registration.py::test_successful_registration_new_user PASSED
tests/e2e/test_user_registration.py::test_registration_duplicate_username PASSED
tests/e2e/test_user_registration.py::test_registration_password_mismatch PASSED
...
✓ Test Case 1 Passed: Registration page is accessible and form is present
✓ Test Case 2 Passed: Successfully registered user 'newuser1234567890'
...
==================== 14 passed in 45.23s ====================
```

## 5. Common Test Runs

```bash
# Run all registration tests
pytest tests/e2e/test_user_registration.py -v

# Run only fast tests (skip slow ones)
pytest tests/e2e/ -m "not slow" -v

# Run tests with detailed output
pytest tests/e2e/test_user_registration.py -v -s

# Run in slow motion for debugging
pytest tests/e2e/test_user_registration.py --headed --slowmo 1000 -v

# Run specific test
pytest tests/e2e/test_user_registration.py::test_successful_registration_new_user -v

# Run tests matching pattern
pytest tests/e2e/ -k "password" -v
```

## 6. Verify Test Results

✅ **All tests pass** - Registration functionality is working correctly!

❌ **Some tests fail** - Check:
1. Is Django running on localhost:8000?
2. Does the registration page URL match `/users/register/`?
3. Are the form field names correct (`username`, `password1`, `password2`)?
4. Are Django password validators configured correctly?

## 7. Next Steps

- Review test details in [README.md](README.md)
- Customize tests for your Django app's specific requirements
- Add tests for login functionality
- Set up CI/CD integration

## Test Coverage

The registration test suite covers:

| # | Test Case | What It Verifies |
|---|-----------|------------------|
| 1 | Page Accessibility | Registration page loads and form exists |
| 2 | Successful Registration | New user can register with valid data |
| 3 | Duplicate Username | System rejects existing usernames |
| 4 | Password Mismatch | Passwords must match |
| 5 | Empty Username | Username field is required |
| 6 | Empty Password | Password fields are required |
| 7 | Weak Password (Short) | Minimum password length enforced |
| 8 | Password Similar to Username | Password can't be too similar |
| 9 | Common Password | Common passwords are rejected |
| 10 | Numeric Password | All-numeric passwords rejected |
| 11 | Form Structure | Form has proper labels/structure |
| 12 | Post-Registration | User can navigate after registering |
| 13 | Multiple Registrations | System handles sequential registrations |
| 14 | Case Sensitivity | Username case handling |

## Troubleshooting

### "Connection refused" error
```bash
# Solution: Start Django server
python manage.py runserver
```

### "Executable doesn't exist" error
```bash
# Solution: Install Playwright browsers
playwright install chromium
```

### Tests fail immediately
```bash
# Solution: Check Django is on localhost:8000
curl http://localhost:8000

# If using different port, update BASE_URL in tests
```

### Can't see what's happening
```bash
# Solution: Run in headed mode
pytest tests/e2e/ --headed -v -s
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest tests/e2e/ -v` | Run all E2E tests |
| `pytest tests/e2e/ --headed` | Show browser |
| `pytest tests/e2e/ -v -s` | Show print statements |
| `pytest -m registration` | Run registration tests only |
| `pytest -k password` | Run tests matching "password" |
| `pytest --durations=10` | Show slowest tests |

## Need Help?

1. Check [README.md](README.md) for detailed documentation
2. Check [tests/README.md](../README.md) for project test overview
3. Review the test code for examples
4. Check Playwright docs: https://playwright.dev/python/

Happy Testing! 🚀
