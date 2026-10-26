from playwright.async_api import expect

from .base_page import BasePage


class OrderConfirmationPage(BasePage):
    async def should_be_open(self):
        await self.wait_for_path("/order-confirmation")
        await self.visible(self.locator("order-confirmation"))
        await expect(self.locator("order-id")).not_to_be_empty()
        return self