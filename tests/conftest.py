import base64
import json
import os
from collections import defaultdict
from contextlib import suppress
from datetime import datetime

import allure
import requests
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
from _pytest.reports import BaseReport
from git import Repo
from pytest import fixture
from selenium import webdriver

from globals.dir_global import ROOT_DIR
from pages.about_page import AboutPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.project_edit_page import ProjectEditPage
from pages.project_type_page import ProjectTypePage
from pages.projects_page import ProjectsPage
from pages.templates_page import TemplatesPage
from utils.excel_parser import ExcelParser
from utils.json_parser import JsonParser


# reads parameters from pytest command line
def pytest_addoption(parser: Parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser that the automation will run in")
    parser.addini("base_url", "Base URL of the application")
    parser.addini("username", "Username for login")
    parser.addini("password", "Password for login")


def pytest_configure(config: Config) -> None:
    config.option.allure_report_dir = "allure-results"


def get_public_ip() -> str:
    return requests.get("http://checkip.amazonaws.com").text.rstrip()


@fixture(scope="session")
def json_reader() -> JsonParser:
    return JsonParser("tests_data.json")


@fixture(scope="session")
def excel_reader() -> ExcelParser:
    return ExcelParser("data.xls")


def pytest_sessionfinish() -> None:
    repo = Repo(ROOT_DIR)
    environment_properties = {
        "Browser": driver.name,
        "Driver_Version": driver.capabilities['browserVersion'],
        "Base_URL": base_url,
        "Commit_Date": datetime.fromtimestamp(repo.head.commit.committed_date).strftime('%c'),
        "Commit_Message": repo.head.commit.message.strip(),
        "Commit_Id": repo.head.object.hexsha,
        "Commit_Author_Name": repo.head.commit.author.name,
        "Branch": repo.active_branch.name
    }
    allure_env_path = os.path.join("allure-results", 'environment.properties')
    with open(allure_env_path, 'w') as f:
        data = '\n'.join([f'{variable}={value}' for variable, value in environment_properties.items()])
        f.write(data)


@fixture(autouse=True)
def create_driver(request: FixtureRequest):
    global browser, base_url, driver, chrome_options
    browser = request.config.option.browser
    base_url = request.config.getini("base_url")
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
    request.cls.driver = driver
    driver.maximize_window()
    driver.get(base_url)
    request.cls.about_page = AboutPage(driver)
    request.cls.login_page = LoginPage(driver)
    request.cls.projects_page = ProjectsPage(driver)
    request.cls.forget_password_page = ForgotPasswordPage(driver)
    request.cls.templates_page = TemplatesPage(driver)
    request.cls.project_type_page = ProjectTypePage(driver)
    request.cls.project_edit_page = ProjectEditPage(driver)
    yield
    driver.quit()


def pytest_exception_interact(report: BaseReport):
    if not report.failed:
        return
    window_count = len(driver.window_handles)
    if window_count == 1:
        allure.attach(body=capture_full_page_screenshot(), name="Full Page Screenshot",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(body=driver.current_url, name="URL", attachment_type=allure.attachment_type.URI_LIST)
    else:
        for window in range(window_count):
            driver.switch_to.window(driver.window_handles[window])
            allure.attach(body=capture_full_page_screenshot(), name=f"Full Page Screen Shot of window in "
                                                                    f"index {window}",
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
    allure.attach(body=json.dumps(attach_network_logs(), indent=4), name="Network Logs",
                  attachment_type=allure.attachment_type.JSON)


def get_response_body(request_id):
    """Get the response body for the specified request ID."""
    return driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})


def get_request_post_data(request_id):
    """Get the request post data for the specified request ID."""
    return driver.execute_cdp_cmd("Network.getRequestPostData", {"requestId": request_id})


def capture_full_page_screenshot() -> bytes:
    """Gets full page screenshot of the current window as a binary data. """
    metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    return base64.b64decode(driver.execute_cdp_cmd("Page.captureScreenshot", {
        "clip": {
            "x": 0,
            "y": 0,
            "width": metrics['contentSize']['width'],
            "height": metrics['contentSize']['height'],
            "scale": 1
        },
        "captureBeyondViewport": True
    })['data'])


def attach_network_logs():
    network_logs = defaultdict(dict)
    for item in [json.loads(log["message"])["message"] for log in driver.get_log("performance")]:
        params = item.get("params")
        if params.get("type") != "XHR":
            continue
        method = item.get("method")
        request_id = params["requestId"]
        network_log = network_logs[request_id]
        if method == "Network.responseReceived":
            network_log["response"] = item
            with suppress(Exception):
                network_log["response"]["body"] = get_response_body(request_id)
        elif method == "Network.requestWillBeSent":
            network_log["request"] = item
            if params.get("request", {}).get("hasPostData"):
                with suppress(Exception):
                    network_log["request"]["body"] = get_request_post_data(request_id)
    return [item for item in network_logs.values() if "response" in item]
