from typing import Union

from selenium.webdriver import Chrome, Firefox, Edge


class BaseTest:
    driver: Union[Chrome, Firefox, Edge] = None
