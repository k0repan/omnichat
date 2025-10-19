# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins


# KB = KeyboardButton
# RKM = ReplyKeyboardMarkup


# def main_kb(user_telegram_id: int):
#     kb_list = [
#         [KB(text="О нас"), KB(text="Профиль")],
#         [KB(text="Сосал?"), KB(text="Сколько детей?")]
#     ]

#     if user_telegram_id in admins:
#         kb_list.append([KB(text="Ого, админ! Дашь номер?", request_contact=True)])

#     kb = RKM(
#         keyboard=kb_list, 
#         resize_keyboard=True, 
#         one_time_keyboard=True,
#         input_field_placeholder="я гей:"
#     )
#     return kb