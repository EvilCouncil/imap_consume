"""Notfiers provide a means of adding notifications to detections."""

import abc
import message_data
# import requests
import discord
import time

class Notifier(abc.ABC): # pylint: disable=too-few-public-methods
    """Abstracted class for notification."""

    @abc.abstractmethod
    def notify(self, msg):
        """Notifies stuff."""

class DiscordNotifier(Notifier): # pylint: disable=too-few-public-methods
    """Sends notificaitons to discord."""

    def __init__(self, target_url):
        self._target_url = target_url
        self._message_count = 0
        self._webhook = discord.Webhook.from_url(self._target_url,
                adapter=discord.RequestsWebhookAdapter())

    def notify(self, msg):
        """Notifies stuff."""
        message = f"To: {msg.to_addr}\nFrom: {msg.from_addr}\nSubject: {msg.subject}\nAttachment SHA256: {msg.attachment_sha256}"
        self._message_count += 1
        if self._message_count > 40:
            time.sleep(2)
            self._message_count = 0
        self._webhook.send(message)
