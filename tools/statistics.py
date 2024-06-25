import psutil

from tools.db.cache_data import SimpleCache
from tools.converts import convert_big_number
import os

url_files = [f.split('.')[0] for f in os.listdir('databases') if f.endswith('.db')]


def total_balance():
    tapswap = 0
    hamster = 0
    cexio = 0
    hamster_earn_per_hour = 0
    data = ""
    for file in url_files:
        client_id = file.split('.json')[0]
        cache_db = SimpleCache(client_id)

        try:
            tapswap += float(cache_db.get('tapswap_balance'))
            data += f"User: `{client_id}` | 🟣 TapSwap: `{convert_big_number(float(cache_db.get('tapswap_balance')))}`\n"
        except:
            pass

        try:
            hamster += float(cache_db.get('hamster_balance'))
            hamster_earn_per_hour += float(cache_db.get('hamster_earn_per_hour'))
            data += f"User: `{client_id}` | 🐹 Hamster: `{convert_big_number(float(cache_db.get('hamster_balance')))}`\n"
            data += f"User: `{client_id}` | 🐹 Hamster PPH: `{convert_big_number(float(cache_db.get('hamster_earn_per_hour')))}`\n"
        except:
            pass

        try:
            cexio += float(cache_db.get('cex_io_balance'))
            data += f"User: `{client_id}` | ❣️Cex IO: `{convert_big_number(float(cache_db.get('cex_io_balance')))}`\n\n"
        except:
            pass

    return tapswap, hamster, cexio, hamster_earn_per_hour, data


def get_server_usage():
    memory = psutil.virtual_memory()
    mem_usage = memory.used / 1e6
    mem_total = memory.total / 1e6
    mem_percent = memory.percent
    cpu_percent = psutil.cpu_percent()

    return {
        'memory_usage_MB': mem_usage,
        'memory_total_MB': mem_total,
        'memory_percent': mem_percent,
        'cpu_percent': cpu_percent
    }
