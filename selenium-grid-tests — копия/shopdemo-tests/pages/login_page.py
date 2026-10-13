import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    HEADING = (By.CSS_SELECTOR, '[data-testid="login-heading"]')
    EMAIL = (By.CSS_SELECTOR, '[data-testid="login-email"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-testid="login-password"]')
    SUBMIT = (By.CSS_SELECTOR, '[data-testid="login-submit-button"]')
    ERROR = (By.CSS_SELECTOR, '[data-testid="login-error"]')

    @allure.step("Проверить страницу входа")
    def should_be_open(self):
        self.wait_for_path("/login")
        self.visible(self.HEADING)
        return self

    @allure.step("Войти пользователем {email}")
    def login_as(self, email, password):
        from .main_page import MainPage

        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return MainPage(self.driver, self.base_url).should_be_open()

    @allure.step("Попытаться войти пользователем {email}")
    def try_login_as(self, email, password):
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return self

    @allure.step("Проверить ошибку авторизации")
    def should_show_invalid_credentials(self):
        assert "Invalid email or password" in self.text(self.ERROR)
        return self