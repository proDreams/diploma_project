from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.settings import bot
from core.utils.get_from_api import get_categories, get_posts, get_scripts, get_script

LST_CAT = {}
LST_POST = {}


async def start_operation(message: Message):
    global LST_CAT
    categories_list = get_categories()
    LST_CAT = categories_list
    builder = InlineKeyboardBuilder()
    for category in categories_list:
        t = f"category_{category['id']}"
        builder.add(
            InlineKeyboardButton(
                text=f"{category['title']}",
                callback_data=t,
            )
        )
    builder.adjust(1)
    await bot.send_message(message.from_user.id, "Выберите категорию:", reply_markup=builder.as_markup())
    # await message.answer("Выберите категорию:", reply_markup=builder.as_markup())


async def category_btn(call: CallbackQuery):
    global LST_CAT, LST_POST
    btn_data = int(call.data.split("_")[1])
    try:
        title = [i["title"] for i in LST_CAT if i["id"] == btn_data][0]
    except IndexError:
        title = 0
    categories_list = get_categories(btn_data)
    posts_list = get_posts(btn_data)
    LST_CAT = categories_list
    LST_POST = posts_list
    category_builder = InlineKeyboardBuilder()
    post_builder = InlineKeyboardBuilder()
    start_btn_markup = InlineKeyboardBuilder()
    start_btn = InlineKeyboardButton(
        text="Вернуться в начало",
        callback_data="start")
    start_btn_markup.add(start_btn)
    await call.message.answer("======================\n"
                              f"Выбранная категория: {title}")
    if not categories_list and not posts_list:
        await call.message.answer("Категории и материалы не найдены.", reply_markup=start_btn_markup.as_markup())
    elif not categories_list:
        for post in posts_list:
            post_builder.add(
                InlineKeyboardButton(
                    text=f"{post['title']}",
                    callback_data=f"post_{post['id']}",
                )
            )
        post_builder.add(start_btn)
        post_builder.adjust(1)
        await call.message.answer("Выберите материал:", reply_markup=post_builder.as_markup())
    elif not posts_list:
        for category in categories_list:
            category_builder.add(
                InlineKeyboardButton(
                    text=f"{category['title']}",
                    callback_data=f"category_{category['id']}",
                )
            )
        category_builder.add(start_btn)
        category_builder.adjust(1)
        await call.message.answer("Выберите Категорию:", reply_markup=category_builder.as_markup())
    else:
        for category in categories_list:
            category_builder.add(
                InlineKeyboardButton(
                    text=f"{category['title']}",
                    callback_data=f"category_{category['id']}",
                )
            )
        category_builder.adjust(1)
        await call.message.answer("Выберите Категорию:", reply_markup=category_builder.as_markup())
        for post in posts_list:
            post_builder.add(
                InlineKeyboardButton(
                    text=f"{post['title']}",
                    callback_data=f"post_{post['id']}",
                )
            )
        post_builder.adjust(1)
        await call.message.answer("Выберите материал:", reply_markup=post_builder.as_markup())
        await call.message.answer("Если ничего не подходит:", reply_markup=start_btn_markup.as_markup())
    await call.answer()


async def post_btn(call: CallbackQuery):
    btn_data = int(call.data.split("_")[1])
    try:
        title = [i["title"] for i in LST_POST if i["id"] == btn_data][0]
    except IndexError:
        title = 0
    scripts_list = get_scripts(btn_data)
    scripts_builder = InlineKeyboardBuilder()
    start_btn_markup = InlineKeyboardBuilder()
    start_btn = InlineKeyboardButton(
        text="Вернуться в начало",
        callback_data="start")
    start_btn_markup.add(start_btn)
    await call.message.answer("======================\n"
                              f"Выбранный материал: {title}")
    if not scripts_list:
        await call.message.answer("Скрипты не найдены.\n"
                                  "Выберите другую категорию или материал", reply_markup=start_btn_markup.as_markup())
    else:
        for script in scripts_list:
            scripts_builder.add(
                InlineKeyboardButton(
                    text=f"{script['title']}",
                    callback_data=f"script_{script['id']}",
                )
            )
        scripts_builder.add(start_btn)
        scripts_builder.adjust(1)
        await call.message.answer("Выберите скрипт:", reply_markup=scripts_builder.as_markup())
    await call.answer()


async def script_btn(call: CallbackQuery):
    btn_data = int(call.data.split("_")[1])
    script = get_script(btn_data)
    start_btn_markup = InlineKeyboardBuilder()
    start_btn = InlineKeyboardButton(
        text="Вернуться в начало",
        callback_data="start")
    start_btn_markup.add(start_btn)
    await call.message.answer(f"{script[0]['title']}\n\n"
                              f"{script[0]['script']}\n\n"
                              f"{script[0]['operation']}", reply_markup=start_btn_markup.as_markup())
