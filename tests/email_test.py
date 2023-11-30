import allure
import pytest
from mailinator import GetMessageRequest

from tests.base_test import BaseTest


@pytest.mark.skip(reason="requires mailinator client")
class TestEmail(BaseTest):
    @allure.title("Verify email count in user inbox")
    def test_verify_email_count(self, mailinator_helper):
        assert {"email subject": 1} == mailinator_helper.count_messages_by_subject(
            "testautomation"
        )

    @allure.title("Verify email content")
    def test_verify_email_body(self, mailinator_helper):
        message = mailinator_helper.mailinator.request(
            GetMessageRequest(
                domain=mailinator_helper.mailinator_domain,
                inbox="testautomation",
                message_id=mailinator_helper.wait_for_email_to_arrive(
                    "testautomation",
                    "purchase is confirmed",
                ).id,
            )
        )
        assert "Thank you for your purchase" in message.parts[0].body
