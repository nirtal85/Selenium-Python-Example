import allure

from pages.basepage import BasePage


class AboutPage(BasePage):
    """ About page - The first page that appears when navigating to base URL"""

    def __init__(self):
        super().__init__()
        self.login_link = ".login"
        self.register_link = ".register"

    @allure.step("Click Login link")
    def click_login_link(self):
        self._click(self.login_link)

    @allure.step("Click Register link")
    def click_register_link(self):
        self._click(self.register_link)
