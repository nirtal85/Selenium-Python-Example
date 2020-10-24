import allure
from pages.basepage import BasePage


class TopMenuBar(BasePage):
    """Top menu bar - The bar that appears on the top of the page prior to login """

    def __init__(self):
        super().__init__()
        self.login_link = "[href='https://app.involve.me/login']"
        self.register_link = "#frontend-navbar-collapse [href='https://app.involve.me/register']"

    @allure.step("Click Login button")
    def click_login(self):
        self._click(self.login_link)

    @allure.step("Click Register button")
    def click_register(self):
        self._click(self.register_link)
