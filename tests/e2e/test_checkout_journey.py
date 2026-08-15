import pytest
from playwright.sync_api import Page

from tests.config import AutomationSettings, Credentials, ShippingAddress
from tests.pages.cart_page import CartPage
from tests.pages.catalog_page import CatalogPage
from tests.pages.checkout_page import CheckoutPage
from tests.pages.login_page import LoginPage
from tests.pages.order_confirmation_page import OrderConfirmationPage


@pytest.mark.e2e
def test_customer_can_complete_checkout(
    configured_page: Page,
    settings: AutomationSettings,
    demo_user: Credentials,
    shipping_address: ShippingAddress,
) -> None:
    login = LoginPage(configured_page, settings.base_url)
    catalog = CatalogPage(configured_page)
    cart = CartPage(configured_page)
    checkout = CheckoutPage(configured_page)
    confirmation = OrderConfirmationPage(configured_page)

    login.open()
    login.sign_in(demo_user)

    catalog.expect_loaded()
    catalog.add_product("Developer Starter Kit")

    cart.expect_total("$49.00")
    cart.proceed_to_checkout()

    checkout.submit(shipping_address)

    confirmation.expect_confirmed_order(order_id="VPX-1001", total="$49.00")
