from telethon import TelegramClient
from telethon.sessions import StringSession


def create_telegram_client(sessionString,api_id,api_hash):
    return TelegramClient(
        StringSession(sessionString),
        api_id,
        api_hash,
        device_model=f"All-In-One(MA)",
    )