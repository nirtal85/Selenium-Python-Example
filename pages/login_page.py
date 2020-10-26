import allure

from pages.top_bars.top_menu_bar import TopMenuBar


class LoginPage(TopMenuBar):
    """ Login Page """

    def __init__(self):
        super().__init__()
        self._username_field = "input[name='email']"
        self._password_field = "input[name='password']"
        self._login_btn = "button[type='submit']"
        self._login_error_message = "div.alert-danger"
        self._page_title = ".e-form-heading"

    @allure.step("Log in with username {0} and password {1}")
    def login(self, username, password):
        self.fill_text(self._username_field, username)
        self.fill_text(self._password_field, password)
        self.click(self._login_btn)

    @allure.step("Get error message")
    def get_error_message(self):
        el = self._driver.find_element_by_css_selector(self._login_error_message)
        return self.get_text(el)

    @allure.step("Get page title")
    def get_page_title(self):
        el = self._driver.find_element_by_css_selector(self._page_title)
        return self.get_text(el)
