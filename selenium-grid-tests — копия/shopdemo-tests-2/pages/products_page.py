from playwright.async_api import expect

from .base_page import BasePage


class ProductsPage(BasePage):
    async def should_be_open(self):
        await self.wait_for_path("/")
        await self.visible(self.locator("product-grid"))
        await expect(self.locator("product-count")).not_to_contain_text(
            "Loading..."
        )
        return self

    async def open_product(self, product_id):
        from .product_detail_page import ProductDetailPage

        await self.clickable(self.locator(f"product-card-{product_id}"))
        page = ProductDetailPage(self.driver, self.base_url)
        return await page.should_be_open(product_id)

    async def search_for(self, query):
        await self.fill(self.locator("search-input"), query)
        return self

    async def should_have_no_results(self):
        await self.visible(self.locator("no-products"))
        await expect(self.locator("product-count")).to_contain_text(
            "0 products found"
        )
        return self