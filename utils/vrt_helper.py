from typing import Tuple, Union

from pytest_check import check
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from visual_regression_tracker import (
    IgnoreArea,
    TestRun,
    TestRunStatus,
    VisualRegressionTracker,
)


class VrtHelper:
    """Helper class for capturing and comparing screenshots in Visual
    Regression Tracker (VRT).

    :param driver: The web driver instance (e.g., Chrome, Firefox,
        Edge).
    :param vrt_tracker: The Visual Regression Tracker for comparing
        screenshots.
    :param wait: The WebDriverWait instance for element synchronization.
    """

    def __init__(
        self,
        driver: Union[Chrome, Firefox, Edge],
        vrt_tracker: VisualRegressionTracker,
        wait: WebDriverWait,
    ):
        self.driver = driver
        self.vrt_tracker = vrt_tracker
        self.wait = wait

    def shoot_page(self, baseline_name: str):
        """Capture a screenshot of the current page compare the captured
        screenshot with a baseline image stored in Visual Regression tracker.

        :param baseline_name: A descriptive name for the baseline image.
        :return: None
        """
        check.equal(
            self.vrt_tracker.track(
                TestRun(
                    name=baseline_name,
                    imageBase64=self.driver.get_screenshot_as_base64(),
                )
            ).testRunResponse.status.name,
            TestRunStatus.OK.name,
        )

    def shoot_page_ang_ignore_elements(
        self, baseline_name: str, elements: list[WebElement]
    ):
        """Capture a screenshot of the current page, define areas to be ignored
        within the screenshot, compare the captured screenshot with a baseline
        image stored in Visual Regression tracker.

        :param baseline_name: A descriptive name for the baseline image.
        :type baseline_name: str
        :param elements: A list of WebElements to be ignored in the
            screenshot.
        :return: None
        """
        ignore_areas = []

        for element_to_ignore in elements:
            ignore_areas.append(
                IgnoreArea(
                    x=element_to_ignore.location["x"],
                    y=element_to_ignore.location["y"],
                    width=element_to_ignore.size["width"],
                    height=element_to_ignore.size["height"],
                )
            )
            check.equal(
                self.vrt_tracker.track(
                    TestRun(
                        name=baseline_name,
                        imageBase64=self.driver.get_screenshot_as_base64(),
                        ignoreAreas=ignore_areas,
                    )
                ).testRunResponse.status.name,
            )

    def shoot_element(self, baseline_name: str, locator: Tuple[str, str]):
        """Capture a screenshot of a specific element on the current page
        compare the captured screenshot with a baseline image stored in Visual
        Regression tracker.

        :param baseline_name: A descriptive name for the baseline image.
        :type baseline_name: str
        :param locator: A tuple containing the type and value of the
            element locator (e.g., (By.ID, 'element_id')).
        :return: None
        """
        element_to_shoot: WebElement = self.wait.until(
            expected_conditions.visibility_of_element_located(locator)
        )
        check.equal(
            self.vrt_tracker.track(
                TestRun(
                    name=baseline_name,
                    imageBase64=element_to_shoot.screenshot_as_base64,
                )
            ).testRunResponse.status.name,
            TestRunStatus.OK.name,
        )
