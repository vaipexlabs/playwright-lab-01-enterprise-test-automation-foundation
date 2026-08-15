import re

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def expect_total(self, total: str) -> None:
        expect(self.page).to_have_url(re.compile(r"/cart$"))
        expect(self.page.get_by_test_id("cart-total")).to_have_text(total)

    def proceed_to_checkout(self) -> None:
        self.page.get_by_role("link", name="Proceed to checkout").click()
