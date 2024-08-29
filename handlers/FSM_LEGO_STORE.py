from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from db import db_main


class LEGOreg(StatesGroup):
    name_lego = State()
    size_lego = State()
    category_lego = State()
    price_lego = State()
    id_lego = State()
    photo_lego = State()
    submit = State()


async def loading(message: types.Message, state: FSMContext, name):
    async with state.proxy() as data:
        data[name] = message.text
    await LEGOreg.next()


async def fsm_start(message: types.Message):
    await message.answer(text="Режим ввода данных товара. \n"
                              "Введите имя товара: \n"
                              "Можете отменить", reply_markup=buttons.cancel)
    await LEGOreg.name_lego.set()


async def load_name(message: types.Message, state: FSMContext):
    await loading(message, state, "name_lego")
    await message.answer(text="Укажите размер товара: ", reply_markup=buttons.sizes)


async def load_size(message: types.Message, state: FSMContext):
    await loading(message, state, "size_lego")
    await message.answer(text="Укажите категорию товара: ", reply_markup=buttons.category)


async def load_category(message: types.Message, state: FSMContext):
    await loading(message, state, "category_lego")
    await message.answer(text="Укажите цену товара: ")


async def load_price(message: types.Message, state: FSMContext):
    await loading(message, state, "price_lego")
    await message.answer(text="Укажите артикул товара: ")


async def load_id(message: types.Message, state: FSMContext):
    await loading(message, state, "id_lego")
    await message.answer(text="Укажите фотографию товара: ")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo_lego'] = message.photo[-1].file_id

    kb = types.ReplyKeyboardMarkup()

    await message.answer_photo(photo=data['photo_lego'],
                               caption=f"Имя: {data['name_lego']}\n"
                                       f"Размер: {data['size_lego']}\n"
                                       f"Категория: {data['category_lego']}\n"
                                       f"Цена: {data['price_lego']}\n"
                                       f"Артикул: {data['id_lego']}\n")
    await LEGOreg.next()
    await message.answer("Сохранить данные товара?", reply_markup=buttons.submit)


async def submit(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup()

    if message.text == "Да":
        async with state.proxy() as data:
            await db_main.sql_insert_lego(
                name=data['name_lego'],
                size=data['size_lego'],
                category=data['category_lego'],
                price=data['price_lego'],
                id_product=data['id_lego'],
                photo=data['photo_lego']
            )
        await message.answer(text='Данные о товаре сохранены!☑️', reply_markup=kb)
        await state.finish()
    else:
        await message.answer(text='Отменено!✖️')
        await state.finish()


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text="Отменино")


def register_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands="reg_lego")
    dp.register_message_handler(load_name, state=LEGOreg.name_lego)
    dp.register_message_handler(load_size, state=LEGOreg.size_lego)
    dp.register_message_handler(load_category, state=LEGOreg.category_lego)
    dp.register_message_handler(load_price, state=LEGOreg.price_lego)
    dp.register_message_handler(load_id, state=LEGOreg.id_lego)
    dp.register_message_handler(submit, state=LEGOreg.submit)
    dp.register_message_handler(load_photo, state=LEGOreg.photo_lego, content_types=['photo'])
