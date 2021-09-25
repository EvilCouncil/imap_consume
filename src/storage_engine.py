"""store email."""

import mysql.connector


class StorageEngine():
    """Takes emails and stores them."""

    def __init__(self, host: str, username: str, password: str, database: str):
        self._host = host
        self._username = username
        self._password = password
        self._database = database
        self._conn = None

    def __enter__(self):
        """Connects to database."""
        self._conn = mysql.connector.connect(
            host=self._host,
            username=self._username,
            password=self._password,
            database=self._database
        )

    def __exit__(self, error_type, value, traceback):
        """Close connections."""
        self._conn.close()

    def store(self, message):
        """Stores messages."""
        # return
        cursor = self._conn.cursor()
        sql_statement = "insert  into mail_track (date_processed, date_received, from_addr, to_addr, subject,"\
        +  "message_md5, message_sha1, message_sha256, message_ssdeep,"\
        + "message_text, attachment_md5, attachment_sha1, attachment_sha256,"\
        + "attachment_ssdeep, attachment_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql_statement, (
            message.process_time,
            message.recv_time,
            message.from_addr,
            message.to_addr,
            message.subject,
            message.message_md5,
            message.message_sha1,
            message.message_sha256,
            message.message_ssdeep,
            message.message_text,
            message.attachment_md5,
            message.attachment_sha1,
            message.attachment_sha256,
            message.attachment_ssdeep,
            message.attachment_data
            ))
        self._conn.commit()
