from datetime import datetime as DATE, timedelta as DELT
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard_bot.kb import kb_command, kb_list
from data_base import sql_db
from aiogram.types import  CallbackQuery
from aiogram.dispatcher.filters import Command
from cal.aiogram_calendar import simple_cal_callback, SimpleCalendar

async def cdm_list(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберете день', reply_markup=kb_list)

async def list_all(message: types.Message):
    if sql_db.presence_of_person(): 
        await bot.send_message(message.from_user.id, 'Список записей: ', reply_markup=kb_command)
        await sql_db.sql_read_all(message)
    else:
        await bot.send_message(message.from_user.id, 'Записи отсутствуют', reply_markup=kb_command)

async def list_today(message: types.Message):
    data = DATE.today()
    print(data)
    if sql_db.search_data_in_table(data): 
        await bot.send_message(message.from_user.id, 'Список записей: ', reply_markup=kb_command)
        await sql_db.sql_list_today(message)
    else:
        await bot.send_message(message.from_user.id, 'Записи отсутствуют', reply_markup=kb_command)

async def list_tomorrow(message: types.Message):
    data = (DATE.now() + DELT(days=1)).strftime("%Y-%m-%d")
    print(data)
    if sql_db.search_data_in_table(data): 
        await bot.send_message(message.from_user.id, 'Список записей: ', reply_markup=kb_command)
        await sql_db.sql_list_tomorrow(message)
    else:
        await bot.send_message(message.from_user.id, 'Записи отсутствуют', reply_markup=kb_command)

async def process_simple_calendar1(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите дату: ", reply_markup=await SimpleCalendar().start_calendar())

@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar2(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        data = date.strftime("%Y-%m-%d")
        if sql_db.search_data_in_table(data): 
            await bot.send_message(callback_query.message.chat.id, 'Список записей: ', reply_markup=kb_command)
            await sql_db.sql_any_date(callback_query.message.chat.id, data)
        else:
            await bot.send_message(callback_query.message.chat.id, 'Записи отсутствуют', reply_markup=kb_command)

def register_handlers_comand_list(dp : Dispatcher):
    dp.register_message_handler(cdm_list, commands = 'посмотреть_записи')
    dp.register_message_handler(list_all, commands = 'все_записи')
    dp.register_message_handler(list_today, commands = 'сегодня')
    dp.register_message_handler(list_tomorrow, commands = 'завтра')
    dp.register_message_handler(process_simple_calendar1, commands ='выбрать_дату')
    #dp.register_message_handler(process_simple_calendar2, simple_cal_callback.filter())