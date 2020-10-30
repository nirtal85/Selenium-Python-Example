import allure
import pytest
from assertpy import assert_that

from pages.about_page import AboutPage
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage


@allure.epic("Workspaces")
@allure.story("WorkSpaces Creation and Editing Functionality")
@allure.severity(allure.severity_level.NORMAL)
class TestWorkspaces:
    _workspace = "test"
    _new_workspace = "another test"

    # performs login operation
    def login(self, prep_properties):
        config = prep_properties
        username = config.config_section_dict("Base Url")["username"]
        password = config.config_section_dict("Base Url")["password"]
        ap = AboutPage()
        lp = LoginPage()
        ap.click_login_link()
        lp.login(username, password)

    @allure.description("Create new Workspace test")
    @pytest.mark.run(order="1")
    def test_create_new_workspace(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        before = pp.get_workspaces_number()
        pp.create_workspace(self._workspace)
        after = pp.get_workspaces_number()
        assert_that(after).is_greater_than(before)

    @allure.description("Rename an existing workspace test")
    @pytest.mark.run(order="2")
    def test_rename_workspace(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        pp.rename_workspace(self._workspace, self._new_workspace)
        assert_that(pp.is_workspace_found(self._new_workspace)).is_true()

    @allure.description("Delete an existing workspace test")
    @pytest.mark.run(order="3")
    def test_delete_workspace(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        before = pp.get_workspaces_number()
        pp.delete_workspace()
        after = pp.get_workspaces_number()
        assert_that(after).is_less_than(before)

    @allure.description(
        "Compare between the actual number of projects seen on page and the number shown in workspaces block")
    @pytest.mark.run(order="4")
    def test_number_of_existing_projects(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        number_of_displayed_projects = pp.get_projects_number_in_page()
        number_of_projects_in_workspace = pp.get_projects_number_from_workspace()
        assert_that(number_of_displayed_projects).is_equal_to(number_of_projects_in_workspace)
