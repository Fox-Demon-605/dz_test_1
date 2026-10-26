from playwright.async_api import expect

from .base_page import BasePage


class LoginPage(BasePage):
    async def should_be_open(self):
        await self.wait_for_path("/login")
        await self.visible(self.locator("login-heading"))
        return self

    async def login_as(self, email, password):
        from .main_page import MainPage

        await self.fill(self.locator("login-email"), email)
        await self.fill(self.locator("login-password"), password)
        await self.clickable(self.locator("login-submit-button"))

        page = MainPage(self.driver, self.base_url)
        return await page.should_be_open()

    async def try_login_as(self, email, password):
        await self.fill(self.locator("login-email"), email)
        await self.fill(self.locator("login-password"), password)
        await self.clickable(self.locator("login-submit-button"))
        return self

    async def should_show_invalid_credentials(self):
        await expect(self.locator("login-error")).to_contain_text(
            "Invalid email or password"
        )
        return self