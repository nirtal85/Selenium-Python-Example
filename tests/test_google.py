from globals import driver_global as dg


class TestGoogle:

    def test_assert_google_title(self):
        driver = dg.DRIVER
        assert driver.title == "not google", "assert failed"
