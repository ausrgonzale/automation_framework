from playwright.sync_api import expect
import re


def test_add_entry_to_topic(
    logged_in_user,
    unique_topic_name,
):

    page = logged_in_user

    entry_text = "This is a test entry created by automation."

    #
    # Navigate to Topics
    #

    page.get_by_role(
        "link",
        name="Topics"
    ).click()

    #
    # Create Topic
    #

    page.get_by_role(
        "link",
        name="Add a new topic"
    ).click()

    page.fill(
        'input[name="text"]',
        unique_topic_name
    )

    page.get_by_role(
        "button",
        name="Add topic"
    ).click()

    #
    # Open Topic
    #

    page.get_by_role(
        "link",
        name=unique_topic_name
    ).click()

    #
    # Add Entry
    #

    page.get_by_role(
        "link",
        name="Add new entry"
    ).click()

    page.fill(
        'textarea[name="text"]',
        entry_text
    )

    page.get_by_role(
        "button",
        name="Add entry"
    ).click()

    #
    # Verify Entry
    #

    expect(
        page.get_by_text(entry_text)
    ).to_be_visible()

from playwright.sync_api import expect


def test_edit_entry(
    logged_in_user,
    unique_topic_name,
):

    page = logged_in_user

    original_entry = "Original entry text created by automation."
    updated_entry = "Updated entry text created by automation."

    #
    # Navigate to Topics
    #

    page.get_by_role(
        "link",
        name="Topics"
    ).click()

    #
    # Create Topic
    #

    page.get_by_role(
        "link",
        name="Add a new topic"
    ).click()

    page.fill(
        'input[name="text"]',
        unique_topic_name
    )

    page.get_by_role(
        "button",
        name="Add topic"
    ).click()

    #
    # Open Topic
    #

    page.get_by_role(
        "link",
        name=unique_topic_name
    ).click()

    #
    # Add Entry
    #

    page.get_by_role(
        "link",
        name="Add new entry"
    ).click()

    page.fill(
        'textarea[name="text"]',
        original_entry
    )

    page.get_by_role(
        "button",
        name="Add entry"
    ).click()

    #
    # Edit Entry
    #

    page.get_by_role(
        "link",
        name="Edit entry"
    ).click()

    page.fill(
        'textarea[name="text"]',
        updated_entry
    )

    page.get_by_role(
        "button",
        name="Save changes"
    ).click()

    #
    # Verify Updated Entry
    #

    expect(
        page.get_by_text(updated_entry)
    ).to_be_visible()

from playwright.sync_api import expect


def test_delete_entry(
    logged_in_user,
    unique_topic_name,
):

    page = logged_in_user

    entry_text = "Entry to be deleted by automation."

    #
    # Navigate to Topics
    #

    page.get_by_role(
        "link",
        name="Topics"
    ).click()

    #
    # Create Topic
    #

    page.get_by_role(
        "link",
        name="Add a new topic"
    ).click()

    page.fill(
        'input[name="text"]',
        unique_topic_name
    )

    page.get_by_role(
        "button",
        name="Add topic"
    ).click()

    #
    # Open Topic
    #

    page.get_by_role(
        "link",
        name=unique_topic_name
    ).click()

    #
    # Add Entry
    #

    page.get_by_role(
        "link",
        name="Add new entry"
    ).click()

    page.fill(
        'textarea[name="text"]',
        entry_text
    )

    page.get_by_role(
        "button",
        name="Add entry"
    ).click()

    #
    # Delete Entry
    #

    page.get_by_role(
        "link",
        name="Delete entry"
    ).click()

    #
    # Confirm Deletion (if confirmation page exists)
    #

    if page.get_by_role("button", name="Delete").is_visible():
        page.get_by_role(
            "button",
            name="Delete"
        ).click()

    #
    # Verify Entry No Longer Exists
    #

    expect(
        page.get_by_text(entry_text)
    ).not_to_be_visible()

from playwright.sync_api import expect


def test_entries_require_login(
    page_with_timeout,
):

    page = page_with_timeout

    #
    # Attempt to access Topics page without logging in
    #

    page.goto("/topics/")

    #
    # Verify redirect to login page
    #

    expect(page).to_have_url(re.compile(r".*/users/login/"))

    expect(
        page.get_by_role(
            "heading",
            name="Log in"
        )
    ).to_be_visible()