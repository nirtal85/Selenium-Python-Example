import allure
import pytest
from assertpy import assert_that

from tests.test_base import BaseTest

users = [
    ("nirt236@gmail.com", "123456"),
    ("elias@gmail.com", "12345Tr")
]


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Security")
@allure.feature("Login")
@pytest.mark.security
class TestLogin(BaseTest):

    @allure.description("valid login")
    @allure.title("Login with valid credentials test")
    @pytest.mark.run(order=1)
    def test_valid_login(self):
        username = self.config_reader.config_section_dict("Base Url")["username"]
        password = self.config_reader.config_section_dict("Base Url")["password"]
        self.pages['about_page'].click_login_link()
        self.pages['login_page'].login(username, password)
        expected_page_title = self.json_reader.read_from_json()["login"]["ws_page_title"]
        assert_that(expected_page_title).is_equal_to(self.pages['projects_page'].get_title())
