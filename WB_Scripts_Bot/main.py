import asyncio
import logging
from aiogram import Dispatcher, F
from aiogram.filters import Command

from core.handlers.print_script import category_btn, post_btn, script_btn, start_operation
from core.handlers.register_user import register, reset
from core.settings import settings, bot
from core.utils.commands import set_commands


async def start_bot():
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, 'Бот запущен')


async def stop_bot():
    await bot.send_message(settings.bots.admin_id, 'Бот остановлен')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - %(message)s",
                        )

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(start_operation, Command(commands="start"))
    dp.message.register(register, Command(commands="register"))
    dp.message.register(reset, Command(commands="reset"))

    dp.callback_query.register(category_btn, F.data.startswith("category_"))
    dp.callback_query.register(post_btn, F.data.startswith("post_"))
    dp.callback_query.register(script_btn, F.data.startswith("script_"))
    dp.callback_query.register(start_operation, F.data.startswith("start"))
    dp.callback_query.register(reset, F.data.startswith("reset"))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
