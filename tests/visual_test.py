import allure
import pytest
from assertpy import assert_that
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from visual_regression_tracker import IgnoreArea, TestRun, TestRunStatus

from tests.base_test import BaseTest


@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Login")
@pytest.mark.security
@pytest.mark.skip(reason="requires a running VRT server")
class TestVisual(BaseTest):
    @allure.title("Visual test of login page")
    def test_login_visual(self, vrt_tracker):
        assert_that(
            vrt_tracker.track(
                TestRun(
                    name="my image",
                    imageBase64=self.driver.get_screenshot_as_base64(),
                )
            ).testRunResponse.status.name
        ).is_equal_to(TestRunStatus.OK)

    @allure.title("Visual test of login page with ignored area")
    def test_login_visual_with_ignore_area(self, vrt_tracker):
        element_to_ignore = self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        location = element_to_ignore.location
        size = element_to_ignore.size
        width, height, x, y = (
            size["width"],
            size["height"],
            location["x"],
            location["y"],
        )
        assert_that(
            vrt_tracker.track(
                TestRun(
                    name="my image",
                    imageBase64=self.driver.get_screenshot_as_base64(),
                    ignoreAreas=(
                        [
                            IgnoreArea(
                                x=x,
                                y=y,
                                width=width,
                                height=height,
                            )
                        ]
                    ),
                )
            ).testRunResponse.status.name
        ).is_equal_to(TestRunStatus.OK)
