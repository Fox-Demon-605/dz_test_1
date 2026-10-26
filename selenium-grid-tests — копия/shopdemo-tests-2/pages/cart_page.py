from playwright.async_api import expect

from .base_page import BasePage


class CartPage(BasePage):
    def _items(self):
        return self.driver.locator('[data-testid^="cart-item-cart-"]')

    async def should_be_open(self):
        await self.wait_for_path("/cart")
        await expect(
            self.locator("checkout-button")
            .or_(self.locator("empty-cart-message"))
            .first
        ).to_be_visible()
        return self

    async def should_contain_product(self, product_name, quantity):
        row = self._items().filter(has_text=product_name).first
        await expect(row).to_be_visible()
        await expect(
            row.locator('[data-testid^="cart-item-quantity-"]')
        ).to_have_text(str(quantity))
        return self

    async def should_have_total(self, expected_total):
        await expect(self.locator("cart-total")).to_have_text(
            expected_total
        )
        return self

    async def proceed_to_checkout(self):
        from .checkout_page import CheckoutPage

        await self.clickable(self.locator("checkout-button"))
        page = CheckoutPage(self.driver, self.base_url)
        return await page.should_be_open()