import pytest
from playwright.sync_api import Page

from tests.config import AutomationSettings, Credentials
from tests.pages.login_page import LoginPage


@pytest.mark.e2e
def test_invalid_credentials_are_rejected(
    configured_page: Page,
    settings: AutomationSettings,
) -> None:
    login = LoginPage(configured_page, settings.base_url)
    invalid_user = Credentials(email=settings.user.email, password="incorrect-password")

    login.open()
    login.sign_in(invalid_user)

    login.expect_error("Email or password is incorrect.")
