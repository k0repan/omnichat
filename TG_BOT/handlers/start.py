from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards import open_menu

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(
        f"Запуск сообщения по команде /start используя фильтр CommandStart().\n\nID: {msg.from_user.id}",
    )
    await open_menu(msg, "main_menu")


@start_router.message(Command("hello"))
async def hello_handler(msg: Message):
    await msg.answer("Hi there!")