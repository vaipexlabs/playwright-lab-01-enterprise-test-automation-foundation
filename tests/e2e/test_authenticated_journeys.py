import pytest
from playwright.sync_api import Page

from tests.config import AutomationSettings
from tests.data import ScenarioDataFactory
from tests.pages.cart_page import CartPage
from tests.pages.catalog_page import CatalogPage
from tests.pages.checkout_page import CheckoutPage
from tests.pages.order_confirmation_page import OrderConfirmationPage


@pytest.mark.e2e
def test_authenticated_customer_can_search_the_catalog(
    authenticated_page: Page,
    settings: AutomationSettings,
) -> None:
    catalog = CatalogPage(authenticated_page)

    catalog.open(settings.base_url)
    catalog.search("Training")

    catalog.expect_product("Observability Workshop Pack")


@pytest.mark.e2e
def test_authenticated_customer_can_checkout_a_field_guide(
    authenticated_page: Page,
    settings: AutomationSettings,
    test_data_factory: ScenarioDataFactory,
) -> None:
    catalog = CatalogPage(authenticated_page)
    cart = CartPage(authenticated_page)
    checkout = CheckoutPage(authenticated_page)
    confirmation = OrderConfirmationPage(authenticated_page)

    catalog.open(settings.base_url)
    catalog.add_product("Platform Engineering Field Guide")

    cart.expect_total("$35.00")
    cart.proceed_to_checkout()

    checkout.submit(test_data_factory.shipping_address("authenticated field-guide checkout"))

    confirmation.expect_confirmed_order(order_id="VPX-1001", total="$35.00")
