import allure
from playwright.sync_api import expect

from .base_page import BasePage


class ProductsPage(BasePage):
    @allure.step("Проверить каталог товаров")
    def should_be_open(self):
        self.wait_for_path("/")
        self.visible(self.locator("product-grid"))
        expect(self.locator("product-count")).not_to_contain_text(
            "Loading..."
        )
        return self

    @allure.step("Открыть товар {product_id}")
    def open_product(self, product_id):
        from .product_detail_page import ProductDetailPage

        self.clickable(self.locator(f"product-card-{product_id}"))
        return ProductDetailPage(
            self.driver, self.base_url
        ).should_be_open(product_id)

    @allure.step("Найти товары по запросу {query}")
    def search_for(self, query):
        self.fill(self.locator("search-input"), query)
        return self

    @allure.step("Проверить отсутствие найденных товаров")
    def should_have_no_results(self):
        self.visible(self.locator("no-products"))
        expect(self.locator("product-count")).to_contain_text(
            "0 products found"
        )
        return self