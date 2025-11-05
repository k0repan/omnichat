import json
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from create_bot import bot


def construct_keyboard(path: str):
    with open("keyboards/menu.json", encoding="UTF-8") as file:
        menu = json.load(file)

    for id in path.split("/"):
        for obj in menu["children"]:
            if obj["id"] == id:
                menu = obj
                break

    text = menu["text"]
    keyboard = InlineKeyboardBuilder()
    for item in menu["keyboard"]:
        keyboard.row()
        keyboard.add(InlineKeyboardButton(text=item["label"], callback_data=item["arg"]))

    return text, keyboard.adjust(1)


async def open_menu_msg(msg: Message, path: str):
    text, keyboard = construct_keyboard(path)
    await msg.answer(text=text, reply_markup=keyboard.as_markup())


async def open_menu_call(call: CallbackQuery, path: str):
    text, keyboard = construct_keyboard(path)
    await call.message.edit_text(text=text, reply_markup=keyboard.as_markup())
    await call.answer()


async def main_menu(msg: Message):
    await open_menu_msg(msg, "main_menu")