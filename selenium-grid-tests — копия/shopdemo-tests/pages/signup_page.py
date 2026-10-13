import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class SignupPage(BasePage):
    HEADING = (By.CSS_SELECTOR, '[data-testid="signup-heading"]')
    NAME = (By.CSS_SELECTOR, '[data-testid="signup-name"]')
    EMAIL = (By.CSS_SELECTOR, '[data-testid="signup-email"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-testid="signup-password"]')
    CONFIRM_PASSWORD = (
        By.CSS_SELECTOR,
        '[data-testid="signup-confirm-password"]',
    )
    SUBMIT = (By.CSS_SELECTOR, '[data-testid="signup-submit-button"]')
    PASSWORD_ERROR = (
        By.CSS_SELECTOR,
        '[data-testid="field-error-signup-confirm-password"]',
    )

    @allure.step("Проверить страницу регистрации")
    def should_be_open(self):
        self.wait_for_path("/signup")
        self.visible(self.HEADING)
        return self

    @allure.step("Зарегистрировать пользователя {name}")
    def register(self, name, email, password):
        from .main_page import MainPage

        self._fill_form(name, email, password, password)
        self.click(self.SUBMIT)
        return MainPage(self.driver, self.base_url).should_be_open()

    @allure.step("Попытаться зарегистрироваться с разными паролями")
    def try_register_with_password_mismatch(
        self, name, email, password, confirmation
    ):
        self._fill_form(name, email, password, confirmation)
        self.click(self.SUBMIT)
        return self

    @allure.step("Проверить ошибку подтверждения пароля")
    def should_show_password_mismatch(self):
        assert "Passwords do not match" in self.text(self.PASSWORD_ERROR)
        return self

    def _fill_form(self, name, email, password, confirmation):
        self.fill(self.NAME, name)
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.fill(self.CONFIRM_PASSWORD, confirmation)