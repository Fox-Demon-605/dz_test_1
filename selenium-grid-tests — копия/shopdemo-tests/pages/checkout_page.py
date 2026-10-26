import allure

from .base_page import BasePage


class CheckoutPage(BasePage):
    @allure.step("Проверить страницу оформления заказа")
    def should_be_open(self):
        self.wait_for_path("/checkout")
        self.visible(self.locator("checkout-form"))
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

        self.fill(self.locator("shipping-first-name"), first_name)
        self.fill(self.locator("shipping-last-name"), last_name)
        self.fill(self.locator("shipping-email"), email)
        self.fill(self.locator("shipping-address"), address)
        self.fill(self.locator("shipping-city"), city)
        self.fill(self.locator("shipping-state"), state)
        self.fill(self.locator("shipping-zip"), zip_code)

        # PaymentPage — компонент этой же страницы /checkout.
        return PaymentPage(self.driver, self.base_url)