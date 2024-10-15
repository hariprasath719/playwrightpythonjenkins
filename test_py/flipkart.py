import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1500)
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
    page.goto("https://www.flipkart.com/")
    yield page
    page.close()


def test_iphone_search_and_validate_price(page, context):
    # Search for the product
    search_box = page.get_by_role("textbox", name="Search for Products, Brands and More")
    search_button = page.get_by_role("button", name="Search for Products, Brands and More")
    product = "Apple IPhone 16 (White, 128 GB)"
    expected_price = "₹79,900"

    # Fill in the search box and click the search button
    search_box.fill(product)
    search_button.click()

    # Wait for the product link to appear and click it
    product_link = page.get_by_role("link", name=product)

    # Handling child window
    with context.expect_page() as new_tab_event:
        product_link.click()

    new_tab = new_tab_event.value

    # Wait for the new tab to load
    new_tab.wait_for_load_state('networkidle')

    # Validate the price
    price = new_tab.locator("div.Nx9bqj.CxhGGd").text_content().strip()
    assert price == expected_price, "Price is not matching"

    new_tab.close()  # Close the new tab





