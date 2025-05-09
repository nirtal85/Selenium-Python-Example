from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from src.pages.top_bars.top_navigate_bar import TopNavigateBar


class TemplatesPage(TopNavigateBar):
    """Templates page - contains variety of templates to select"""

    _TEMPLATES_BLOCK: tuple[str, str] = (By.CSS_SELECTOR, "#template-gallery tbody tr")
    _CHOOSE_BUTTON: tuple[str, str] = (By.CSS_SELECTOR, "a .btn.btn-primary")

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def choose_template(self, template_name: str) -> None:
        self.wait.until(
            expected_conditions.visibility_of_all_elements_located(self._TEMPLATES_BLOCK)
        )
        templates = self.wait.until(
            expected_conditions.visibility_of_all_elements_located(self._TEMPLATES_BLOCK)
        )
        for template in templates:
            if template_name in template.text:
                button = template.find_element(*self._CHOOSE_BUTTON)
                self.move_to_element(button)
                button.click()
                break
