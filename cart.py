"""
Shopping Cart module - core business logic for an e-commerce cart demo.

This is intentionally realistic (stock limits, discount codes, checkout
errors) so the resulting test suite and Allure report have something
meaningful to show in a demo.
"""


class EmptyCartError(Exception):
    """Raised when checkout is attempted on an empty cart."""
    pass


class OutOfStockError(Exception):
    """Raised when requested quantity exceeds available stock."""
    pass


class InvalidDiscountError(Exception):
    """Raised when an invalid discount code is applied."""
    pass


DISCOUNT_CODES = {
    "SAVE10": 0.10,
    "SAVE20": 0.20,
    "WELCOME5": 0.05,
}


class Product:
    def __init__(self, sku, name, price, stock):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.sku = sku
        self.name = name
        self.price = price
        self.stock = stock


class ShoppingCart:
    def __init__(self):
        self.items = {}     # sku -> quantity
        self.catalog = {}   # sku -> Product
        self.discount_rate = 0.0

    def register_product(self, product: Product):
        self.catalog[product.sku] = product

    def add_item(self, sku, quantity=1):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if sku not in self.catalog:
            raise KeyError(f"Product {sku} not found in catalog")

        product = self.catalog[sku]
        current_qty = self.items.get(sku, 0)

        if current_qty + quantity > product.stock:
            raise OutOfStockError(
                f"Only {product.stock - current_qty} units of {product.name} left in stock"
            )

        self.items[sku] = current_qty + quantity

    def remove_item(self, sku, quantity=1):
        if sku not in self.items:
            raise KeyError(f"{sku} is not in the cart")
        if quantity >= self.items[sku]:
            del self.items[sku]
        else:
            self.items[sku] -= quantity

    def apply_discount(self, code):
        if code not in DISCOUNT_CODES:
            raise InvalidDiscountError(f"Discount code '{code}' is not valid")
        self.discount_rate = DISCOUNT_CODES[code]

    def subtotal(self):
        return sum(self.catalog[sku].price * qty for sku, qty in self.items.items())

    def total(self):
        return round(self.subtotal() * (1 - self.discount_rate), 2)

    def checkout(self):
        if not self.items:
            raise EmptyCartError("Cannot checkout an empty cart")

        # Deduct purchased quantities from stock
        for sku, qty in self.items.items():
            self.catalog[sku].stock -= qty

        final_total = self.total()
        self.items = {}
        self.discount_rate = 0.0
        return final_total
