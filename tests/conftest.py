from datetime import datetime
import json
import allure
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from globals import driver_global as dg
from utils.config_parser import ConfigParserIni


# reads parameters from pytest command line
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


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
def create_driver(prep_properties, request):
    browser = request.config.option.browser
    config_reader = prep_properties
    base_url = config_reader.config_section_dict("Base Url")["base_url"]
    if browser == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser == "remote":
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "86.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False
            }
        }
        driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities=capabilities)
    elif browser == "chrome_headless":
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    dg.DRIVER = driver
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(base_url)
    yield driver
    driver.quit()


# need to pass driver pronto
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport():
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "setup" or rep.when == "call":
        if rep.failed:
            screenshot_name = 'screenshot on failure: %s' % datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            allure.attach(dg.DRIVER.get_screenshot_as_png(), name=screenshot_name,
                          attachment_type=allure.attachment_type.PNG)
