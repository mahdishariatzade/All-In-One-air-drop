from telethon import TelegramClient

from tools.configs import api_id, api_hash, bot_token

client = TelegramClient('bot', api_id, api_hash)
client.start(bot_token=bot_token)
