import base64
import json
import os
from collections import defaultdict
from contextlib import suppress
from datetime import datetime

import allure
import requests
from _pytest.config.argparsing import Parser
from _pytest.fixtures import fixture
from _pytest.nodes import Item
from _pytest.reports import BaseReport
from git import Repo
from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.support.wait import WebDriverWait

from globals import dir_global
from globals.dir_global import ROOT_DIR
from pages.about_page import AboutPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.project_edit_page import ProjectEditPage
from pages.project_type_page import ProjectTypePage
from pages.projects_page import ProjectsPage
from pages.templates_page import TemplatesPage
from utils.excel_parser import ExcelParser
from utils.web_driver_listener import DriverEventListener


def pytest_addoption(parser: Parser) -> None:
    """reads parameters from pytest command line"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="browser that the automation will run in",
    )
    parser.addoption(
        "--decorate_driver",
        action="store",
        default=False,
        help="should we decorate the driver",
    )
    parser.addini("base_url", "Base URL of the application")
    parser.addini("username", "Username for login")
    parser.addini("password", "Password for login")


@fixture(scope="session")
def json_data() -> dict:
    json_path = os.path.join(dir_global.DATA_FILES_PATH, "tests_data.json")
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data


def get_public_ip() -> str:
    return requests.get("http://checkip.amazonaws.com").text.rstrip()


@fixture(scope="session")
def excel_reader() -> ExcelParser:
    return ExcelParser("data.xls")


def pytest_sessionfinish() -> None:
    repo = Repo(ROOT_DIR)
    environment_properties = {
        "Browser": driver.name,
        "Driver_Version": driver.capabilities["browserVersion"],
        "Base_URL": base_url,
        "Commit_Date": datetime.fromtimestamp(repo.head.commit.committed_date).strftime(
            "%c"
        ),
        "Commit_Message": repo.head.commit.message.strip(),
        "Commit_Id": repo.head.object.hexsha,
        "Commit_Author_Name": repo.head.commit.author.name,
        "Branch": repo.active_branch.name,
    }
    allure_env_path = os.path.join("allure-results", "environment.properties")
    with open(allure_env_path, "w") as f:
        data = "\n".join(
            [
                f"{variable}={value}"
                for variable, value in environment_properties.items()
            ]
        )
        f.write(data)


def pytest_runtest_setup(item: Item) -> None:
    global browser, base_url, driver, chrome_options
    browser = item.config.option.browser
    base_url = item.config.getini("base_url")
    if browser in ("chrome", "chrome_headless"):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
        )
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option(
            "prefs",
            {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.geolocation": 1,
                "profile.default_content_setting_values.media_stream_camera": 1,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )
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
        case "remote":
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                desired_capabilities={
                    "browserName": "chrome",
                    "browserVersion": "114.0",
                    "selenoid:options": {
                        "enableVNC": True,
                        "enableVideo": True,
                        "videoName": f"{item.name}.mp4",
                    },
                },
            )
        case _:
            if item.config.option.decorate_driver:
                driver = EventFiringWebDriver(
                    webdriver.Chrome(options=chrome_options), DriverEventListener()
                )
            else:
                driver = webdriver.Chrome(options=chrome_options)
    item.cls.driver = driver
    driver.maximize_window()
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
    item.cls.wait = wait
    item.cls.about_page = AboutPage(driver, wait)
    item.cls.login_page = LoginPage(driver, wait)
    item.cls.projects_page = ProjectsPage(driver, wait)
    item.cls.forget_password_page = ForgotPasswordPage(driver, wait)
    item.cls.templates_page = TemplatesPage(driver, wait)
    item.cls.project_type_page = ProjectTypePage(driver, wait)
    item.cls.project_edit_page = ProjectEditPage(driver, wait)


def pytest_runtest_teardown() -> None:
    driver.quit()


def pytest_exception_interact(report: BaseReport) -> None:
    if not report.failed:
        return
    window_count = len(driver.window_handles)
    if window_count == 1:
        allure.attach(
            body=capture_full_page_screenshot(),
            name="Full Page Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            body=driver.current_url,
            name="URL",
            attachment_type=allure.attachment_type.URI_LIST,
        )
    else:
        for window in range(window_count):
            driver.switch_to.window(driver.window_handles[window])
            allure.attach(
                body=capture_full_page_screenshot(),
                name=f"Full Page Screen Shot of window in index {window}",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                body=driver.current_url,
                name=f"URL of window in index {window}",
                attachment_type=allure.attachment_type.URI_LIST,
            )
    allure.attach(
        body=get_public_ip(),
        name="public ip address",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        body=json.dumps(driver.get_cookies(), indent=4),
        name="Cookies",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        body=json.dumps(
            {
                item[0]: item[1]
                for item in driver.execute_script(
                    "return Object.entries(sessionStorage);"
                )
            },
            indent=4,
        ),
        name="Session Storage",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        body=json.dumps(
            {
                item[0]: item[1]
                for item in driver.execute_script(
                    "return Object.entries(localStorage);"
                )
            },
            indent=4,
        ),
        name="Local Storage",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        body=json.dumps(driver.get_log("browser"), indent=4),
        name="Console Logs",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        body=json.dumps(attach_network_logs(), indent=4),
        name="Network Logs",
        attachment_type=allure.attachment_type.JSON,
    )


def get_response_body(request_id):
    """Get the response body for the specified request ID."""
    return driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})


def get_request_post_data(request_id):
    """Get the request post data for the specified request ID."""
    return driver.execute_cdp_cmd(
        "Network.getRequestPostData", {"requestId": request_id}
    )


def capture_full_page_screenshot() -> bytes:
    """Gets full page screenshot of the current window as a binary data."""
    metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    return base64.b64decode(
        driver.execute_cdp_cmd(
            "Page.captureScreenshot",
            {
                "clip": {
                    "x": 0,
                    "y": 0,
                    "width": metrics["contentSize"]["width"],
                    "height": metrics["contentSize"]["height"],
                    "scale": 1,
                },
                "captureBeyondViewport": True,
            },
        )["data"]
    )


def attach_network_logs():
    network_logs = defaultdict(dict)
    for item in [
        json.loads(log["message"])["message"] for log in driver.get_log("performance")
    ]:
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
