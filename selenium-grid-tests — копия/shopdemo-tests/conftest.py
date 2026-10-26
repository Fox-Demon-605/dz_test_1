import json
import logging

import allure
import pytest


LOGGER = logging.getLogger(__name__)


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

    page.on(
        "console",
        lambda message: console_messages.append(
            {"type": message.type, "text": message.text}
        ),
    )
    page.on(
        "pageerror",
        lambda error: page_errors.append(str(error)),
    )
    page.on(
        "request",
        lambda req: network_events.append(
            {
                "event": "request",
                "method": req.method,
                "url": req.url,
            }
        ),
    )
    page.on(
        "response",
        lambda response: network_events.append(
            {
                "event": "response",
                "status": response.status,
                "url": response.url,
            }
        ),
    )

    request.node._playwright_page = page
    request.node._console_messages = console_messages
    request.node._page_errors = page_errors
    request.node._network_events = network_events

    return page


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
        allure.attach(
            page.screenshot(full_page=True),
            name="Скриншот при падении",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        LOGGER.exception("Не удалось снять скриншот")

    _attach_json(
        getattr(item, "_console_messages", []),
        "Сообщения консоли",
    )
    _attach_json(
        getattr(item, "_page_errors", []),
        "Ошибки страницы",
    )
    _attach_json(
        getattr(item, "_network_events", []),
        "Сетевые события",
    )