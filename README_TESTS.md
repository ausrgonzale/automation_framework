# Learning Logs - Playwright Login Tests

This test suite contains 5 comprehensive Playwright test cases for testing the login functionality of the Learning Logs Django application.

## Test Cases Included

1. **test_successful_login**: Tests successful login with valid credentials
2. **test_invalid_username_login**: Tests login failure with an invalid username
3. **test_invalid_password_login**: Tests login failure with an incorrect password
4. **test_empty_fields_login**: Tests form validation with empty fields
5. **test_successful_login_and_logout**: Tests the complete login/logout flow

## Prerequisites

- Python 3.7 or higher
- Django application running on `http://localhost:8000`
- A test user account with credentials:
  - Username: `testuser`
  - Password: `testpass123`

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install
```

### 3. Create Test User in Django

Before running tests, create a test user in your Django application:

```bash
# In your Django project directory
python manage.py shell
```

Then in the Python shell:

```python
from django.contrib.auth.models import User
User.objects.create_user('testuser', 'test@example.com', 'testpass123')
exit()
```

## Running the Tests

### Run All Tests

```bash
pytest test_login.py -v
```

### Run a Specific Test

```bash
pytest test_login.py::test_successful_login -v
```

### Run Tests with Browser Visible (Headed Mode)

```bash
pytest test_login.py -v --headed
```

### Run Tests with Slower Execution (for debugging)

```bash
pytest test_login.py -v --headed --slowmo 1000
```

### Run Tests in Different Browsers

```bash
# Chrome/Chromium (default)
pytest test_login.py -v --browser chromium

# Firefox
pytest test_login.py -v --browser firefox

# WebKit (Safari)
pytest test_login.py -v --browser webkit
```

### Generate HTML Report

```bash
pytest test_login.py -v --html=report.html --self-contained-html
```

## Test Coverage

The test suite covers:

- ✅ Successful authentication with valid credentials
- ✅ Failed authentication with invalid username
- ✅ Failed authentication with invalid password
- ✅ Form validation for empty fields
- ✅ Complete login and logout workflow
- ✅ URL redirections after login/logout
- ✅ Visibility of UI elements based on authentication state

## Customization

### Changing Credentials

If you want to use different test credentials, update the username and password in `test_login.py`:

```python
page.fill('input[name="username"]', "your_username")
page.fill('input[name="password"]', "your_password")
```

### Changing Base URL

If your application runs on a different URL, update the `BASE_URL` constant in `test_login.py`:

```python
BASE_URL = "http://your-url:port"
```

### Adjusting Selectors

If your Django template uses different HTML structure, you may need to adjust the selectors in the test file. Common selectors to check:

- Login link: `text=Log in`
- Logout link: `text=Log out`
- Username input: `input[name="username"]`
- Password input: `input[name="password"]`
- Submit button: `button[type="submit"]`

## Troubleshooting

### Django Server Not Running

Make sure your Django development server is running:

```bash
python manage.py runserver
```

### Element Not Found Errors

- Check that your Django templates have the expected text and element names
- Use `--headed` and `--slowmo` flags to see what's happening
- Verify the selectors match your HTML structure

### Timeout Errors

- Increase timeout in test file if your server is slow
- Ensure the Django server is responding at `http://localhost:8000`

### Test User Doesn't Exist

Create the test user as shown in the setup instructions above.

## CI/CD Integration

These tests can be easily integrated into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    playwright install --with-deps

- name: Run Django server
  run: python manage.py runserver &
  
- name: Run tests
  run: pytest test_login.py -v
```

## Additional Resources

- [Playwright Python Documentation](https://playwright.dev/python/docs/intro)
- [pytest Documentation](https://docs.pytest.org/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
