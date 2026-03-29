from playwright.sync_api import expect


def test_successful_login(logged_in_user, base_url):
    """
    Verify user can log in successfully.
    """

    page = logged_in_user

    expect(page).to_have_url(
        base_url + "/"
    )

    expect(
        page.get_by_role(
            "link",
            name="Log out"
        )
    ).to_be_visible()


def test_invalid_username(page, base_url):
    """
    Verify login fails with invalid username.
    """

    page.goto(
        f"{base_url}/users/login/"
    )

    page.fill(
        'input[name="username"]',
        "invaliduser"
    )

    page.fill(
        'input[name="password"]',
        "testpass123"
    )

    page.get_by_role(
        "button",
        name="Log in"
    ).click()

    expect(
    page.get_by_text(
        "Please enter a correct username and password."
        )
    ).to_be_visible()


def test_invalid_password(page, base_url):
    """
    Verify login fails with wrong password.
    """

    page.goto(
        f"{base_url}/users/login/"
    )

    page.fill(
        'input[name="username"]',
        "testuser"
    )

    page.fill(
        'input[name="password"]',
        "wrongpassword"
    )

    page.get_by_role(
        "button",
        name="Log in"
    ).click()

    expect(
    page.get_by_text(
        "Please enter a correct username and password."
        )
    ).to_be_visible()


def test_logout(logged_in_user, base_url):
    """
    Verify user can log out successfully.
    """

    page = logged_in_user

    page.get_by_role(
        "link",
        name="Log out"
    ).click()

    expect(page).to_have_url(
        base_url + "/"
    )

    expect(
        page.get_by_role(
            "link",
            name="Log in"
        )
    ).to_be_visible()