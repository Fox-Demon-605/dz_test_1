from time import perf_counter
from urllib.parse import urlparse

import allure
from playwright.sync_api import expect

from .base_page import BasePage


class RegistrationPage(BasePage):
    def __init__(self, driver, base_url, metrics=None):
        super().__init__(driver, base_url)
        self.metrics = metrics if metrics is not None else []

    def _record_metric(self, operation, started_at):
        self.metrics.append(
            {
                "operation": operation,
                "duration_ms": round(
                    (perf_counter() - started_at) * 1000, 2
                ),
            }
        )

    @allure.step("Открыть страницу регистрации и измерить время загрузки")
    def open_registration(self):
        started_at = perf_counter()
        self.open("/signup")
        self.should_be_open()
        self._record_metric("registration_page_load", started_at)
        return self

    @allure.step("Проверить страницу регистрации")
    def should_be_open(self):
        self.wait_for_path("/signup")
        self.visible(self.locator("signup-heading"))
        return self

    @allure.step("Заполнить форму регистрации")
    def fill_registration(self, name, email, password, confirmation):
        started_at = perf_counter()
        self.fill(self.locator("signup-name"), name)
        self.fill(self.locator("signup-email"), email)
        self.fill(self.locator("signup-password"), password)
        self.fill(
            self.locator("signup-confirm-password"),
            confirmation,
        )
        self._record_metric("registration_form_fill", started_at)
        return self

    @allure.step("Отправить форму регистрации и измерить время отклика")
    def submit(self):
        started_at = perf_counter()
        self.clickable(self.locator("signup-submit-button"))

        # Фиксируем отклик как появление известной ошибки либо переход
        # на главную после успешной регистрации.
        self.driver.wait_for_function(
            """() =>
                location.pathname === "/" ||
                !!document.querySelector(
                    '[data-testid="field-error-signup-confirm-password"]'
                ) ||
                !!document.querySelector(
                    '[data-testid^="field-error-signup-"]'
                ) ||
                !!document.querySelector(
                    '[data-testid="signup-error"]'
                )
            """,
            timeout=self.TIMEOUT,
        )
        self._record_metric("registration_form_response", started_at)
        return self

    @allure.step("Проверить успешную регистрацию пользователя {name}")
    def should_register_user(self, name):
        self.wait_for_path("/")
        expect(self.locator("user-greeting")).to_have_text(
            f"Hi, {name}",
            timeout=self.TIMEOUT,
        )
        return self

    @allure.step("Проверить, что регистрация отклонена")
    def should_stay_on_registration(self):
        expect(self.driver).to_have_url(
            f"{self.base_url}/signup",
            timeout=self.TIMEOUT,
        )
        expect(self.locator("signup-heading")).to_be_visible(
            timeout=self.TIMEOUT
        )
        return self

    @allure.step("Проверить ошибку несовпадения паролей")
    def should_show_password_mismatch(self):
        expect(
            self.locator("field-error-signup-confirm-password")
        ).to_contain_text(
            "Passwords do not match",
            timeout=self.TIMEOUT,
        )
        return self

    @allure.step("Проверить ошибку валидации поля {test_id}")
    def should_show_field_error(self, test_id):
        error = self.locator(f"field-error-{test_id}")
        expect(error).to_be_visible(timeout=self.TIMEOUT)
        expect(error).not_to_be_empty(timeout=self.TIMEOUT)
        return self

    @allure.step("Проверить, что текст имени отображается безопасно")
    def should_greet_as_plain_text(self, name):
        self.should_register_user(name)
        greeting = self.locator("user-greeting")

        expect(greeting).to_have_text(
            f"Hi, {name}",
            timeout=self.TIMEOUT,
        )
        assert greeting.locator("script, img, svg").count() == 0, (
            "Имя пользователя не должно создавать HTML-элементы"
        )
        return self

    @allure.step("Проверить, что пароль не попал в адрес страницы")
    def should_not_expose_password_in_url(self, password):
        url = self.driver.url
        parsed = urlparse(url)
        assert password not in url, "Пароль обнаружен в URL"
        assert not parsed.username and not parsed.password, (
            "Учётные данные обнаружены в URL"
        )
        return self

    @allure.step("Проверить, что пароль не отображается в консоли и URL запросов")
    def should_not_expose_password_in_diagnostics(
        self, password, console_messages, network_events
    ):
        console_text = str(console_messages)
        network_urls = " ".join(
            event.get("url", "") for event in network_events
        )
        assert password not in console_text, (
            "Пароль обнаружен в логах консоли"
        )
        assert password not in network_urls, (
            "Пароль обнаружен в URL сетевого запроса"
        )
        return self