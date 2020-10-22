import pytest
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

    request.addfinalizer(kill_driver)
