import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class AboutPage(BasePage):
    """About page - The first page that appears when navigating to base URL"""

    LOGIN_LINK: tuple[str, str] = (By.CSS_SELECTOR, ".login")
    REGISTER_LINK: tuple[str, str] = (By.CSS_SELECTOR, ".register")

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    @allure.step("Click Login link")
    def click_login_link(self) -> None:
        self.click(self.LOGIN_LINK)

    @allure.step("Click Register link")
    def click_register_link(self) -> None:
        self.click(self.REGISTER_LINK)
