import pytest

# https://stackoverflow.com/questions/63292928/add-pytest-fixtures-to-a-test-class-using-dependency-injection
# /63436993#63436993
from utils.excel_parser import ExcelParser
from utils.json_parser import JsonParser


class BaseTest:
    @pytest.fixture(autouse=True)
    def injector(self, pages, prep_properties):
        # instantiates pages object, and data readers
        self.pages = pages
        self.json_reader = JsonParser("tests_data.json")
        self.config_reader = prep_properties
        self.excel_reader = ExcelParser("data.xls")
