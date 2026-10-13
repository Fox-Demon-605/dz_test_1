import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class PaymentPage(BasePage):
    CARD_NAME = (By.CSS_SELECTOR, '[data-testid="payment-name"]')
    CARD_NUMBER = (
        By.CSS_SELECTOR,
        '[data-testid="payment-card-number"]',
    )
    EXPIRY = (By.CSS_SELECTOR, '[data-testid="payment-expiry"]')
    CVV = (By.CSS_SELECTOR, '[data-testid="payment-cvv"]')
    PLACE_ORDER = (
        By.CSS_SELECTOR,
        '[data-testid="submit-order-button"]',
    )
    CARD_ERROR = (
        By.CSS_SELECTOR,
        '[data-testid="field-error-payment-card-number"]',
    )

    @allure.step("Ввести платёжные данные")
    def enter_card_details(self, name, number, expiry, cvv):
        self.fill(self.CARD_NAME, name)
        self.fill(self.CARD_NUMBER, number)
        self.fill(self.EXPIRY, expiry)
        self.fill(self.CVV, cvv)
        return self

    @allure.step("Подтвердить покупку")
    def place_order(self):
        from .order_confirmation_page import OrderConfirmationPage

        self.click(self.PLACE_ORDER)
        return OrderConfirmationPage(
            self.driver, self.base_url
        ).should_be_open()

    @allure.step("Попытаться разместить заказ")
    def try_to_place_order(self):
        self.click(self.PLACE_ORDER)
        return self

    @allure.step("Проверить ошибку номера карты")
    def should_show_card_number_error(self):
        assert "16 digits" in self.text(self.CARD_ERROR)
        return self