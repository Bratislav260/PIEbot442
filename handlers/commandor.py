from aiogram import Dispatcher, types
from config import bot
import os
from aiogram.types import InputFile
from random import *


async def info_handler(message: types.Message):
    await message.answer("👾Бот созданной для удобной покупки лего игрушек👾")


async def start_handler(message: types.Message):
    await message.answer("🎈🎈🎈             Вас приветствует Leg0 Store👾        🎈🎈🎈\n"
                         "🎈                                                          🎈\n"
                         "Укажите АРТИКУЛ товара для его просмотро и дальнейшего заимодействие")


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_handler, commands=['info'])
