from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from config import bot, admins
from db import db_main


class LEGOget(StatesGroup):
    id_lego = State()
    size_lego = State()
    count_lego = State()
    number = State()
    submit = State()


async def loading(message: types.Message, state: FSMContext, name):
    async with state.proxy() as data_get:
        data_get[name] = message.text
    await LEGOget.next()


async def fsm_start(message: types.Message):
    await message.answer(text="Режим ввода через артикула товара. \n"
                              "Введите артикул товара: \n"
                              "Можете отменить", reply_markup=buttons.cancel)
    await LEGOget.id_lego.set()


async def load_id(message: types.Message, state: FSMContext):
    await loading(message, state, "id_lego")
    await message.answer(text="Укажите размер товара: ", reply_markup=buttons.sizes)


async def load_size(message: types.Message, state: FSMContext):
    await loading(message, state, "size_lego")
    await message.answer(text="Укажите количество товара: ")


async def load_count(message: types.Message, state: FSMContext):
    await loading(message, state, "count_lego")
    await message.answer(text="Укажите свой телефонный номер для связи: ")


async def load_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data_get:
        data_get["number"] = message.text

    kb = types.ReplyKeyboardMarkup()

    await message.answer(f"Артикул: {data_get['id_lego']}\n"
                         f"Размер: {data_get['size_lego']}\n"
                         f"Количество: {data_get['count_lego']}\n"
                         f"Ваш номер телефона: {data_get['number']}")
    await LEGOget.next()
    await message.answer("Ввести данные товара?", reply_markup=buttons.submit)


async def submit(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup()
    if message.text == "Да":
        async with state.proxy() as data_get:
            await db_main.sql_insert_lego_get(
                id_product=data_get['id_lego'],
                size=data_get['size_lego'],
                count=data_get['count_lego'],
                number=data_get['number'],
            )

        for admin in admins:
            await bot.send_message(chat_id=admin, text=f"{data_get['id_lego']}\n"
                                              f"{data_get['size_lego']}\n"
                                              f"{data_get['count_lego']}\n"
                                              f"{data_get['number']}")

        await message.answer(text='Данные о товаре сохранены!☑️\n'
                                  'Запрос был отправлен админу', reply_markup=kb)

        await state.finish()
    else:
        await message.answer(text='Отменено!✖️')
        await state.finish()


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text="Отменино")


def register_get_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands="pro_lego")
    dp.register_message_handler(load_id, state=LEGOget.id_lego)
    dp.register_message_handler(load_size, state=LEGOget.size_lego)
    dp.register_message_handler(load_count, state=LEGOget.count_lego)
    dp.register_message_handler(load_number, state=LEGOget.number)
    dp.register_message_handler(submit, state=LEGOget.submit)