import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from helper_enums.status_enum import StatusEnum
from pages.top_bars.top_navigate_bar import TopNavigateBar


class ProjectsPage(TopNavigateBar):
    """ Projects page - Where projects are added and edited"""

    _START_BUTTON = (By.CSS_SELECTOR, "#app .px-4 a")
    _CREATE_NEW_WORKSPACE_BUTTON = (By.CSS_SELECTOR, ".font-medium button")
    _WORKSPACE_EDIT_BUTTON = (By.CSS_SELECTOR, "[data-icon='chevron-down']")
    _RENAME_WORKSPACE_BUTTON = (By.CSS_SELECTOR, ".mr-3 .hover\\:bg-gray-600")
    _DELETE_WORKSPACE_BUTTON = (By.CSS_SELECTOR, ".mr-3 .text-red-600")
    _RENAME_FIELD = (By.CSS_SELECTOR, ".vue-portal-target input")
    _CONFIRMATION_BUTTON = (By.CSS_SELECTOR, "#confirm-create-button")
    _NEW_WORKSPACE_NAME_FIELD = (By.CSS_SELECTOR, "[placeholder='Workspace name']")
    _DELETE_WORKSPACE_FIELD = (By.CSS_SELECTOR, ".h-12")
    _CREATE_PROJECT_BUTTON = (By.CSS_SELECTOR, ".hidden.px-3")
    _SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-icon='search']")
    _SEARCH_FIELD = (By.CSS_SELECTOR, "[type='text']")
    _CONFIRM_DELETE_PROJECT_BUTTON = (By.CSS_SELECTOR, "#confirm-delete-button")
    _CANCEL_PROJECT_DELETION_BUTTON = (By.CSS_SELECTOR, "form [type='button']")
    _PROJECT_PAGE_TITLE = (By.CSS_SELECTOR, "#app h1.leading-tight.truncate")
    _NO_PROJECT_FOUND_MSG = (By.CSS_SELECTOR, "#app h1.block")
    _NUMBER_OF_PROJECTS_IN_WORKSPACE_BLOCK = (By.CSS_SELECTOR, "span:nth-child(2)")
    _DROP_DOWN_BUTTON = (By.CSS_SELECTOR, ".justify-right button svg")
    _DELETE_PROJECT_BUTTON = (By.XPATH, "//button[text()='Delete Project']")

    _WORKSPACE_LIST = (By.CSS_SELECTOR, ".mt-6 a")
    _PROJECTS_BLOCK = (By.CSS_SELECTOR, "#app .max-w-full div .mt-4 > .mt-8 > div")
    _PROJECTS_TITLES = (By.CSS_SELECTOR, "h1 a")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Create new workspace {workspace_name}")
    def create_workspace(self, workspace_name):
        self.click(self._CREATE_NEW_WORKSPACE_BUTTON)
        self.fill_text(self._NEW_WORKSPACE_NAME_FIELD, workspace_name)
        self.click(self._CONFIRMATION_BUTTON)

    @allure.step("Delete a workspace")
    def delete_workspace(self):
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        # in case only the main workspace exists, then create another
        if len(workspaces) < 2:
            self.create_workspace("test")
            workspaces = self._wait.until(
                expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        # click on the second created workspace
        workspaces[1].click()
        self.click(self._WORKSPACE_EDIT_BUTTON)
        self.click(self._DELETE_WORKSPACE_BUTTON)
        # get the name of the workspace to delete from the background text in delete workspace field
        name = self._driver.find_element(*self._DELETE_WORKSPACE_FIELD).get_attribute("placeholder")
        self.fill_text(self._DELETE_WORKSPACE_FIELD, name)
        self.click(self._CONFIRMATION_BUTTON)

    @allure.step("Rename workspace {old_name} to {new_name}")
    def rename_workspace(self, old_name, new_name):
        flag = False
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        # get workspaces as text
        workspaces_text_list = [workspace.text for workspace in workspaces]
        # if the old workspace name is not present in list, then add it
        for i in range(len(workspaces_text_list)):
            if old_name in workspaces_text_list[i]:
                flag = True
                break
        # case the old workspace is not present
        if not flag:
            self.create_workspace(old_name)
            workspaces = self._wait.until(
                expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        for workspace in workspaces:
            if old_name in workspace.text:
                workspace.click()
                self.click(self._WORKSPACE_EDIT_BUTTON)
                self.click(self._RENAME_WORKSPACE_BUTTON)
                self.fill_text(self._RENAME_FIELD, new_name)
                self.click(self._CONFIRMATION_BUTTON)
                break

    @allure.step("Start a new project")
    def create_new_project(self):
        if self.is_elem_displayed(self._driver.find_element(*self._START_BUTTON)):
            self.click(self._START_BUTTON)
        elif self.is_elem_displayed(self._driver.find_element(*self._CREATE_PROJECT_BUTTON)):
            self.click(self._CREATE_NEW_WORKSPACE_BUTTON)

    @allure.step("Search for project {project_name}")
    def search_project(self, project_name):
        self.click(self._SEARCH_BUTTON)
        self.fill_text(self._SEARCH_FIELD, project_name)

    @allure.step("Delete or cancel deletion of project {project_name}")
    def delete_project(self, project_name, status="confirm"):
        projects = self._wait.until(expected_conditions.visibility_of_all_elements_located(self._PROJECTS_BLOCK))
        deleted_project = None
        for project in projects:
            if project_name in project.text:
                deleted_project = project
                self.click_drop_down_menu(project)
                project.find_element(*self._DELETE_PROJECT_BUTTON).click()
                break
        if status == StatusEnum.CANCEL.value:
            self.click(self._CANCEL_PROJECT_DELETION_BUTTON)
        elif status == StatusEnum.CONFIRM.value:
            self.click(self._CONFIRM_DELETE_PROJECT_BUTTON)
            self._wait.until(expected_conditions.invisibility_of_element(deleted_project))

    @allure.step("Get workspaces number")
    def get_workspaces_number(self):
        self._wait.until(
            expected_conditions.invisibility_of_element_located(self._NEW_WORKSPACE_NAME_FIELD))
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        return len(workspaces)

    @allure.step("Get number of projects display on page")
    def get_projects_number_in_page(self):
        projects = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._PROJECTS_BLOCK))
        return len(projects)

    @allure.step("Get number of projects displayed next to main workspace (My Workspace) name")
    def get_projects_number_from_workspace(self):
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        number = workspaces[0].find_element(*self._NUMBER_OF_PROJECTS_IN_WORKSPACE_BLOCK)
        return int(number.text)

    @allure.step("Verify if workspace {workspace_name} exists")
    def is_workspace_found(self, workspace_name):
        self._wait.until(expected_conditions.invisibility_of_element_located(self._RENAME_FIELD))
        workspaces = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._WORKSPACE_LIST))
        for workspace in workspaces:
            if workspace_name in workspace.text:
                return True
        return False

    @allure.step("Get projects' page title")
    def get_title(self):
        return self.get_text(self._PROJECT_PAGE_TITLE)

    def get_no_project_found_msg(self):
        return self.get_text(self._NO_PROJECT_FOUND_MSG)

    @allure.step("Check if {project_name} is present")
    def is_project_found(self, project_name):
        projects_titles = self._wait.until(
            expected_conditions.visibility_of_all_elements_located(self._PROJECTS_TITLES))
        for project_title in projects_titles:
            if project_name != project_title.text.lower():
                return False
        return True

    # clicks on a specific project's drop down arrow
    def click_drop_down_menu(self, project):
        dropdown_menu_button = project.find_element(*self._DROP_DOWN_BUTTON)
        dropdown_menu_button.click()
