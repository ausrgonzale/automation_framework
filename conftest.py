import os
import uuid
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

TEST_USERNAME = "testuser"
TEST_PASSWORD = "SecurePass123!"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="function")
def page_with_timeout(page):
    page.set_default_timeout(DEFAULT_TIMEOUT)
    return page


@pytest.fixture(scope="function")
def logged_in_user(page_with_timeout, base_url):

    page = page_with_timeout

    page.goto(f"{base_url}/users/login/")

    page.fill(
        'input[name="username"]',
        TEST_USERNAME
    )

    page.fill(
        'input[name="password"]',
        TEST_PASSWORD
    )

    page.get_by_role(
        "button",
        name="Log in"
    ).click()

    # Validate login worked
    expect(
        page.get_by_role(
            "link",
            name="Log out"
        )
    ).to_be_visible()

    return page


@pytest.fixture
def unique_username():

    username = f"testuser_{uuid.uuid4().hex[:8]}"

    yield username

@pytest.fixture
def unique_topic_name():

    import uuid

    return f"Automation Testing {uuid.uuid4().hex[:6]}"

@pytest.fixture
def unique_entry_text():

    import uuid

    return f"Entry {uuid.uuid4().hex[:6]}"
