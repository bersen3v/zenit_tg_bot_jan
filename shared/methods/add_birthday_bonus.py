from datetime import datetime

from aiogram.types import FSInputFile

import shared.keyboards.reply_keyboards.keyboards as kb
from bot import bot
from data.users.users_data import tg_users_data
from domain.entities.freebet import Freebet
from domain.entities.user import User
from shared.methods.add_freebet import add_freebet
from shared.methods.clear_chat import clear_chat
from shared.methods.generate_freebet_key import key_generator


async def add_birthday_bonus(user: User):
    date_format = '%d/%m/%Y'
    birthday_date = datetime.strptime(user.birthday, date_format)
    # today = datetime.strptime("2025-01-02 16:25:30.667101", date_format)
    today = datetime.now()
    today_is_birthday = birthday_date.day == today.day and birthday_date.month == today.month
    if today_is_birthday:
        await clear_chat(user)
        keyboard = kb.main_kb(user.player_id == -31415926)
        hello_message = await bot.send_message(chat_id=user.telegram_id, text="Привет!", reply_markup=keyboard)
        msg = await bot.send_photo(
            chat_id=user.telegram_id,
            photo=FSInputFile('assets/freebet_555.png'),
            caption="С днем рождения! Дарим тебе фрибет на 555 рублей! Он находится в твоем личном кабинете"
        )
        user.last_message_id = msg.message_id
        await tg_users_data.update_user(user)
        await tg_users_data.add_to_all_messages(user, message_id=hello_message.message_id)
        await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
        await add_freebet(user, Freebet('День рождения (555)', 555, uuid=next(key_generator)))
