from urllib.parse import urlparse

import allure
from playwright.sync_api import Page, expect


class BasePage:
    TIMEOUT = 15_000

    def __init__(self, driver: Page, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.driver.set_default_timeout(self.TIMEOUT)

    def locator(self, test_id: str):
        return self.driver.get_by_test_id(test_id)

    @allure.step("Открыть страницу {path}")
    def open(self, path="/"):
        self.driver.goto(f"{self.base_url}{path}")
        return self

    def visible(self, locator):
        expect(locator).to_be_visible(timeout=self.TIMEOUT)
        return locator

    def clickable(self, locator):
        expect(locator).to_be_enabled(timeout=self.TIMEOUT)
        locator.click()

    def fill(self, locator, value):
        locator.fill(str(value))

    def text(self, locator):
        self.visible(locator)
        return locator.inner_text()

    def wait_for_path(self, path):
        self.driver.wait_for_url(
            lambda url: urlparse(str(url)).path == path,
            timeout=self.TIMEOUT,
        )
        return self

    def wait_for_path_prefix(self, prefix):
        self.driver.wait_for_url(
            lambda url: urlparse(str(url)).path.startswith(prefix),
            timeout=self.TIMEOUT,
        )
        return self