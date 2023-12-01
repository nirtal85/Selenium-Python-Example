from unittest import TestCase

import allure
import pytest

from tests.base_test import BaseTest


@pytest.mark.skip(reason="requires mailinator client")
class TestEmail(BaseTest):
    @allure.title("Verify email count in user inbox")
    def test_verify_email_count(self, mailinator_helper):
        subject_counts = mailinator_helper.count_messages_by_subject("testautomation")
        TestCase().assertDictEqual({"some subject": 1}, subject_counts)

    @allure.title("Verify email content")
    def test_verify_email_body(self, mailinator_helper):
        message = mailinator_helper.get_message(
            "testautomation", "purchase is confirmed"
        )
        assert "Thank you for your purchase" in message.parts[0].body
