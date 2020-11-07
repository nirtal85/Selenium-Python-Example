import allure
import pytest
from assertpy import assert_that

from pages.about_page import AboutPage
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from utils.json_parser import JsonParser

users = [
    ("nirt236@gmail.com", "123456"),
    ("elias@gmail.com", "12345Tr")
]


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Security")
@allure.story("Login Feature's Functionality")
@pytest.mark.security
class TestLogin:
    _JSON_FILE_NAME = "tests_data.json"

    @allure.description("test invalid login")
    @allure.title("Login with invalid credentials test")
    @pytest.mark.parametrize("email, password", users)
    @pytest.mark.run(order=3)
    def test_invalid_login(self, create_driver, email, password):
        json_reader = JsonParser(self._JSON_FILE_NAME)
        about_page = AboutPage()
        about_page.click_login_link()
        login_page = LoginPage()
        login_page.login(email, password)
        expected_error_msg = json_reader.read_from_json()["login_test"]["error_message"]
        assert_that(expected_error_msg).is_equal_to(login_page.get_error_message())

    @allure.description("Test valid login")
    @allure.title("Login with valid credentials test")
    @pytest.mark.run(order=1)
    def test_valid_login(self, create_driver, prep_properties):
        config_reader = prep_properties
        username = config_reader.config_section_dict("Base Url")["username"]
        password = config_reader.config_section_dict("Base Url")["password"]
        json_reader = JsonParser(self._JSON_FILE_NAME)
        about_page = AboutPage()
        login_page = LoginPage()
        projects_page = ProjectsPage()
        about_page.click_login_link()
        login_page.login(username, password)
        expected_page_title = json_reader.read_from_json()["login_test"]["ws_page_title"]
        assert_that(expected_page_title).is_equal_to(projects_page.get_title())

    @allure.description("Log out from app")
    @allure.title("Logout of system test")
    @pytest.mark.run(order=2)
    def test_logout(self, create_driver, prep_properties):
        config_reader = prep_properties
        username = config_reader.config_section_dict("Base Url")["username"]
        password = config_reader.config_section_dict("Base Url")["password"]
        json_reader = JsonParser(self._JSON_FILE_NAME)
        about_page = AboutPage()
        about_page.click_login_link()
        login_page = LoginPage()
        projects_page = ProjectsPage()
        login_page.login(username, password)
        projects_page.logout()
        expected_page_title = json_reader.read_from_json()["login_test"]["lg_page_title"]
        assert_that(expected_page_title).is_equal_to(login_page.get_page_title())

    @allure.description("Skip Test example")
    @allure.title("Skipped test example")
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_skip(self):
        pass
