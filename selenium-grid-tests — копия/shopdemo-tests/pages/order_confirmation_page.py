import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage


class OrderConfirmationPage(BasePage):
    CONFIRMATION = (
        By.CSS_SELECTOR,
        '[data-testid="order-confirmation"]',
    )
    ORDER_ID = (By.CSS_SELECTOR, '[data-testid="order-id"]')

    @allure.step("Проверить подтверждение заказа")
    def should_be_open(self):
        self.wait_for_path("/order-confirmation")
        self.visible(self.CONFIRMATION)
        assert self.text(self.ORDER_ID).strip()
        return self