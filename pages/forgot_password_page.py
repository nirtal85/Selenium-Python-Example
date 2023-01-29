import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    EMAIL_FIELD = (By.CSS_SELECTOR, "[name=email]")
    SEND_PASSWORD_RESET_LINK_BUTTON = (By.CSS_SELECTOR, "[type=submit]")
    ERROR_MSG = (By.CSS_SELECTOR, '.alert-danger')
    SUCCESS_MSG = (By.CSS_SELECTOR, '.alert-success')
    PAGE_TITLE = (By.CSS_SELECTOR, ".e-form-heading")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Send password reset link to email address: {email}")
    def send_password_reset_link(self, email: str) -> None:
        self.fill_text(self.EMAIL_FIELD, email)
        self.click(self.SEND_PASSWORD_RESET_LINK_BUTTON)

    @allure.step("Get invalid email message")
    def get_invalid_email_msg(self) -> str:
        return self.get_text(self.ERROR_MSG)

    @allure.step("Get success message")
    def get_success_msg(self) -> str:
        return self.get_text(self.SUCCESS_MSG)

    @allure.step("Get Forgot password page title")
    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)
