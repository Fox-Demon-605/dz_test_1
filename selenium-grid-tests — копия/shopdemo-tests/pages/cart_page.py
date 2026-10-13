import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class CartPage(BasePage):
    CHECKOUT = (By.CSS_SELECTOR, '[data-testid="checkout-button"]')
    TOTAL = (By.CSS_SELECTOR, '[data-testid="cart-total"]')
    EMPTY = (By.CSS_SELECTOR, '[data-testid="empty-cart-message"]')

    @allure.step("Проверить страницу корзины")
    def should_be_open(self):
        self.wait_for_path("/cart")
        self.wait.until(
            EC.any_of(
                EC.visibility_of_element_located(self.CHECKOUT),
                EC.visibility_of_element_located(self.EMPTY),
            )
        )
        return self

    @allure.step("Проверить количество {quantity} у товара {product_name}")
    def should_contain_product(self, product_name, quantity):
        self.wait.until(
            lambda driver: any(
                product_name in element.text
                for element in driver.find_elements(
                    By.CSS_SELECTOR,
                    '[data-testid^="cart-item-cart-"]',
                )
            )
        )

        rows = self.driver.find_elements(
            By.CSS_SELECTOR,
            '[data-testid^="cart-item-cart-"]',
        )
        matching_row = next(
            row for row in rows if product_name in row.text
        )
        quantity_element = matching_row.find_element(
            By.CSS_SELECTOR,
            '[data-testid^="cart-item-quantity-"]',
        )
        assert int(quantity_element.text) == quantity
        return self

    @allure.step("Проверить сумму корзины {expected_total}")
    def should_have_total(self, expected_total):
        assert self.text(self.TOTAL) == expected_total
        return self

    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self):
        from .checkout_page import CheckoutPage

        self.click(self.CHECKOUT)
        return CheckoutPage(
            self.driver, self.base_url
        ).should_be_open()