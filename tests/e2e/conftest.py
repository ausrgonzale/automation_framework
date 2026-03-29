import os
import pytest
from playwright.sync_api import expect

BASE_URL = os.getenv(
    "BASE_URL",
    "http://localhost:8000"
)

DEFAULT_TIMEOUT = int(
    os.getenv(
        "PLAYWRIGHT_TIMEOUT",
        "5000"
    )
)

@pytest.fixture(scope="session")
def base_url():
    """
    Central base URL fixture.
    """
    return BASE_URL


@pytest.fixture(scope="function")
def page_with_timeout(page):
    """
    Apply consistent timeout to every test page.
    """
    page.set_default_timeout(DEFAULT_TIMEOUT)
    return page


@pytest.fixture(scope="function")
def logged_in_user(page_with_timeout, base_url):
    """
    Reusable login fixture.
    Logs user into the application.
    """

    page = page_with_timeout

    page.goto(f"{base_url}/users/login/")

    page.fill(
        'input[name="username"]',
        "testuser"
    )

    page.fill(
        'input[name="password"]',
        "SecurePass123!"
    )

    page.get_by_role(
        "button",
        name="Log in"
    ).click()

    # Check if login failed — show the real message
    error_message = page.locator(".errorlist").first

    if error_message.is_visible():
        raise AssertionError(
            f"Login failed: {error_message.inner_text()}"
        )

    return page