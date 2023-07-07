from typing import List, Union

from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.wait import WebDriverWait


class DriverEventListener(AbstractEventListener):
    def after_find(
        self, by: By, value: str, driver: Union[Chrome, Firefox, Edge]
    ) -> None:
        webelements: List[WebElement] = driver.find_elements(by=by, value=value)
        for element in webelements:
            if element.is_displayed():
                driver.execute_script(
                    "arguments[0].setAttribute('style', 'border: 2px solid red;');",
                    element,
                )

    def before_click(
        self, element: WebElement, driver: Union[Chrome, Firefox, Edge]
    ) -> None:
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.element_to_be_clickable(element))
