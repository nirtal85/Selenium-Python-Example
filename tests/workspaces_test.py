import os

import allure
import pytest
from assertpy import assert_that

from src.enums.status import Status
from src.pages.about_page import AboutPage
from src.pages.login_page import LoginPage
from src.utilities.data import Data
from tests.base_test import BaseTest


def login(about_page: AboutPage, login_page: LoginPage):
    about_page.click_login_link()
    login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))


@allure.epic("Workspaces")
@allure.story("WorkSpaces Creation and Editing Functionality")
@allure.severity(allure.severity_level.NORMAL)
class TestWorkspaces(BaseTest):
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self):
        login(self.about_page, self.login_page)

    @allure.description("Create new Workspace")
    @allure.title("Create new workspace test")
    @pytest.mark.run(order=1)
    def test_create_new_workspace(self, data: Data) -> None:
        before = self.projects_page.get_workspaces_number()
        self.projects_page.create_workspace(data.workspace.name)
        after = self.projects_page.get_workspaces_number()
        assert_that(after).described_as("number of displayed workspaces").is_greater_than(before)

    @allure.description("Rename an existing workspace")
    @allure.title("Rename an existing workspace test")
    @pytest.mark.run(order=2)
    def test_rename_workspace(self, data: Data) -> None:
        self.projects_page.rename_workspace(data.workspace.name, data.workspace.new_name)
        assert_that(self.projects_page.is_workspace_found(data.workspace.new_name)).described_as(
            "status"
        ).is_true()

    @allure.description("Delete an existing workspace")
    @allure.title("Delete existing workspace")
    @pytest.mark.run(order=3)
    def test_delete_workspace(self) -> None:
        before = self.projects_page.get_workspaces_number()
        self.projects_page.delete_workspace()
        after = self.projects_page.get_workspaces_number()
        assert_that(after).described_as("workspace number").is_less_than(before)

    @allure.description(
        "Compare between the actual number of projects seen on page and the number shown in workspaces block"
    )
    @allure.title("Number of projects displayed in page test")
    @pytest.mark.run(order=4)
    def test_number_of_existing_projects(self) -> None:
        number_of_displayed_projects = self.projects_page.get_projects_number_in_page()
        number_of_projects_in_workspace = self.projects_page.get_projects_number_from_workspace()
        assert_that(number_of_displayed_projects).described_as(
            "number of displayed projects"
        ).is_equal_to(number_of_projects_in_workspace)

    @allure.description("Selecting and adding a project to workspace")
    @allure.title("Add project to workspace test")
    @pytest.mark.run(order=5)
    def test_add_project_to_workspace(self, data: Data) -> None:
        before = self.projects_page.get_projects_number_in_page()
        self.projects_page.create_new_project()
        self.project_type_page.select_project(data.workspace.project_type)
        self.templates_page.choose_template(data.workspace.template_type)
        self.project_edit_page.edit_project_prep(
            data.workspace.project_name,
            data.workspace.final_slide,
        )
        self.project_edit_page.click_save_and_exit()
        after = self.projects_page.get_projects_number_in_page()
        assert_that(before + 1).described_as("number of displayed projects").is_equal_to(after)

    @allure.description("Search for an existing project")
    @allure.title("Search for existing project test")
    @pytest.mark.run(order=6)
    def test_search_project(self, data: Data) -> None:
        self.projects_page.search_project(data.workspace.project_name)
        expected_status = self.projects_page.is_project_found(data.workspace.project_name)
        assert_that(expected_status).described_as("status").is_true()

    @allure.description("Search for a non existing project")
    @allure.title("Search for non existing project")
    @pytest.mark.run(order=7)
    def test_search_for_non_existing_project(self, data: Data) -> None:
        self.projects_page.search_project(data.workspace.non_existing_project)
        assert_that(self.projects_page.get_no_project_found_message()).described_as(
            "not found message"
        ).is_equal_to(data.workspace.no_project_found_message)

    @allure.description("Cancel project deletion")
    @allure.title("Cancel a project deletion")
    @pytest.mark.run(order=8)
    def test_cancel_project_deletion(self, data: Data) -> None:
        before = self.projects_page.get_projects_number_in_page()
        self.projects_page.delete_project(data.workspace.project_name, Status.CANCEL.value)
        after = self.projects_page.get_projects_number_in_page()
        assert_that(before).described_as("number of displayed projects").is_equal_to(after)

    @allure.description("Deleting an existing project from workspace")
    @allure.title("Delete existing project")
    @pytest.mark.run(order=9)
    def test_delete_project(self, data: Data) -> None:
        with allure.step("grand parent step"), allure.step("parent step"):
            before = self.projects_page.get_projects_number_in_page()
            self.projects_page.delete_project(data.workspace.project_name)
            after = self.projects_page.get_projects_number_in_page()
            assert_that(before).described_as("number of displayed projects").is_equal_to(
                after + 1
            )
