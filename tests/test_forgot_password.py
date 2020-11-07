import allure
import pytest
from assertpy import assert_that

from tests.test_base import BaseTest
from utils.excel_parser import ExcelParser


@allure.epic("Security")
@allure.story("Forgot Password Feature's Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.security
class TestForgotPassword(BaseTest):
    _SUCCESS_MSG = "A reset link has been sent to the email address, if it has been used to register for an account."
    _ERROR_MSG = "We can't find a user with that e-mail address."
    _DATA_FILE_NAME = "data.xlsx"

    @allure.description("Forgot password feature test with a valid email address")
    @allure.title("Forgot Password with valid email test")
    def test_valid_email(self, prep_properties):
        config_reader = prep_properties
        email = config_reader.config_section_dict("Base Url")["username"]
        self.pages['about_page'].click_login_link()
        self.pages['login_page'].click_forgot_password()
        self.pages['forgot_password_page'].send_password_reset_link(email)
        assert_that(self._SUCCESS_MSG).is_equal_to(self.pages['forgot_password_page'].get_success_msg())

    @allure.description("Forgot Password feature test with invalid email address")
    @allure.title("Forgot Password with invalid email test")
    def test_invalid_email(self):
        excel_reader = ExcelParser(self._DATA_FILE_NAME)
        emails = excel_reader.read_from_excel("Emails")
        self.pages['about_page'].click_login_link()
        self.pages['login_page'].click_forgot_password()
        self.pages['forgot_password_page'].send_password_reset_link(emails[0])
        assert_that(self._ERROR_MSG).is_equal_to(self.pages['forgot_password_page'].get_invalid_email_msg())
