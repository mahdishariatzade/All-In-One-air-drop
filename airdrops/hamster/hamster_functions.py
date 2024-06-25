import concurrent.futures

from tools.db.cache_data import SimpleCache
from airdrops.hamster.hamster import HamsterCombat
from tools.logger import setup_custom_logger
from tools.configs import max_days_for_return
from tools.statistics import url_files

logger = setup_custom_logger('hamster Functions')


def hamster_do_tasks():
    def task(file):
        client_id = file.split('.json')[0]
        cache_db = SimpleCache(client_id)
        hamster_url = cache_db.get('hamster_url')
        try:
            hamster_client = HamsterCombat(hamster_url, max_days_for_return, client_id)
            hamster_client.do_tasks()
            return f"User: {client_id} | Tasks done"
        except Exception as e:
            logger.warning(f"User: {client_id} | Error in Hamster Tasks: " + str(e))
            return f"User: {client_id} | Error: {str(e)}"

    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        results = list(executor.map(task, url_files))
    return results


def daily_cipher(cipher: str):
    def task(file):
        client_id = file.split('.json')[0]
        cache_db = SimpleCache(client_id)
        hamster_url = cache_db.get('hamster_url')
        try:
            hamster_client = HamsterCombat(hamster_url, max_days_for_return, client_id)
            hamster_client.claim_daily_cipher(cipher)
            return f"User: {client_id} | Daily cipher claimed"
        except Exception as e:
            logger.warning(f"User: {client_id} | Error in Hamster Daily Cipher: " + str(e))
            return f"User: {client_id} | Error: {str(e)}"

    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        results = list(executor.map(task, url_files))
    return results


def daily_combo():
    def task(file):
        client_id = file.split('.json')[0]
        cache_db = SimpleCache(client_id)
        hamster_url = cache_db.get('hamster_url')
        try:
            hamster_client = HamsterCombat(hamster_url, max_days_for_return, client_id)
            hamster_client.claim_daily_combo()
            return f"User: {client_id} | Daily combo claimed"
        except Exception as e:
            logger.warning(f"User: {client_id} | Error in Hamster Daily Combo: " + str(e))
            return f"User: {client_id} | Error: {str(e)}"

    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        results = list(executor.map(task, url_files))

    return results


def buy_card(item: str):
    def task(file):
        client_id = file.split('.json')[0]
        cache_db = SimpleCache(client_id)
        hamster_url = cache_db.get('hamster_url')
        try:
            hamster_client = HamsterCombat(hamster_url, max_days_for_return, client_id)
            r = hamster_client.upgrade_item(item)
            return f"User: {client_id} | Card bought: {r}"
        except Exception as e:
            logger.warning(f"User: {client_id} | Error in Hamster buy card: " + str(e))
            return f"User: {client_id} | Error: {str(e)}"

    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        results = list(executor.map(task, url_files))
    return results
