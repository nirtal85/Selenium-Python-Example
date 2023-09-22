import allure
import pytest
from assertpy import assert_that
from visual_regression_tracker import TestRun, TestRunStatus

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
