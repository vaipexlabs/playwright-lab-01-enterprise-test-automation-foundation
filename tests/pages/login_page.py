import re

from playwright.sync_api import Page, expect

from tests.config import Credentials


class LoginPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(self.base_url)
        expect(self.page).to_have_url(re.compile(r"/login$"))
        expect(self.page.get_by_role("heading", name="Welcome to Vaipex Store")).to_be_visible()

    def sign_in(self, user: Credentials) -> None:
        self.page.get_by_label("Email").fill(user.email)
        self.page.get_by_label("Password").fill(user.password)
        self.page.get_by_role("button", name="Sign in").click()
