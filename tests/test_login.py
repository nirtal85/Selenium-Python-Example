import allure
import pytest

from pages.login_page import LoginPage
from pages.top_bars.top_menu_bar import TopMenuBar


class TestLogin:

    @allure.description("test invalid login")
    @pytest.mark.parametrize("email,password", [("nirt236@gmail.com", "123456"), ("elias@gmail.com", "12345Tr")])
    def test_invalid_login(self, email, password):
        tb = TopMenuBar()
        tb.click_login()
        lp = LoginPage()
        lp.login(email, password)
        assert lp.get_error_message() == "These credentials do not match our records."
