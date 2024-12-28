import asyncio
import logging
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.filters import Filter, Command
from functions import start_command_reply, stop_command_state, new_command_answer, show_books_command, handle_message
import sys
import states
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

dp = Dispatcher()


async def main() -> None:
    dp.message.register(start_command_reply, Command('start'))
    dp.message.register(stop_command_state, Command('stop'))
    dp.message.register(new_command_answer, states.SignUp.username)
    dp.message.register(show_books_command, Command('books'))
    dp.message.register(handle_message)

    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands([
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command='/books', description="Kitoblar ro'yxatini olish")
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())