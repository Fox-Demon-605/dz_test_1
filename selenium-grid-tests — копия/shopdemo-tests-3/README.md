UI-тесты интернет-магазина
Проект автоматизированных UI-тестов интернет-магазина на Python, pytest и Playwright. Результаты тестов собираются для Allure.

Тесты проверяют регистрацию и авторизацию, работу с каталогом и корзиной, оформление заказа, валидацию форм и отдельные сценарии безопасности.

Структура проекта
.
├── pages/
│   ├── base_page.py
│   ├── registration_page.py
│   ├── signup_page.py
│   ├── main_page.py
│   ├── login_page.py
│   ├── products_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── payment_page.py
│   └── order_confirmation_page.py
├── tests/
│   ├── test_registration.py
│   ├── test_auth.py
│   └── test_purchase.py
├── conftest.py
└── pytest.ini

BasePage содержит общие действия с элементами. Остальные классы в pages/ описывают страницы приложения. Тесты используют Page Object для выполнения пользовательских сценариев.

Требования
Python и pip;
запущенное тестируемое приложение;
пакеты pytest, pytest-playwright, playwright, allure-pytest;
Chromium и Firefox, установленные через Playwright;
Allure CLI для просмотра отчёта.
Установка
Windows PowerShell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pytest pytest-playwright playwright allure-pytest
python -m playwright install chromium firefox

Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest pytest-playwright playwright allure-pytest
python -m playwright install chromium firefox

Настройка окружения
Перед запуском тестов приложение должно быть запущено. По умолчанию используется адрес http://localhost:3000. Чтобы указать другой адрес, задайте переменную окружения BASE_URL.

Windows PowerShell:

$env:BASE_URL = "http://localhost:3000"

Linux / macOS:

export BASE_URL="http://localhost:3000"

Параметр	Значение
Браузеры	Chromium и Firefox
Размер окна	1440 × 1000
Таймаут операций Page Object	15 000 мс
Таймаут навигации	15 000 мс
Результаты Allure	artifacts/allure-results
JSON-метрики	artifacts/metrics
Запуск тестов
Все тесты:

python -m pytest

Тесты регистрации:

python -m pytest tests/test_registration.py

Запуск по маркерам:

python -m pytest -m security
python -m pytest -m smoke
python -m pytest -m auth
python -m pytest -m purchase

Тестовые сценарии
Авторизация
регистрация и проверка приветствия;
успешный вход;
вход с неверным паролем;
выход из аккаунта;
отказ в регистрации при несовпадающих паролях.
Для проверки входа используется учётная запись demo@shopdemo.com. Она должна существовать в тестовом приложении.

Регистрация
успешная регистрация;
проверка пустого имени, email, пароля и подтверждения пароля;
проверка некорректного email;
проверка отсутствия пароля в URL, сообщениях консоли и URL сетевых запросов;
проверка безопасного отображения введённого имени.
Покупка
добавление товара в корзину;
проверка количества товара;
успешное оформление заказа;
отклонение некорректного номера карты.
Метрики и отчёты
Для сценариев регистрации измеряется время загрузки страницы, заполнения формы и ожидания результата после отправки. Метрики сохраняются в JSON-файлы в artifacts/metrics и прикрепляются к Allure.

Результаты тестов сохраняются в artifacts/allure-results. Для просмотра отчёта выполните:

allure serve artifacts/allure-results

При падении теста к результатам прикрепляются скриншот, сообщения консоли, ошибки страницы и сетевые события. Тела и заголовки запросов не сохраняются; из URL сетевых событий удаляются параметры запроса.