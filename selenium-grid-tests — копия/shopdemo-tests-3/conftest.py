import json
import logging
import os
from pathlib import Path

import allure
import pytest


LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent
METRICS_DIR = PROJECT_ROOT / "artifacts" / "metrics"


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://localhost:3000").rstrip("/")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 1000},
    }


@pytest.fixture
def driver(request, page):
    console_messages = []
    page_errors = []
    network_events = []

    # Аналог требования «неявное ожидание = 0» для Playwright.
    # Явные ожидания указаны в Page Object.
    page.set_default_timeout(0)
    page.set_default_navigation_timeout(15_000)

    page.on(
        "console",
        lambda message: console_messages.append(
            {"type": message.type, "text": message.text}
        ),
    )
    page.on("pageerror", lambda error: page_errors.append(str(error)))

    # Не сохраняем тела запросов и заголовки: в них могут быть пароли и токены.
    page.on(
        "request",
        lambda req: network_events.append(
            {
                "event": "request",
                "method": req.method,
                "url": req.url.split("?")[0],
            }
        ),
    )
    page.on(
        "response",
        lambda response: network_events.append(
            {
                "event": "response",
                "status": response.status,
                "url": response.url.split("?")[0],
            }
        ),
    )

    request.node._playwright_page = page
    request.node._console_messages = console_messages
    request.node._page_errors = page_errors
    request.node._network_events = network_events
    request.node._metrics = []

    yield page

    # Сначала сохраняем метрики, затем закрываем страницу.
    metrics = request.node._metrics
    if metrics:
        METRICS_DIR.mkdir(parents=True, exist_ok=True)
        browser_name = request.node.funcargs.get("browser_name", "browser")
        test_name = request.node.name.replace("/", "_").replace("\\", "_")
        metrics_file = METRICS_DIR / f"{test_name}-{browser_name}.json"
        metrics_file.write_text(
            json.dumps(metrics, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        allure.attach(
            json.dumps(metrics, ensure_ascii=False, indent=2),
            name="Метрики теста",
            attachment_type=allure.attachment_type.JSON,
        )

    if not page.is_closed():
        page.close()


def _attach_json(data, name):
    try:
        allure.attach(
            json.dumps(data, ensure_ascii=False, indent=2),
            name=name,
            attachment_type=allure.attachment_type.JSON,
        )
    except Exception:
        LOGGER.exception("Не удалось прикрепить %s", name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = getattr(item, "_playwright_page", None)
    if page is None:
        return

    try:
        if not page.is_closed():
            allure.attach(
                page.screenshot(full_page=True),
                name="Скриншот при падении",
                attachment_type=allure.attachment_type.PNG,
            )
    except Exception:
        LOGGER.exception("Не удалось снять скриншот")

    _attach_json(
        getattr(item, "_console_messages", []),
        "Логи консоли браузера",
    )
    _attach_json(
        getattr(item, "_page_errors", []),
        "Ошибки страницы",
    )
    _attach_json(
        getattr(item, "_network_events", []),
        "Сетевые запросы и ответы",
    )