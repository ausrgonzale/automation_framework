# Installation Guide - E2E Tests

Complete setup guide for the E2E test suite.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Django application running on localhost:8000
- Internet connection (for initial Playwright installation)

## Step-by-Step Installation

### Step 1: Install Python Dependencies

#### Option A: Install all E2E dependencies
```bash
pip install -r tests/e2e/requirements.txt
```

#### Option B: Install minimal dependencies
```bash
pip install pytest playwright pytest-playwright
```

#### Option C: Add to existing requirements.txt
Add these lines to your project's `requirements.txt`:
```txt
pytest>=7.4.0
playwright>=1.40.0
pytest-playwright>=0.4.3
```

Then install:
```bash
pip install -r requirements.txt
```

### Step 2: Install Playwright Browsers

**Required** - Install browser binaries:
```bash
# Install Chromium (recommended for testing)
playwright install chromium

# Or install all browsers (larger download)
playwright install
```

### Step 3: Verify Installation

```bash
# Check pytest is installed
pytest --version

# Check playwright is installed
playwright --version

# Should see something like:
# pytest 7.4.0
# Version 1.40.0
```

### Step 4: Verify Django Setup

Make sure your Django app has:

1. **Registration view** at `/users/register/`
2. **Registration form** with fields:
   - `username`
   - `password1`
   - `password2`
3. **Django running** on localhost:8000

Start Django:
```bash
python manage.py runserver
```

Verify in browser:
```
http://localhost:8000/users/register/
```

### Step 5: Run First Test

```bash
# Run all registration tests
pytest tests/e2e/test_user_registration.py -v

# Or run in headed mode to see it work
pytest tests/e2e/test_user_registration.py --headed -v
```

## Troubleshooting Installation

### Issue: "pytest: command not found"
**Solution:**
```bash
# Ensure pytest is installed
pip install pytest

# Or if using Python 3 specifically
pip3 install pytest

# Verify
pytest --version
```

### Issue: "playwright: command not found"
**Solution:**
```bash
# Install playwright
pip install playwright

# Then install browsers
playwright install chromium
```

### Issue: "Executable doesn't exist" when running tests
**Solution:**
```bash
# Install Playwright browsers
playwright install chromium

# If that fails, try
python -m playwright install chromium
```

### Issue: Permission denied for run_tests.sh
**Solution:**
```bash
# Make script executable (Linux/Mac)
chmod +x tests/e2e/run_tests.sh

# Then run
./tests/e2e/run_tests.sh -r
```

### Issue: ModuleNotFoundError: No module named 'playwright'
**Solution:**
```bash
# Ensure playwright is installed in the active environment
pip install playwright pytest-playwright

# Check which Python you're using
which python
which pytest

# They should be in the same environment
```

### Issue: Tests fail with "Connection refused"
**Solution:**
```bash
# Start Django server in a separate terminal
python manage.py runserver

# Verify it's running
curl http://localhost:8000
```

## Platform-Specific Instructions

### Linux

```bash
# Install dependencies
pip install -r tests/e2e/requirements.txt

# Install Playwright browsers
playwright install chromium

# May need to install system dependencies
playwright install-deps

# Make test runner executable
chmod +x tests/e2e/run_tests.sh

# Run tests
./tests/e2e/run_tests.sh -r -v
```

### macOS

```bash
# Install dependencies
pip3 install -r tests/e2e/requirements.txt

# Install Playwright browsers
playwright install chromium

# Make test runner executable
chmod +x tests/e2e/run_tests.sh

# Run tests
./tests/e2e/run_tests.sh -r -v
```

### Windows

```cmd
REM Install dependencies
pip install -r tests\e2e\requirements.txt

REM Install Playwright browsers
playwright install chromium

REM Run tests
pytest tests\e2e\test_user_registration.py -v

REM Or use batch script
tests\e2e\run_tests.bat -r -v
```

## Virtual Environment Setup (Recommended)

### Create Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Install in Virtual Environment

```bash
# Activate venv first, then:
pip install -r tests/e2e/requirements.txt
playwright install chromium
```

### Verify Virtual Environment

```bash
# Should show path in your project's venv
which python    # Linux/Mac
where python    # Windows

# Run tests
pytest tests/e2e/ -v
```

## Docker Setup (Optional)

If you want to run tests in Docker:

### Create Dockerfile

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-focal

WORKDIR /app

COPY requirements.txt .
COPY tests/e2e/requirements.txt tests/e2e/
RUN pip install -r requirements.txt
RUN pip install -r tests/e2e/requirements.txt

COPY . .

CMD ["pytest", "tests/e2e/", "-v"]
```

### Build and Run

```bash
# Build image
docker build -t django-e2e-tests .

# Run tests
docker run --network="host" django-e2e-tests
```

## CI/CD Setup

### GitHub Actions

Create `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r tests/e2e/requirements.txt
        playwright install chromium
        playwright install-deps
    
    - name: Start Django server
      run: |
        python manage.py migrate
        python manage.py runserver &
        sleep 5
    
    - name: Run E2E tests
      run: pytest tests/e2e/ -v
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: test-results/
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
e2e-tests:
  image: mcr.microsoft.com/playwright/python:v1.40.0-focal
  
  before_script:
    - pip install -r requirements.txt
    - pip install -r tests/e2e/requirements.txt
  
  script:
    - python manage.py migrate
    - python manage.py runserver &
    - sleep 5
    - pytest tests/e2e/ -v
  
  artifacts:
    when: always
    paths:
      - test-results/
```

## Verify Complete Setup

Run this checklist:

```bash
# 1. Check Python version
python --version
# Should be 3.8+

# 2. Check pytest
pytest --version
# Should show pytest 7.4.0+

# 3. Check playwright
playwright --version
# Should show Version 1.40.0+

# 4. Check Django is running
curl http://localhost:8000
# Should get response (not connection refused)

# 5. Run a simple test
pytest tests/e2e/test_user_registration.py::test_registration_page_accessibility -v
# Should PASS

# 6. Run all tests
pytest tests/e2e/test_user_registration.py -v
# Most should PASS
```

## Next Steps

After successful installation:

1. ✅ Read [QUICKSTART.md](QUICKSTART.md) for running tests
2. ✅ Read [README.md](README.md) for detailed documentation
3. ✅ Run tests in headed mode to see them in action
4. ✅ Customize tests for your specific Django app
5. ✅ Set up CI/CD integration

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting-installation) section above
2. Review [README.md](README.md) for detailed documentation
3. Check Playwright installation docs: https://playwright.dev/python/docs/intro
4. Check pytest docs: https://docs.pytest.org/

## Dependencies Summary

### Core (Required)
- `pytest` - Testing framework
- `playwright` - Browser automation
- `pytest-playwright` - Playwright integration with pytest

### Optional (Recommended)
- `pytest-html` - Generate HTML reports
- `pytest-xdist` - Run tests in parallel
- `pytest-timeout` - Timeout management
- `pytest-cov` - Code coverage

### System Requirements
- Python 3.8+
- ~300MB disk space for Chromium
- Internet connection for initial setup

---

**Installation Complete!** 🎉

Now run your first test:
```bash
pytest tests/e2e/test_user_registration.py --headed -v
```
