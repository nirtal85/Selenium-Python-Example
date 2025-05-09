import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class TopMenuBar(BasePage):
    """Top menu bar - The bar that appears on the top of the page prior to login"""

    LOGIN_LINK = (By.CSS_SELECTOR, ".login")
    REGISTER_LINK = (By.CSS_SELECTOR, ".register")

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    @allure.step("Click Login button")
    def click_login(self):
        self.click(self.LOGIN_LINK)

    @allure.step("Click Register button")
    def click_register(self):
        self.click(self.REGISTER_LINK)
