from typing import Union, List

from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


class DriverEventListener(AbstractEventListener):
    def after_find(self, by: By, value: str, driver: Union[Chrome, Firefox, Edge]) -> None:
        webelements: List[WebElement] = driver.find_elements(by=by, value=value)
        for element in webelements:
            if element.is_displayed():
                driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", element)