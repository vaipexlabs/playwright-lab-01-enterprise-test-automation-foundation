from __future__ import annotations

from collections.abc import Callable, Generator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from tests.config import AutomationSettings, Credentials, ShippingAddress
from tests.data import ScenarioDataFactory
from tests.pages.catalog_page import CatalogPage
from tests.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def settings(app_server: str) -> AutomationSettings:
    return AutomationSettings.from_environment(default_base_url=app_server)


@pytest.fixture
def configured_page(page: Page, settings: AutomationSettings) -> Page:
    page.set_default_timeout(settings.timeout_ms)
    page.set_default_navigation_timeout(settings.timeout_ms)
    return page


@pytest.fixture(scope="session")
def authenticated_state(
    browser: Browser,
    settings: AutomationSettings,
    demo_user: Credentials,
    tmp_path_factory: pytest.TempPathFactory,
    worker_id: str,
) -> Path:
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(settings.timeout_ms)
    page.set_default_navigation_timeout(settings.timeout_ms)
    login = LoginPage(page, settings.base_url)
    login.open()
    login.sign_in(demo_user)
    CatalogPage(page).expect_loaded()

    state_directory = tmp_path_factory.mktemp(f"authenticated-{worker_id}")
    state_path = state_directory / "storage-state.json"
    context.storage_state(path=state_path)
    context.close()
    return state_path


@pytest.fixture
def authenticated_page(
    new_context: Callable[..., BrowserContext],
    authenticated_state: Path,
    settings: AutomationSettings,
) -> Generator[Page]:
    context = new_context(storage_state=authenticated_state)
    page = context.new_page()
    page.set_default_timeout(settings.timeout_ms)
    page.set_default_navigation_timeout(settings.timeout_ms)
    try:
        yield page
    finally:
        context.close()


@pytest.fixture(scope="session")
def demo_user(settings: AutomationSettings) -> Credentials:
    return settings.user


@pytest.fixture(scope="session")
def shipping_address(settings: AutomationSettings) -> ShippingAddress:
    return settings.shipping_address


@pytest.fixture(scope="session")
def test_data_factory(worker_id: str) -> ScenarioDataFactory:
    return ScenarioDataFactory(worker_id=worker_id)
