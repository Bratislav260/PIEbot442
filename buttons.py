from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Отмена"))

sizes = ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Маленький"), KeyboardButton("Средний"), KeyboardButton("Большой")]], resize_keyboard=True)

submit = ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Да"), KeyboardButton("Нет")]], resize_keyboard=True)

category = ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Лего: Сити"), KeyboardButton("Лего: Бэтмен"), KeyboardButton("Лего: Марвел")]], resize_keyboard=True)
