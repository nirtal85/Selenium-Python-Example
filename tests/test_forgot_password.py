import allure
import pytest
from assertpy import assert_that

from tests.test_base import BaseTest


@allure.epic("Security")
@allure.story("Forgot Password Feature's Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.security
class TestForgotPassword(BaseTest):

    @allure.description("Forgot password with a valid email address")
    @allure.title("Forgot Password with valid email test")
    def test_valid_email(self):
        email = self.config_reader.config_section_dict("Base Url")["username"]
        self.pages['about_page'].click_login_link()
        self.pages['login_page'].click_forgot_password()
        self.pages['forgot_password_page'].send_password_reset_link(email)
        expected_success_msg = self.json_reader.read_from_json()["forgot_password"]["success_message"]
        assert_that(expected_success_msg).is_equal_to(self.pages['forgot_password_page'].get_success_msg())

    @allure.description("Forgot Password with invalid email address")
    @allure.title("Forgot Password with invalid email test")
    def test_invalid_email(self):
        emails = self.excel_reader.read_from_excel("Emails")
        self.pages['about_page'].click_login_link()
        self.pages['login_page'].click_forgot_password()
        self.pages['forgot_password_page'].send_password_reset_link(emails[0])
        expected_error_msg = self.json_reader.read_from_json()["forgot_password"]["error_message"]
        assert_that(expected_error_msg).is_equal_to(self.pages['forgot_password_page'].get_invalid_email_msg())

    @allure.description("Exception catching")
    @allure.title("Exception test")
    def test_expected_exception_on_page_title(self):
        self.pages['about_page'].click_login_link()
        self.pages['login_page'].click_forgot_password()
        with pytest.raises(AssertionError) as e:
            assert self.pages['forgot_password_page'].get_page_title() == "something else"
        assert "AssertionError" in str(e)
