import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    EMAIL_FIELD = (By.CSS_SELECTOR, "[name='email']")
    SEND_PASSWORD_RESET_LINK_BTN = (By.CSS_SELECTOR, "[type='submit']")
    ERROR_MSG = (By.CSS_SELECTOR, '.alert-danger')
    SUCCESS_MSG = (By.CSS_SELECTOR, '.alert-success')

    def __init__(self):
        super().__init__()

    @allure.step("Send password reset link to email address: {email}")
    def send_password_reset_link(self, email):
        self.fill_text(self.EMAIL_FIELD, email)
        self.click(self.SEND_PASSWORD_RESET_LINK_BTN)

    @allure.step("Get invalid email message")
    def get_invalid_email_msg(self):
        return self.get_text(self._driver.find_element(*self.ERROR_MSG))

    @allure.step("Get success message")
    def get_success_msg(self):
        return self.get_text(self._driver.find_element(*self.SUCCESS_MSG))
