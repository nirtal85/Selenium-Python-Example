from datetime import datetime
import json
import allure
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from globals import driver_global as dg
from utils.config_parser import ConfigParserIni


@pytest.fixture
def read_from_json():
    # read from file
    with open("config.json") as json_file:
        json_reader = json.load(json_file)
    return json_reader


@pytest.fixture(scope="session")
def prep_properties():
    config_reader = ConfigParserIni("props.ini")
    return config_reader


@pytest.fixture
def create_driver(prep_properties):
    config_reader = prep_properties
    browser = config_reader.config_section_dict("Browsers")["browser"]
    base_url = config_reader.config_section_dict("Base Url")["base_url"]
    if browser == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    dg.DRIVER = driver
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(base_url)
    yield driver
    driver.quit()


#
# @pytest.fixture(autouse=True)
# def navigate_to_base_url(prep_properties):
#     config_reader = prep_properties
#     base_url = config_reader.config_section_dict("Base Url")["base_url"]
#     dg.DRIVER.get(base_url)

# hello world
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport():
#     outcome = yield
#     rep = outcome.get_result()
#     if rep.when == "setup" or rep.when == "call":
#         if rep.failed:
#             screenshot_name = 'screenshot on failure: %s' % datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
#             allure.attach(dg.DRIVER.get_screenshot_as_png(), name=screenshot_name,
#                           attachment_type=allure.attachment_type.PNG)
