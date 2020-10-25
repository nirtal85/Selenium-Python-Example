from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self):
        super().__init__()
        self._username_field = "input[name='email']"
        self._password_field = "input[name='password']"
        self._login_btn = "button[type='submit']"
        self._login_error_message = "div.alert-danger"

    def login(self, user_name, password):
        self.fill_text(self._username_field, user_name)
        self.fill_text(self._password_field, password)
        self.click(self._login_btn)

    def get_error_message(self):
        el = self._driver.find_element_by_css_selector(self._login_error_message)
        return self.get_text(el)
