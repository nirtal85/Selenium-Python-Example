import allure
import pytest
from assertpy import assert_that

from helper_enums.status_enum import StatusEnum
from tests.test_base import BaseTest


# performs login operation
def login(prep_properties, pages):
    username = prep_properties.config_section_dict("Base Url")["username"]
    password = prep_properties.config_section_dict("Base Url")["password"]
    pages['about_page'].click_login_link()
    pages['login_page'].login(username, password)


@allure.epic("Workspaces")
@allure.story("WorkSpaces Creation and Editing Functionality")
@allure.severity(allure.severity_level.NORMAL)
class TestWorkspaces(BaseTest):

    @allure.description("Create new Workspace")
    @allure.title("Create new workspace test")
    @pytest.mark.run(order=1)
    def test_create_new_workspace(self):
        login(self.config_reader, self.pages)
        before = self.pages['projects_page'].get_workspaces_number()
        self.pages['projects_page'].create_workspace(self.json_reader.read_from_json()["workspace"]["name"])
        after = self.pages['projects_page'].get_workspaces_number()
        assert_that(after).is_greater_than(before)

    @allure.description("Rename an existing workspace")
    @allure.title("Rename an existing workspace test")
    @pytest.mark.run(order=2)
    def test_rename_workspace(self):
        login(self.config_reader, self.pages)
        self.pages['projects_page'].rename_workspace(self.json_reader.read_from_json()["workspace"]["name"],
                                                     self.json_reader.read_from_json()["workspace"][
                                                         "new_name"])
        expected_status = self.pages['projects_page'].is_workspace_found(
            self.json_reader.read_from_json()["workspace"]["new_name"])
        assert_that(expected_status).is_true()

    @allure.description("Delete an existing workspace")
    @allure.title("Delete existing workspace")
    @pytest.mark.run(order=3)
    def test_delete_workspace(self):
        login(self.config_reader, self.pages)
        before = self.pages['projects_page'].get_workspaces_number()
        self.pages['projects_page'].delete_workspace()
        after = self.pages['projects_page'].get_workspaces_number()
        assert_that(after).is_less_than(before)

    @allure.description(
        "Compare between the actual number of projects seen on page and the number shown in workspaces block")
    @allure.title("Number of projects displayed in page test")
    @pytest.mark.run(order=4)
    def test_number_of_existing_projects(self):
        login(self.config_reader, self.pages)
        number_of_displayed_projects = self.pages['projects_page'].get_projects_number_in_page()
        number_of_projects_in_workspace = self.pages['projects_page'].get_projects_number_from_workspace()
        assert_that(number_of_displayed_projects).is_equal_to(number_of_projects_in_workspace)

    @allure.description("Selecting and adding a project to workspace")
    @allure.title("Add project to workspace test")
    @pytest.mark.run(order=5)
    def test_add_project_to_workspace(self):
        login(self.config_reader, self.pages)
        before = self.pages['projects_page'].get_projects_number_in_page()
        self.pages['projects_page'].create_new_project()
        self.pages['project_type_page'].select_project(self.json_reader.read_from_json()["workspace"]["project_type"])
        self.pages['templates_page'].choose_template(self.json_reader.read_from_json()["workspace"]["template_type"])
        self.pages['project_edit_page'].edit_project_prep(
            self.json_reader.read_from_json()["workspace"]["project_name"],
            self.json_reader.read_from_json()["workspace"]["final_slide"])
        self.pages['project_edit_page'].click_save_and_exit()
        after = self.pages['projects_page'].get_projects_number_in_page()
        assert_that(before + 1).is_equal_to(after)

    @allure.description("Search for an existing project")
    @allure.title("Search for existing project test")
    @pytest.mark.run(order=6)
    def test_search_project(self):
        login(self.config_reader, self.pages)
        self.pages['projects_page'].search_project(self.json_reader.read_from_json()["workspace"]["project_name"])
        expected_status = self.pages['projects_page'].is_project_found(
            self.json_reader.read_from_json()["workspace"]["project_name"])
        assert_that(expected_status).is_true()

    @allure.description("Search for a non existing project")
    @allure.title("Search for non existing project")
    @pytest.mark.run(order=7)
    def test_search_for_non_existing_project(self):
        login(self.config_reader, self.pages)
        self.pages['projects_page'].search_project(
            self.json_reader.read_from_json()["workspace"]["non_existing_project"])
        expected_not_found_msg = self.json_reader.read_from_json()["workspace"]["no_project_found_msg"]
        assert_that(expected_not_found_msg).is_equal_to(self.pages['projects_page'].get_no_project_found_msg())

    @allure.description("Cancel project deletion")
    @allure.title("Cancel a project deletion")
    @pytest.mark.run(order=8)
    def test_cancel_project_deletion(self):
        login(self.config_reader, self.pages)
        before = self.pages['projects_page'].get_projects_number_in_page()
        self.pages['projects_page'].delete_project(self.json_reader.read_from_json()["workspace"]["project_name"],
                                                   StatusEnum.CANCEL.value)
        after = self.pages['projects_page'].get_projects_number_in_page()
        assert_that(before).is_equal_to(after)

    @allure.description("Deleting an existing project from workspace")
    @allure.title("Delete existing project")
    @pytest.mark.run(order=9)
    def test_delete_project(self):
        login(self.config_reader, self.pages)
        before = self.pages['projects_page'].get_projects_number_in_page()
        self.pages['projects_page'].delete_project(self.json_reader.read_from_json()["workspace"]["project_name"])
        after = self.pages['projects_page'].get_projects_number_in_page()
        assert_that(before).is_equal_to(after + 1)
