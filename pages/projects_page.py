import allure
from selenium.webdriver.common.by import By

from pages.top_bars.top_navigate_bar import TopNavigateBar
import selenium.webdriver.support.expected_conditions as EC


class ProjectsPage(TopNavigateBar):
    """ Projects page - Where projects are added and edited"""

    _workspaces_list = ".mt-6 a"
    _projects_block = "#app .max-w-full div .mt-4 > .mt-8 > div"
    _create_new_workspace_btn = ".font-medium button"
    _workspace_edit_btn = "[data-icon='chevron-down']"
    _rename_workspace_btn = ".mr-3 .hover\\:bg-gray-600"
    _delete_workspace_btn = ".mr-3 .text-red-600"
    _rename_field = ".vue-portal-target input"
    _confirmation_btn = "#confirm-create-button"
    _new_workspace_name_field = "[placeholder='Workspace name']"
    _delete_workspace_field = ".h-12"
    _create_project_btn = ".hidden.px-3"
    _search_btn = "[data-icon='search']"
    _search_field = "[type='text']"
    _confirm_delete_project_btn = "#confirm-delete-button"
    _cancel_project_deletion_btn = "form [type='button'"
    _project_page_title = "#app h1.leading-tight.truncate"

    def __init__(self):
        super().__init__()

    @allure.step("Create new workspace {1}")
    def create_workspace(self, workspace_name):
        self.click(self._create_new_workspace_btn)
        self.fill_text(self._new_workspace_name_field, workspace_name)
        self.click(self._confirmation_btn)

    @allure.step("Delete a workspace")
    def delete_workspace(self):
        workspaces = self._wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self._workspaces_list)))
        # in case only the main workspace exists, then create another
        if len(workspaces) < 2:
            self.create_workspace("test")
            workspaces = self._wait.until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self._workspaces_list)))
        # click on the second created workspace
        workspaces[1].click()
        self.click(self._workspace_edit_btn)
        self.click(self._delete_workspace_btn)
        # get the name of the workspace to delete from the background text in delete workspace field
        name = self._driver.find_element_by_css_selector(self._delete_workspace_field).get_attribute("placeholder")
        self.fill_text(self._delete_workspace_field, name)
        self.click(self._confirmation_btn)

    @allure.step("Rename workspace {0} to {1}")
    def rename_workspace(self, old_name, new_name):
        flag = False
        workspaces = self._wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self._workspaces_list)))
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
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self._workspaces_list)))
        for workspace in workspaces:
            if old_name in workspace.text:
                workspace.click()
                self.click(self._workspace_edit_btn)
                self.click(self._rename_workspace_btn)
                self.fill_text(self._rename_field, new_name)
                self.click(self._confirmation_btn)
                break

    @allure.step("Get workspaces number")
    def get_workspaces_number(self):
        self._wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, self._new_workspace_name_field)))
        workspaces = self._wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self._workspaces_list)))
        return len(workspaces)

    @allure.step("Get number of projects display on page")
    def get_projects_number_in_page(self):
        projects = self._wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self._projects_block)))
        return len(projects)

    @allure.step("Get number of projects displayed next to main workspace (My Workspace) name")
    def get_projects_number_from_workspace(self):
        workspaces = self._wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self._workspaces_list)))
        number = workspaces[0].find_element_by_css_selector("span:nth-child(2)")
        return int(self.get_text(number))

    @allure.step("Get projects' page title")
    def get_title(self):
        el = self._driver.find_element_by_css_selector(self._project_page_title)
        return self.get_text(el)

    @allure.step("Verify if workspace {1} exists")
    def is_workspace_found(self, workspace_name):
        self._wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, self._rename_field)))
        workspaces = self._wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, self._workspaces_list)))
        for workspace in workspaces:
            if workspace_name in workspace.text:
                return True
        return False
