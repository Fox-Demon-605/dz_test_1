import asyncio
import json
import threading
from concurrent.futures import Future

import allure
import pytest
from playwright.async_api import async_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:3000",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=("chromium", "firefox", "webkit"),
    )


@pytest.fixture(scope="session")
def async_runner():
    loop = asyncio.new_event_loop()
    ready = threading.Event()

    def run_loop():
        asyncio.set_event_loop(loop)
        ready.set()
        loop.run_forever()

    thread = threading.Thread(
        target=run_loop,
        name="playwright-event-loop",
        daemon=True,
    )
    thread.start()
    ready.wait()

    def run(coroutine):
        future: Future = asyncio.run_coroutine_threadsafe(coroutine, loop)
        return future.result()

    try:
        yield run
    finally:
        loop.call_soon_threadsafe(loop.stop)
        thread.join()
        loop.close()


@pytest.fixture(scope="session")
def browser(async_runner, request):
    async def start():
        playwright = await async_playwright().start()
        browser_name = request.config.getoption("--browser")
        instance = await getattr(playwright, browser_name).launch()
        return playwright, instance

    playwright, instance = async_runner(start())

    try:
        yield instance
    finally:
        async_runner(instance.close())
        async_runner(playwright.stop())


@pytest.fixture
def driver(async_runner, browser, request):
    async def start():
        context = await browser.new_context(
            viewport={"width": 1440, "height": 1000},
        )
        page = await context.new_page()
        return context, page

    context, page = async_runner(start())

    console_messages = []
    page_errors = []
    network_events = []

    def subscribe():
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
            lambda browser_request: network_events.append(
                {
                    "event": "request",
                    "method": browser_request.method,
                    "url": browser_request.url,
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

    async def subscribe_in_loop():
        subscribe()

    async_runner(subscribe_in_loop())

    yield page

    report = getattr(request.node, "rep_call", None)

    if report is not None and report.failed:
        try:
            screenshot = async_runner(page.screenshot())
            allure.attach(
                screenshot,
                name="Скриншот при падении",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as error:
            page_errors.append(f"Не удалось сделать скриншот: {error}")

        for data, name in (
            (console_messages, "Сообщения консоли"),
            (page_errors, "Ошибки страницы"),
            (network_events, "Сетевые события"),
        ):
            allure.attach(
                json.dumps(data, ensure_ascii=False, indent=2),
                name=name,
                attachment_type=allure.attachment_type.JSON,
            )

    async_runner(context.close())


@pytest.fixture
def app_url(request):
    return request.config.getoption("--base-url").rstrip("/")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)