from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
import aiogram.utils.markdown as md
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
import datetime
from create_bot import dp, bot
from keyboard_bot.kb import kb_rec_client_stop, kb_command
from cal.aiogram_calendar import simple_cal_callback, SimpleCalendar
from data_base import sql_db

class client(StatesGroup):
    name = State()
    data = State()

async def rec_client_start(message : types.Message):
    await client.name.set()
    await bot.send_message(message.chat.id,'Введите имя',reply_markup=kb_rec_client_stop)

async def cancellation(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.chat.id,'отмена записи', reply_markup=kb_command)

async def enter_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await client.data.set()
    await bot.send_message(message.chat.id,'Введите дату',reply_markup=await SimpleCalendar().start_calendar())

@dp.callback_query_handler(simple_cal_callback.filter(), state=client.data)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    print(datetime.datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d"), datetime.datetime.strptime(datetime.date.today().strftime("%Y-%m-%d"), "%Y-%m-%d"))
    if (datetime.datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d") >= datetime.datetime.strptime(datetime.date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")):
        if selected:
            async with state.proxy() as data:
                data['data'] = date.strftime("%Y-%m-%d")
        async with state.proxy() as data:
            await callback_query.message.answer(md.text(
                        md.text('Имя: ', data['name']),
                        md.text('Дата: ', data['data']),
                        sep='\n',
                    ), 
                    reply_markup=kb_command)
            
            await sql_db.sql_add_command(state)
        await state.finish()
    else:
        await callback_query.message.answer(md.text('Эта дата уже прошла. Выберете другую дату'), reply_markup=kb_command)
        await state.finish()

def register_handlers_rec_client(dp : Dispatcher):
    dp.register_message_handler(rec_client_start, commands = 'записать_клиента', state = None)
    dp.register_message_handler(cancellation, state="*", commands='отмена')  
    dp.register_message_handler(enter_name, state=client.name)
    #dp.register_message_handler(process_simple_calendar, simple_cal_callback.filter(), state=client.data)
