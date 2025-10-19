from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
IKB = InlineKeyboardButton
IKM = InlineKeyboardMarkup
IKBuilder = InlineKeyboardBuilder


def main_kb():
    inline_kb_list = [
        [IKB(text="", callback_data="")]
    ]
    return IKM(inline_keyboard=inline_kb_list)