from urllib.parse import urlparse

import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    TIMEOUT = 15

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    @allure.step("Открыть страницу {path}")
    def open(self, path="/"):
        self.driver.get(f"{self.base_url}{path}")
        return self

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.clickable(locator).click()

    def fill(self, locator, value):
        element = self.visible(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator):
        return self.visible(locator).text

    def wait_for_path(self, path):
        self.wait.until(
            lambda driver: urlparse(driver.current_url).path == path
        )
        return self

    def wait_for_path_prefix(self, prefix):
        self.wait.until(
            lambda driver: urlparse(driver.current_url).path.startswith(prefix)
        )
        return self