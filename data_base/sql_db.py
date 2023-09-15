from aiogram.dispatcher import FSMContext
import sqlite3 as sq
from aiogram import types
from create_bot import bot
from keyboard_bot.kb import kb_rec_client_stop, kb_command

def sql_start():
    global base, cur
    base = sq.connect('clients.db')
    cur = base.cursor()
    if base:
        print('DB connected!')
    base.execute('CREATE TABLE IF NOT EXISTS client(id INTEGER PRIMARY KEY, name char(50), data DATA)') #autoincrement
    base.commit()

async def sql_add_command(state: FSMContext):
    async with state.proxy() as data:
        cur.execute('INSERT INTO client (name, data) VALUES(?, ?)', (data['name'], data['data'],))
        base.commit()

def search_data_in_table(data):
    cur.execute('SELECT 1 FROM `client` WHERE data = (?)', (data,))
    val = cur.fetchall()
    return val

def presence_of_person():
    cur.execute('SELECT 1 FROM `client` WHERE id = 1')
    val = cur.fetchall()
    print(val)
    return val

async def sql_read_all(message : types.Message):
    for ret in cur.execute('SELECT name, data FROM client').fetchall():
        await bot.send_message(message.from_user.id, f'Имя: {ret[0]}\n Дата: {ret[1]}')

async def sql_list_today(message : types.Message):
    for ret in cur.execute("SELECT name, data FROM client WHERE data == date('now')").fetchall():
        await bot.send_message(message.from_user.id, f'Имя: {ret[0]}\nДата: {ret[1]}')

async def sql_list_tomorrow(message : types.Message):
    for ret in cur.execute("SELECT name, data FROM client WHERE data == date('now', '+1 day')").fetchall():
        await bot.send_message(message.from_user.id, f'Имя: {ret[0]}\nДата: {ret[1]}')

async def sql_any_date(id, data):
    for ret in cur.execute("SELECT name, data FROM client WHERE data = (?)", (data,)).fetchall():
        await bot.send_message(id, f'Имя: {ret[0]}\nДата: {ret[1]}')