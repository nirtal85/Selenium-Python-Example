import re
from collections import Counter

from mailinator import GetInboxRequest, GetMessageRequest, Mailinator, Message
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)


class MailinatorHelper:
    """A class for performing email-related actions using the Mailinator
    service.

    This class provides methods to interact with the Mailinator API and perform actions
    such as waiting for specific emails to arrive and counting email subjects in an inbox.

    Args:
        mailinator (Mailinator): An instance of the Mailinator client.
        mailinator_domain (str): The domain name associated with the Mailinator service.

    Attributes:
        mailinator (Mailinator): An instance of the Mailinator client.
        mailinator_domain (str): The domain name associated with the Mailinator service.

    Example:
        # Initialize the EmailActions class with the Mailinator client and domain name.
        email_actions = EmailActions(mailinator_client, "example.com")

    """

    def __init__(self, mailinator: Mailinator, mailinator_domain: str):
        self.mailinator = mailinator
        self.mailinator_domain = mailinator_domain

    @retry(
        retry=retry_if_result(lambda x: x is None),
        stop=(stop_after_attempt(3)),
        wait=wait_fixed(4),
    )
    def __get_message_id(self, user_email: str, email_subject: str) -> str:
        """Wait for an email to arrive with a specific subject in a user's
        inbox and return its message ID.

        This method requests the inbox of a specified user and waits until an email with the
        provided subject arrives. Once the email is found, it returns the message ID of the
        first email that matches the given subject.

        Args:
            user_email (str): The email address of the user.
            email_subject (str): The subject of the email to wait for.

        Returns:
            str or None: The message ID of the email with the specified subject, or None if the email
            is not found within the inbox.

        Raises:
            Any exceptions raised by the underlying `self.mailinator.request` method when
            fetching the inbox.

        """
        messages = self.mailinator.request(
            GetInboxRequest(
                domain=self.mailinator_domain,
                inbox=user_email.split("@")[0],
            )
        ).msgs
        filtered_messages: list[Message] = [
            message
            for message in messages
            if message.to == user_email.split("@")[0]
            and message.subject.casefold() == email_subject.casefold()
        ]
        return filtered_messages[0].id if filtered_messages else None

    def get_message(self, user_email: str, email_subject: str) -> Message:
        """Retrieve the email message with the specified subject in a user's
        inbox.

        This method retrieves the email message with the specified subject in a user's
        inbox using the previously obtained message ID.

        Args:
            user_email (str): The email address of the user.
            email_subject (str): The subject of the email to retrieve.

        Returns:
            Message: The email message with the specified subject.

        Raises:
            Any exceptions raised by the underlying `self.mailinator.request` method when
            fetching the email message.

        """
        return self.mailinator.request(
            GetMessageRequest(
                domain=self.mailinator_domain,
                message_id=self.__get_message_id(user_email, email_subject),
            )
        )

    @retry(
        stop=stop_after_delay(30),
        wait=wait_fixed(1),
        retry=retry_if_result(lambda x: x is None) | retry_if_exception_type(Exception),
    )
    def get_otp_code(self, user_email: str) -> str | None:
        """Retrieves a 6-digit OTP code from an email in the Mailinator inbox.

        This method:
        1. Waits for up to 30 seconds, polling every second, for an email to arrive.
        2. Retrieves the email message from Mailinator.
        3. Extracts the first 6-digit OTP code found in the email body.

        Args:
            user_email (str): The email address to check for an OTP.

        Returns:
            str: The extracted 6-digit OTP code.

        Raises:
            RuntimeError: If no OTP is found in the email message.

        """
        message: Message = self.get_message(user_email, "Verify your email address")
        if not message.parts:
            return None
        email_body = message.parts[0].body
        if match := re.search(r"\b(\d{6})\b", email_body):
            return match[1]
        raise RuntimeError("OTP not found in email message")

    def count_messages_by_subject(self, user_email: str) -> dict[str, int]:
        """Count the occurrences of email subjects in a user's inbox.

        This method fetches the messages in a specified user's inbox, extracts the subjects
        of each email, and counts how many times each subject appears in the inbox.

        Args:
            user_email (str): The email address of the user whose inbox is being counted.

        Returns:
            dict[str, int]: A dictionary where keys are unique email subjects and values are
            their respective counts in the user's inbox.

        Raises:
            Any exceptions raised by the underlying `self.mailinator.request` method when
            fetching the inbox.

        Example:
            from unittest import TestCase
            subject_counts = count_messages_by_subject(self, "user@example.com")
            TestCase().assertDictEqual({"some subject": 1}, subject_counts)

        """
        messages = self.mailinator.request(
            GetInboxRequest(
                domain=self.mailinator_domain,
                inbox=user_email.split("@")[0],
            )
        ).msgs
        # Use a list comprehension to extract the subjects from each message
        subjects = [message.subject for message in messages]
        # Count the occurrences of each subject
        return dict(Counter(subjects))
