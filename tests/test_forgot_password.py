import allure
import pytest
from assertpy import assert_that

from pages.about_page import AboutPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from utils.excel_parser import ExcelParser
from utils.json_parser import JsonParser


@allure.epic("Security")
@allure.story("Forgot Password Feature's Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.security
class TestForgotPassword:
    _DATA_FILE_NAME = "data.xlsx"
    _JSON_FILE_NAME = "tests_data.json"

    @allure.description("Forgot password feature test with a valid email address")
    @allure.title("Forgot Password with valid email test")
    def test_valid_email(self, create_driver, prep_properties):
        config_reader = prep_properties
        json_reader = JsonParser(self._JSON_FILE_NAME)
        email = config_reader.config_section_dict("Base Url")["username"]
        about_page = AboutPage()
        login_page = LoginPage()
        forgot_password_page = ForgotPasswordPage()
        about_page.click_login_link()
        login_page.click_forgot_password()
        forgot_password_page.send_password_reset_link(email)
        expected_success_msg = json_reader.read_from_json()["forgot_password_test"]["success_message"]
        assert_that(expected_success_msg).is_equal_to(forgot_password_page.get_success_msg())

    @allure.description("Forgot Password feature test with invalid email address")
    @allure.title("Forgot Password with invalid email test")
    def test_invalid_email(self, create_driver):
        json_reader = JsonParser(self._JSON_FILE_NAME)
        about_page = AboutPage()
        login_page = LoginPage()
        forgot_password_page = ForgotPasswordPage()
        excel_reader = ExcelParser(self._DATA_FILE_NAME)
        emails = excel_reader.read_from_excel("Emails")
        about_page.click_login_link()
        login_page.click_forgot_password()
        forgot_password_page.send_password_reset_link(emails[0])
        expected_error_msg = json_reader.read_from_json()["forgot_password_test"]["error_message"]
        assert_that(expected_error_msg).is_equal_to(forgot_password_page.get_invalid_email_msg())
