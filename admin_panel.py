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

import db
import main
from config import *
from main import *





async def admin_get_info(message: types.Message):
    async def add_money(message: types.Message):
        _data = check_money(message.chat.id)
        await bot.send_message(message.chat.id, text=f'Ваш баланс: {_data[4]}')





@dp.message_handler(text=['⚠ Сколько пользователей в базе ⚠'])
async def add_money(message: types.Message):
	_data = check_money(message.chat.id)

	await bot.send_message(message.chat.id, text=f'asdsad {_data[4]}')











