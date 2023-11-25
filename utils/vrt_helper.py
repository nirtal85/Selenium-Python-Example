import time
from contextlib import suppress
from typing import Tuple, Union

from pytest_check import check
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.common.by import By
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
        time.sleep(8)
        with suppress(Exception):
            self.censor_all_times()
            self.censor_all_dates()
            self.censor_credit_card_expiration()
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
        time.sleep(8)
        with suppress(Exception):
            self.censor_all_times()
            self.censor_all_dates()
            self.censor_credit_card_expiration()
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
        time.sleep(8)
        with suppress(Exception):
            self.censor_all_times()
            self.censor_all_dates()
            self.censor_credit_card_expiration()
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

    def censor_all_dates(self) -> None:
        """Replaces the dates in the text of all elements with "placeholder"
        characters.

        This method iterates through each month and finds elements
        containing that month in the text. It then replaces the day and
        year or just the day in the text with placeholders.
        :return: None
        """
        day_and_year_regex = " [0-3]?[0-9], [0-9]{4}"
        day_regex = " [0-3]?[0-9]"
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        for month in months:
            elements_with_month = self.driver.find_elements(
                By.XPATH, f"//p[contains(. , '{month}')]"
            )
            elements_with_month += self.driver.find_elements(
                By.XPATH, f"//*[contains(text(), '{month}')]"
            )

            if elements_with_month:
                for element_with_month in elements_with_month:
                    element_text = element_with_month.text
                    element_text = element_text.replace(
                        month + day_and_year_regex, "mmm dd, yyyy"
                    ).replace(month + day_regex, "mmm dd")

                    self.driver.execute_script(
                        f"arguments[0].innerHTML='{element_text}';",
                        element_with_month,
                    )

    def censor_credit_card_expiration(self) -> None:
        """Replaces the dates of credit card expiration with "placeholder"
        characters.

        Finds elements containing the text 'Expires' and replaces the
        content with a placeholder.
        :return: None
        """
        if credit_card_expiration_element := self.driver.find_elements(
            By.XPATH, "//p[contains(. , 'Expires')]"
        ):
            element_text = "Expires mm/dddd"
            self.driver.execute_script(
                f"arguments[0].innerHTML='{element_text}';",
                credit_card_expiration_element[0],
            )

    def censor_all_times(self) -> None:
        """Replaces the times (hours:minutes AM/PM) in the text of all elements
        with "placeholder" characters.

        Finds elements with text containing ':' and 'AM' or 'PM', then
        replaces the time format with placeholders.
        :return: None
        """
        time_regex = "[0-9]{1,2}:[0-9]{1,2} (AM|PM)"
        if elements_with_time := self.driver.find_elements(
            By.XPATH,
            "//*[text()[contains(., ':') and (contains(., 'AM') or contains(., 'PM'))]]",
        ):
            for element_with_time in elements_with_time:
                element_text = element_with_time.text
                element_text = element_text.replace(time_regex, "hh:mm AA")

                self.driver.execute_script(
                    f"arguments[0].innerHTML='{element_text}';", element_with_time
                )
