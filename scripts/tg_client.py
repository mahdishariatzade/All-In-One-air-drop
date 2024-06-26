import time

from telethon.sync import TelegramClient
from telethon.sync import functions
from telethon.tl.types import InputBotAppShortName

from telegram.create_client import create_telegram_client
from tools.db.cache_data import SimpleCache


def getUrl(client: TelegramClient, peer: str, bot: str, url: str, platform: str = "ios", start_param: str = ""):
    return client(
        functions.messages.RequestWebViewRequest(
            peer=peer,
            bot=bot,
            platform=platform,
            url=url,
            from_bot_menu=False,
            start_param=start_param
        )
    )


def getAppUrl(client: TelegramClient, bot: str, platform: str = "ios", start_param: str = "",
              short_name: str = "start"):
    return client(
        functions.messages.RequestAppWebViewRequest(
            peer="me",
            app=InputBotAppShortName(
                bot_id=client.get_input_entity(bot), short_name=short_name),
            platform=platform,
            start_param=start_param
        )
    )


def create_client(sessionString, api_id, api_hash, admin, cexio_ref_code):
    client = create_telegram_client(sessionString, api_id, api_hash)

    client.start()

    client_id = client.get_me(True).user_id

    cache_db = SimpleCache(client_id)

    if not cache_db.exists('start_bots'):
        client.send_message('tapswap_bot', f'/start r_{admin}')
        time.sleep(6)
        client.send_message('hamster_kombat_bot', f'/start kentId{admin}')
        time.sleep(6)
        client.send_message('cexio_tap_bot', f'/start {cexio_ref_code}')

        cache_db.set('start_bots', 3)

    if not cache_db.exists('tapswap_url'):
        tapswap_url = getUrl(
            client,
            'tapswap_bot',
            'tapswap_bot',
            'https://app.tapswap.ai/'
        ).url

        cache_db.set('tapswap_url', tapswap_url)
        time.sleep(6)

    if not cache_db.exists('hamster_url'):
        hamster_url = getAppUrl(
            client,
            'hamster_kombat_bot',
            start_param=f"kentId{admin}"
        ).url

        cache_db.set('hamster_url', hamster_url)
        time.sleep(6)

    if not cache_db.exists('cex_io_url'):
        cex_io_url = getUrl(
            client,
            'cexio_tap_bot',
            'cexio_tap_bot',
            'https://cexp.cex.io/'
        ).url

        cache_db.set('cex_io_url', cex_io_url)
        time.sleep(6)

    client.disconnect()
