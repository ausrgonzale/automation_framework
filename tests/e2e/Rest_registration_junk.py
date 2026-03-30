"""
Playwright test cases for Learning Logs Django application user registration functionality.
Tests cover successful registration, validation, and duplicate user handling.
"""

import pytest
from playwright.sync_api import Page, expect
import time


# Base URL for the application
BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="function")
def context_page(page: Page):
    """Fixture to provide a fresh page for each test."""
    page.goto(BASE_URL)
    yield page


def test_successful_registration_new_user(context_page: Page):
    """
    Test Case 1: Successful Registration with New User
    Verify that a new user can successfully register.
    """
    page = context_page
    
    # Generate unique username with timestamp to avoid conflicts
    timestamp = str(int(time.time()))
    new_username = f"newuser{timestamp}"
    new_password = "newpass123"
    
    # Navigate to registration page
    # Try common registration link texts
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
    page.click('button[type="submit"]')
    
    # Verify successful registration - should redirect to home page
    expect(page).to_have_url(BASE_URL + "/", timeout=5000)
    
    # Verify user is logged in
    expect(page.locator("text=Log out")).to_be_visible(timeout=3000)
    
    print(f"✓ Test Case 1 Passed: Successfully registered user '{new_username}'")


def test_registration_duplicate_user_fails(context_page: Page):
    """
    Test Case 2: Registration Fails with Existing User
    Verify that registration fails when trying to register with an existing username.
    This test should FAIL as 'testuser' already exists.
    """
    username = "testuser"   # already exists
    password = "SecurePass123!"

    page = context_page
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form with existing username
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password1"]', "testpass123")
    page.fill('input[name="password2"]', "testpass123")
    
    # Submit registration form
    page.click('button[type="submit"]')
    
    # Verify registration failed - should stay on registration page or show error
    expect(page).to_have_url(f"{BASE_URL}/users/register/", timeout=5000)
    
    # Check for error message indicating username already exists
    expect(page.locator("text=/already exists|already taken|username.*already/i")).to_be_visible(timeout=3000)
    
    print("✓ Test Case 2 Passed: Duplicate user registration correctly rejected")


def test_registration_password_mismatch(context_page: Page):
    """
    Test Case 3: Registration Fails with Password Mismatch
    Verify that registration fails when passwords don't match.
    """
    page = context_page
    
    # Generate unique username
    timestamp = str(int(time.time()))
    new_username = f"mismatchuser{timestamp}"
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form with mismatched passwords
    page.fill('input[name="username"]', new_username)
    page.fill('input[name="password1"]', "password123")
    page.fill('input[name="password2"]', "differentpass123")
    
    # Submit registration form
    page.click('button[type="submit"]')
    
    # Verify registration failed - should stay on registration page
    expect(page).to_have_url(f"{BASE_URL}/users/register/", timeout=5000)
    
    # Check for error message about password mismatch
    expect(page.locator("text=/password.*match|passwords.*same|identical/i")).to_be_visible(timeout=3000)
    
    print("✓ Test Case 3 Passed: Password mismatch validation working")


def test_registration_empty_fields(context_page: Page):
    """
    Test Case 4: Registration Fails with Empty Fields
    Verify that form validation prevents submission with empty fields.
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
    
    # Try to submit with empty fields
    page.click('button[type="submit"]')
    
    # Verify we're still on the registration page
    expect(page).to_have_url(f"{BASE_URL}/users/register/", timeout=5000)
    
    # Should show validation errors or stay on page
    # Check that we didn't get redirected (which would indicate success)
    assert page.url == f"{BASE_URL}/users/register/"
    
    print("✓ Test Case 4 Passed: Empty fields validation working")


def test_registration_weak_password(context_page: Page):
    """
    Test Case 5: Registration Fails with Weak Password
    Verify that password validation prevents weak passwords (if Django password validators are configured).
    """
    page = context_page
    
    # Generate unique username
    timestamp = str(int(time.time()))
    new_username = f"weakpassuser{timestamp}"
    
    # Navigate to registration page
    try:
        page.click("text=Register", timeout=3000)
    except:
        try:
            page.click("text=Sign up", timeout=3000)
        except:
            page.click("a[href*='register']", timeout=3000)
    
    # Fill in registration form with weak password
    page.fill('input[name="username"]', new_username)
    weak_password = "123"
    page.fill('input[name="password1"]', weak_password)
    page.fill('input[name="password2"]', weak_password)
    
    # Submit registration form
    page.click('button[type="submit"]')
    
    # Verify registration failed - should stay on registration page or show error
    # Django's default password validators should reject this
    expect(page).to_have_url(f"{BASE_URL}/users/register/", timeout=5000)
    
    print("✓ Test Case 5 Passed: Weak password validation working")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
