import re
from playwright.sync_api import expect

def test_create_topic(logged_in_user, unique_topic_name):

    page = logged_in_user

    page.get_by_role(
        "link",
        name="Topics"
    ).click()

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

    expect(
        page.get_by_text(unique_topic_name)
    ).to_be_visible()