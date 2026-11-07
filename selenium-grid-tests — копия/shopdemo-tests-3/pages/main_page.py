import allure
from playwright.sync_api import expect

from .base_page import BasePage


class MainPage(BasePage):
    @allure.step("Проверить, что открыт магазин")
    def should_be_open(self):
        self.wait_for_path("/")
        self.visible(self.locator("product-count"))
        return self

    @allure.step("Проверить приветствие пользователя {name}")
    def should_greet(self, name):
        expect(self.locator("user-greeting")).to_have_text(f"Hi, {name}")
        return self

    @allure.step("Перейти к регистрации")
    def go_to_signup(self):
        from .signup_page import SignupPage

        self.clickable(self.locator("nav-signup-link"))
        return SignupPage(self.driver, self.base_url).should_be_open()

    @allure.step("Перейти к авторизации")
    def go_to_login(self):
        from .login_page import LoginPage

        self.clickable(self.locator("nav-login-link"))
        return LoginPage(self.driver, self.base_url).should_be_open()

    @allure.step("Перейти к каталогу")
    def browse_products(self):
        from .products_page import ProductsPage

        return ProductsPage(self.driver, self.base_url).should_be_open()

    @allure.step("Открыть корзину")
    def go_to_cart(self):
        from .cart_page import CartPage

        self.clickable(self.locator("cart-link"))
        return CartPage(self.driver, self.base_url).should_be_open()

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.clickable(self.locator("logout-button"))
        self.visible(self.locator("nav-login-link"))
        return self