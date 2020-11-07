import allure
import pytest
from assertpy import assert_that

from helper_enums.status_enum import StatusEnum
from tests.test_base import BaseTest
from utils.json_parser import JsonParser


# performs login operation
def login(prep_properties, pages):
    config = prep_properties
    username = config.config_section_dict("Base Url")["username"]
    password = config.config_section_dict("Base Url")["password"]
    pages['about_page'].click_login_link()
    pages['login_page'].login(username, password)


@allure.epic("Workspaces")
@allure.story("WorkSpaces Creation and Editing Functionality")
@allure.severity(allure.severity_level.NORMAL)
class TestWorkspaces(BaseTest):
    _DATA_FILE_NAME = "workspaces_test_data.json"

    @allure.description("Create new Workspace test")
    @allure.title("Create new workspace test")
    @pytest.mark.run(order=1)
    def test_create_new_workspace(self, prep_properties):
        login(prep_properties, self.pages)
        json_reader = JsonParser(self._DATA_FILE_NAME)
        before = self.pages['projects_page'].get_workspaces_number()
        self.pages['projects_page'].create_workspace(json_reader.read_from_json()["workspace_name"])
        after = self.pages['projects_page'].get_workspaces_number()
        assert_that(after).is_greater_than(before)

    @allure.description("Rename an existing workspace test")
    @allure.title("Rename an existing workspace test")
    @pytest.mark.run(order=2)
    def test_rename_workspace(self, prep_properties):
        login(prep_properties, self.pages)
        json_reader = JsonParser(self._DATA_FILE_NAME)
        self.pages['projects_page'].rename_workspace(json_reader.read_from_json()["workspace_name"],
                                                     json_reader.read_from_json()["new_workspace_name"])
        assert_that(self.pages['projects_page'].is_workspace_found(
            json_reader.read_from_json()["new_workspace_name"])).is_true()

    @allure.description("Delete an existing workspace test")
    @allure.title("Delete existing workspace test")
    @pytest.mark.run(order=3)
    def test_delete_workspace(self, prep_properties):
        login(prep_properties, self.pages)
        before = self.pages['projects_page'].get_workspaces_number()
        self.pages['projects_page'].delete_workspace()
        after = self.pages['projects_page'].get_workspaces_number()
        assert_that(after).is_less_than(before)

    @allure.description(
        "Compare between the actual number of projects seen on page and the number shown in workspaces block")
    @allure.title("Number of projects displayed in page test")
    @pytest.mark.run(order=4)
    def test_number_of_existing_projects(self, prep_properties):
        login(prep_properties, self.pages)
        number_of_displayed_projects = self.pages['projects_page'].get_projects_number_in_page()
        number_of_projects_in_workspace = self.pages['projects_page'].get_projects_number_from_workspace()
        assert_that(number_of_displayed_projects).is_equal_to(number_of_projects_in_workspace)

    @allure.description("Selecting and adding a project to workspace")
    @allure.title("Add project to workspace test")
    @pytest.mark.run(order=5)
    def test_add_project_to_workspace(self, prep_properties):
        login(prep_properties, self.pages)
        json_reader = JsonParser(self._DATA_FILE_NAME)
        before = self.pages['projects_page'].get_projects_number_in_page()
        self.pages['projects_page'].create_new_project()
        self.pages['project_type_page'].select_project(json_reader.read_from_json()["project_type"])
        self.pages['templates_page'].choose_template(json_reader.read_from_json()["template_type"])
        self.pages['project_edit_page'].edit_project_prep(json_reader.read_from_json()["project_name"],
                                                          json_reader.read_from_json()["final_slide"])
        self.pages['project_edit_page'].click_save_and_exit()
        after = self.pages['projects_page'].get_projects_number_in_page()
        assert_that(before + 1).is_equal_to(after)

    @allure.description("Search for an existing project")
    @allure.title("Search for existing project test")
    @pytest.mark.run(order=6)
    def test_search_project(self, prep_properties):
        login(prep_properties, self.pages)
        json_reader = JsonParser(self._DATA_FILE_NAME)
        self.pages['projects_page'].search_project(json_reader.read_from_json()["project_name"])
        assert_that(
            self.pages['projects_page'].is_project_found(json_reader.read_from_json()["project_name"])).is_true()

    @allure.description("Search for a non existing project")
    @allure.title("Search for non existing project test")
    @pytest.mark.run(order=7)
    def test_search_for_non_existing_project(self, prep_properties):
        login(prep_properties, self.pages)
        json_reader = JsonParser(self._DATA_FILE_NAME)
        self.pages['projects_page'].search_project("Non Existing")
        assert_that(json_reader.read_from_json()["no_project_found_msg"]).is_equal_to(
            self.pages['projects_page'].get_no_project_found_msg())

    @allure.description("Cancel project deletion")
    @allure.title("Cancel a project deletion test")
    @pytest.mark.run(order=8)
    def test_cancel_project_deletion(self, prep_properties):
        login(prep_properties, self.pages)
        json_reader = JsonParser(self._DATA_FILE_NAME)
        before = self.pages['projects_page'].get_projects_number_in_page()
        self.pages['projects_page'].delete_project(json_reader.read_from_json()["project_name"],
                                                   StatusEnum.CANCEL.value)
        after = self.pages['projects_page'].get_projects_number_in_page()
        assert_that(before).is_equal_to(after)

    @allure.description("Deleting an existing project from workspace")
    @allure.title("Delete existing project test")
    @pytest.mark.run(order=9)
    def test_delete_project(self, prep_properties):
        login(prep_properties, self.pages)
        json_reader = JsonParser(self._DATA_FILE_NAME)
        before = self.pages['projects_page'].get_projects_number_in_page()
        self.pages['projects_page'].delete_project(json_reader.read_from_json()["project_name"])
        after = self.pages['projects_page'].get_projects_number_in_page()
        assert_that(before).is_equal_to(after + 1)
