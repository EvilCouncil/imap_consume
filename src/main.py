#!/usr/bin/env python
"""Download and catalogue emails."""

# import sys
import os
import email_client
import notifier
import storage_engine
from loguru import logger


def main():
    """Main function."""
    # logger.add(sys.stdout, serialize=True)
    logger.info("Starting to collect email.")
    server = os.environ["IMAP_SERVER"]
    username = os.environ["IMAP_USER"]
    password = os.environ["IMAP_PASSWORD"]
    client = email_client.MailClient(server, username, password)

    storage_host = os.environ["STORAGE_SERVER"]
    storage_user = os.environ["STORAGE_USER"]
    storage_password = os.environ["STORAGE_PASSWORD"]
    storage_database = os.environ["STORAGE_DATABASE"]

    hook_url = os.environ["DISCORD_URL"]
    discord_notify = notifier.DiscordNotifier(hook_url)

    storage_client = storage_engine.StorageEngine(
        storage_host,
        storage_user,
        storage_password,
        storage_database)
    with client:
        with storage_client:
            message_id = 1
            for message in client.messages():
                logger.info(f"processing message: {message_id}")
                message_id += 1
                for part in message.messages():
                    try:
                        discord_notify.notify(part)
                        storage_client.store(part)
                    except Exception as e:
                        logger.error(f"Error parsing attachment: {e}")
                client.delete(message)
                # import sys; sys.exit(0)

if __name__ == "__main__":
    main()
