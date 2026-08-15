from playwright.sync_api import Page

from tests.config import ShippingAddress


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def submit(self, address: ShippingAddress) -> None:
        self.page.get_by_label("Full name").fill(address.full_name)
        self.page.get_by_label("Street address").fill(address.street)
        self.page.get_by_label("City").fill(address.city)
        self.page.get_by_label("Postal code").fill(address.postal_code)
        self.page.get_by_role("button", name="Place order").click()
