import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.goto("https://bootswatch.com/default/")
    yield page
    page.close()


def test_link_is_visible(page):
    link_selector = page.get_by_role("link", name="Link").first
    assert link_selector.is_visible(), "Link is not visible"


def test_fill_textbox(page):
    text_to_fill = page.get_by_role("textbox", name="Default input")
    text_to_fill.fill("Hariprasath")
    assert text_to_fill.input_value() == "Hariprasath", "Text box was not filled correctly"


def test_checkbox_is_checked(page):
    checked_checkbox = page.get_by_role("checkbox", name="Checked checkbox")
    assert checked_checkbox.is_checked()





