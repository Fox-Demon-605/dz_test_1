import allure
import pytest

from pages.main_page import MainPage


def checkout_with_shipping(driver, base_url, quantity=1):
    return (
        MainPage(driver, base_url)
        .open()
        .should_be_open()
        .browse_products()
        .open_product("prod-001")
        .add_to_cart(quantity=quantity)
        .go_to_cart()
        .proceed_to_checkout()
        .enter_shipping_details(
            first_name="Test",
            last_name="Student",
            email="student@example.com",
            address="123 Test Street",
            city="Boston",
            state="MA",
            zip_code="02108",
        )
    )


@allure.feature("Покупка")
@allure.story("Корзина")
@allure.title("Товар добавляется в корзину")
@pytest.mark.purchase
@pytest.mark.smoke
def test_12_add_product_to_cart(driver, base_url):
    (
        MainPage(driver, base_url)
        .open()
        .should_be_open()
        .browse_products()
        .open_product("prod-001")
        .add_to_cart()
        .go_to_cart()
        .should_contain_product("Wireless Headphones", 1)
    )


@allure.feature("Покупка")
@allure.story("Количество товара")
@allure.title("В корзине отображается выбранное количество товара")
@pytest.mark.purchase
def test_13_product_quantity_in_cart(driver, base_url):
    (
        MainPage(driver, base_url)
        .open()
        .should_be_open()
        .browse_products()
        .open_product("prod-001")
        .add_to_cart(quantity=3)
        .go_to_cart()
        .should_contain_product("Wireless Headphones", 3)
    )


@allure.feature("Покупка")
@allure.story("Оформление заказа")
@allure.title("Покупатель успешно оформляет заказ")
@pytest.mark.purchase
@pytest.mark.smoke
def test_14_place_order(driver, base_url):
    (
        checkout_with_shipping(driver, base_url)
        .enter_card_details(
            name="Test Student",
            number="4111111111111111",
            expiry="12/29",
            cvv="123",
        )
        .place_order()
    )


@allure.feature("Покупка")
@allure.story("Валидация оплаты")
@allure.title("Заказ не оформляется при неверном номере карты")
@pytest.mark.purchase
def test_15_reject_invalid_card(driver, base_url):
    (
        checkout_with_shipping(driver, base_url)
        .enter_card_details(
            name="Test Student",
            number="123",
            expiry="12/29",
            cvv="123",
        )
        .try_to_place_order()
        .should_show_card_number_error()
    )