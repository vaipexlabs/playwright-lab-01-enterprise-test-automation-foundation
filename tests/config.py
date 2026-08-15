from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class Credentials:
    email: str
    password: str


@dataclass(frozen=True)
class ShippingAddress:
    full_name: str
    street: str
    city: str
    postal_code: str


@dataclass(frozen=True)
class AutomationSettings:
    base_url: str
    timeout_ms: int
    user: Credentials
    shipping_address: ShippingAddress

    @classmethod
    def from_environment(cls, default_base_url: str) -> AutomationSettings:
        base_url = os.getenv("VAIPEX_BASE_URL", default_base_url).strip().rstrip("/")
        parsed_url = urlparse(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("VAIPEX_BASE_URL must be an absolute HTTP or HTTPS URL.")

        raw_timeout = os.getenv("VAIPEX_EXPECT_TIMEOUT_MS", "5000")
        try:
            timeout_ms = int(raw_timeout)
        except ValueError as error:
            raise ValueError("VAIPEX_EXPECT_TIMEOUT_MS must be an integer.") from error
        if timeout_ms <= 0:
            raise ValueError("VAIPEX_EXPECT_TIMEOUT_MS must be greater than zero.")

        user = Credentials(
            email=os.getenv("VAIPEX_DEMO_EMAIL", "demo@vaipex.io").strip(),
            password=os.getenv("VAIPEX_DEMO_PASSWORD", "vaipex-demo"),
        )
        if not user.email or not user.password:
            raise ValueError("Demo credentials must not be empty.")

        shipping_address = ShippingAddress(
            full_name=os.getenv("VAIPEX_SHIPPING_NAME", "Vaipex Developer").strip(),
            street=os.getenv("VAIPEX_SHIPPING_STREET", "100 Platform Way").strip(),
            city=os.getenv("VAIPEX_SHIPPING_CITY", "Cloud City").strip(),
            postal_code=os.getenv("VAIPEX_SHIPPING_POSTAL_CODE", "10001").strip(),
        )
        if not all(
            (
                shipping_address.full_name,
                shipping_address.street,
                shipping_address.city,
                shipping_address.postal_code,
            )
        ):
            raise ValueError("Shipping-address values must not be empty.")

        return cls(
            base_url=base_url,
            timeout_ms=timeout_ms,
            user=user,
            shipping_address=shipping_address,
        )
