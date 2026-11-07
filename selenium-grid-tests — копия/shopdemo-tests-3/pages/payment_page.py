import allure
from playwright.sync_api import expect

from .base_page import BasePage


class PaymentPage(BasePage):
    @allure.step("Ввести платёжные данные")
    def enter_card_details(self, name, number, expiry, cvv):
        self.fill(self.locator("payment-name"), name)
        self.fill(self.locator("payment-card-number"), number)
        self.fill(self.locator("payment-expiry"), expiry)
        self.fill(self.locator("payment-cvv"), cvv)
        return self

    @allure.step("Подтвердить покупку")
    def place_order(self):
        from .order_confirmation_page import OrderConfirmationPage

        self.clickable(self.locator("submit-order-button"))
        return OrderConfirmationPage(
            self.driver, self.base_url
        ).should_be_open()

    @allure.step("Попытаться разместить заказ")
    def try_to_place_order(self):
        self.clickable(self.locator("submit-order-button"))
        return self

    @allure.step("Проверить ошибку номера карты")
    def should_show_card_number_error(self):
        expect(
            self.locator("field-error-payment-card-number")
        ).to_contain_text("16 digits")
        return self