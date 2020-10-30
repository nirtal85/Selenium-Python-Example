import allure

from pages.base_page import BasePage


class AboutPage(BasePage):
    """ About page - The first page that appears when navigating to base URL"""

    _login_link = ".login"
    _register_link = ".register"

    def __init__(self):
        super().__init__()

    @allure.step("Click Login link")
    def click_login_link(self):
        self.click(self._login_link)

    @allure.step("Click Register link")
    def click_register_link(self):
        self.click(self._register_link)
