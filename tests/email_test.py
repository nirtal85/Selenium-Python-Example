from unittest import TestCase

import allure
import pytest

from tests.base_test import BaseTest


@pytest.mark.skip(reason="requires mailinator client")
class TestEmail(BaseTest):
    @allure.title("Verify email count in user inbox")
    def test_verify_email_count(self, mailinator_helper) -> None:
        subject_counts = mailinator_helper.count_messages_by_subject("testautomation")
        TestCase().assertDictEqual({"some subject": 1}, subject_counts)

    @allure.title("Verify email content")
    def test_verify_email_body(self, mailinator_helper) -> None:
        message = mailinator_helper.get_message("testautomation", "purchase is confirmed")
        assert "Thank you for your purchase" in message.parts[0].body

    @allure.title("Get OTP code from email")
    def test_verify_otp_code(self, mailinator_helper) -> None:
        otp_code = mailinator_helper.get_otp_code("testautomation")
        assert otp_code.isdigit(), f"OTP code '{otp_code}' is not a digit string"
        assert len(otp_code) == 6, f"OTP code '{otp_code}' is not 6 digits long"
