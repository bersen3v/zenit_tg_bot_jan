from aiogram.types import ReplyKeyboardMarkup

from shared.keyboards.reply_keyboards.buttons import Buttons

admins = []


def main_kb(is_admin: int):
    kb_list = [
        [Buttons.btn_stocks, Buttons.btn_adresses],
        [Buttons.btn_questions, Buttons.btn_contcts],
        [Buttons.btn_complaints, Buttons.btn_profile]
    ]

    if is_admin == 1:
        kb_list.append([Buttons.btn_admins_panel])

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True
    )
    return keyboard


def no_main_kb(user_telegram_id: int):
    kb_list = [
        [Buttons.btn_stocks, Buttons.btn_adresses],
    ]
    if user_telegram_id in admins:
        kb_list.append([Buttons.btn_admins_panel])

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True
    )
    return keyboard
