from datetime import datetime

import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from globals import driver_global


@pytest.fixture(scope="class", autouse=True)
def create_driver(request):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver_global.DRIVER = driver
    driver.get("https://www.google.com")

    def kill_driver():
        driver.quit()
        # outcome = yield
        # rep = outcome.get_result()
        # if rep.failed:
        #     screenshot_name = 'screenshot-%s.png' % datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        #     allure.attach(driver.get_screenshot_as_png(), name=screenshot_name,
        #                   attachment_type=allure.attachment_type.PNG)
        # if request.node.rep.failed:
        #     screenshot_name = 'screenshot-%s.png' % datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        #     allure.attach(driver.get_screenshot_as_png(), name=screenshot_name,
        #                   attachment_type=allure.attachment_type.PNG)

    request.addfinalizer(kill_driver)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item):
        outcome = yield
        rep = outcome.get_result()
        if rep.when == "setup" or rep.when == "call":
            if rep.failed:
                screenshot_name = 'screenshot-%s.png' % datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                allure.attach(driver.get_screenshot_as_png(), name=screenshot_name,
                              attachment_type=allure.attachment_type.PNG)
