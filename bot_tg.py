from aiogram.utils import executor
from create_bot import dp
from data_base import sql_db


async def on_startup(_):
    print('Бот онлайн')
    sql_db.sql_start()

from comands import register_handlers
from record_client import register_handlers_rec_client
from comand_list import register_handlers_comand_list

register_handlers(dp)
register_handlers_comand_list(dp)
register_handlers_rec_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)