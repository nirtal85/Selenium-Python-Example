from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from pages.top_bars.top_navigate_bar import TopNavigateBar


class TemplatesPage(TopNavigateBar):
    """ Templates page - contains variety of templates to select """

    _TEMPLATES_BLOCK = (By.CSS_SELECTOR, "#template-gallery tbody tr")

    def __init__(self):
        super().__init__()

    def choose_template(self, template_name):
        self._wait.until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, "#template-gallery")))
        templates = self._wait.until(expected_conditions.visibility_of_all_elements_located(self._TEMPLATES_BLOCK))
        for template in templates:
            if template_name in template.text:
                button = template.find_element(By.CSS_SELECTOR, "a .btn.btn-primary")
                self.move_to_element(button)
                button.click()
                break
