import allure
import pytest

from pages.about_page import AboutPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from assertpy import assert_that


@allure.epic("Security")
@allure.story("Forgot Password Feature's Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.security
class TestForgotPassword:
    _success_msg = "A reset link has been sent to the email address, if it has been used to register for an account."
    _error_msg = "We can't find a user with that e-mail address."

    @allure.description("Forgot password feature test with a valid email address")
    def test_valid_email(self, create_driver, prep_properties):
        config_reader = prep_properties
        email = config_reader.config_section_dict("Base Url")["username"]
        about_page = AboutPage()
        login_page = LoginPage()
        forgot_password_page = ForgotPasswordPage()
        about_page.click_login_link()
        login_page.click_forgot_password()
        forgot_password_page.send_password_reset_link(email)
        assert_that(forgot_password_page.get_success_msg()).is_equal_to(self._success_msg)

    @allure.description("Forgot Password feature test with invalid email address")
    def test_invalid_email(self, create_driver):
        about_page = AboutPage()
        login_page = LoginPage()
        forgot_password_page = ForgotPasswordPage()
        about_page.click_login_link()
        login_page.click_forgot_password()
        forgot_password_page.send_password_reset_link("something@gmail.com")
        assert_that(forgot_password_page.get_invalid_email_msg()).is_equal_to(self._error_msg)
