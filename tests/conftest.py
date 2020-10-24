from datetime import datetime

import allure
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from globals import driver_global as dg
from utils.config_parser import ConfigParserIni


@pytest.fixture
def prep_properties():
    config_reader = ConfigParserIni("props.ini")
    return config_reader


@pytest.fixture(scope="class", autouse=True)
def create_driver(request):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    dg.DRIVER = driver
    driver.implicitly_wait(5)
    driver.maximize_window()

    def kill_driver():
        driver.quit()

    request.addfinalizer(kill_driver)


@pytest.fixture(autouse=True)
def navigate_to_base_url(prep_properties):
    config_reader = prep_properties
    base_url = config_reader.config_section_dict("Base Url")["base_url"]
    dg.DRIVER.get(base_url)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "setup" or rep.when == "call":
        if rep.failed:
            screenshot_name = 'screenshot-%s.png' % datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            allure.attach(dg.DRIVER.get_screenshot_as_png(), name=screenshot_name,
                          attachment_type=allure.attachment_type.PNG)
