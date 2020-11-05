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
    _JSON_FILE_NAME = "forgot_password_test_data.json"

    @allure.description("Forgot password feature test with a valid email address")
    @allure.title("Forgot Password feature test with a valid email")
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
        success = json_reader.read_from_json()["success message"]
        assert_that(success).is_equal_to(forgot_password_page.get_success_msg())

    @allure.description("Forgot Password feature test with invalid email address")
    @allure.title("Forgot Password feature test with an invalid email")
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
        error = json_reader.read_from_json()["error message"]
        assert_that(error).is_equal_to(forgot_password_page.get_invalid_email_msg())
