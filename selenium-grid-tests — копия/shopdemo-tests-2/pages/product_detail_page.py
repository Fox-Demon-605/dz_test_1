from .base_page import BasePage


class ProductDetailPage(BasePage):
    async def should_be_open(self, product_id):
        await self.wait_for_path(f"/products/{product_id}")
        await self.visible(self.locator("product-name"))
        return self

    async def add_to_cart(self, quantity=1):
        await self.fill(self.locator("quantity-input"), quantity)
        await self.clickable(self.locator("add-to-cart-button"))
        await self.visible(self.locator("added-notification"))
        return self

    async def go_to_cart(self):
        from .cart_page import CartPage

        await self.clickable(self.locator("cart-link"))
        page = CartPage(self.driver, self.base_url)
        return await page.should_be_open()