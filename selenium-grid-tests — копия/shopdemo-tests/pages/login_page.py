import allure
from playwright.sync_api import expect

from .base_page import BasePage


class LoginPage(BasePage):
    @allure.step("Проверить страницу входа")
    def should_be_open(self):
        self.wait_for_path("/login")
        self.visible(self.locator("login-heading"))
        return self

    @allure.step("Войти пользователем {email}")
    def login_as(self, email, password):
        from .main_page import MainPage

        self.fill(self.locator("login-email"), email)
        self.fill(self.locator("login-password"), password)
        self.clickable(self.locator("login-submit-button"))

        return MainPage(self.driver, self.base_url).should_be_open()

    @allure.step("Попытаться войти пользователем {email}")
    def try_login_as(self, email, password):
        self.fill(self.locator("login-email"), email)
        self.fill(self.locator("login-password"), password)
        self.clickable(self.locator("login-submit-button"))
        return self

    @allure.step("Проверить ошибку авторизации")
    def should_show_invalid_credentials(self):
        expect(self.locator("login-error")).to_contain_text(
            "Invalid email or password"
        )
        return self