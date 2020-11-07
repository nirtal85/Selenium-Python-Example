import allure
import pytest
from assertpy import assert_that


from utils.json_parser import JsonParser
from tests.test_base import BaseTest


users = [
    ("nirt236@gmail.com", "123456"),
    ("elias@gmail.com", "12345Tr")
]


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Security")
@allure.story("Login Feature's Functionality")
@pytest.mark.security

    _JSON_FILE_NAME = "tests_data.json"

class TestLogin(BaseTest):


    @allure.description("test invalid login")
    @allure.title("Login with invalid credentials test")
    @pytest.mark.parametrize("email, password", users)
    @pytest.mark.run(order=3)

        json_reader = JsonParser(self._JSON_FILE_NAME)
        expected_error_msg = json_reader.read_from_json()["login_test"]["error_message"]
        assert_that(expected_error_msg).is_equal_to(login_page.get_error_message())

    def test_invalid_login(self, email, password):
        self.pages['about_page'].click_login_link()
        self.pages['login_page'].login(email, password)


    @allure.description("Test valid login")
    @allure.title("Login with valid credentials test")
    @pytest.mark.run(order=1)
    def test_valid_login(self, prep_properties):
        config_reader = prep_properties
        username = config_reader.config_section_dict("Base Url")["username"]
        password = config_reader.config_section_dict("Base Url")["password"]

        json_reader = JsonParser(self._JSON_FILE_NAME)
        expected_page_title = json_reader.read_from_json()["login_test"]["ws_page_title"]
        assert_that(expected_page_title).is_equal_to(projects_page.get_title())

        self.pages['about_page'].click_login_link()
        self.pages['login_page'].login(username, password)

    @allure.description("Log out from app")
    @allure.title("Logout of system test")
    @pytest.mark.run(order=2)
    def test_logout(self, prep_properties):
        config_reader = prep_properties
        username = config_reader.config_section_dict("Base Url")["username"]
        password = config_reader.config_section_dict("Base Url")["password"]

        json_reader = JsonParser(self._JSON_FILE_NAME)
        expected_page_title = json_reader.read_from_json()["login_test"]["lg_page_title"]
        assert_that(expected_page_title).is_equal_to(login_page.get_page_title())

        self.pages['about_page'].click_login_link()
        self.pages['login_page'].login(username, password)
        self.pages['projects_page'].logout()


    @allure.description("Skip Test example")
    @allure.title("Skipped test example")
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_skip(self):
        pass
