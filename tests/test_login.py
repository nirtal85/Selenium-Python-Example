import allure
import pytest

from tests.test_base import BaseTest

users = [
    ("nirt236@gmail.com", "123456"),
    ("elias@gmail.com", "12345Tr")
]


@allure.severity(allure.severity_level.BLOCKER)
@allure.epic("Security")
@allure.feature("Login")
@pytest.mark.security
class TestLogin(BaseTest):

    @allure.description("Skip Test example")
    @allure.title("Skipped test example")
    def test_skip(self):
        pass
