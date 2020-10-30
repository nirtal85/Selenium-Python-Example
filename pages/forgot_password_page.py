import allure

from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    """ Forgot Password Page"""

    _email_field = "[name='email']"
    _send_password_reset_link_btn = "[type='submit']"
    _error_msg = ".alert-danger"
    _success_msg = ".alert-success"

    def __init__(self):
        super().__init__()

    @allure.step("Send password reset link to email address: {1}")
    def send_password_reset_link(self, email):
        self.fill_text(self._email_field, email)
        self.click(self._send_password_reset_link_btn)

    @allure.step("Get invalid email message")
    def get_invalid_email_msg(self):
        return self.get_text(self._driver.find_element_by_css_selector(self._error_msg))

    @allure.step("Get success message")
    def get_success_msg(self):
        return self.get_text(self._driver.find_element_by_css_selector(self._success_msg))
