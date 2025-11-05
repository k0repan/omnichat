from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards import open_menu_msg
from create_bot import admins

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(
        "Приветствую! Пожалуйста, опишите свою проблему или воспользуйтесь быстрым выбором ниже!",
    )
    if msg.from_user.id in admins:
        await msg.answer("Имеются права администратора!")
    await open_menu_msg(msg, "main_menu")


@start_router.message(Command("hello"))
async def hello_handler(msg: Message):
    await msg.answer("Hi there!")