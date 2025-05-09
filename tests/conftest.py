import base64
import json
import logging
import os
from collections import defaultdict
from contextlib import suppress

import allure
import pytest
import requests
from _pytest.config.argparsing import Parser
from _pytest.fixtures import fixture
from _pytest.nodes import Item
from dotenv import load_dotenv
from mailinator import Mailinator
from mysql.connector import MySQLConnection
from requests_toolbelt.utils import dump
from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.support.wait import WebDriverWait
from visual_regression_tracker import VisualRegressionTracker

from src.pages.about_page import AboutPage
from src.pages.forgot_password_page import ForgotPasswordPage
from src.pages.login_page import LoginPage
from src.pages.project_edit_page import ProjectEditPage
from src.pages.project_type_page import ProjectTypePage
from src.pages.projects_page import ProjectsPage
from src.pages.templates_page import TemplatesPage
from src.utilities.constants import Constants
from src.utilities.mailinator_helper import MailinatorHelper
from src.utilities.web_driver_listener import DriverEventListener
from src.utilities.excel_parser import ExcelParser
from src.utilities.data import Data
from src.utilities.vrt_helper import VrtHelper

drivers = ("chrome", "firefox", "chrome_headless", "remote")


def pytest_addoption(parser: Parser) -> None:
    """Reads parameters from pytest command line."""
    parser.addoption(
        "--driver",
        action="store",
        choices=drivers,
        default="chrome",
        help="driver to run tests against",
    )
    parser.addoption(
        "--decorate_driver",
        action="store",
        default=False,
        help="should we decorate the driver",
    )


@fixture(scope="session")
def data() -> Data:
    json_path = Constants.DATA_PATH / "tests_data.json"
    with open(json_path, encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return Data.from_dict(json_data)


def get_public_ip(session: requests.Session) -> str:
    return session.get("http://checkip.amazonaws.com", timeout=40).text.rstrip()


@fixture(scope="session")
def excel_reader() -> ExcelParser:
    return ExcelParser("data.xls")


@pytest.fixture(scope="session", autouse=True)
def session_request():
    """Fixture to create a session object with a logging hook for HTTP
    requests.

    This fixture is based on a helpful solution provided on StackOverflow:
    https://stackoverflow.com/a/70351922

    Returns:
        requests.Session: A session object with a logging hook.

    """
    session = requests.Session()
    session.headers = {"User-Agent": Constants.AUTOMATION_USER_AGENT}
    session.hooks["response"] = lambda response, *args, **kwargs: allure.attach(
        dump.dump_all(response).decode("utf-8"),
        name=f"HTTP logs of {response.url}",
        attachment_type=allure.attachment_type.TEXT,
    )
    yield session
    session.close()


@fixture(scope="session")
def mailinator_helper() -> MailinatorHelper:
    return MailinatorHelper(
        Mailinator(os.environ.get("MAILINATOR_API_KEY")),
        os.environ.get("MAILINATOR_DOMAIN_NAME"),
    )


@pytest.fixture(scope="session")
def db_connection():
    """Fixture to establish a database connection."""
    connection = MySQLConnection(user="root", password="1234", database="world")
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def vrt_helper():
    """Fixture for creating a Visual Regression Tracker (VRT) helper object.

    This fixture sets up a Visual Regression Tracker helper object that provides
    convenient methods for capturing and comparing screenshots with a Visual Regression
    Tracker (VRT) server. It starts the VRT server before all tests and stops it
    after all tests have completed.

    Usage:
    1. Import this fixture into your test module.
    2. Use the returned `VrtHelper` instance as a parameter in your test functions to
       access methods for VRT-related tasks.

    Links:
    - Visual Regression Tracker GitHub Repository: https://github.com/Visual-Regression-Tracker/examples-python
    - Visual Regression Tracker SDK for Python: https://github.com/Visual-Regression-Tracker/sdk-python
    """
    vrt = VisualRegressionTracker()
    vrt.start()
    yield VrtHelper(driver, vrt, wait)
    vrt.stop()


def pytest_runtest_setup(item: Item) -> None:
    global browser, driver, chrome_options, wait, console_messages, javascript_errors
    browser = item.config.getoption("driver")
    base_url = item.config.getoption("base_url")
    if browser in ("chrome", "chrome_headless"):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})
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
                "safebrowsing.enabled": False,
                "download.default_directory": os.path.abspath(
                    Constants.CHROME_DOWNLOAD_DIRECTORY.absolute().as_posix()
                ),
            },
        )
        chrome_options.enable_bidi = True
        # https://forum.robotframework.org/t/maximize-window-chromedriver-133/8416/3
        chrome_options.browser_version = "132"
        chrome_options.add_argument("disable-dev-shm-usage")
        chrome_options.add_argument("no-sandbox")
        chrome_options.add_argument("allow-file-access-from-files")
        chrome_options.add_argument("use-fake-device-for-media-stream")
        chrome_options.add_argument("hide-scrollbars")
        chrome_options.add_argument("disable-popup-blocking")
        chrome_options.add_argument("disable-notifications")
        chrome_options.add_argument("disable-infobars")
        # https://www.selenium.dev/blog/2024/chrome-browser-woes/
        chrome_options.add_argument("disable-search-engine-choice-screen")
        chrome_options.add_argument(
            "disable-features=IsolateOrigins,site-per-process,VizDisplayCompositor,"
            "SidePanelPinning,OptimizationGuideModelDownloading,OptimizationHintsFetching,"
            "OptimizationTargetPrediction,OptimizationHints"
        )
        # example of adding specific chrome option based on test file name
        if item.fspath.purebasename == "workspaces_test":
            chrome_options.add_argument("use-fake-ui-for-media-stream")
        # example of adding specific chrome option based on test name
        if item.name == "test_invalid_login":
            chrome_options.add_argument(f"user-agent={Constants.AUTOMATION_USER_AGENT}")
    match browser:
        case "firefox":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.enable_bidi = True
            driver = webdriver.Firefox(firefox_options)
        case "chrome_headless":
            chrome_options.add_argument("headless=new")
            chrome_options.add_argument("force-device-scale-factor=0.6")
            chrome_options.add_argument("window-size=1920,1080")
            driver = webdriver.Chrome(options=chrome_options)
        # https://stackoverflow.com/questions/76430192/getting-typeerror-webdriver-init-got-an-unexpected-keyword-argument-desi
        case "remote":
            chrome_options = webdriver.ChromeOptions()
            # https://aerokube.com/images/latest/#_chrome
            chrome_options.browser_version = "128.0"
            chrome_options.set_capability(
                "selenoid:options",
                {
                    "enableVNC": True,
                    "enableVideo": True,
                    "videoName": f"{item.name}.mp4",
                },
            )
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub", options=chrome_options
            )
        case _:
            if item.config.getoption("decorate_driver"):
                driver = EventFiringWebDriver(
                    webdriver.Chrome(options=chrome_options), DriverEventListener()
                )
            else:
                driver = webdriver.Chrome(options=chrome_options)
    item.cls.driver = driver
    driver.maximize_window()
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
    if browser != "remote":
        console_messages = []
        driver.script.add_console_message_handler(
            lambda log_entry: console_messages.append(log_entry.__dict__)
        )
        javascript_errors = []
        driver.script.add_javascript_error_handler(
            lambda log_entry: javascript_errors.append(log_entry.__dict__)
        )
    item.cls.wait = wait
    item.cls.about_page = AboutPage(driver, wait)
    item.cls.login_page = LoginPage(driver, wait)
    item.cls.projects_page = ProjectsPage(driver, wait)
    item.cls.forget_password_page = ForgotPasswordPage(driver, wait)
    item.cls.templates_page = TemplatesPage(driver, wait)
    item.cls.project_type_page = ProjectTypePage(driver, wait)
    item.cls.project_edit_page = ProjectEditPage(driver, wait)


def pytest_runtest_teardown() -> None:
    """Pytest hook for teardown after each test.

    Checks if the 'driver' variable is present in the local or global namespace.
    If found, it calls the 'quit()' method on the 'driver' object to close the browser.

    Note: This function assumes that the 'driver' variable is used for browser automation,
    and its presence is necessary for cleanup.

    Returns:
        None

    """
    if "driver" in locals() or "driver" in globals():
        driver.quit()


def pytest_sessionstart() -> None:
    """Loading sensitive data from environment variables.

    and setting selenium logging
    """
    load_dotenv()
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("selenium")
    logger.setLevel(logging.DEBUG)


def pytest_exception_interact(node: Item) -> None:
    """Pytest hook for interacting with exceptions during test execution.

    If the 'driver' variable is present in the local or global namespace, this function performs various
    actions for reporting using the 'allure' reporting framework. If 'driver' is not present, the function
    returns without taking any action.

    Args:
        node (Item): The pytest Item representing the test item.

    Returns:
        None

    """
    session_request: requests.Session = node.funcargs["session_request"]
    if "driver" not in locals() and "driver" not in globals():
        return
    window_count = len(driver.window_handles)
    if browser == "remote":
        allure.attach(
            body="<html><body><video width='100%%' height='100%%' controls autoplay><source "
            f"src='http://localhost:4444/video/{node.name}.mp4' "
            "type='video/mp4'></video></body></html>",
            name="Video record",
            attachment_type=allure.attachment_type.HTML,
        )
        if window_count == 1:
            allure.attach(
                body=driver.get_screenshot_as_png(),
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
                    body=driver.get_screenshot_as_png(),
                    name=f"Full Page Screen Shot of window in index {window}",
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach(
                    body=driver.current_url,
                    name=f"URL of window in index {window}",
                    attachment_type=allure.attachment_type.URI_LIST,
                )
    with allure.step("public ip address"):
        get_public_ip(session_request)
    allure.attach(
        body=json.dumps(driver.get_cookies(), indent=4),
        name="Cookies",
        attachment_type=allure.attachment_type.JSON,
    )
    allure.attach(
        body=json.dumps(
            {
                item[0]: item[1]
                for item in driver.execute_script("return Object.entries(sessionStorage);")
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
                for item in driver.execute_script("return Object.entries(localStorage);")
            },
            indent=4,
        ),
        name="Local Storage",
        attachment_type=allure.attachment_type.JSON,
    )

    if browser != "remote":
        # https://github.com/lana-20/selenium-webdriver-bidi
        if console_messages:
            allure.attach(
                body=json.dumps(console_messages, indent=4),
                name="Console Logs",
                attachment_type=allure.attachment_type.JSON,
            )
        if javascript_errors:
            allure.attach(
                body=json.dumps(javascript_errors, indent=4),
                name="JavaScript Errors",
                attachment_type=allure.attachment_type.JSON,
            )
        # looks like cdp not working with remote: https://github.com/SeleniumHQ/selenium/issues/8672
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
            body=json.dumps(attach_network_logs(), indent=4),
            name="Network Logs",
            attachment_type=allure.attachment_type.JSON,
        )


def get_response_body(request_id):
    """Get the response body for the specified request ID."""
    return driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})


def get_request_post_data(request_id):
    """Get the request post data for the specified request ID."""
    return driver.execute_cdp_cmd("Network.getRequestPostData", {"requestId": request_id})


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
