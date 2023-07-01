from typing import Tuple

import allure
from selenium.webdriver.common.by import By

from pages.top_bars.top_menu_bar import TopMenuBar


class LoginPage(TopMenuBar):
    """ Login Page """
    USERNAME_FIELD: Tuple[str, str] = (By.CSS_SELECTOR, "input[type=email]")
    PASSWORD_FIELD: Tuple[str, str] = (By.CSS_SELECTOR, "input[type=password]")
    LOGIN_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "button[type=submit]")
    LOGIN_ERROR_MESSAGE: Tuple[str, str] = (By.CSS_SELECTOR, "div.alert-danger")
    PAGE_TITLE: Tuple[str, str] = (By.CSS_SELECTOR, ".e-form-heading")
    FORGOT_PASSWORD_LINK: Tuple[str, str] = (By.CSS_SELECTOR, "[href='https://app.involve.me/password/reset']")

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    @allure.step("Log in with username: {username} and password: {password}")
    def login(self, username: str, password: str) -> None:
        self.fill_text(self.USERNAME_FIELD, username)
        self.fill_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        return self.get_text(self.LOGIN_ERROR_MESSAGE)

    @allure.step("Get page title")
    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    @allure.step("Click Forgot Password link")
    def click_forgot_password(self) -> None:
        self.click(self.FORGOT_PASSWORD_LINK)
