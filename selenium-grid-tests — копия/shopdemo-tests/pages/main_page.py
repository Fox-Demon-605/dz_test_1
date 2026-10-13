import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class MainPage(BasePage):
    PRODUCT_COUNT = (By.CSS_SELECTOR, '[data-testid="product-count"]')
    USER_GREETING = (By.CSS_SELECTOR, '[data-testid="user-greeting"]')
    NAV_LOGIN = (By.CSS_SELECTOR, '[data-testid="nav-login-link"]')
    NAV_SIGNUP = (By.CSS_SELECTOR, '[data-testid="nav-signup-link"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-testid="cart-link"]')
    LOGOUT = (By.CSS_SELECTOR, '[data-testid="logout-button"]')

    @allure.step("Проверить, что открыт магазин")
    def should_be_open(self):
        self.wait_for_path("/")
        self.visible(self.PRODUCT_COUNT)
        return self

    @allure.step("Проверить приветствие пользователя {name}")
    def should_greet(self, name):
        assert self.text(self.USER_GREETING) == f"Hi, {name}"
        return self

    @allure.step("Перейти к регистрации")
    def go_to_signup(self):
        from .signup_page import SignupPage

        self.click(self.NAV_SIGNUP)
        return SignupPage(self.driver, self.base_url).should_be_open()

    @allure.step("Перейти к авторизации")
    def go_to_login(self):
        from .login_page import LoginPage

        self.click(self.NAV_LOGIN)
        return LoginPage(self.driver, self.base_url).should_be_open()

    @allure.step("Перейти к каталогу")
    def browse_products(self):
        from .products_page import ProductsPage

        return ProductsPage(self.driver, self.base_url).should_be_open()

    @allure.step("Открыть корзину")
    def go_to_cart(self):
        from .cart_page import CartPage

        self.click(self.CART_LINK)
        return CartPage(self.driver, self.base_url).should_be_open()

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.click(self.LOGOUT)
        self.visible(self.NAV_LOGIN)
        return self