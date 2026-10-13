import json
import logging

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

LOGGER = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:3000",
        help="URL ShopDemo, видимый браузеру Selenium Grid",
    )
    parser.addoption(
        "--grid-url",
        action="store",
        default="http://localhost:4444",
        help="Адрес Selenium Grid",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Браузер для тестов",
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")


@pytest.fixture
def grid_url(request):
    return request.config.getoption("--grid-url").rstrip("/")


@pytest.fixture
def driver(request, base_url, grid_url):
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        options = ChromeOptions()
        options.set_capability(
            "goog:loggingPrefs",
            {"browser": "ALL", "performance": "ALL"},
        )
    else:
        options = FirefoxOptions()

    options.add_argument("--width=1440")
    options.add_argument("--height=1000")

    web_driver = webdriver.Remote(
        command_executor=grid_url,
        options=options,
    )
    web_driver.implicitly_wait(0)

    request.node._web_driver = web_driver

    try:
        yield web_driver
    finally:
        web_driver.quit()


def _attach_logs(driver, log_type, attachment_name):
    try:
        available_types = driver.log_types
        if log_type not in available_types:
            LOGGER.info("Тип логов %s недоступен в этой сессии", log_type)
            return

        entries = driver.get_log(log_type)
        allure.attach(
            json.dumps(entries, ensure_ascii=False, indent=2),
            name=attachment_name,
            attachment_type=allure.attachment_type.JSON,
        )
    except Exception:
        LOGGER.exception("Не удалось получить логи %s", log_type)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver = getattr(item, "_web_driver", None)
    if driver is None:
        return

    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Скриншот при падении",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        LOGGER.exception("Не удалось снять скриншот")

    _attach_logs(driver, "browser", "Логи браузера")

    if driver.capabilities.get("browserName", "").lower() == "chrome":
        _attach_logs(
            driver,
            "performance",
            "Chrome performance logs — Network events",
        )