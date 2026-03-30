from playwright.sync_api import expect


def test_add_entry_to_topic(
    logged_in_user,
    unique_topic_name
):

    page = logged_in_user

    # Go to Topics
    page.get_by_role(
        "link",
        name="Topics"
    ).click()

    # Create a topic
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

    # Open the topic
    page.get_by_role(
        "link",
        name=unique_topic_name
    ).click()

    # Add entry
    page.get_by_role(
        "link",
        name="Add new entry"
    ).click()

    entry_text = "First automated entry"

    page.fill(
        'textarea[name="text"]',
        entry_text
    )

    page.get_by_role(
        "button",
        name="Add entry"
    ).click()

    expect(
        page.get_by_text(entry_text)
    ).to_be_visible()