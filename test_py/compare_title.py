import pytest
from playwright.sync_api import sync_playwright


# Define a fixture to start Playwright and create a new browser context
@pytest.fixture(scope="function")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to True for headless mode
        context = browser.new_context()
        yield context
        browser.close()


def test_compare_title(browser_context):
    # Create a new page in the browser context
    page = browser_context.new_page()

    # Navigate to the desired URL
    url = 'https://google.com'  # Change this to your desired URL
    page.goto(url)

    # Get the actual title of the page
    actual_title = page.title()
    print(f"Actual Title: {actual_title}")

    # Define the expected title
    expected_title = 'Google'  # Change this to your expected title

    # Compare the actual title with the expected title
    assert actual_title == expected_title, f"Title mismatch! Expected: '{expected_title}', but got: '{actual_title}'"

    # Close the page
    page.close()
