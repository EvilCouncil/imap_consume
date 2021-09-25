#!/usr/bin/env python
"""Download and catalogue emails."""

import base64
import time
import hashlib
import json
import ssdeep

class Message():
    """holds message data."""

    def __init__(self, email_id):
        self._email_id = email_id
        self._data = list()

    def append(self, mdata):
        """Add a new message data object."""
        self._data.append(mdata)

    def messages(self):
        """Loop through all messages."""
        for message in self._data:
            yield message

    @property
    def email_id(self):
        """getter for email id."""
        return self._email_id


class MessageData(): # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """Holds data for an email."""

    def __init__(self, recv_time: int, from_addr: str, to_addr: str, subject: str):
        self._process_time = time.time()
        self._recv_time = recv_time
        self._from_addr = from_addr
        self._to_addr = to_addr
        self._subject = subject
        self._message_text = None
        self._message_format = None
        self._message_md5 = None
        self._message_sha1 = None
        self._message_sha256 = None
        self._message_ssdeep = None
        self._attachment_data = None
        self._attachment_md5 = None
        self._attachment_sha1 = None
        self._attachment_sha256 = None
        self._attachment_ssdeep = None

    @property
    def process_time(self):
        """process_time getter."""
        return self._process_time

    @property
    def recv_time(self):
        """recv_time getter."""
        return self._recv_time

    @property
    def from_addr(self):
        """from_addr getter."""
        return self._from_addr

    @property
    def to_addr(self):
        """to_addr getter"""
        return self._to_addr

    @property
    def subject(self):
        """subject getter"""
        if not self._subject:
            return "NO_SUBJECT_SET"
        return self._subject

    @property
    def message_md5(self):
        """message md5 getter"""
        return self._message_md5

    @property
    def message_sha1(self):
        """message sha1 getter"""
        return self._message_sha1

    @property
    def message_sha256(self):
        """message sha256 getter"""
        return self._message_sha256

    @property
    def message_ssdeep(self):
        """message ssdeep."""
        return self._message_ssdeep


    @property
    def message_text(self):
        """message getter."""
        return self._message_text

    @property
    def attachment_md5(self):
        """attachment md5 getter"""
        return self._attachment_md5

    @property
    def attachment_sha1(self):
        """attachment sha1 getter"""
        return self._attachment_sha1

    @property
    def attachment_sha256(self):
        """attachment sha256 getter"""
        return self._attachment_sha256

    @property
    def attachment_ssdeep(self):
        """attachment ssdeep."""
        return self._attachment_ssdeep

    @property
    def attachment_data(self):
        """attachment getter."""
        if self._attachment_data is None:
            return "no_attachment"
        return self._attachment_data

    @message_text.setter
    def message_text(self, message_text):
        """message setter."""
        self._message_text = message_text
        self._message_md5 = hashlib.md5(self._message_text.encode()).hexdigest()
        self._message_sha1 = hashlib.sha1(self._message_text.encode()).hexdigest()
        self._message_sha256 = hashlib.sha256(self._message_text.encode()).hexdigest()
        self._message_ssdeep = ssdeep.hash(self._message_text)

    @attachment_data.setter
    def attachment_data(self, attachment_data):
        """attachment setter."""
        self._attachment_data = base64.b64encode(attachment_data)
        self._attachment_md5 = hashlib.md5(attachment_data).hexdigest()
        self._attachment_sha1 = hashlib.sha1(attachment_data).hexdigest()
        self._attachment_sha256 = hashlib.sha256(attachment_data).hexdigest()
        self._attachment_ssdeep = ssdeep.hash(attachment_data)

    def json(self) -> str:
        """return json reprensation of object fields."""
        return json.dumps(self.__dict__)
