import allure
import pytest
from _pytest.fixtures import FixtureRequest
from assertpy import assert_that

from tests.test_base import BaseTest

users = [("nirt236@gmail.com", "123456"), ("elias@gmail.com", "12345Tr")]


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Security")
@allure.feature("Login")
@pytest.mark.security
class TestLogin(BaseTest):
    @allure.description("invalid login")
    @allure.title("Login with invalid credentials test")
    @pytest.mark.parametrize("email, password", users)
    @pytest.mark.run(order=3)
    def test_invalid_login(self, email: str, password: str, json_data: dict):
        self.about_page.click_login_link()
        self.login_page.login(email, password)
        expected_error_message = json_data["login"]["error_message"]
        assert_that(expected_error_message).is_equal_to(
            self.login_page.get_error_message()
        )

    @allure.description("Basic sanity")
    @pytest.mark.devRun
    def test_sanity(self, base_url):
        assert_that(self.driver.current_url).is_equal_to(base_url)

    @allure.description("valid login")
    @allure.title("Login with valid credentials test")
    @pytest.mark.run(order=1)
    def test_valid_login(self, json_data: dict, request: FixtureRequest):
        username = request.config.getini("username")
        password = request.config.getini("password")
        self.about_page.click_login_link()
        self.login_page.login(username, password)
        expected_page_title = json_data["login"]["ws_page_title"]
        assert_that(expected_page_title).is_equal_to(self.project_page.get_title())

    @allure.description("Log out from app")
    @allure.title("Logout of system test")
    @allure.story("As a user i want to be able to logout after a successful login.")
    @pytest.mark.run(order=2)
    def test_logout(self, json_data: dict, request: FixtureRequest):
        username = request.config.getini("username")
        password = request.config.getini("password")
        # example of a simple text attachment
        allure.attach(
            body=username, name="username", attachment_type=allure.attachment_type.TEXT
        )
        self.about_page.click_login_link()
        self.login_page.login(username, password)
        self.project_page.logout()
        expected_page_title = json_data["login"]["lg_page_title"]
        assert_that(expected_page_title).is_equal_to(self.login_page.get_page_title())

    @allure.description("Skip Test example")
    @allure.title("Skipped test example")
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_skip(self):
        pass
