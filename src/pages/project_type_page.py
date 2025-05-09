import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from src.pages.top_bars.top_navigate_bar import TopNavigateBar


class ProjectTypePage(TopNavigateBar):
    """Project Type page - where one can choose which kind of templates to work with"""

    _START_FROM_SCRATCH_BUTTON: tuple[str, str] = (By.CSS_SELECTOR, ".blank div.icon")
    _PROJECTS_BLOCK: tuple[str, str] = (
        By.CSS_SELECTOR,
        "#app-layout div:nth-child(3) .title",
    )

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    @allure.step("Select project {project_name} from projects menu")
    def select_project(self, project_name: str) -> None:
        projects = self.wait.until(
            expected_conditions.visibility_of_all_elements_located(self._PROJECTS_BLOCK)
        )
        for project in projects:
            if project_name == project.text.lower():
                project.click()
                break
