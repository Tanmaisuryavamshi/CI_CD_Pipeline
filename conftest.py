import pytest

from cart import ShoppingCart, Product


@pytest.fixture
def catalog():
    """A small, realistic product catalog for the demo."""
    return [
        Product(sku="LAPTOP01", name="ProBook Laptop", price=55000.0, stock=5),
        Product(sku="MOUSE01", name="Wireless Mouse", price=799.0, stock=50),
        Product(sku="KEYBOARD01", name="Mechanical Keyboard", price=2499.0, stock=0),
    ]


@pytest.fixture
def cart(catalog):
    """A ShoppingCart pre-loaded with the demo catalog."""
    c = ShoppingCart()
    for product in catalog:
        c.register_product(product)
    return c
