from urllib.parse import urlparse

import allure
from playwright.sync_api import Page, expect


class BasePage:
    TIMEOUT = 15_000

    def __init__(self, driver: Page, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    @allure.step("Найти элемент по data-testid: {test_id}")
    def locator(self, test_id: str):
        return self.driver.get_by_test_id(test_id)

    @allure.step("Открыть страницу {path}")
    def open(self, path="/"):
        self.driver.goto(
            f"{self.base_url}{path}",
            timeout=self.TIMEOUT,
        )
        return self

    @allure.step("Дождаться видимости элемента")
    def visible(self, locator):
        expect(locator).to_be_visible(timeout=self.TIMEOUT)
        return locator

    @allure.step("Нажать на элемент")
    def clickable(self, locator):
        expect(locator).to_be_visible(timeout=self.TIMEOUT)
        expect(locator).to_be_enabled(timeout=self.TIMEOUT)
        locator.click(timeout=self.TIMEOUT)
        return self

    @allure.step("Заполнить поле")
    def fill(self, locator, value):
        expect(locator).to_be_visible(timeout=self.TIMEOUT)
        locator.fill(str(value), timeout=self.TIMEOUT)
        return self

    @allure.step("Получить текст элемента")
    def text(self, locator):
        self.visible(locator)
        return locator.inner_text(timeout=self.TIMEOUT)

    @allure.step("Дождаться пути {path}")
    def wait_for_path(self, path):
        self.driver.wait_for_url(
            lambda url: urlparse(str(url)).path == path,
            timeout=self.TIMEOUT,
        )
        return self

    @allure.step("Дождаться пути с префиксом {prefix}")
    def wait_for_path_prefix(self, prefix):
        self.driver.wait_for_url(
            lambda url: urlparse(str(url)).path.startswith(prefix),
            timeout=self.TIMEOUT,
        )
        return self