from playwright.async_api import expect

from .base_page import BasePage


class SignupPage(BasePage):
    async def should_be_open(self):
        await self.wait_for_path("/signup")
        await self.visible(self.locator("signup-heading"))
        return self

    async def _fill_form(self, name, email, password, confirmation):
        await self.fill(self.locator("signup-name"), name)
        await self.fill(self.locator("signup-email"), email)
        await self.fill(self.locator("signup-password"), password)
        await self.fill(
            self.locator("signup-confirm-password"),
            confirmation,
        )

    async def register(self, name, email, password):
        from .main_page import MainPage

        await self._fill_form(name, email, password, password)
        await self.clickable(self.locator("signup-submit-button"))
        page = MainPage(self.driver, self.base_url)
        return await page.should_be_open()

    async def try_register_with_password_mismatch(
        self, name, email, password, confirmation
    ):
        await self._fill_form(name, email, password, confirmation)
        await self.clickable(self.locator("signup-submit-button"))
        return self

    async def should_show_password_mismatch(self):
        await expect(
            self.locator("field-error-signup-confirm-password")
        ).to_contain_text("Passwords do not match")
        return self