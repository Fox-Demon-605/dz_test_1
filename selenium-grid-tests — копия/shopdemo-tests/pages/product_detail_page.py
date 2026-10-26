import allure

from .base_page import BasePage


class ProductDetailPage(BasePage):
    @allure.step("Проверить карточку товара {product_id}")
    def should_be_open(self, product_id):
        self.wait_for_path(f"/products/{product_id}")
        self.visible(self.locator("product-name"))
        return self

    @allure.step("Добавить {quantity} шт. товара в корзину")
    def add_to_cart(self, quantity=1):
        self.fill(self.locator("quantity-input"), quantity)
        self.clickable(self.locator("add-to-cart-button"))
        self.visible(self.locator("added-notification"))
        return self

    @allure.step("Открыть корзину")
    def go_to_cart(self):
        from .cart_page import CartPage

        self.clickable(self.locator("cart-link"))
        return CartPage(self.driver, self.base_url).should_be_open()