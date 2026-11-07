from uuid import uuid4

import allure
import pytest

from pages.main_page import MainPage


def new_email():
    return f"student-{uuid4().hex}@example.com"


@allure.feature("Авторизация")
@allure.story("Регистрация")
@allure.title("Новый пользователь регистрируется и видит приветствие")
@pytest.mark.auth
@pytest.mark.smoke
def test_register_user(driver, base_url):
    (
        MainPage(driver, base_url)
        .open()
        .should_be_open()
        .go_to_signup()
        .register(
            name="Test Student",
            email=new_email(),
            password="StrongPass123",
        )
        .should_greet("Test Student")
    )


@allure.feature("Авторизация")
@allure.story("Вход")
@allure.title("Существующий пользователь успешно входит")
@pytest.mark.auth
@pytest.mark.smoke
def test_login_valid_user(driver, base_url):
    (
        MainPage(driver, base_url)
        .open()
        .should_be_open()
        .go_to_login()
        .login_as(
            "demo@shopdemo.com",
            "Demo@123",
        )
        .should_greet("Demo User")
    )


@allure.feature("Авторизация")
@allure.story("Вход")
@allure.title("Неверный пароль вызывает ошибку")
@pytest.mark.auth
def test_login_invalid_password(driver, base_url):
    (
        MainPage(driver, base_url)
        .open()
        .should_be_open()
        .go_to_login()
        .try_login_as(
            "demo@shopdemo.com",
            "wrong-password",
        )
        .should_show_invalid_credentials()
    )


@allure.feature("Авторизация")
@allure.story("Выход")
@allure.title("Авторизованный пользователь выходит из аккаунта")
@pytest.mark.auth
def test_logout(driver, base_url):
    (
        MainPage(driver, base_url)
        .open()
        .should_be_open()
        .go_to_login()
        .login_as(
            "demo@shopdemo.com",
            "Demo@123",
        )
        .should_greet("Demo User")
        .logout()
    )


@allure.feature("Авторизация")
@allure.story("Регистрация")
@allure.title("Разные пароли блокируют регистрацию")
@pytest.mark.auth
def test_signup_password_mismatch(driver, base_url):
    (
        MainPage(driver, base_url)
        .open()
        .should_be_open()
        .go_to_signup()
        .try_register_with_password_mismatch(
            name="Test Student",
            email=new_email(),
            password="StrongPass123",
            confirmation="DifferentPass123",
        )
        .should_show_password_mismatch()
    )