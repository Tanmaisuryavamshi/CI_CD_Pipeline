import allure
import pytest

from cart import EmptyCartError, OutOfStockError, InvalidDiscountError


@allure.feature("Shopping Cart")
@allure.story("Add items")
class TestAddItem:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Adding an in-stock item increases cart quantity")
    def test_add_item_success(self, cart):
        with allure.step("Add 2 units of LAPTOP01 to the cart"):
            cart.add_item("LAPTOP01", quantity=2)
        with allure.step("Verify cart contains 2 units"):
            assert cart.items["LAPTOP01"] == 2

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Adding a non-existent SKU raises KeyError")
    def test_add_item_unknown_sku(self, cart):
        with allure.step("Attempt to add a product not in the catalog"):
            with pytest.raises(KeyError):
                cart.add_item("DOES_NOT_EXIST")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Adding more than available stock raises OutOfStockError")
    def test_add_item_out_of_stock(self, cart):
        with allure.step("Attempt to add 100 units of MOUSE01 (only 50 in stock)"):
            with pytest.raises(OutOfStockError):
                cart.add_item("MOUSE01", quantity=100)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Adding an item that is already out of stock fails immediately")
    def test_add_item_zero_stock_product(self, cart):
        with allure.step("Attempt to add KEYBOARD01, which has zero stock"):
            with pytest.raises(OutOfStockError):
                cart.add_item("KEYBOARD01", quantity=1)

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Adding zero or negative quantity raises ValueError")
    @pytest.mark.parametrize("bad_qty", [0, -1, -5])
    def test_add_item_invalid_quantity(self, cart, bad_qty):
        with pytest.raises(ValueError):
            cart.add_item("MOUSE01", quantity=bad_qty)


@allure.feature("Shopping Cart")
@allure.story("Discounts")
class TestDiscounts:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Valid discount codes apply the correct rate")
    @pytest.mark.parametrize("code,expected_rate", [
        ("SAVE10", 0.10),
        ("SAVE20", 0.20),
        ("WELCOME5", 0.05),
    ])
    def test_apply_valid_discount(self, cart, code, expected_rate):
        with allure.step(f"Apply discount code {code}"):
            cart.apply_discount(code)
        assert cart.discount_rate == expected_rate

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Invalid discount code raises InvalidDiscountError")
    def test_apply_invalid_discount(self, cart):
        with pytest.raises(InvalidDiscountError):
            cart.apply_discount("NOT_REAL_CODE")


@allure.feature("Shopping Cart")
@allure.story("Checkout")
class TestCheckout:

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Checkout on an empty cart raises EmptyCartError")
    def test_checkout_empty_cart(self, cart):
        with allure.step("Attempt checkout with nothing in the cart"):
            with pytest.raises(EmptyCartError):
                cart.checkout()

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Checkout calculates the correct total with a discount applied")
    def test_checkout_with_discount(self, cart):
        with allure.step("Add 1 laptop and 2 mice to the cart"):
            cart.add_item("LAPTOP01", quantity=1)
            cart.add_item("MOUSE01", quantity=2)

        with allure.step("Apply a 10% discount code"):
            cart.apply_discount("SAVE10")

        with allure.step("Checkout and verify the final total"):
            total = cart.checkout()
            expected = round((55000.0 + 2 * 799.0) * 0.90, 2)
            assert total == expected

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Checkout deducts purchased quantity from stock")
    def test_checkout_reduces_stock(self, cart):
        cart.add_item("MOUSE01", quantity=5)
        cart.checkout()
        assert cart.catalog["MOUSE01"].stock == 45

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Cart resets to empty after a successful checkout")
    def test_checkout_resets_cart(self, cart):
        cart.add_item("MOUSE01", quantity=1)
        cart.checkout()
        assert cart.items == {}
        assert cart.discount_rate == 0.0


@allure.feature("Shopping Cart")
@allure.story("Remove items")
class TestRemoveItem:

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Removing an item not in the cart raises KeyError")
    def test_remove_item_not_in_cart(self, cart):
        with pytest.raises(KeyError):
            cart.remove_item("LAPTOP01")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Removing a partial quantity leaves the remainder in the cart")
    def test_remove_partial_quantity(self, cart):
        cart.add_item("MOUSE01", quantity=5)
        cart.remove_item("MOUSE01", quantity=2)
        assert cart.items["MOUSE01"] == 3

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Removing the full quantity clears the item from the cart")
    def test_remove_full_quantity(self, cart):
        cart.add_item("MOUSE01", quantity=2)
        cart.remove_item("MOUSE01", quantity=2)
        assert "MOUSE01" not in cart.items
