import json
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def open_menu(msg: Message, path: str):
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
        if item["action"] == "menu":
            if item["arg"].startswith("/"):
                key_path = item["arg"][1:]
            elif item["arg"].startswith("../"):
                key_path = "/".join(path.split("/")[:-1] + [item["args"][3:]])
            keyboard.add(InlineKeyboardButton(text=item["label"], callback_data=key_path))
        
        elif item["action"] == "func":
            keyboard.add(InlineKeyboardButton(text=item["label"], callback_data=item["arg"]))

    await msg.answer(text=text, reply_markup=keyboard.as_markup())


async def main_menu(msg: Message):
    await open_menu(msg, "main_menu")