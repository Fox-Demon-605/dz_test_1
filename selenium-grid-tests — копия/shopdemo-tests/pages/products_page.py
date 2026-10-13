import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class ProductsPage(BasePage):
    SEARCH = (By.CSS_SELECTOR, '[data-testid="search-input"]')
    PRODUCT_COUNT = (By.CSS_SELECTOR, '[data-testid="product-count"]')
    PRODUCT_GRID = (By.CSS_SELECTOR, '[data-testid="product-grid"]')
    NO_PRODUCTS = (By.CSS_SELECTOR, '[data-testid="no-products"]')

    @allure.step("Проверить каталог товаров")
    def should_be_open(self):
        self.wait_for_path("/")
        self.visible(self.PRODUCT_GRID)
        self.wait.until(
            lambda driver: "Loading..." not in driver.find_element(
                *self.PRODUCT_COUNT
            ).text
        )
        return self

    @allure.step("Открыть товар {product_id}")
    def open_product(self, product_id):
        from .product_detail_page import ProductDetailPage

        locator = (
            By.CSS_SELECTOR,
            f'[data-testid="product-card-{product_id}"]',
        )
        self.click(locator)
        return ProductDetailPage(
            self.driver, self.base_url
        ).should_be_open(product_id)

    @allure.step("Найти товары по запросу {query}")
    def search_for(self, query):
        self.fill(self.SEARCH, query)
        return self

    @allure.step("Проверить отсутствие найденных товаров")
    def should_have_no_results(self):
        self.visible(self.NO_PRODUCTS)
        self.wait.until(
            EC.text_to_be_present_in_element(
                self.PRODUCT_COUNT,
                "0 products found",
            )
        )
        return self