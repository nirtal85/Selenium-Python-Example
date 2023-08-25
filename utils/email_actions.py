from collections import Counter

from mailinator import GetInboxRequest, Mailinator, Message


class EmailActions:

    """
    A class for performing email-related actions using the Mailinator service.

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

    def wait_for_email_to_arrive(self, user_email: str, email_subject: str) -> Message:
        """
        Wait for an email to arrive with a specific subject in a user's inbox.

        This method requests the inbox of a specified user and waits until an email with the
        provided subject arrives. Once the email is found, it returns the first email that
        matches the given subject.

        Args:
            user_email (str): The email address of the user.
            email_subject (str): The subject of the email to wait for.

        Returns:
            Message or None: The email message with the specified subject, or None if the email
            is not found within the inbox.

        Raises:
            Any exceptions raised by the underlying `self.mailinator.request` method when
            fetching the inbox.

        Example:
            email = wait_for_email_to_arrive(self, "user@example.com", "Important Subject")
            if email:
                print(f"Found email: {email.subject}")
            else:
                print("Email not found within the specified timeout.")
        """
        messages = self.mailinator.request(
            GetInboxRequest(
                domain=self.mailinator_domain,
                inbox=user_email.split("@")[0],
            )
        ).msgs
        filtered_messages = [
            message
            for message in messages
            if message.to == user_email.split("@")[0]
            and message.subject == email_subject
        ]
        return filtered_messages[0] if filtered_messages else None

    def count_messages_by_subject(self, user_email: str) -> dict[str, int]:
        """
        Count the occurrences of email subjects in a user's inbox.

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
