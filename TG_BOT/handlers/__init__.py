from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards import open_menu_call


inline_router = Router()


@inline_router.callback_query(F.data.startswith("/"))
async def process_inline_keyboard(call: CallbackQuery):
    await open_menu_call(call, call.data)