import json
import os
import socket

import allure
import pytest
from assertpy import assert_that

from tests.base_test import BaseTest
from src.utilities.constants import Constants
from src.utilities.data import Data

users = [("nirt236@gmail.com", "123456"), ("elias@gmail.com", "12345Tr")]


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Security")
@allure.feature("Login")
@pytest.mark.security
class TestLogin(BaseTest):
    @allure.description("invalid login")
    @allure.title("Login with invalid credentials test")
    @pytest.mark.parametrize("email, password", users)
    @pytest.mark.run(order=3)
    def test_invalid_login(self, email: str, password: str, data: Data) -> None:
        self.about_page.click_login_link()
        self.login_page.login(email, password)
        assert_that(self.login_page.get_error_message()).described_as(
            "login error message"
        ).is_equal_to(data.login.error_message)

    @allure.description("Basic sanity")
    @pytest.mark.devRun
    def test_sanity(self, base_url) -> None:
        assert_that(self.driver.current_url).described_as("URL").is_equal_to(base_url)

    @allure.description("valid login")
    @allure.title("Login with valid credentials test")
    @allure.tag("Tagged test")
    @pytest.mark.flaky(reruns=1)
    def test_valid_login(self, data: Data) -> None:
        self.about_page.set_geo_location(30.3079823, -97.893803)
        self.about_page.click_login_link()
        self.login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        assert_that(self.projects_page.get_title()).described_as("page title").is_equal_to(
            data.workspace.page_title
        )

    @allure.description("Log out from app")
    @allure.title("Logout of system test")
    @allure.story("As a user I want to be able to logout after a successful login.")
    def test_logout(self, data: Data) -> None:
        """Test case to verify the logout functionality.

        :param data: An instance of the Data dataclass containing test data.
        :type data: Data

        Source:
        - Example attachments from Allure-Pytest GitHub repository: https://github.com/allure-framework/allure-python/tree/master/allure-pytest/examples

        Steps:
        1. Perform a login with valid credentials.
        2. Click on the logout link.
        3. Verify that the page title matches the expected title after logout.

        Attachments:
        - A simple text attachment with masked password and hidden hostname.
        - Example HTML attachment.
        - Example file attachment (dog.png).
        - Example text content attachment.
        - Example CSV content attachment.
        - Example JSON content attachment.
        - Example XML content attachment.
        - Example URI list attachment.

        :return: None
        """
        allure.dynamic.parameter("password", "qwerty", mode=allure.parameter_mode.MASKED)
        allure.dynamic.parameter(
            "hostname", socket.gethostname(), mode=allure.parameter_mode.HIDDEN
        )
        allure.attach(
            "<h1>Example html attachment</h1>",
            name="HTML Attachment Example",
            attachment_type=allure.attachment_type.HTML,
        )
        # example of a file attachment
        allure.attach.file(
            Constants.DATA_PATH / "dog.png",
            name="File Attachment Example",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            "Some text content",
            name="Text Attachment Example",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            "first,second,third\none,two,three",
            name="CSV Attachment Example",
            attachment_type=allure.attachment_type.CSV,
        )
        allure.attach(
            json.dumps({"first": 1, "second": 2}, indent=2),
            name="JSON Attachment Example",
            attachment_type=allure.attachment_type.JSON,
        )
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
                <tag>
                     <inside>...</inside>
                 </tag>
             """
        allure.attach(
            xml_content,
            name="XML Attachment Example",
            attachment_type=allure.attachment_type.XML,
        )
        allure.attach(
            "\n".join(
                [
                    "https://github.com/allure-framework",
                    "https://github.com/allure-examples",
                ]
            ),
            name="URI List Attachment Example",
            attachment_type=allure.attachment_type.URI_LIST,
        )
        self.about_page.click_login_link()
        self.login_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        self.projects_page.logout()
        assert_that(self.login_page.get_page_title()).described_as("page title").is_equal_to(
            data.login.page_title
        )

    @allure.description("Skip Test example")
    @allure.title("Skipped test example")
    @allure.label("owner", "nir tal")
    @pytest.mark.skip(reason="skip test example")
    def test_skip(self) -> None:
        pass
