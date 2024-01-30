import allure
import pytest
from assertpy import assert_that
from mysql.connector import MySQLConnection


@pytest.mark.skip(reason="requires database connection")
class TestDatabaseExample:
    @allure.title("Verify population amounts")
    def test_verify_population_amount(self):
        with MySQLConnection(
            user="root", password="1234", database="world"
        ) as connection:
            cursor = connection.cursor()
            cursor.execute("select Population from city where CountryCode='DNK'")
            population_amount = [item[0] for item in cursor.fetchall()]
        assert_that(population_amount).described_as("population amount").is_equal_to(
            [495699, 284846, 183912, 161161, 90327]
        )
