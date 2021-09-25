"""Download and catalogue emails."""

import imaplib
import email
import email.utils
import message_data
import datetime
import re
from dateutil import parser


class MailClient(): # pylint: disable=too-few-public-methods
    """Connect to an imap server and download data."""

    def __init__(self, server, username, password):
        self._server = server
        self._username = username
        self._password = password
        self._mbox = None

    def __enter__(self):
        self._mbox = imaplib.IMAP4_SSL(self._server)
        self._mbox.login(self._username, self._password)
        self._mbox.select()

    def __exit__(self, error_type, value, traceback):
        self._mbox.close()
        self._mbox.logout()

    def process_message(self, message_id: int):
        """Processes a specific message."""
        # print("message_id", message_id)
        _, data = self._mbox.fetch(message_id, "(RFC822)")
        try:
            message_body = data[0][1]
            mail = email.message_from_bytes(message_body)
            # encoding = mail['Content-Transfer-Encoding']
            # print("Body:", mail['body']())

            emails = message_data.Message(message_id)
            for part in mail.walk():
                content_type = part.get_content_type()
                date_str = mail.get('date')
                msg_date = int(parser.parse(date_str).timestamp())
                msg_data = message_data.MessageData(msg_date, mail['from'], mail['to'], mail['subject'])
                # print("msg received date: ", date_str)
                # print("msg received datetime: ", msg_date)
                # print(content_type)
                if content_type == "application/octet-stream":
                    # print(part.get_filename())
                    data = part.get_payload(decode=True)
                    msg_data.attachment_data = data
                if content_type in ('text/plain', 'text/html'):
                    text = part.get_payload()
                    msg_data.message_text = text
                emails.append(msg_data)
            return emails
        except UnicodeDecodeError as decode_error:
            print(decode_error)


    def messages(self) -> message_data.MessageData:
        """Downloads the emails."""
        _, items = self._mbox.search(None, "(ALL)")
        items = items[0].split()
        for emailid in items:
            message = self.process_message(emailid)
            yield message

    def delete(self, message: message_data.MessageData):
        """Deletes a message."""
        print(f"Deleting message {message.email_id}")
        self._mbox.store(message.email_id, "+FLAGS", r"(\Deleted)")
