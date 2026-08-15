from __future__ import annotations

import hashlib
import re

from tests.config import ShippingAddress


class ScenarioDataFactory:
    def __init__(self, worker_id: str) -> None:
        self.worker_id = worker_id

    def shipping_address(self, scenario: str) -> ShippingAddress:
        normalized_scenario = re.sub(r"[^a-z0-9]+", "-", scenario.casefold()).strip("-")
        identity = f"{self.worker_id}:{normalized_scenario}"
        suffix = hashlib.sha256(identity.encode()).hexdigest()[:8].upper()
        return ShippingAddress(
            full_name=f"Vaipex Test {suffix}",
            street=f"{int(suffix[:4], 16) % 900 + 100} Automation Way",
            city="Test City",
            postal_code=f"{int(suffix[4:], 16) % 90000 + 10000:05d}",
        )
