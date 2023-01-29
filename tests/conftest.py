import os
import subprocess
from datetime import datetime

import allure
import requests
from pytest import fixture, hookimpl
from selenium import webdriver

from pages.about_page import AboutPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.project_edit_page import ProjectEditPage
from pages.project_type_page import ProjectTypePage
from pages.projects_page import ProjectsPage
from pages.templates_page import TemplatesPage
from utils.config_parser import AllureEnvironmentParser
from utils.config_parser import ConfigParserIni


# reads parameters from pytest command line
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser that the automation will run in")


def get_public_ip():
    return requests.get("http://checkip.amazonaws.com").text.rstrip()


@fixture(scope="session")
def prep_properties():
    return ConfigParserIni("props.ini")


@fixture(autouse=True, scope="session")
# fetch browser type and base url then writes a dictionary of key-value pair into allure's environment.properties file
def write_allure_environment(prep_properties):
    yield
    env_parser = AllureEnvironmentParser("environment.properties")
    # Run the 'git log' command to retrieve the latest commit information
    result = subprocess.run(['git', '-C', os.getcwd(), 'log', '-1', '--pretty=format:"%h|%cd|%B|%an|%d"'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Split the result into separate pieces of information
    commit_info = result.stdout.strip().split('|')
    commit_id = commit_info[0]
    commit_date = commit_info[1]
    commit_message = commit_info[2]
    commit_author = commit_info[3]
    working_branch = commit_info[4]
    env_parser.write_to_allure_env(
        {
            "Browser": driver.name,
            "Driver_Version": driver.capabilities['browserVersion'],
            "Base_URL": base_url,
            "Commit_Date": commit_date,
            "Commit Message": commit_message,
            "Commit Id": commit_id,
            "Commit_Author_Name": commit_author,
            "Branch": working_branch
        })


# https://stackoverflow.com/a/61433141/4515129
@fixture
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


@fixture(autouse=True)
def create_driver(write_allure_environment, prep_properties, request):
    global browser, base_url, driver
    browser = request.config.option.browser
    base_url = prep_properties.config_section_dict("Base Url")["base_url"]

    if browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "chrome_headless":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(base_url)
    yield
    if request.node.rep_call.failed:
        screenshot_name = f"screenshot on failure: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"
        allure.attach(body=driver.get_screenshot_as_png(), name=screenshot_name,
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(body=get_public_ip(), name="public ip address", attachment_type=allure.attachment_type.TEXT)
    driver.quit()


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, f"rep_{rep.when}", rep)
