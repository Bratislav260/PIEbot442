import logging
from config import dp, bot
from aiogram.utils import executor
from config import STAFF
from handlers import commandor, FSM_LEGO_STORE, FSM_GET
from db import db_main


async def on_startup(_):
    for i in STAFF:
        await bot.send_message(chat_id=i, text="Бот включен✅")
        await db_main.sql_creat()


commandor.register_commands(dp)
FSM_LEGO_STORE.register_fsm(dp)
FSM_GET.register_get_fsm(dp)


async def on_shutdown(_):
    for i in STAFF:
        await bot.send_message(chat_id=i, text="Бот выключен❌")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)