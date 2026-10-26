from uuid import uuid4

import allure
from playwright.async_api import expect
from pytest_bdd import given, scenarios, then, when

from pages.main_page import MainPage


scenarios("features/shopdemo.feature")


@given("я открываю магазин", target_fixture="current_page")
def open_store(driver, app_url, async_runner):
    return async_runner(MainPage(driver, app_url).open())


@given("я открыл страницу авторизации", target_fixture="current_page")
def open_login(driver, app_url, async_runner):
    async def action():
        main_page = await MainPage(driver, app_url).open()
        return await main_page.go_to_login()

    return async_runner(action())


@given("я вошёл в аккаунт", target_fixture="current_page")
def logged_in(driver, app_url, async_runner):
    async def action():
        main_page = await MainPage(driver, app_url).open()
        login_page = await main_page.go_to_login()
        return await login_page.login_as(
            "demo@shopdemo.com",
            "Demo@123",
        )

    return async_runner(action())


@given("я открыл страницу регистрации", target_fixture="current_page")
def open_signup(driver, app_url, async_runner):
    async def action():
        main_page = await MainPage(driver, app_url).open()
        return await main_page.go_to_signup()

    return async_runner(action())


@given("я открываю каталог", target_fixture="current_page")
def open_catalog(driver, app_url, async_runner):
    async def action():
        main_page = await MainPage(driver, app_url).open()
        return await main_page.browse_products()

    return async_runner(action())


@given("я открыл карточку товара", target_fixture="current_page")
def open_product(driver, app_url, async_runner):
    async def action():
        main_page = await MainPage(driver, app_url).open()
        products_page = await main_page.browse_products()
        return await products_page.open_product("prod-001")

    return async_runner(action())


@given("я добавил товар в корзину", target_fixture="current_page")
def product_in_cart(driver, app_url, async_runner):
    async def action():
        main_page = await MainPage(driver, app_url).open()
        products_page = await main_page.browse_products()
        product_page = await products_page.open_product("prod-001")
        await product_page.add_to_cart(quantity=1)
        return await product_page.go_to_cart()

    return async_runner(action())


@when("я перехожу к авторизации", target_fixture="current_page")
def go_to_login(current_page, async_runner):
    return async_runner(current_page.go_to_login())


@when("я вхожу с корректными данными", target_fixture="current_page")
def valid_login(current_page, async_runner):
    return async_runner(
        current_page.login_as("demo@shopdemo.com", "Demo@123")
    )


@when("я вхожу с неверным паролем", target_fixture="current_page")
def invalid_login(current_page, async_runner):
    return async_runner(
        current_page.try_login_as(
            "demo@shopdemo.com",
            "wrong-password",
        )
    )


@when("я выхожу из аккаунта", target_fixture="current_page")
def logout(current_page, async_runner):
    return async_runner(current_page.logout())


@when("я перехожу к регистрации", target_fixture="current_page")
def go_to_signup(current_page, async_runner):
    return async_runner(current_page.go_to_signup())


@when("я регистрируюсь с разными паролями", target_fixture="current_page")
def register_with_different_passwords(current_page, async_runner):
    return async_runner(
        current_page.try_register_with_password_mismatch(
            name="Test Student",
            email=f"test-{uuid4().hex}@example.com",
            password="StrongPass123",
            confirmation="DifferentPass123",
        )
    )


@when("я ищу отсутствующий товар", target_fixture="current_page")
def search_missing_product(current_page, async_runner):
    return async_runner(
        current_page.search_for(f"not-existing-{uuid4().hex}")
    )


@when("я добавляю товар в корзину", target_fixture="current_page")
def add_product_to_cart(current_page, async_runner):
    async def action():
        await current_page.add_to_cart(quantity=1)
        return await current_page.go_to_cart()

    return async_runner(action())


@when(
    "я заполняю доставку и оплачиваю заказ",
    target_fixture="current_page",
)
def complete_order(current_page, async_runner):
    async def action():
        checkout_page = await current_page.proceed_to_checkout()

        payment_page = await checkout_page.enter_shipping_details(
            first_name="Test",
            last_name="Student",
            email="student@example.com",
            address="123 Test Street",
            city="Boston",
            state="MA",
            zip_code="02108",
        )

        await payment_page.enter_card_details(
            name="Test Student",
            number="4111111111111111",
            expiry="12/29",
            cvv="123",
        )

        return await payment_page.place_order()

    return async_runner(action())


@then("главная страница отображается")
def check_main(current_page, async_runner):
    with allure.step("Проверить главную страницу"):
        async_runner(current_page.should_be_open())


@then("страница авторизации отображается")
def check_login(current_page, async_runner):
    with allure.step("Проверить страницу авторизации"):
        async_runner(current_page.should_be_open())


@then("отображается приветствие пользователя")
def check_greeting(current_page, async_runner):
    with allure.step("Проверить приветствие"):
        async_runner(current_page.should_greet("Demo User"))


@then("отображается ошибка авторизации")
def check_login_error(current_page, async_runner):
    with allure.step("Проверить ошибку авторизации"):
        async_runner(
            current_page.should_show_invalid_credentials()
        )


@then("отображается ссылка для входа")
def check_logged_out(current_page, async_runner):
    with allure.step("Проверить выход из аккаунта"):
        async_runner(
            expect(
                current_page.locator("nav-login-link")
            ).to_be_visible()
        )


@then("страница регистрации отображается")
def check_signup(current_page, async_runner):
    with allure.step("Проверить страницу регистрации"):
        async_runner(current_page.should_be_open())


@then("отображается ошибка подтверждения пароля")
def check_password_mismatch(current_page, async_runner):
    with allure.step("Проверить ошибку подтверждения пароля"):
        async_runner(current_page.should_show_password_mismatch())


@then("каталог сообщает об отсутствии товаров")
def check_no_products(current_page, async_runner):
    with allure.step("Проверить отсутствие товаров"):
        async_runner(current_page.should_have_no_results())


@then("товар отображается в корзине")
def check_cart(current_page, async_runner):
    with allure.step("Проверить товар в корзине"):
        async_runner(
            current_page.should_contain_product(
                product_name="Wireless Headphones",
                quantity=1,
            )
        )


@then("отображается подтверждение заказа")
def check_order(current_page, async_runner):
    with allure.step("Проверить подтверждение заказа"):
        async_runner(current_page.should_be_open())