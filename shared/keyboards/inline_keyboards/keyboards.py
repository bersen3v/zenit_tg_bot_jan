from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from shared.constants import questions_map, stocks_map


def questions_kb():
    kb_list = [[InlineKeyboardButton(text=i.replace("questions_", ""), callback_data=i)] for i in questions_map.keys()]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def stocks_kb():
    kb_list = [[InlineKeyboardButton(text=i.replace("stocks_", ""), callback_data=i)] for i in stocks_map.keys()]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def lk_kb():
    kb_list = [[InlineKeyboardButton(text="🔐Авторизоваться", callback_data='auth')]]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def lk_auth_kb():
    kb_list = [
        [InlineKeyboardButton(text="🔁Попробовать еще раз", callback_data='auth')],
        [InlineKeyboardButton(text="❌Отмена", callback_data='main_menu')],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def lk_authorized_kb():
    kb_list = [
        [InlineKeyboardButton(text="🆓Мои фрибеты", callback_data='freebets')],
        [InlineKeyboardButton(text="❌Выйти", callback_data='main_menu_exit')],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def lk_freebets_kb(user_freebets):
    kb_list = [
        [InlineKeyboardButton(text=i.name[0], callback_data=f"frbbtn_{i.name[0]}_{i.uuid[0]}_{i.summa[0]}")] for i in
        user_freebets
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def admin_kb():
    kb_list = [
        [InlineKeyboardButton(text="Обновить базу", callback_data="load_data")],
        [InlineKeyboardButton(text="Рассылки", callback_data="mailing")],
        [InlineKeyboardButton(text="Подарить фрибеты", callback_data="frb_giveaway")],
        [InlineKeyboardButton(text="Статистика", callback_data="statistics")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def load_data_kb():
    kb_list = [
        [InlineKeyboardButton(text="Отменить", callback_data="load_data_exit")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def mailing_kb():
    kb_list = [
        [InlineKeyboardButton(text="Рассылка всем", callback_data="mailing_to_all")],
        [InlineKeyboardButton(text="Рассылка авторизованным", callback_data="mailing_to_authorized")],
        [InlineKeyboardButton(text="Рассылка по номерам игроков", callback_data="ids_mailing")],
        [InlineKeyboardButton(text="Рассылка видео", callback_data="send_circle_video")],

    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def mailing_final_kb():
    kb_list = [
        [InlineKeyboardButton(text="Отправить", callback_data="send")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def ids_mailing_final_kb():
    kb_list = [
        [InlineKeyboardButton(text="Отправить", callback_data="send_by_ids")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def ids_frb_mailing_final_kb():
    kb_list = [
        [InlineKeyboardButton(text="Отправить", callback_data="send_by_ids_frb")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def send_circle_video_final_kb():
    kb_list = [
        [InlineKeyboardButton(text="Отправить", callback_data="send_circle_video_final")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard


def complaints_kb():
    kb_list = [
        [InlineKeyboardButton(text="🚨Оставить жалобу", callback_data="send_complaint")],
        [InlineKeyboardButton(text="🎰Не работает ИРМ", callback_data="send_complaint_irm")],
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list
    )
    return keyboard
