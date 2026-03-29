"""
Playwright test cases for Learning Logs Django application login functionality.
Tests cover various login scenarios including successful login, invalid credentials,
empty fields, logout, and navigation.

OPTIMIZED VERSION: Uses shared fixtures and reduced timeouts for faster execution.
"""

import pytest
from playwright.sync_api import Page, expect


# Base URL for the application
BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="function")
def context_page(page: Page):
    """Fixture to provide a fresh page for each test."""
    page.goto(BASE_URL)
    yield page


@pytest.mark.login
def test_successful_login(context_page: Page):
    """
    Test Case 1: Successful Login
    Verify that a user can successfully log in with valid credentials.
    """
    page = context_page
    
    # Navigate to login page
    page.click("text=Log in")
    
    # Verify we're on the login page
    expect(page).to_have_url(f"{BASE_URL}/users/login/")
    expect(page.locator("h1, h2")).to_contain_text("Log in")
    
    # Fill in login credentials
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testpass123")
    
    # Click login button
    page.click('button[type="submit"]')
    
    # Verify successful login - should redirect to home page
    expect(page).to_have_url(BASE_URL + "/")
    
    # Verify user is logged in
    expect(page.locator("text=Log out")).to_be_visible()
    
    print("✓ Test Case 1 Passed: Successful login")


@pytest.mark.login
def test_invalid_username_login(context_page: Page):
    """
    Test Case 2: Login with Invalid Username
    Verify that login fails with an invalid username.
    """
    page = context_page
    
    # Navigate to login page
    page.click("text=Log in")
    
    # Fill in invalid credentials
    page.fill('input[name="username"]', "invaliduser123")
    page.fill('input[name="password"]', "somepassword")
    
    # Click login button
    page.click('button[type="submit"]')
    
    # Verify login failed - should stay on login page
    expect(page).to_have_url(f"{BASE_URL}/users/login/")
    
    # Check for error message
    expect(page.locator("text=/invalid|incorrect|error/i")).to_be_visible(timeout=3000)
    
    # Verify user is not logged in
    expect(page.locator("text=Log in")).to_be_visible()
    
    print("✓ Test Case 2 Passed: Invalid username handled correctly")


@pytest.mark.login
def test_invalid_password_login(context_page: Page):
    """
    Test Case 3: Login with Invalid Password
    Verify that login fails with a valid username but incorrect password.
    """
    page = context_page
    
    # Navigate to login page
    page.click("text=Log in")
    
    # Fill in valid username but wrong password
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "wrongpassword")
    
    # Click login button
    page.click('button[type="submit"]')
    
    # Verify login failed
    expect(page).to_have_url(f"{BASE_URL}/users/login/")
    
    # Check for error message
    expect(page.locator("text=/invalid|incorrect|error/i")).to_be_visible(timeout=3000)
    
    # Verify user is not logged in
    expect(page.locator("text=Log in")).to_be_visible()
    
    print("✓ Test Case 3 Passed: Invalid password handled correctly")


@pytest.mark.login
def test_empty_fields_login(context_page: Page):
    """
    Test Case 4: Login with Empty Fields
    Verify that form validation prevents submission with empty username/password.
    """
    page = context_page
    
    # Navigate to login page
    page.click("text=Log in")
    
    # Try to submit with empty fields
    page.click('button[type="submit"]')
    
    # Verify we're still on the login page
    expect(page).to_have_url(f"{BASE_URL}/users/login/")
    
    # Check that browser validation or server-side validation prevents login
    expect(page.locator("text=Log in")).to_be_visible()
    
    # Try with empty password only
    page.fill('input[name="username"]', "testuser")
    page.click('button[type="submit"]')
    
    # Should still be on login page or show error
    expect(page).to_have_url(f"{BASE_URL}/users/login/")
    
    print("✓ Test Case 4 Passed: Empty fields validation working")


@pytest.mark.login
@pytest.mark.auth
def test_successful_login_and_logout(context_page: Page):
    """
    Test Case 5: Successful Login and Logout Flow
    Verify that a user can log in and then successfully log out.
    """
    page = context_page
    
    # Navigate to login page
    page.click("text=Log in")
    
    # Login with valid credentials
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testpass123")
    page.click('button[type="submit"]')
    
    # Verify successful login
    expect(page).to_have_url(BASE_URL + "/")
    expect(page.locator("text=Log out")).to_be_visible()
    
    # Now logout
    page.click("text=Log out")
    
    # Verify successful logout - should redirect to home page
    expect(page).to_have_url(BASE_URL + "/")
    
    # Verify user is logged out
    expect(page.locator("text=Log in")).to_be_visible()
    expect(page.locator("text=Log out")).not_to_be_visible()
    
    print("✓ Test Case 5 Passed: Login and logout flow successful")


@pytest.mark.auth
def test_quick_login_with_helper(page: Page, quick_login):
    """
    Test Case 6: Using Quick Login Helper (Performance Test)
    Demonstrates the use of the quick_login helper fixture for faster test setup.
    """
    # Use the quick login helper
    quick_login(page)
    
    # Verify we're logged in
    expect(page.locator("text=Log out")).to_be_visible()
    
    print("✓ Test Case 6 Passed: Quick login helper working")


@pytest.mark.auth
def test_authenticated_fixture(authenticated_page: Page):
    """
    Test Case 7: Using Authenticated Page Fixture (Performance Test)
    Demonstrates the use of the authenticated_page fixture for tests that start authenticated.
    This is much faster than logging in manually in each test.
    """
    page = authenticated_page
    
    # Page is already authenticated, verify it
    expect(page.locator("text=Log out")).to_be_visible()
    
    # Can immediately test authenticated features
    print("✓ Test Case 7 Passed: Authenticated page fixture working")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
