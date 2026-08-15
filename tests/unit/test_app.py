from fastapi.testclient import TestClient

from vaipex_store.main import app, orders


def test_health_contract() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "vaipex-store"}


def test_invalid_login_is_rejected() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/login",
            data={"email": "demo@vaipex.io", "password": "wrong"},
        )

    assert response.status_code == 401
    assert "Email or password is incorrect." in response.text


def test_complete_purchase_journey() -> None:
    orders.clear()
    with TestClient(app) as client:
        login = client.post(
            "/login",
            data={"email": "demo@vaipex.io", "password": "vaipex-demo"},
        )
        add_to_cart = client.post("/cart/starter-kit")
        checkout = client.post(
            "/checkout",
            data={
                "full_name": "Vaipex Developer",
                "address": "100 Platform Way",
                "city": "Cloud City",
                "postal_code": "10001",
            },
        )

    assert login.status_code == 200
    assert add_to_cart.status_code == 200
    assert checkout.status_code == 200
    assert "Order confirmed" in checkout.text
    assert "VPX-1001" in checkout.text
