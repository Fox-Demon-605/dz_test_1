import allure
from playwright.sync_api import expect

from .base_page import BasePage


class CartPage(BasePage):
    def _items(self):
        return self.driver.locator('[data-testid^="cart-item-cart-"]')

    @allure.step("Проверить страницу корзины")
    def should_be_open(self):
        self.wait_for_path("/cart")
        expect(
            self.locator("checkout-button").or_(
                self.locator("empty-cart-message")
            ).first
        ).to_be_visible()
        return self

    @allure.step("Проверить количество {quantity} у товара {product_name}")
    def should_contain_product(self, product_name, quantity):
        row = self._items().filter(has_text=product_name).first
        expect(row).to_be_visible()

        quantity_element = row.locator(
            '[data-testid^="cart-item-quantity-"]'
        )
        expect(quantity_element).to_have_text(str(quantity))
        return self

    @allure.step("Проверить сумму корзины {expected_total}")
    def should_have_total(self, expected_total):
        expect(self.locator("cart-total")).to_have_text(expected_total)
        return self

    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self):
        from .checkout_page import CheckoutPage

        self.clickable(self.locator("checkout-button"))
        return CheckoutPage(
            self.driver, self.base_url
        ).should_be_open()