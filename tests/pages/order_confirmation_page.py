import re

from playwright.sync_api import Page, expect


class OrderConfirmationPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def expect_confirmed_order(self, order_id: str, total: str) -> None:
        expect(self.page).to_have_url(re.compile(rf"/orders/{re.escape(order_id)}$"))
        expect(self.page.get_by_role("heading", name="Order confirmed")).to_be_visible()
        expect(self.page.get_by_test_id("order-id")).to_have_text(order_id)
        expect(self.page.get_by_test_id("order-total")).to_have_text(total)
