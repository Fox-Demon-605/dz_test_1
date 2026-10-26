from playwright.async_api import expect

from .base_page import BasePage


class MainPage(BasePage):
    async def should_be_open(self):
        await self.wait_for_path("/")
        await self.visible(self.locator("product-count"))
        return self

    async def should_greet(self, name):
        await expect(self.locator("user-greeting")).to_have_text(
            f"Hi, {name}"
        )
        return self

    async def go_to_login(self):
        from .login_page import LoginPage

        await self.clickable(self.locator("nav-login-link"))
        page = LoginPage(self.driver, self.base_url)
        return await page.should_be_open()

    async def go_to_signup(self):
        from .signup_page import SignupPage

        await self.clickable(self.locator("nav-signup-link"))
        page = SignupPage(self.driver, self.base_url)
        return await page.should_be_open()

    async def browse_products(self):
        from .products_page import ProductsPage

        page = ProductsPage(self.driver, self.base_url)
        return await page.should_be_open()

    async def go_to_cart(self):
        from .cart_page import CartPage

        await self.clickable(self.locator("cart-link"))
        page = CartPage(self.driver, self.base_url)
        return await page.should_be_open()

    async def logout(self):
        await self.clickable(self.locator("logout-button"))
        await self.visible(self.locator("nav-login-link"))
        return self