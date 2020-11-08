from datetime import datetime

import allure
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.about_page import AboutPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.project_edit_page import ProjectEditPage
from pages.project_type_page import ProjectTypePage
from pages.projects_page import ProjectsPage
from pages.templates_page import TemplatesPage
from utils.config_parser import ConfigParserIni
from utils.config_parser import EnvironmentParser


# reads parameters from pytest command line
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser that the automation will run in")


# writes a dictionary of key values into allure's environment.properties file
def write_to_allure_env_file(dic):
    env_parser = EnvironmentParser("environment.properties")
    env_parser.write_to_allure_env(dic)


@pytest.fixture(scope="session")
# instantiates ini file parses object
def prep_properties():
    config_reader = ConfigParserIni("props.ini")
    return config_reader


# https://stackoverflow.com/a/61433141/4515129
@pytest.fixture
# Instantiates Page Objects
def pages():
    about_page = AboutPage(driver)
    projects_page = ProjectsPage(driver)
    forgot_password_page = ForgotPasswordPage(driver)
    login_page = LoginPage(driver)
    project_type_page = ProjectTypePage(driver)
    templates_page = TemplatesPage(driver)
    project_edit_page = ProjectEditPage(driver)
    return locals()


@pytest.fixture(autouse=True)
# Performs setup and tear down
def create_driver(prep_properties, request):
    global driver
    browser = request.config.option.browser
    config_reader = prep_properties
    base_url = config_reader.config_section_dict("Base Url")["base_url"]
    write_to_allure_env_file({"browser": browser, "base_url": base_url})
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
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(base_url)
    yield
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# Takes screen shot if test fails
def pytest_runtest_makereport():
    outcome = yield
    assert driver is not None, "Expected instance of a Web Driver but got None instead"
    rep = outcome.get_result()
    if (rep.when == "setup" or rep.when == "call") and rep.failed:
        screenshot_name = 'screenshot on failure: %s' % datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        allure.attach(driver.get_screenshot_as_png(), name=screenshot_name,
                      attachment_type=allure.attachment_type.PNG)
