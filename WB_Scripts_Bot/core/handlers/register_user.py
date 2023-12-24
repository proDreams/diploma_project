from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.settings import bot
from core.utils.get_from_api import check_user, register_user, reset_password


async def register(message: Message):
    markup_exists = InlineKeyboardBuilder()
    markup_back = InlineKeyboardBuilder()
    back_btn = InlineKeyboardButton(
        text="Вернуться в начало",
        callback_data="start")
    reset_btn = InlineKeyboardButton(
        text="Сбросить пароль",
        callback_data="reset")
    markup_exists.add(reset_btn)
    markup_exists.add(back_btn)
    markup_back.add(back_btn)

    if check_user(message.from_user.id):
        await message.answer("Вы уже зарегистрированы!\n", reply_markup=markup_exists.as_markup())
    else:
        response = register_user(message.from_user.username, message.from_user.id)
        print(response)
        await message.answer("Регистрация прошла успешно.\n"
                             f"Логин: {response['username']}\n"
                             f"Пароль: {response['password']}",
                             reply_markup=markup_back.as_markup())


async def reset(message: Message):
    markup_back = InlineKeyboardBuilder()
    back_btn = InlineKeyboardButton(
        text="Вернуться в начало",
        callback_data="start")
    markup_back.add(back_btn)
    response = reset_password(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           "Пароль успешно сброшен!\n"
                           "Новые данные:\n"
                           f"Логин: {response['username']}\n"
                           f"Пароль: {response['password']}",
                           reply_markup=markup_back.as_markup())

