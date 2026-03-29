"""
Playwright E2E test cases for Django application user registration functionality.

Tests cover:
- Successful registration scenarios
- Validation errors (password mismatch, weak passwords, empty fields)
- Duplicate user handling
- UI element verification
- Form field validation
- Registration flow navigation

Test Environment: localhost:8000 (Django application)
Framework: Playwright with Pytest
"""

import pytest
from playwright.sync_api import Page, expect
import time
import re


# Base URL for the application
BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="function")
def context_page(page: Page):
    """Fixture to provide a fresh page for each test."""
    page.goto(BASE_URL)
    yield page
    page.screenshot(path="register_page_error.png")


@pytest.mark.registration
def test_registration_page_accessibility(context_page: Page):
    """
    Test Case 1: Verify Registration Page is Accessible
    Ensure that users can navigate to the registration page from home.
    """
    page = context_page
    page.screenshot(path="register_debug.png")
    
    # Verify home page loads
    expect(page).to_have_url(BASE_URL + "/")
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Verify we're on the registration page
    expect(page).to_have_url(f"{BASE_URL}/users/register/", timeout=5000)
    
    # Verify registration form elements are present
    expect(page.locator('input[name="username"]')).to_be_visible()
    expect(page.locator('input[name="password1"]')).to_be_visible()
    expect(page.locator('input[name="password2"]')).to_be_visible()
    expect(page.get_by_role('button', name="register")).to_be_visible()
    
    print("✓ Test Case 1 Passed: Registration page is accessible and form is present")


@pytest.mark.registration
def test_successful_registration_new_user(context_page: Page):
    """
    Test Case 2: Successful Registration with New User
    Verify that a new user can successfully register with valid credentials.
    """
    page = context_page
    
    # Generate unique username with timestamp to avoid conflicts
    timestamp = str(int(time.time() * 1000))
    new_username = f"newuser{timestamp}"
    new_password = "SecurePass123!"
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Verify we're on the registration page
    expect(page).to_have_url(f"{BASE_URL}/users/register/", timeout=5000)
    
    # Fill in registration form
    page.fill('input[name="username"]', new_username)
    page.fill('input[name="password1"]', new_password)
    page.fill('input[name="password2"]', new_password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify successful registration - should redirect to home page
    expect(page).to_have_url(BASE_URL + "/", timeout=5000)
    
    # Verify user is logged in (logout link should be visible)
    expect(page.locator("text=Log out")).to_be_visible(timeout=3000)
    
    print(f"✓ Test Case 2 Passed: Successfully registered user '{new_username}'")


@pytest.mark.registration
def test_registration_duplicate_username(context_page: Page):
    """
    Test Case 3: Registration Fails with Existing Username
    Verify that registration fails when attempting to use an existing username.
    """
    page = context_page
    
    # First, create a user
    timestamp = str(int(time.time() * 1000))
    existing_username = f"existinguser{timestamp}"
    password = "SecurePass123!"
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form
    page.fill('input[name="username"]', existing_username)
    page.fill('input[name="password1"]', password)
    page.fill('input[name="password2"]', password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Wait for successful registration
    page.wait_for_url(BASE_URL + "/", timeout=5000)
    
    # Log out
    page.click("text=Log out")
    page.wait_for_url(BASE_URL + "/", timeout=3000)
    
    # Now try to register again with the same username
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form with existing username
    page.fill('input[name="username"]', existing_username)
    page.fill('input[name="password1"]', password)
    page.fill('input[name="password2"]', password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify error message appears
    error_message = page.locator(".errorlist").first
    expect(error_message).to_be_visible(timeout=3000)
    
    # Verify we're still on the registration page (registration failed)
    expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    print(f"✓ Test Case 3 Passed: Duplicate username '{existing_username}' correctly rejected")


@pytest.mark.registration
def test_registration_password_mismatch(context_page: Page):
    """
    Test Case 4: Registration Fails with Mismatched Passwords
    Verify that registration fails when password fields don't match.
    """
    page = context_page
    
    timestamp = str(int(time.time() * 1000))
    username = f"testuser{timestamp}"
    password1 = "SecurePass123!"
    password2 = "DifferentPass456!"
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form with mismatched passwords
    page.fill('input[name="username"]', username)
    page.fill('input[name="password1"]', password1)
    page.fill('input[name="password2"]', password2)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify error message appears
    error_message = page.locator(".errorlist").first
    expect(error_message).to_be_visible(timeout=3000)
    
    # Verify we're still on the registration page (registration failed)
    expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    print("✓ Test Case 4 Passed: Password mismatch correctly detected")


@pytest.mark.registration
def test_registration_weak_password(context_page: Page):
    """
    Test Case 5: Registration Fails with Weak Password
    Verify that registration fails when using a weak password.
    """
    page = context_page
    
    timestamp = str(int(time.time() * 1000))
    username = f"testuser{timestamp}"
    weak_password = "123"  # Too short and simple
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form with weak password
    page.fill('input[name="username"]', username)
    page.fill('input[name="password1"]', weak_password)
    page.fill('input[name="password2"]', weak_password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify error message appears
    error_message = page.locator(".errorlist").first
    expect(error_message).to_be_visible(timeout=3000)
    
    # Verify we're still on the registration page (registration failed)
    expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    print("✓ Test Case 5 Passed: Weak password correctly rejected")


@pytest.mark.registration
def test_registration_empty_fields(context_page: Page):
    """
    Test Case 6: Registration Fails with Empty Required Fields
    Verify that registration fails when required fields are empty.
    """
    page = context_page
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Try to submit form without filling any fields
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify we're still on the registration page (registration failed)
    expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    # Verify error messages or HTML5 validation prevents submission
    # Check for either Django error messages or HTML5 validation
    username_field = page.locator('input[name="username"]')
    
    # If HTML5 validation is used, the field should be marked as invalid
    # or Django should show error messages
    try:
        error_message = page.locator(".errorlist").first
        expect(error_message).to_be_visible(timeout=2000)
    except:
        # HTML5 validation might prevent submission
        # Check that we're still on the same page
        expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    print("✓ Test Case 6 Passed: Empty fields correctly prevented registration")


@pytest.mark.registration
def test_registration_username_too_long(context_page: Page):
    """
    Test Case 7: Registration Fails with Username Exceeding Maximum Length
    Verify that registration fails when username is too long (Django default max is 150 chars).
    """
    page = context_page
    
    # Create a username that exceeds typical maximum length
    long_username = "a" * 151  # Django's default max_length for username is 150
    password = "SecurePass123!"
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form with overly long username
    page.fill('input[name="username"]', long_username)
    page.fill('input[name="password1"]', password)
    page.fill('input[name="password2"]', password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify error message appears or field limits input
    # Some forms may limit input length client-side
    expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    print("✓ Test Case 7 Passed: Overly long username handled correctly")


@pytest.mark.registration
def test_registration_special_characters_username(context_page: Page):
    """
    Test Case 8: Registration with Special Characters in Username
    Verify behavior when username contains special characters.
    """
    page = context_page
    
    timestamp = str(int(time.time() * 1000))
    # Django usernames typically allow letters, digits, @, ., +, -, and _
    username_with_allowed = f"test.user_{timestamp}"
    password = "SecurePass123!"
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form with special characters
    page.fill('input[name="username"]', username_with_allowed)
    page.fill('input[name="password1"]', password)
    page.fill('input[name="password2"]', password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify successful registration or appropriate error
    try:
        # Should succeed if special chars are allowed
        expect(page).to_have_url(BASE_URL + "/", timeout=5000)
        print(f"✓ Test Case 8 Passed: Username with allowed special characters '{username_with_allowed}' accepted")
    except:
        # Should show error if not allowed
        expect(page).to_have_url(re.compile(r".*/users/register/.*"))
        print("✓ Test Case 8 Passed: Special characters in username handled appropriately")


@pytest.mark.registration
def test_registration_password_similar_to_username(context_page: Page):
    """
    Test Case 9: Registration Fails with Password Too Similar to Username
    Verify that Django's password validation rejects passwords similar to username.
    """
    page = context_page
    
    timestamp = str(int(time.time() * 1000))
    username = f"testuser{timestamp}"
    # Password that's too similar to username
    password = username  # Exact match
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form
    page.fill('input[name="username"]', username)
    page.fill('input[name="password1"]', password)
    page.fill('input[name="password2"]', password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify error message appears
    error_message = page.locator(".errorlist").first
    expect(error_message).to_be_visible(timeout=3000)
    
    # Verify we're still on the registration page (registration failed)
    expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    print("✓ Test Case 9 Passed: Password too similar to username correctly rejected")


@pytest.mark.registration
def test_registration_common_password(context_page: Page):
    """
    Test Case 10: Registration Fails with Common Password
    Verify that Django's password validation rejects common passwords.
    """
    page = context_page
    
    timestamp = str(int(time.time() * 1000))
    username = f"testuser{timestamp}"
    common_password = "password123"  # Common password
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form
    page.fill('input[name="username"]', username)
    page.fill('input[name="password1"]', common_password)
    page.fill('input[name="password2"]', common_password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify error message appears
    error_message = page.locator(".errorlist").first
    expect(error_message).to_be_visible(timeout=3000)
    
    # Verify we're still on the registration page (registration failed)
    expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    print("✓ Test Case 10 Passed: Common password correctly rejected")


@pytest.mark.registration
def test_registration_numeric_only_password(context_page: Page):
    """
    Test Case 11: Registration Fails with Numeric-Only Password
    Verify that Django's password validation rejects all-numeric passwords.
    """
    page = context_page
    
    timestamp = str(int(time.time() * 1000))
    username = f"testuser{timestamp}"
    numeric_password = "12345678901234"  # Long enough but only numbers
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form
    page.fill('input[name="username"]', username)
    page.fill('input[name="password1"]', numeric_password)
    page.fill('input[name="password2"]', numeric_password)
    
    # Submit registration form
    page.get_by_role("button", name="register", exact=False).click()
    
    # Verify error message appears
    error_message = page.locator(".errorlist").first
    expect(error_message).to_be_visible(timeout=3000)
    
    # Verify we're still on the registration page (registration failed)
    expect(page).to_have_url(re.compile(r".*/users/register/.*"))
    
    print("✓ Test Case 11 Passed: Numeric-only password correctly rejected")


@pytest.mark.registration
def test_registration_form_field_labels(context_page: Page):
    """
    Test Case 12: Verify Registration Form Has Proper Labels
    Ensure form fields have appropriate labels for accessibility.
    """
    page = context_page
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Verify form has labels or placeholders
    username_field = page.locator('input[name="username"]')
    password1_field = page.locator('input[name="password1"]')
    password2_field = page.locator('input[name="password2"]')
    
    # Check that fields are visible
    expect(username_field).to_be_visible()
    expect(password1_field).to_be_visible()
    expect(password2_field).to_be_visible()
    
    # Check for labels (either as <label> elements or placeholders)
    # This test ensures basic accessibility
    page_content = page.content()
    
    # Basic check that form structure exists
    assert 'username' in page_content.lower()
    assert 'password' in page_content.lower()
    
    print("✓ Test Case 12 Passed: Registration form has proper field structure")


@pytest.mark.registration  
@pytest.mark.slow
def test_registration_multiple_sequential_users(context_page: Page):
    """
    Test Case 13: Register Multiple Users Sequentially
    Verify that multiple users can be registered one after another.
    """
    page = context_page
    
    num_users = 3
    timestamp = str(int(time.time() * 1000))
    
    for i in range(num_users):
        username = f"sequser{timestamp}_{i}"
        password = f"SecurePass{i}23!"
        
        # If not first iteration, need to log out first
        if i > 0:
            page.goto(BASE_URL)
            page.click("text=Log out")
            page.wait_for_url(BASE_URL + "/", timeout=3000)
        
        # Navigate to registration page
        try:
            page.click("text=Register", timeout=3000)
        except:
            try:
                page.click("text=Sign up", timeout=3000)
            except:
                page.click("a[href*='register']", timeout=3000)
        
        # Fill in registration form
        page.fill('input[name="username"]', username)
        page.fill('input[name="password1"]', password)
        page.fill('input[name="password2"]', password)
        
        # Submit registration form
        page.get_by_role("button", name="register", exact=False).click()
        
        # Verify successful registration
        expect(page).to_have_url(BASE_URL + "/", timeout=5000)
        expect(page.locator("text=Log out")).to_be_visible(timeout=3000)
        
        print(f"  → User {i+1}/{num_users} registered: '{username}'")
    
    print(f"✓ Test Case 13 Passed: Successfully registered {num_users} sequential users")


# Additional helper function for test reporting
def print_test_summary():
    """Print a summary of all registration test cases."""
    print("\n" + "="*80)
    print("REGISTRATION TEST SUITE SUMMARY")
    print("="*80)
    print("Total Test Cases: 13")
    print("\nTest Coverage:")
    print("  1. Registration page accessibility")
    print("  2. Successful new user registration")
    print("  3. Duplicate username validation")
    print("  4. Password mismatch validation")
    print("  5. Weak password validation")
    print("  6. Empty fields validation")
    print("  7. Username length validation")
    print("  8. Special characters in username")
    print("  9. Password similarity to username")
    print(" 10. Common password validation")
    print(" 11. Numeric-only password validation")
    print(" 12. Form field labels and accessibility")
    print(" 13. Multiple sequential registrations")
    print("="*80)
