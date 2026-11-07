import allure
from playwright.sync_api import expect

from .base_page import BasePage


class OrderConfirmationPage(BasePage):
    @allure.step("Проверить подтверждение заказа")
    def should_be_open(self):
        self.wait_for_path("/order-confirmation")
        self.visible(self.locator("order-confirmation"))
        expect(self.locator("order-id")).not_to_be_empty()
        return self