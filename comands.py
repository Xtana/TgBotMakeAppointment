from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard_bot.kb import kb_command, kb_list
from data_base import sql_db

async def cmd_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать в бот barber, чтобы узнать все мои возможности введите',reply_markup=kb_command)

async def cmd_read(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберете день',reply_markup=kb_list)
    print("Отработало")
    await sql_db.sql_read(message)

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_read, commands=['/посмотреть_записи'])