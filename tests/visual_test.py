import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions

from tests.base_test import BaseTest


@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Login")
@pytest.mark.security
@pytest.mark.skip(reason="requires a running VRT server")
class TestVisual(BaseTest):
    @allure.title("Visual test of login page")
    def test_shoot_page(self, vrt_helper):
        vrt_helper.shoot_page("page baseline")

    @allure.title("Visual test of login page with ignored area")
    def test_shoot_page_with_ignore_area(self, vrt_helper):
        element_to_ignore: WebElement = self.wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        elements_to_ignore_list = [element_to_ignore]
        vrt_helper.shoot_page_ang_ignore_elements(
            "page baseline with ignored element", elements_to_ignore_list
        )

    @allure.title("Visual test of login page element")
    def test_shoot_element(self, vrt_helper):
        vrt_helper.shoot_element("element baseline", (By.CSS_SELECTOR, "h1"))
