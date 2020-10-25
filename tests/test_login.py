import allure
import pytest

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from pages.top_bars.top_menu_bar import TopMenuBar


@allure.severity(severity_level="BLOCKER")
@allure.epic("Login Feature's Functionality")
class TestLogin:

    @allure.description("test invalid login")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("email,password", [("nirt236@gmail.com", "123456"), ("elias@gmail.com", "12345Tr")])
    def test_invalid_login(self, email, password):
        tb = TopMenuBar()
        tb.click_login()
        lp = LoginPage()
        lp.login(email, password)
        assert lp.get_error_message() == "These credentials do not match our records."

    @allure.description("Test valid login")
    @pytest.mark.run(order=2)
    def test_valid_login(self, prep_properties):
        config_reader = prep_properties
        username = config_reader.config_section_dict("Base Url")["username"]
        password = config_reader.config_section_dict("Base Url")["password"]
        tb = TopMenuBar()
        lp = LoginPage()
        pp = ProjectsPage()
        tb.click_login()
        lp.login(username, password)
        assert pp.get_title() == "My Workspace"

    @allure.description("Log out from app")
    @pytest.mark.run(order=3)
    def test_logout(self):
        pp = ProjectsPage()
        lp = LoginPage()
        pp.logout()
        # assert lp.get_page_title() == "Log in"
