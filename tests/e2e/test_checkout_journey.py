import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_customer_can_complete_checkout(page: Page, base_url: str) -> None:
    page.goto(base_url)

    expect(page).to_have_url(re.compile(r"/login$"))
    expect(page.get_by_role("heading", name="Welcome to Vaipex Store")).to_be_visible()

    page.get_by_label("Email").fill("demo@vaipex.io")
    page.get_by_label("Password").fill("vaipex-demo")
    page.get_by_role("button", name="Sign in").click()

    expect(page).to_have_url(re.compile(r"/products$"))
    expect(
        page.get_by_role("heading", name="Practical resources for modern delivery")
    ).to_be_visible()

    starter_kit = page.get_by_test_id("product-starter-kit")
    expect(starter_kit).to_contain_text("Developer Starter Kit")
    starter_kit.get_by_role("button", name="Add to cart").click()

    expect(page).to_have_url(re.compile(r"/cart$"))
    expect(page.get_by_test_id("cart-total")).to_have_text("$49.00")
    page.get_by_role("link", name="Proceed to checkout").click()

    page.get_by_label("Full name").fill("Vaipex Developer")
    page.get_by_label("Street address").fill("100 Platform Way")
    page.get_by_label("City").fill("Cloud City")
    page.get_by_label("Postal code").fill("10001")
    page.get_by_role("button", name="Place order").click()

    expect(page).to_have_url(re.compile(r"/orders/VPX-1001$"))
    expect(page.get_by_role("heading", name="Order confirmed")).to_be_visible()
    expect(page.get_by_test_id("order-id")).to_have_text("VPX-1001")
