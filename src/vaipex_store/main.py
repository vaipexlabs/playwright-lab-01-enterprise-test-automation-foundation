from __future__ import annotations

import os
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

PACKAGE_ROOT = Path(__file__).parent
DEMO_EMAIL = "demo@vaipex.io"
DEMO_PASSWORD = "vaipex-demo"


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    description: str
    price: float
    category: str


PRODUCTS = (
    Product(
        "starter-kit",
        "Developer Starter Kit",
        "A curated toolkit for productive teams.",
        49.00,
        "Tooling",
    ),
    Product(
        "platform-guide",
        "Platform Engineering Field Guide",
        "Practical patterns for internal platforms.",
        35.00,
        "Books",
    ),
    Product(
        "observability-pack",
        "Observability Workshop Pack",
        "Hands-on metrics, logs, and traces exercises.",
        79.00,
        "Training",
    ),
)
PRODUCT_BY_ID = {product.id: product for product in PRODUCTS}
orders: dict[str, dict[str, object]] = {}

app = FastAPI(title="Vaipex Store", version="0.1.0")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("VAIPEX_SESSION_SECRET", "local-vaipex-store-session-secret"),
    same_site="lax",
    https_only=False,
)
app.mount("/static", StaticFiles(directory=PACKAGE_ROOT / "static"), name="static")
templates = Jinja2Templates(directory=PACKAGE_ROOT / "templates")


def signed_in(request: Request) -> bool:
    return request.session.get("user") == DEMO_EMAIL


def sign_in_redirect() -> RedirectResponse:
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)


def cart_summary(request: Request) -> tuple[list[dict[str, object]], float]:
    quantities = Counter(request.session.get("cart", []))
    items: list[dict[str, object]] = []
    total = 0.0
    for product in PRODUCTS:
        quantity = quantities.get(product.id, 0)
        if not quantity:
            continue
        subtotal = product.price * quantity
        total += subtotal
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
    return items, total


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "vaipex-store"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> RedirectResponse:
    destination = "/products" if signed_in(request) else "/login"
    return RedirectResponse(destination, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})


@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> Response:
    if email != DEMO_EMAIL or password != DEMO_PASSWORD:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Email or password is incorrect."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    request.session.clear()
    request.session["user"] = DEMO_EMAIL
    request.session["cart"] = []
    return RedirectResponse("/products", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/logout")
def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return sign_in_redirect()


@app.get("/products", response_class=HTMLResponse)
def products_page(request: Request, q: Annotated[str, Query()] = "") -> Response:
    if not signed_in(request):
        return sign_in_redirect()
    normalized_query = q.strip().casefold()
    visible_products = [
        product
        for product in PRODUCTS
        if not normalized_query
        or normalized_query in product.name.casefold()
        or normalized_query in product.category.casefold()
    ]
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={
            "products": visible_products,
            "query": q,
            "cart_count": len(request.session.get("cart", [])),
        },
    )


@app.post("/cart/{product_id}")
def add_to_cart(request: Request, product_id: str) -> RedirectResponse:
    if not signed_in(request):
        return sign_in_redirect()
    if product_id not in PRODUCT_BY_ID:
        raise HTTPException(status_code=404, detail="Product not found")
    cart = list(request.session.get("cart", []))
    cart.append(product_id)
    request.session["cart"] = cart
    return RedirectResponse("/cart", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request) -> Response:
    if not signed_in(request):
        return sign_in_redirect()
    items, total = cart_summary(request)
    return templates.TemplateResponse(
        request=request,
        name="cart.html",
        context={
            "items": items,
            "total": total,
            "cart_count": len(request.session.get("cart", [])),
        },
    )


@app.post("/cart/{product_id}/remove")
def remove_from_cart(request: Request, product_id: str) -> RedirectResponse:
    if not signed_in(request):
        return sign_in_redirect()
    request.session["cart"] = [
        item for item in request.session.get("cart", []) if item != product_id
    ]
    return RedirectResponse("/cart", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request) -> Response:
    if not signed_in(request):
        return sign_in_redirect()
    items, total = cart_summary(request)
    if not items:
        return RedirectResponse("/products", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        request=request,
        name="checkout.html",
        context={"error": None, "total": total, "cart_count": len(request.session.get("cart", []))},
    )


@app.post("/checkout", response_class=HTMLResponse)
def complete_checkout(
    request: Request,
    full_name: Annotated[str, Form()],
    address: Annotated[str, Form()],
    city: Annotated[str, Form()],
    postal_code: Annotated[str, Form()],
) -> Response:
    if not signed_in(request):
        return sign_in_redirect()
    items, total = cart_summary(request)
    if not items:
        return RedirectResponse("/products", status_code=status.HTTP_303_SEE_OTHER)
    if not all(value.strip() for value in (full_name, address, city, postal_code)):
        return templates.TemplateResponse(
            request=request,
            name="checkout.html",
            context={
                "error": "Complete every shipping field.",
                "total": total,
                "cart_count": len(request.session.get("cart", [])),
            },
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
    order_id = f"VPX-{1000 + len(orders) + 1}"
    order = {
        "id": order_id,
        "customer": full_name.strip(),
        "total": total,
        "items": items,
        "status": "Confirmed",
    }
    orders[order_id] = order
    request.session["cart"] = []
    return RedirectResponse(f"/orders/{order_id}", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/orders/{order_id}", response_class=HTMLResponse)
def order_page(request: Request, order_id: str) -> Response:
    if not signed_in(request):
        return sign_in_redirect()
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return templates.TemplateResponse(
        request=request, name="order.html", context={"order": order, "cart_count": 0}
    )


@app.get("/api/catalog")
def catalog() -> dict[str, list[dict[str, object]]]:
    return {"products": [asdict(product) for product in PRODUCTS]}


@app.post("/api/test/reset")
def reset_test_state(request: Request) -> dict[str, str]:
    if os.getenv("VAIPEX_TEST_MODE") != "1":
        raise HTTPException(status_code=403, detail="Test controls are disabled")
    orders.clear()
    request.session.clear()
    return {"status": "reset"}
