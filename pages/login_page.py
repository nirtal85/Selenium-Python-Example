import allure

from pages.top_bars.top_menu_bar import TopMenuBar


class LoginPage(TopMenuBar):
    """ Login Page """

    _username_field = "input[name='email']"
    _password_field = "input[name='password']"
    _login_btn = "button[type='submit']"
    _login_error_message = "div.alert-danger"
    _page_title = ".e-form-heading"
    _forgot_password_link = '[href="https://app.involve.me/password/reset"]'

    def __init__(self):
        super().__init__()

    @allure.step("Log in with username: {username} and password: {password}")
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

    @allure.step("Click Forgot Password link")
    def click_forgot_password(self):
        self.click(self._forgot_password_link)
