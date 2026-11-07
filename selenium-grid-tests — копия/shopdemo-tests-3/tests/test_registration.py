from uuid import uuid4

import allure
import pytest

from pages.registration_page import RegistrationPage


def unique_email():
    return f"student-{uuid4().hex}@example.com"


@pytest.fixture
def registration_page(driver, base_url, request):
    return RegistrationPage(
        driver,
        base_url,
        metrics=request.node._metrics,
    )


@allure.feature("Регистрация")
@allure.story("Успешная регистрация")
@allure.title("Новый пользователь успешно регистрируется")
@pytest.mark.auth
@pytest.mark.smoke
def test_registration_success(registration_page):
    name = "Test Student"

    (
        registration_page
        .open_registration()
        .fill_registration(
            name=name,
            email=unique_email(),
            password="StrongPass123",
            confirmation="StrongPass123",
        )
        .submit()
        .should_register_user(name)
    )


@allure.feature("Регистрация")
@allure.story("Негативные сценарии")
@allure.title("Регистрация отклонена при разных паролях")
@pytest.mark.auth
def test_registration_password_mismatch(registration_page):
    (
        registration_page
        .open_registration()
        .fill_registration(
            name="Test Student",
            email=unique_email(),
            password="StrongPass123",
            confirmation="DifferentPass123",
        )
        .submit()
        .should_stay_on_registration()
        .should_show_password_mismatch()
    )


@allure.feature("Регистрация")
@allure.story("Негативные сценарии")
@allure.title("Регистрация отклонена без имени")
@pytest.mark.auth
def test_registration_empty_name(registration_page):
    (
        registration_page
        .open_registration()
        .fill_registration(
            name="",
            email=unique_email(),
            password="StrongPass123",
            confirmation="StrongPass123",
        )
        .submit()
        .should_stay_on_registration()
        .should_show_field_error("signup-name")
    )


@allure.feature("Регистрация")
@allure.story("Негативные сценарии")
@allure.title("Регистрация отклонена без email")
@pytest.mark.auth
def test_registration_empty_email(registration_page):
    (
        registration_page
        .open_registration()
        .fill_registration(
            name="Test Student",
            email="",
            password="StrongPass123",
            confirmation="StrongPass123",
        )
        .submit()
        .should_stay_on_registration()
        .should_show_field_error("signup-email")
    )


@allure.feature("Регистрация")
@allure.story("Негативные сценарии")
@allure.title("Регистрация отклонена при некорректном email")
@pytest.mark.auth
def test_registration_invalid_email(registration_page):
    (
        registration_page
        .open_registration()
        .fill_registration(
            name="Test Student",
            email="not-an-email",
            password="StrongPass123",
            confirmation="StrongPass123",
        )
        .submit()
        .should_stay_on_registration()
        .should_show_field_error("signup-email")
    )


@allure.feature("Регистрация")
@allure.story("Негативные сценарии")
@allure.title("Регистрация отклонена без пароля")
@pytest.mark.auth
def test_registration_empty_password(registration_page):
    (
        registration_page
        .open_registration()
        .fill_registration(
            name="Test Student",
            email=unique_email(),
            password="",
            confirmation="",
        )
        .submit()
        .should_stay_on_registration()
        .should_show_field_error("signup-password")
    )


@allure.feature("Регистрация")
@allure.story("Негативные сценарии")
@allure.title("Регистрация отклонена без подтверждения пароля")
@pytest.mark.auth
def test_registration_empty_confirmation(registration_page):
    (
        registration_page
        .open_registration()
        .fill_registration(
            name="Test Student",
            email=unique_email(),
            password="StrongPass123",
            confirmation="",
        )
        .submit()
        .should_stay_on_registration()
        .should_show_field_error("signup-confirm-password")
    )


@allure.feature("Регистрация")
@allure.story("Безопасность")
@allure.title("Пароль не появляется в URL и диагностике")
@pytest.mark.auth
@pytest.mark.security
def test_registration_password_not_exposed(
    registration_page, request
):
    password = f"StrongPass-{uuid4().hex}"

    (
        registration_page
        .open_registration()
        .fill_registration(
            name="Test Student",
            email=unique_email(),
            password=password,
            confirmation=password,
        )
        .submit()
        .should_register_user("Test Student")
        .should_not_expose_password_in_url(password)
        .should_not_expose_password_in_diagnostics(
            password,
            request.node._console_messages,
            request.node._network_events,
        )
    )


@allure.feature("Регистрация")
@allure.story("Безопасность")
@allure.title("Имя пользователя отображается как текст, а не как HTML")
@pytest.mark.auth
@pytest.mark.security
def test_registration_name_is_not_rendered_as_html(registration_page):
    name = "Test <script>window.__xss_test = 1</script>"

    (
        registration_page
        .open_registration()
        .fill_registration(
            name=name,
            email=unique_email(),
            password="StrongPass123",
            confirmation="StrongPass123",
        )
        .submit()
        .should_greet_as_plain_text(name)
    )