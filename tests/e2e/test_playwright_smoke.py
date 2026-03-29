def test_homepage_title(page):
    """
    Basic smoke test to verify Playwright launches
    and can navigate to a page.
    """

    page.goto("https://example.com")

    assert "Example" in page.title()