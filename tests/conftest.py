from __future__ import annotations

import pytest
from playwright.sync_api import Page

from tests.config import AutomationSettings, Credentials, ShippingAddress


@pytest.fixture(scope="session")
def settings(app_server: str) -> AutomationSettings:
    return AutomationSettings.from_environment(default_base_url=app_server)


@pytest.fixture
def configured_page(page: Page, settings: AutomationSettings) -> Page:
    page.set_default_timeout(settings.timeout_ms)
    page.set_default_navigation_timeout(settings.timeout_ms)
    return page


@pytest.fixture(scope="session")
def demo_user(settings: AutomationSettings) -> Credentials:
    return settings.user


@pytest.fixture(scope="session")
def shipping_address(settings: AutomationSettings) -> ShippingAddress:
    return settings.shipping_address
