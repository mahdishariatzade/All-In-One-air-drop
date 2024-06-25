import time

from telethon import events

from airdrops.hamster.hamster_functions import daily_combo, daily_cipher, buy_card
from airdrops.hamster.hamster_functions import hamster_do_tasks
from scripts.tg_client import create_client
from send_taps import connect
from telegram.bot_client import client
from tools.configs import *
from tools.converts import convert_big_number
from tools.logger import setup_custom_logger
from tools.scheduler import scheduler
from tools.statistics import total_balance, get_server_usage
from tools.statistics import url_files

logger = setup_custom_logger("mainapp")

scheduler.add_job(hamster_do_tasks, "interval", hours=12, name='daily_reward', id="daily_reward")

for session in accounts:
    create_client(session, api_id, api_hash, admin, cexio_ref_code)

clickers = {}

START_TIME = time.time()

for file in url_files:
    job = scheduler.add_job(connect, "interval", seconds=60, args=[file])

db = {
    'click': 'on',
    'start': False
}


@client.on(events.NewMessage(incoming=True, from_users=[admin], pattern=r'/start'))
async def handler(event):
    await event.reply('To view the menu, send /help. 😉')


@client.on(events.NewMessage(incoming=True, from_users=[admin], pattern=r'/ping'))
async def handler(event):
    await event.reply('I am online! 🌐')


@client.on(events.NewMessage(incoming=True, from_users=[admin], pattern=r'/claim_daily_combo'))
async def handler(event):
    m = await event.reply('It might take some time ⏳.')
    daily_combo()
    await m.edit('🚀 Your request has been sent.')


@client.on(events.NewMessage(incoming=True, from_users=[admin], pattern=r'/cipher'))
async def handler(event):
    text = event.raw_text
    cipher = text.split('/cipher ')[1]
    m = await event.reply('It might take some time ⏳.')
    daily_cipher(cipher)
    await m.edit('🚀 Your request has been sent.')


@client.on(events.NewMessage(incoming=True, from_users=[admin], pattern=r'/click (\w+)'))
async def handler(event):
    stats = event.pattern_match.group(1)
    if stats not in ['off', 'on']:
        await event.reply('❌ Bad Command!')
    db['click'] = stats
    if stats == 'on':
        job_names = [job.name for job in scheduler.get_jobs()]
        if 'send_taps' not in job_names:
            await event.reply('✅ Mining Started!')
        else:
            await event.reply('Mining already Started!')
    else:
        scheduler.remove_job('send_taps')
        await event.reply('💤 Mining turned off!')


@client.on(events.NewMessage(incoming=True, from_users=[admin], pattern=r'/buy (\w+)'))
async def handler(event):
    item = event.pattern_match.group(1)
    m = await event.reply('It might take some time ⏳.')
    buy_card(item)
    await m.edit('🚀 Your request has been sent.')


@client.on(events.NewMessage(incoming=True, from_users=[admin], pattern=r'/balance'))
async def handler(event):
    m = await event.reply('Calculating the inventory. It might take some time ⏳.')
    tapswap, hamster, cexio, hamster_earn_per_hour, data = total_balance()
    await m.edit(f"""Total number of clickers: `{len(url_files)}`
Total inventories:

🤖 Total TapSwap: `{convert_big_number(tapswap)}`
🐹 Total Hamster: `{convert_big_number(hamster)}`
🔗 Total CEX IO:  `{convert_big_number(cexio)}`

🐹 Total Hamster Earn Per Hour:  `{convert_big_number(hamster_earn_per_hour)}`
🐹 Total Hamster Earn Per Day:   `{convert_big_number(hamster_earn_per_hour * 24)}`
""")
    pass


@client.on(events.NewMessage(incoming=True, from_users=[admin], pattern=r'/help'))
async def handler(event):
    su = get_server_usage()

    mem_usage = su['memory_usage_MB']
    mem_total = su['memory_total_MB']
    mem_percent = su['memory_percent']
    cpu_percent = su['cpu_percent']
    _clicker_stats = "ON 🟢" if db['click'] == 'on' else "OFF 🔴"

    await event.reply(f"""
📊 Clicker stats: `{_clicker_stats}`
🎛 CPU usage: `{cpu_percent:.2f}%`
🎚 Memory usage: `{mem_usage:.2f}/{mem_total:.2f} MB ({mem_percent:.2f}%)`
------------------------------
🤖 Global commands:
🟢 `/click on` - Start collecting (Hamster ~ TapSwap ~ Cex IO)
🔴 `/click off` - Stop collecting (Hamster ~ TapSwap ~ Cex IO)
------------------------------
🟡 `/ping` - Check if the robot is online
🟢 `/help` - Display help menu
⚪️ `/balance` - Show Total balance
⚫️ `/stop` - Stop the robot
------------------------------
🐹 Special Hamster Commands:
🟠 `/buy `ITEM - Purchase an item/card ( `/buy Fan tokens` )
🟠 `/claim_daily_combo` - Claim daily combo ( `You need to purchase items by commands` )
🟠 `/cipher `CIPHER - Claim daily cipher ( `/cipher BTC` )
""")


scheduler.start()
client.run_until_disconnected()
