import allure
import pytest
from pages.about_page import AboutPage
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from assertpy import assert_that


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Login Feature's Functionality")
class TestLogin:
    _error_msg = "These credentials do not match our records."
    _page_title = "My Workspace"

    @allure.description("test invalid login")
    @pytest.mark.parametrize("email,password", [("nirt236@gmail.com", "123456"), ("elias@gmail.com", "12345Tr")])
    @pytest.mark.run(order=3)
    def test_invalid_login(self, email, password):
        ap = AboutPage()
        ap.click_login_link()
        lp = LoginPage()
        lp.login(email, password)
        assert_that(lp.get_error_message()).is_equal_to(self._error_msg)

    @allure.description("Test valid login")
    @pytest.mark.run(order=1)
    @pytest.mark.incremental
    def test_valid_login(self, prep_properties):
        config_reader = prep_properties
        username = config_reader.config_section_dict("Base Url")["username"]
        password = config_reader.config_section_dict("Base Url")["password"]
        ap = AboutPage()
        lp = LoginPage()
        pp = ProjectsPage()
        ap.click_login_link()
        lp.login(username, password)
        assert_that(pp.get_title()).is_equal_to(self._page_title)

    @allure.description("Log out from app")
    @pytest.mark.run(order=2)
    @pytest.mark.incremental
    def test_logout(self):
        ap = AboutPage()
        ap.click_login_link()
        pp = ProjectsPage()
        pp.logout()
        lp = LoginPage()
        assert_that(lp.get_page_title()).is_true()
