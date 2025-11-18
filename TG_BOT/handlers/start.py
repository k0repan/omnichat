from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import open_menu_msg
from create_bot import admins


start_router = Router()


@start_router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer(f"Приветствую! Пожалуйста, опишите свою проблему или воспользуйтесь быстрым выбором ниже.")
    if msg.from_user.id in admins:
        await msg.answer("Имеются права администратора!")

    await open_menu_msg(msg, "main_menu")