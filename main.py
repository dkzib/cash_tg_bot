import sqlite3
import string
import os, time, random
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import *
from aiogram import types
from db import *
import db
from messages import *
from aiogram import types

from config import *
##########################################################################################################################

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())



@dp.message_handler(commands=["start"])
async def menu(message: types.Message, state: FSMContext):
	user_id_db = message.chat.id
	if user_id_db == 5559462803:
		await bot.send_message(message.chat.id, text=f'палю как админа')
	b1 = KeyboardButton('🔐 Профиль 👤')
	b2 = KeyboardButton('⚙ Настройки ⚙')
	b3 = KeyboardButton('🛠 Другое 🛠')

	b33 = KeyboardButton('/start')
	b4 = KeyboardButton('Как сломать бота (для терентия)')
	b0 = KeyboardButton('🤙 Интерактивное меню 🤙')

	buttons = ReplyKeyboardMarkup(resize_keyboard=True)
	buttons.add(b1).add(b2).add(b3)




###################################################### ЗАПИСЬ В БД######################################################

	dataq = message.date
	print(dataq)
	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
			id INTEGER,
			username TEXT,
			fname TEXT,
			starttime TEXT,
			money INTEGER
			)
			""")
	connect.commit()
	people_id = message.chat.id
	people_username = message.from_user.username
	people_fname = message.from_user.first_name
	stock_money = 0

	people_starttime = dataq
	cursor.execute(f"SELECT id FROM login_id WHERE id = '{people_id}'")
	if cursor.fetchone() is None:
		cursor.execute("INSERT INTO login_id VALUES(?, ?, ?, ?, ?);", (people_id,
																	people_username,
																	people_fname,
																	people_starttime,
																	stock_money))
		connect.commit()
	cursor.close()
###################################################### ЗАПИСЬ В БД######################################################

	_data = check_all_info(message.chat.id)
	await bot.send_message(chat_id=message.chat.id, text=f'Здравствуй, {message.chat.username}')
	await bot.send_message(message.chat.id, text=f'👤 Твой login:   `{_data[1]}`\n\n'
												 f'👤 Твой id:   `{_data[0]}`\n\n'
												 f'👤 Дата регистрации: `{_data[3]}`\n\n\n'
												 f'👤 Баланс:   `{_data[4]}`', reply_markup=buttons,
						   parse_mode=types.ParseMode.MARKDOWN)
	await message.delete()


'''============================================МАШИНА СОСТОЯНИЙ=================================================='''

@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message, index):
	argument = str(index)
	state = dp.current_state(user=message.from_user.id)
	if not argument:
		await state.reset_state()
		return await message.reply(MESSAGES['state_reset'])
	if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
		return await message.reply(MESSAGES['invalid_key'].format(key=argument))

	await state.set_state(TestStates.all()[int(argument)])
	await message.reply(MESSAGES['popol'], reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_test_state_case_met(message: types.Message):
	mes = message.text
	if mes.isdigit():
		argument = message.get_args()
		state = dp.current_state(user=message.from_user.id)
		a = int(mes)
		add_money_db(message.chat.id, a)
		await state.reset_state()
		return await message.reply(MESSAGES['add_money_success'])
	else:
		await bot.send_message(message.chat.id, text=f'Не понимаю о чём вы, введите еще раз.')

@dp.message_handler(state=TestStates.TEST_STATE_2)
async def first_test_state_case_met(message: types.Message):
	mes = message.text
	if mes.isdigit():
		argument = message.get_args()
		state = dp.current_state(user=message.from_user.id)
		a = int(mes)
		remove_money_db(message.chat.id, a)
		await state.reset_state()
		return await message.reply(MESSAGES['remove_money_success'])
	else:
		await bot.send_message(message.chat.id, text=f'Не понимаю о чём вы, введите еще раз.')

'''==================================================HANDLERS СООБЩЕНИЙ=================================================='''


@dp.message_handler(text=['🏦 Проверить баланс 🏦'])
async def add_money(message: types.Message):
	_data = check_money(message.chat.id)

	await bot.send_message(message.chat.id, text=f'Ваш баланс: {_data[4]}')

@dp.message_handler(text=['🏦 Баланс 500 🏦'])
async def add_money(message: types.Message):
	add_money2(message.chat.id)
	await bot.send_message(message.chat.id, text=f'Ваш баланс успешно пополнен!')

@dp.message_handler(text=['🏦 Баланс 0 🏦'])
async def add_money(message: types.Message):
	remove_money(message.chat.id)
	await bot.send_message(message.chat.id, text=f'Ваш баланс успешно уменьшен!')

@dp.message_handler(text=['🏦 Ввести для пополнения 🏦'])
async def add_money(message: types.Message):
	index = 1
	await process_setstate_command(message, index)

@dp.message_handler(text=['🏦 Ввести для уменьшения 🏦'])
async def add_money(message: types.Message):
	index = 2
	await process_setstate_command(message, index)


@dp.message_handler(text=['🔐 Профиль 👤'])
async def profile_menu(message: types.Message):
	try:
		b1 = KeyboardButton('🏦 Баланс 500 🏦')
		b2 = KeyboardButton('🏦 Баланс 0 🏦')
		b3 = KeyboardButton('🏦 Проверить баланс 🏦')
		b4 = KeyboardButton('🏦 Ввести для пополнения 🏦')
		b5 = KeyboardButton('🔙 Назад 🔙')
		b6 = KeyboardButton('🏦 Ввести для уменьшения 🏦')
		buttons = ReplyKeyboardMarkup(resize_keyboard=True)
		buttons.add(b3).add(b4).add(b6).add(b1,b2).add(b5)

		_data = check_all_info(message.chat.id)
		await bot.send_message(message.chat.id, text=f'👤 Твой login:   `{_data[1]}`\n\n'
													 f'👤 Твой id:   `{_data[0]}`\n\n'
													 f'👤 Дата регистрации: `{_data[3]}`\n\n\n'
													 f'👤 Баланс:   `{_data[4]}`', parse_mode=types.ParseMode.MARKDOWN,
													reply_markup=buttons)
	except:
		await bot.send_message(message.chat.id, text=f'Вас нет в базе данных!')

@dp.message_handler(text=['⚙ Настройки ⚙'])
async def b2(message: types.Message):
	b3 = KeyboardButton('📁 Чек базы данных 📁')
	b4 = KeyboardButton('📤 Удалить себя из бд 📤')
	b44 = KeyboardButton('📥 Добавить себя в бд 📥')
	b5 = KeyboardButton('Автор')
	b6 = KeyboardButton('🔙 Назад 🔙')
	buttons2 = ReplyKeyboardMarkup(resize_keyboard=True)
	buttons2.add(b3).add(b4).add(b44).add(b5, b6)
	await bot.send_message(chat_id=message.chat.id, text=f'Меню настроек:', reply_markup=buttons2)

@dp.message_handler(text=['🛠 Другое 🛠'])
async def b2(message: types.Message):
	b1 = KeyboardButton('🤙 Интерактивное меню 🤙')
	b2 = KeyboardButton('Как сломать бота (для терентия)')
	b3 = KeyboardButton('/start')
	b4 = KeyboardButton('🔙 Назад 🔙')
	buttons2 = ReplyKeyboardMarkup(resize_keyboard=True)
	buttons2.add(b1).add(b2).add(b3).add(b4)
	await bot.send_message(chat_id=message.chat.id, text=f'Меню настроек:', reply_markup=buttons2)

@dp.message_handler(text=['🤙 Интерактивное меню 🤙'])
async def inline_menu(message: types.Message):
	markup = InlineKeyboardMarkup()
	markup.add(InlineKeyboardButton(text='Профиль', callback_data='profile'))
	markup.add(InlineKeyboardButton(text='Настройки', callback_data='settings'))
	markup.add(InlineKeyboardButton(text='Закрыть', callback_data='close_main'))
	photo = open('backrounds/brnd2.jpg', 'rb')
	await bot.send_photo(chat_id=message.chat.id, photo=photo,caption=f'описание', reply_markup=markup)
	# await bot.send_message(chat_id=message.chat.id, text='--- кнопка ниже ---', reply_markup=markup, )

@dp.message_handler(text= ['📤 Удалить себя из бд 📤'])
async def delete(message):
	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()
	people_id = message.chat.id
	cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
	connect.commit()
	connect.close()
	await bot.send_message(message.chat.id, text=f'Удаление прошло успешно!')

@dp.message_handler(text= ['📥 Добавить себя в бд 📥'])
async def create_again(message):
	dataq = message.date
	print(dataq)
	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
				id INTEGER,
				username TEXT,
				fname TEXT,
				starttime TEXT,
				money INTEGER
				)
				""")
	connect.commit()
	people_id = message.chat.id
	people_username = message.from_user.username
	people_fname = message.from_user.first_name

	people_starttime = dataq
	cursor.execute(f"SELECT id FROM login_id WHERE id = '{people_id}'")
	stock_money = 0
	if cursor.fetchone() is None:
		cursor.execute("INSERT INTO login_id VALUES(?, ?, ?, ?, ?);", (people_id,
																	people_username,
																	people_fname,
																	people_starttime,
																	stock_money))
		connect.commit()
	cursor.close()

	await bot.send_message(message.chat.id, text=f'Добавление прошло успешно!')


@dp.message_handler(text=['🔙 Назад 🔙'])
async def back_menu(message: types.Message):
	b1 = KeyboardButton('🔐 Профиль 👤')
	b2 = KeyboardButton('⚙ Настройки ⚙')
	b3 = KeyboardButton('🛠 Другое 🛠')

	buttons = ReplyKeyboardMarkup(resize_keyboard=True)
	buttons.add(b1).add(b2).add(b3)
	await bot.send_message(chat_id=message.chat.id, text=f'Главное меню:', reply_markup=buttons)


@dp.message_handler(text=['📁 Чек базы данных 📁'])
async def b2(message: types.Message):
	m = get_people_id()
	await bot.send_message(message.chat.id, text=f'Количество пользователей в базе: {m}')

@dp.message_handler(text=['Как сломать бота (для терентия)'])
async def b2(message: types.Message):
	await bot.send_message(message.chat.id, text=f'1. Бота сломать на 100проц невозможно\n'
												 f'2. Зачем, а главное зачем? это делать?\n'
												 f'3. Удаляешь себя из бд\n'
												 f'4. Пробуешь проверить баланс -> profit\n'
												 f'Гайд чего делать не надо')


# улавливает все сообщения и отвечает цифры/буквы

# @dp.message_handler()
# async def add_money(message: types.Message):
# 	await bot.send_message(message.chat.id, text='Сообщение принято!')
# 	print(type(message.text))
# 	print(message.text)
# 	mes = message.text
# 	if mes.isdigit():
# 		await bot.send_message(message.chat.id, text=f'Я понял. Пополняю баланс')
# 		a = int(mes)
# 		test2(message.chat.id, a)
# 	else:
# 		await bot.send_message(message.chat.id, text=f'Не понимаю о чём ты')

#------------------------------------------HANDLERS ИНЛАЙН КНОПОК------------------------------------------------#


@dp.callback_query_handler(lambda c: c.data)
async def answer(call: types.CallbackQuery):
	if call.data == 'profile':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		markup = InlineKeyboardMarkup()
		markup.add(InlineKeyboardButton(text='Узнать ID', callback_data='get_id'))
		markup.add(InlineKeyboardButton(text='Узнать ник', callback_data='get_nick'))
		markup.add(InlineKeyboardButton(text='Назад', callback_data='back_main'))
		photo = open('backrounds/brnd3.jpg', 'rb')
		await bot.send_photo(call.from_user.id, photo=photo, reply_markup=markup)
	elif call.data == 'get_id':
		await bot.send_message(call.from_user.id, text=f'Ваш ID: {call.from_user.id}')
	elif call.data == 'get_nick':
		await bot.send_message(call.from_user.id, text=f'Ваш ник: {call.from_user.username}')
	elif call.data == 'back_main':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		markup = InlineKeyboardMarkup()
		markup.add(InlineKeyboardButton(text='Профиль', callback_data='profile'))
		markup.add(InlineKeyboardButton(text='Настройки', callback_data='settings'))
		markup.add(InlineKeyboardButton(text='Закрыть', callback_data='close_main'))
		photo = open('backrounds/brnd2.jpg', 'rb')
		await bot.send_photo(call.from_user.id, photo=photo, reply_markup=markup)
	elif call.data == 'settings':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		markup = InlineKeyboardMarkup()
		markup.add(InlineKeyboardButton(text='Количество пользователей в бд', callback_data='2'))
		markup.add(InlineKeyboardButton(text='Удалить себя из бд', callback_data='1'))
		markup.add(InlineKeyboardButton(text='Добавить себя в бд', callback_data='3'))
		markup.add(InlineKeyboardButton(text='Назад', callback_data='back_main'))
		photo = open('backrounds/brnd4.jpg', 'rb')
		await bot.send_photo(call.from_user.id, photo=photo, reply_markup=markup)
	elif call.data == 'close_main':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
	elif call.data == '2':
		await bot.send_message(call.from_user.id, text=f'Пользователей в бд: {get_people_id()}')
	elif call.data == '1':
		connect = sqlite3.connect('users.db')
		cursor = connect.cursor()
		people_id = call.from_user.id
		cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
		connect.commit()
		connect.close()
		await bot.send_message(call.from_user.id, text=f'Удаление прошло успешно! \nКоличество пользователей в бд: {get_people_id()}')
	elif call.data == '3':
		dataq = call.message.date
		print(dataq)
		connect = sqlite3.connect('users.db')
		cursor = connect.cursor()
		cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
						id INTEGER,
						username TEXT,
						fname TEXT,
						starttime TEXT,
						money INTEGER
						)
						""")
		connect.commit()
		people_id = call.from_user.id
		people_username = call.from_user.username
		people_fname = call.from_user.first_name
		stock_money = 0
		people_starttime = dataq
		cursor.execute(f"SELECT id FROM login_id WHERE id = '{people_id}'")
		if cursor.fetchone() is None:
			cursor.execute("INSERT INTO login_id VALUES(?, ?, ?, ?, ?);", (people_id,
																		people_username,
																		people_fname,
																		people_starttime,
																		stock_money))
			connect.commit()
		cursor.close()
		await bot.send_message(call.from_user.id, text=f'Добавление прошло успешно! \nКоличество пользователей в бд: {get_people_id()}')

executor.start_polling(dp)