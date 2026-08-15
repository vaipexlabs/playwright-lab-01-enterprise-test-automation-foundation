import os

import pytest
from playwright.sync_api import Page, expect

from tests.config import AutomationSettings
from tests.pages.catalog_page import CatalogPage


@pytest.mark.e2e
@pytest.mark.evidence_demo
@pytest.mark.skipif(
    os.getenv("VAIPEX_RUN_FAILURE_DEMO") != "1",
    reason="Run through scripts/demonstrate-failure.sh",
)
def test_expected_failure_captures_diagnostic_evidence(
    authenticated_page: Page,
    settings: AutomationSettings,
) -> None:
    catalog = CatalogPage(authenticated_page)
    catalog.open(settings.base_url)

    expect(
        authenticated_page.get_by_role("heading", name="This heading does not exist")
    ).to_be_visible(timeout=1000)
