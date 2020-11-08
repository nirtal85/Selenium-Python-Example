import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProjectEditPage(BasePage):
    """ Project Edit page - the page where adding to and editing projects is done """

    _PROJECT_NAME_FIELD = (By.CSS_SELECTOR, "input#project-name")
    _THANK_YOU_PAGE_TYPE_BUTTON = (By.CSS_SELECTOR, "[for='select-single-outcome']")
    _OUTCOME_PAGES_TYPE_BUTTON = (By.CSS_SELECTOR, "[for='select-outcomes']")
    _START_EDITING_BUTTON = (By.CSS_SELECTOR, ".swal-button.swal-button--confirm")
    _SAVE_AND_EXIT_BUTTON = (By.CSS_SELECTOR, ".e-close.nav-link")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Click SAVE & EXIT button")
    def click_save_and_exit(self):
        self.click(self._SAVE_AND_EXIT_BUTTON)

    @allure.step("Open new project for editing - project name: {project_name}, project type: {project_type}")
    def edit_project_prep(self, project_name, project_type):
        self.fill_text(self._PROJECT_NAME_FIELD, project_name)
        if project_type == "thank you page":
            self.click(self._THANK_YOU_PAGE_TYPE_BUTTON)
        elif project_type == "outcome":
            self.click(self._OUTCOME_PAGES_TYPE_BUTTON)
        else:
            self.click(self._THANK_YOU_PAGE_TYPE_BUTTON)
        self.click(self._START_EDITING_BUTTON)
