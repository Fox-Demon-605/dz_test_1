import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class CheckoutPage(BasePage):
    FORM = (By.CSS_SELECTOR, '[data-testid="checkout-form"]')

    FIRST_NAME = (
        By.CSS_SELECTOR,
        '[data-testid="shipping-first-name"]',
    )
    LAST_NAME = (
        By.CSS_SELECTOR,
        '[data-testid="shipping-last-name"]',
    )
    EMAIL = (By.CSS_SELECTOR, '[data-testid="shipping-email"]')
    ADDRESS = (By.CSS_SELECTOR, '[data-testid="shipping-address"]')
    CITY = (By.CSS_SELECTOR, '[data-testid="shipping-city"]')
    STATE = (By.CSS_SELECTOR, '[data-testid="shipping-state"]')
    ZIP = (By.CSS_SELECTOR, '[data-testid="shipping-zip"]')

    @allure.step("Проверить страницу оформления заказа")
    def should_be_open(self):
        self.wait_for_path("/checkout")
        self.visible(self.FORM)
        return self

    @allure.step("Заполнить данные доставки")
    def enter_shipping_details(
        self,
        first_name,
        last_name,
        email,
        address,
        city,
        state,
        zip_code,
    ):
        from .payment_page import PaymentPage

        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.EMAIL, email)
        self.fill(self.ADDRESS, address)
        self.fill(self.CITY, city)
        self.fill(self.STATE, state)
        self.fill(self.ZIP, zip_code)

        return PaymentPage(self.driver, self.base_url)