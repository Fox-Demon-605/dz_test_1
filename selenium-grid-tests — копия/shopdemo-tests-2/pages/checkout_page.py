from .base_page import BasePage


class CheckoutPage(BasePage):
    async def should_be_open(self):
        await self.wait_for_path("/checkout")
        await self.visible(self.locator("checkout-form"))
        return self

    async def enter_shipping_details(
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

        await self.fill(self.locator("shipping-first-name"), first_name)
        await self.fill(self.locator("shipping-last-name"), last_name)
        await self.fill(self.locator("shipping-email"), email)
        await self.fill(self.locator("shipping-address"), address)
        await self.fill(self.locator("shipping-city"), city)
        await self.fill(self.locator("shipping-state"), state)
        await self.fill(self.locator("shipping-zip"), zip_code)

        return PaymentPage(self.driver, self.base_url)