import allure
import pytest
from assertpy import assert_that
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from visual_regression_tracker import IgnoreArea, TestRun, TestRunStatus

from tests.base_test import BaseTest


@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Login")
@pytest.mark.security
@pytest.mark.skip(reason="requires a running VRT server")
class TestVisual(BaseTest):
    @allure.title("Visual test of login page")
    def test_shoot_page(self, vrt_tracker):
        assert_that(
            vrt_tracker.track(
                TestRun(
                    name="my image",
                    imageBase64=self.driver.get_screenshot_as_base64(),
                )
            ).testRunResponse.status.name
        ).is_equal_to(TestRunStatus.OK.name)

    @allure.title("Visual test of login page with ignored area")
    def test_shoot_page_with_ignore_area(self, vrt_tracker):
        element_to_ignore: WebElement = self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        assert_that(
            vrt_tracker.track(
                TestRun(
                    name="my image",
                    imageBase64=self.driver.get_screenshot_as_base64(),
                    ignoreAreas=(
                        [
                            IgnoreArea(
                                x=element_to_ignore.location["x"],
                                y=element_to_ignore.location["y"],
                                width=element_to_ignore.size["width"],
                                height=element_to_ignore.size["height"],
                            )
                        ]
                    ),
                )
            ).testRunResponse.status.name
        ).is_equal_to(TestRunStatus.OK.name)

    @allure.title("Visual test of login page element")
    def test_shoot_element(self, vrt_tracker):
        element_to_shoot: WebElement = self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        assert_that(
            vrt_tracker.track(
                TestRun(
                    name="my image",
                    imageBase64=element_to_shoot.screenshot_as_base64,
                )
            ).testRunResponse.status.name
        ).is_equal_to(TestRunStatus.OK.name)
