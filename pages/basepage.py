from selenium.common.exceptions import NoSuchElementException

from globals import driver_global as dg
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.expected_conditions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as AC


class BasePage:
    """ Wrapper for selenium operations """

    def __init__(self):
        self._driver = dg.DRIVER
        self._wait = WebDriverWait(self._driver, 10)

    def _click(self, locator):
        el = self._wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        self._highlight_element(el, "green")
        el.click()

    def _fill_text(self, locator, txt):
        el = self._wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        el.clear()
        self._highlight_element(el, "green")
        el.send_keys(txt)

    def _clear_text(self, locator):
        el = self._wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        el.clear()

    def _scroll_to_bottom(self):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _submit(self, el):
        self._highlight_element(el, "green")
        el.submit()

    def _get_text(self, el):
        self._wait.until(EC.visibility_of(el))
        return el.text

    def _move_to_element(self, el):
        action = AC(self._driver)
        self._wait.until(EC.visibility_of(el))
        action.move_to_element(el).perform()

    def _is_elem_displayed(self, el):
        try:
            return el.is_displayed()
        except StaleElementReferenceException:
            return False
        except NoSuchElementException:
            return False

    def _highlight_element(self, el, color):
        original_style = el.get_attribute("style")
        new_style = "background-color:yellow;border: 1px solid " + color + original_style
        self._driver.execute_script(
            "var tmpArguments = arguments;setTimeout(function () {tmpArguments[0].setAttribute('style', '"
            + new_style + "');},0);", el)
        dg.DRIVER.execute_script(
            "var tmpArguments = arguments;setTimeout(function () {tmpArguments[0].setAttribute('style', '"
            + original_style + "');},400);", el)
