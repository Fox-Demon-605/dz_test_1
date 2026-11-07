import allure
from playwright.sync_api import expect

from .base_page import BasePage


class SignupPage(BasePage):
    @allure.step("Проверить страницу регистрации")
    def should_be_open(self):
        self.wait_for_path("/signup")
        self.visible(self.locator("signup-heading"))
        return self

    @allure.step("Зарегистрировать пользователя {name}")
    def register(self, name, email, password):
        from .main_page import MainPage

        self._fill_form(name, email, password, password)
        self.clickable(self.locator("signup-submit-button"))
        return MainPage(self.driver, self.base_url).should_be_open()

    @allure.step("Попытаться зарегистрироваться с разными паролями")
    def try_register_with_password_mismatch(
        self, name, email, password, confirmation
    ):
        self._fill_form(name, email, password, confirmation)
        self.clickable(self.locator("signup-submit-button"))
        return self

    @allure.step("Проверить ошибку подтверждения пароля")
    def should_show_password_mismatch(self):
        expect(
            self.locator("field-error-signup-confirm-password")
        ).to_contain_text("Passwords do not match")
        return self

    def _fill_form(self, name, email, password, confirmation):
        self.fill(self.locator("signup-name"), name)
        self.fill(self.locator("signup-email"), email)
        self.fill(self.locator("signup-password"), password)
        self.fill(
            self.locator("signup-confirm-password"),
            confirmation,
        )