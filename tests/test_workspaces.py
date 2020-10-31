import allure
import pytest
from assertpy import assert_that

from pages.about_page import AboutPage
from pages.login_page import LoginPage
from pages.project_edit_page import ProjectEditPage
from pages.project_type_page import ProjectTypePage
from pages.projects_page import ProjectsPage
from pages.top_bars.templates_page import TemplatesPage


@allure.epic("Workspaces")
@allure.story("WorkSpaces Creation and Editing Functionality")
@allure.severity(allure.severity_level.NORMAL)
class TestWorkspaces:
    _workspace = "test"
    _new_workspace = "another test"
    _project_type = "quiz"
    _template_type = "Blank"
    _project_name = "test project"
    _final_slide = "Thank you page"
    _no_project_found_msg = "No project matches the criteria"

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
    @pytest.mark.run(order=1)
    def test_create_new_workspace(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        before = pp.get_workspaces_number()
        pp.create_workspace(self._workspace)
        after = pp.get_workspaces_number()
        assert_that(after).is_greater_than(before)

    @allure.description("Rename an existing workspace test")
    @pytest.mark.run(order=2)
    def test_rename_workspace(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        pp.rename_workspace(self._workspace, self._new_workspace)
        assert_that(pp.is_workspace_found(self._new_workspace)).is_true()

    @allure.description("Delete an existing workspace test")
    @pytest.mark.run(order=3)
    def test_delete_workspace(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        before = pp.get_workspaces_number()
        pp.delete_workspace()
        after = pp.get_workspaces_number()
        assert_that(after).is_less_than(before)

    @allure.description(
        "Compare between the actual number of projects seen on page and the number shown in workspaces block")
    @pytest.mark.run(order=4)
    def test_number_of_existing_projects(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        number_of_displayed_projects = pp.get_projects_number_in_page()
        number_of_projects_in_workspace = pp.get_projects_number_from_workspace()
        assert_that(number_of_displayed_projects).is_equal_to(number_of_projects_in_workspace)

    @allure.description("Selecting and adding a project to workspace")
    @pytest.mark.run(order=5)
    def test_add_project_to_workspace(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        ptp = ProjectTypePage()
        tp = TemplatesPage()
        pep = ProjectEditPage()
        before = pp.get_projects_number_in_page()
        pp.create_new_project()
        ptp.select_project(self._project_type)
        tp.choose_template(self._template_type)
        pep.edit_project_prep(self._project_name, self._final_slide)
        pep.click_save_and_exit()
        after = pp.get_projects_number_in_page()
        assert_that(after).is_equal_to(before + 1)

    @allure.description("Search for an existing project")
    @pytest.mark.run(order=6)
    def test_search_project(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        pp.search_project(self._project_name)
        assert_that(pp.is_project_found(self._project_name)).is_true()

    @allure.description("Search for a non existing project")
    @pytest.mark.run(order=7)
    def test_search_for_non_existing_project(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        pp.search_project("Non Existing")
        assert_that(pp.get_no_project_found_msg()).is_equal_to(self._no_project_found_msg)

    @allure.description("Cancel project deletion")
    @pytest.mark.run(order=8)
    def test_cancel_project_deletion(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        before = pp.get_projects_number_in_page()
        pp.delete_project(self._project_name, "cancel")
        after = pp.get_projects_number_in_page()
        assert_that(after).is_equal_to(before)

    @allure.description("Deleting an existing project from workspace")
    @pytest.mark.run(order=9)
    def test_delete_project(self, create_driver, prep_properties):
        self.login(prep_properties)
        pp = ProjectsPage()
        before = pp.get_projects_number_in_page()
        pp.delete_project(self._project_name)
        after = pp.get_projects_number_in_page()
        assert_that(after).is_equal_to(before - 1)
