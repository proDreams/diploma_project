import os

from aiogram import Bot
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: str


@dataclass
class Settings:
    bots: Bots


def get_settings():

    return Settings(
        bots=Bots(
            bot_token=os.environ.get('BOT_TOKEN'),
            admin_id=os.environ.get('ADMIN_ID')
        )
    )


settings = get_settings()
bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
