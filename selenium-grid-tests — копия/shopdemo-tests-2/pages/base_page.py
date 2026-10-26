from urllib.parse import urlparse

from playwright.async_api import Page, expect


class BasePage:
    TIMEOUT = 15_000

    def __init__(self, driver: Page, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.driver.set_default_timeout(self.TIMEOUT)

    def locator(self, test_id: str):
        return self.driver.get_by_test_id(test_id)

    async def open(self, path="/"):
        await self.driver.goto(f"{self.base_url}{path}")
        return self

    async def visible(self, locator):
        await expect(locator).to_be_visible(timeout=self.TIMEOUT)
        return locator

    async def clickable(self, locator):
        await expect(locator).to_be_enabled(timeout=self.TIMEOUT)
        await locator.click()

    async def fill(self, locator, value):
        await locator.fill(str(value))

    async def wait_for_path(self, path):
        await self.driver.wait_for_url(
            lambda url: urlparse(str(url)).path == path,
            timeout=self.TIMEOUT,
        )
        return self