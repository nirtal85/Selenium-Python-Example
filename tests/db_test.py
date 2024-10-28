import allure
import pytest
from assertpy import assert_that


@pytest.mark.skip(reason="requires database connection")
class TestDatabaseExample:
    @allure.title("Verify population amounts")
    def test_verify_population_amount(self, db_connection):
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT Population FROM city WHERE CountryCode='DNK'")
            population_amount = [item[0] for item in cursor.fetchall()]
            assert_that(population_amount).described_as(
                "population amount"
            ).is_equal_to([495699, 284846, 183912, 161161, 90327])
