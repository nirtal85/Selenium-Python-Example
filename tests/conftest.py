import json
from collections import defaultdict
from contextlib import suppress
from datetime import datetime
from http import HTTPStatus

import allure
import requests
from git import Repo
from pytest import fixture, hookimpl
from selenium import webdriver

from globals.dir_global import ROOT_DIR
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


def get_public_ip() -> str:
    return requests.get("http://checkip.amazonaws.com").text.rstrip()


@fixture(scope="session")
def prep_properties():
    return ConfigParserIni("props.ini")


@fixture(autouse=True, scope="session")
# fetch browser type and base url then writes a dictionary of key-value pair into allure's environment.properties file
def write_allure_environment(prep_properties):
    yield
    repo = Repo(ROOT_DIR)
    env_parser = AllureEnvironmentParser("environment.properties")
    env_parser.write_to_allure_env(
        {
            "Browser": driver.name,
            "Driver_Version": driver.capabilities['browserVersion'],
            "Base_URL": base_url,
            "Commit_Date": datetime.fromtimestamp(repo.head.commit.committed_date).strftime('%c'),
            "Commit_Message": repo.head.commit.message.strip(),
            "Commit_Id": repo.head.object.hexsha,
            "Commit_Author_Name": repo.head.commit.author.name,
            "Branch": repo.active_branch.name
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
    global browser, base_url, driver, chrome_options
    browser = request.config.option.browser
    base_url = prep_properties.config_section_dict("Base Url")["base_url"]
    if browser in ("chrome", "chrome_headless"):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
        )
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False})
        chrome_options.add_argument("disable-dev-shm-usage")
        chrome_options.add_argument("no-sandbox")
        chrome_options.add_argument("allow-file-access-from-files")
        chrome_options.add_argument("use-fake-device-for-media-stream")
        chrome_options.add_argument("use-fake-ui-for-media-stream")
        chrome_options.add_argument("hide-scrollbars")
        chrome_options.add_argument("disable-features=VizDisplayCompositor")
        chrome_options.add_argument("disable-features=IsolateOrigins,site-per-process")
        chrome_options.add_argument("disable-popup-blocking")
        chrome_options.add_argument("disable-dev-shm-usage")
        chrome_options.add_argument("disable-notifications")
    match browser:
        case "firefox":
            driver = webdriver.Firefox()
        case "chrome_headless":
            chrome_options.add_argument("headless=new")
            driver = webdriver.Chrome(options=chrome_options)
        case _:
            driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get(base_url)
    yield
    if request.node.rep_call.failed:
        window_count = len(driver.window_handles)
        if window_count == 1:
            allure.attach(body=driver.get_screenshot_as_png(), name="Screenshot",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(body=driver.current_url, name="URL", attachment_type=allure.attachment_type.URI_LIST)
        else:
            for window in range(window_count):
                driver.switch_to.window(driver.window_handles[window])
                allure.attach(body=driver.get_screenshot_as_png(),
                              name=f"Full Page Screen Shot of window in index {window}",
                              attachment_type=allure.attachment_type.PNG)
                allure.attach(body=driver.current_url, name=f"URL of window in index {window}",
                              attachment_type=allure.attachment_type.URI_LIST)
    allure.attach(body=get_public_ip(), name="public ip address", attachment_type=allure.attachment_type.TEXT)
    allure.attach(body=json.dumps(driver.get_cookies(), indent=4), name="Cookies",
                  attachment_type=allure.attachment_type.JSON)
    allure.attach(body=json.dumps(
        {item[0]: item[1] for item in driver.execute_script("return Object.entries(sessionStorage);")}, indent=4),
        name="Session Storage", attachment_type=allure.attachment_type.JSON)
    allure.attach(body=json.dumps(
        {item[0]: item[1] for item in driver.execute_script("return Object.entries(localStorage);")}, indent=4),
        name="Local Storage", attachment_type=allure.attachment_type.JSON)
    allure.attach(body=json.dumps(driver.get_log("browser"), indent=4), name="Console Logs",
                  attachment_type=allure.attachment_type.JSON)
    allure.attach(
        body=json.dumps(attach_network_logs()[0], indent=4),
        name="Bad Responses Network Logs",
        attachment_type=allure.attachment_type.JSON
    )
    allure.attach(
        body=json.dumps(attach_network_logs()[1], indent=4),
        name="Good Responses Network Logs",
        attachment_type=allure.attachment_type.JSON
    )
    driver.quit()


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, f"rep_{rep.when}", rep)


def get_response_body(request_id):
    """Get the response body for the specified request ID."""
    return driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})


def get_request_post_data(request_id):
    """Get the request post data for the specified request ID."""
    return driver.execute_cdp_cmd("Network.getRequestPostData", {"requestId": request_id})


def attach_network_logs():
    bad_responses = defaultdict(dict)
    good_responses = defaultdict(dict)
    for item in [json.loads(log["message"])["message"] for log in driver.get_log("performance")]:
        params = item.get("params")
        if params.get("type") != "XHR":
            continue
        method = item.get("method")
        request_id = params["requestId"]
        if method == "Network.responseReceived":
            response_status = item["params"]["response"]["status"]
            if response_status >= HTTPStatus.BAD_REQUEST:
                response_log = bad_responses[request_id]
            else:
                response_log = good_responses[request_id]
            response_log["response"] = item
            with suppress(Exception):
                response_log["response"]["body"] = get_response_body(request_id)
        elif method == "Network.requestWillBeSent":
            request_log = good_responses[request_id]
            request_log["request"] = item
            if params.get("request", {}).get("hasPostData"):
                with suppress(Exception):
                    request_log["request"]["body"] = get_request_post_data(request_id)
    bad_responses = [item for item in bad_responses.values() if "response" in item]
    good_responses = [item for item in good_responses.values() if "response" in item]
    return bad_responses, good_responses
