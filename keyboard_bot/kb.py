from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопки меню
b1_command = KeyboardButton('/записать_клиента')
b2_command = KeyboardButton('/удалить_запись')
b3_command = KeyboardButton('/статистика_финансов')
b4_command = KeyboardButton('/посмотреть_записи')
kb_command = ReplyKeyboardMarkup(resize_keyboard=True)
kb_command.add(b1_command).insert(b2_command).add(b3_command).add(b4_command) # rov(b1,b2,b3) - в строку

# кнопка для команды /отмена в /записать_клиента
b1_rec_client_stop = KeyboardButton('/отмена')
kb_rec_client_stop = ReplyKeyboardMarkup(resize_keyboard=True)
kb_rec_client_stop.add(b1_rec_client_stop)

# кнопки для выбора периуда в /посмотреть записи 
b0_list = KeyboardButton('/все_записи')
b1_list = KeyboardButton('/сегодня')
b2_list = KeyboardButton('/завтра')
b3_list = KeyboardButton('/выбрать_дату')
kb_list = ReplyKeyboardMarkup(resize_keyboard=True)
kb_list.add(b0_list).add(b1_list).insert(b2_list).add(b3_list)

