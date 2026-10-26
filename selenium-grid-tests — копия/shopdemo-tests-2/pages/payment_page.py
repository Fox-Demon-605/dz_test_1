from playwright.async_api import expect

from .base_page import BasePage


class PaymentPage(BasePage):
    async def enter_card_details(self, name, number, expiry, cvv):
        await self.fill(self.locator("payment-name"), name)
        await self.fill(self.locator("payment-card-number"), number)
        await self.fill(self.locator("payment-expiry"), expiry)
        await self.fill(self.locator("payment-cvv"), cvv)
        return self

    async def place_order(self):
        from .order_confirmation_page import OrderConfirmationPage

        await self.clickable(self.locator("submit-order-button"))
        page = OrderConfirmationPage(self.driver, self.base_url)
        return await page.should_be_open()

    async def try_to_place_order(self):
        await self.clickable(self.locator("submit-order-button"))
        return self

    async def should_show_card_number_error(self):
        await expect(
            self.locator("field-error-payment-card-number")
        ).to_contain_text("16 digits")
        return self