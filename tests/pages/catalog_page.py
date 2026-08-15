import re

from playwright.sync_api import Page, expect


class CatalogPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/products$"))
        expect(
            self.page.get_by_role("heading", name="Practical resources for modern delivery")
        ).to_be_visible()

    def add_product(self, product_name: str) -> None:
        product = (
            self.page.get_by_test_id("product-grid")
            .locator("article")
            .filter(has_text=product_name)
        )
        expect(product).to_have_count(1)
        product.get_by_role("button", name="Add to cart").click()
