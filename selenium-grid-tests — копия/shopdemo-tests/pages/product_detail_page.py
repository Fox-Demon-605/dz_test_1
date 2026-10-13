import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class ProductDetailPage(BasePage):
    NAME = (By.CSS_SELECTOR, '[data-testid="product-name"]')
    PRICE = (By.CSS_SELECTOR, '[data-testid="product-price"]')
    QUANTITY = (By.CSS_SELECTOR, '[data-testid="quantity-input"]')
    ADD_TO_CART = (
        By.CSS_SELECTOR,
        '[data-testid="add-to-cart-button"]',
    )
    ADDED_NOTIFICATION = (
        By.CSS_SELECTOR,
        '[data-testid="added-notification"]',
    )
    CART_LINK = (By.CSS_SELECTOR, '[data-testid="cart-link"]')

    @allure.step("Проверить карточку товара {product_id}")
    def should_be_open(self, product_id):
        self.wait_for_path(f"/products/{product_id}")
        self.visible(self.NAME)
        return self

    @allure.step("Добавить {quantity} шт. товара в корзину")
    def add_to_cart(self, quantity=1):
        self.fill(self.QUANTITY, str(quantity))
        self.click(self.ADD_TO_CART)
        self.visible(self.ADDED_NOTIFICATION)
        return self

    @allure.step("Открыть корзину")
    def go_to_cart(self):
        from .cart_page import CartPage

        self.click(self.CART_LINK)
        return CartPage(self.driver, self.base_url).should_be_open()