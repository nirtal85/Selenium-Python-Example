import allure
import pytest
from assertpy import assert_that

users = [
    ("nirt236@gmail.com", "123456"),
    ("elias@gmail.com", "12345Tr")
]


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Security")
@allure.story("Login Feature's Functionality")
@pytest.mark.security
@pytest.mark.usefixtures("create_driver")
class TestLogin:
    _error_msg = "These credentials do not match our records."
    _page_title = "My Workspace"

    @allure.description("test invalid login")
    @allure.title("Login with invalid credentials test")
    @pytest.mark.parametrize("email, password", users)
    @pytest.mark.run(order=3)
    def test_invalid_login(self, email, password, about_page, login_page):
        about_page.click_login_link()
        login_page.login(email, password)
        assert_that(self._error_msg).is_equal_to(login_page.get_error_message())

    @allure.description("Test valid login")
    @allure.title("Login with valid credentials test")
    @pytest.mark.run(order=1)
    def test_valid_login(self, prep_properties, about_page, login_page, projects_page):
        config_reader = prep_properties
        username = config_reader.config_section_dict("Base Url")["username"]
        password = config_reader.config_section_dict("Base Url")["password"]
        about_page.click_login_link()
        login_page.login(username, password)
        assert_that(self._page_title).is_equal_to(projects_page.get_title())

    @allure.description("Log out from app")
    @allure.title("Logout of system test")
    @pytest.mark.run(order=2)
    def test_logout(self, prep_properties, about_page, login_page, projects_page):
        config_reader = prep_properties
        username = config_reader.config_section_dict("Base Url")["username"]
        password = config_reader.config_section_dict("Base Url")["password"]
        about_page.click_login_link()
        login_page.login(username, password)
        projects_page.logout()
        assert_that('Log in').is_equal_to(login_page.get_page_title())

    @allure.description("Skip Test example")
    @allure.title("Skipped test example")
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_skip(self):
        pass
