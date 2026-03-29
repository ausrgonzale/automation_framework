"""
Pytest configuration file for Playwright tests.
This file contains shared fixtures and configuration for all test files.
Includes performance optimizations and authenticated user fixtures.
"""

import pytest
import time
from playwright.sync_api import Playwright, Browser, BrowserContext, Page, expect


# Base URL for the application
BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context arguments with performance optimizations.
    - Reduced viewport for faster rendering
    - Disabled animations
    - Faster navigation timeout
    """
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
        "ignore_https_errors": True,
        # Reduce default timeout for faster failure detection
        "default_timeout": 10000,  # 10 seconds instead of 30
    }


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    """
    Create browser instance with performance optimizations.
    Session-scoped to reuse browser across tests.
    """
    browser = playwright.chromium.launch(
        headless=False,  # Can be overridden with --headed flag
        slow_mo=0,  # No artificial slowdown (can be overridden with --slowmo)
        # Performance optimizations
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-setuid-sandbox',
        ]
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    Create a new browser context for each test.
    This ensures test isolation while reusing the browser.
    """
    context = browser.new_context()
    
    # Set faster default timeouts
    context.set_default_timeout(10000)  # 10 seconds
    context.set_default_navigation_timeout(10000)  # 10 seconds
    
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """
    Create a new page for each test with optimized settings.
    """
    page = context.new_page()
    
    # Reduce timeout for expect assertions
    expect.set_options(timeout=5000)  # 5 seconds for assertions
    
    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(context: BrowserContext):
    """
    Fixture that provides a page with an already authenticated user.
    This fixture logs in once and provides the authenticated page,
    significantly speeding up tests that require authentication.
    
    Uses the existing 'testuser' / 'testpass123' credentials.
    """
    page = context.new_page()
    expect.set_options(timeout=5000)
    
    # Navigate to login page
    page.goto(BASE_URL)
    page.click("text=Log in", timeout=3000)
    
    # Login with test credentials
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "testpass123")
    page.click('button[type="submit"]')
    
    # Wait for successful login
    expect(page).to_have_url(BASE_URL + "/", timeout=5000)
    expect(page.locator("text=Log out")).to_be_visible(timeout=3000)
    
    yield page
    page.close()


@pytest.fixture(scope="function")
def registered_user(context: BrowserContext):
    """
    Fixture that creates and returns a newly registered user.
    Returns a dictionary with username, password, and authenticated page.
    
    This is useful for tests that need a fresh user account.
    """
    page = context.new_page()
    expect.set_options(timeout=5000)
    
    # Generate unique username
    timestamp = str(int(time.time() * 1000))  # millisecond precision
    username = f"autouser{timestamp}"
    password = "autopass123"
    
    # Navigate to registration page
    page.goto(BASE_URL)
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
    
    # Submit registration
    page.click('button[type="submit"]')
    
    # Wait for successful registration
    expect(page).to_have_url(BASE_URL + "/", timeout=5000)
    
    user_data = {
        "username": username,
        "password": password,
        "page": page
    }
    
    yield user_data
    page.close()


@pytest.fixture(scope="function")
def quick_login():
    """
    Helper function for quick login in tests.
    Returns a function that can be called with a page object.
    """
    def login(page: Page, username: str = "testuser", password: str = "testpass123"):
        """Quick login helper function."""
        page.goto(BASE_URL)
        page.click("text=Log in", timeout=3000)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        expect(page).to_have_url(BASE_URL + "/", timeout=5000)
    
    return login


@pytest.fixture(scope="function")
def quick_register():
    """
    Helper function for quick registration in tests.
    Returns a function that can be called with a page object.
    """
    def register(page: Page, username: str = None, password: str = "testpass123"):
        """Quick registration helper function."""
        if username is None:
            timestamp = str(int(time.time() * 1000))
            username = f"user{timestamp}"
        
        page.goto(BASE_URL)
        try:
            page.click("text=Register", timeout=3000)
        except:
            try:
                page.click("text=Sign up", timeout=3000)
            except:
                page.click("a[href*='register']", timeout=3000)
        
        page.fill('input[name="username"]', username)
        page.fill('input[name="password1"]', password)
        page.fill('input[name="password2"]', password)
        page.click('button[type="submit"]')
        
        return {"username": username, "password": password}
    
    return register


# Performance marker
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "auth: marks tests that require authentication"
    )
    config.addinivalue_line(
        "markers", "registration: marks tests related to user registration"
    )
    config.addinivalue_line(
        "markers", "login: marks tests related to user login"
    )
