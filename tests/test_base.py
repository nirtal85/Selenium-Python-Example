import pytest


# https://stackoverflow.com/questions/63292928/add-pytest-fixtures-to-a-test-class-using-dependency-injection/63436993#63436993
class BaseTest:
    @pytest.fixture(autouse=True)
    def injector(self, pages):
        self.pages = pages
