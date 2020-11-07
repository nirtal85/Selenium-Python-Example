from datetime import datetime

import allure
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from globals import driver_global as dg
from pages.about_page import AboutPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.project_edit_page import ProjectEditPage
from pages.project_type_page import ProjectTypePage
from pages.projects_page import ProjectsPage
from pages.templates_page import TemplatesPage
from utils.config_parser import ConfigParserIni


# reads parameters from pytest command line
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser that the automation will run in")


@pytest.fixture(scope="session")
def prep_properties():
    config_reader = ConfigParserIni("props.ini")
    return config_reader


# https://stackoverflow.com/a/61433141/4515129
@pytest.fixture
def pages():
    about_page = AboutPage()
    projects_page = ProjectsPage()
    forgot_password_page = ForgotPasswordPage()
    login_page = LoginPage()
    project_type_page = ProjectTypePage()
    templates_page = TemplatesPage()
    project_edit_page = ProjectEditPage()
    return locals()


@pytest.fixture(autouse=True)
def create_driver(prep_properties, request):
    browser = request.config.option.browser
    config_reader = prep_properties
    base_url = config_reader.config_section_dict("Base Url")["base_url"]
    if browser == "firefox":
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
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install())
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
    driver = dg.DRIVER
    assert driver is not None, "Expected instance of a Web Driver but got None instead"
    rep = outcome.get_result()
    if (rep.when == "setup" or rep.when == "call") and rep.failed:
        screenshot_name = 'screenshot on failure: %s' % datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        allure.attach(driver.get_screenshot_as_png(), name=screenshot_name,
                      attachment_type=allure.attachment_type.PNG)
