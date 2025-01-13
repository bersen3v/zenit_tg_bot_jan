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


async def add_freebet_bonus(user: User):
    date_format = '%Y-%m-%d %H:%M:%S.%f'
    reg_date = datetime.strptime(user.reg_date, date_format)
    # today = datetime.strptime("2025-01-02 16:25:30.667101", date_format)
    today = datetime.now()
    diff = (today - reg_date).days

    if diff == 1:
        await add_freebet(user, Freebet("За 1 день в боте (101)", summa=101, uuid=next(key_generator)))
        await send_bonus(user, "assets/freebet_101.jpeg",
                         "Привет! Ты пользуешься ботом ровно 1 день. За это мы дарим тебе фрибет на 101 рубль! Он находится в твоем личном кабинете")
    elif diff == 5:
        await add_freebet(user, Freebet("За 5 дней в боте (303)", summa=303, uuid=next(key_generator)))
        await send_bonus(user, "assets/freebet_303.jpeg",
                         "Привет! Ты пользуешься ботом ровно 5 дней. За это мы дарим тебе фрибет на 303 рубля! Он находится в твоем личном кабинете")
    elif diff == 10:
        await add_freebet(user, Freebet("За 10 дней в боте (505)", summa=505, uuid=next(key_generator)))
        await send_bonus(user, "assets/freebet_505.jpeg",
                         "Привет! Ты пользуешься ботом ровно 10 дней. За это мы дарим тебе фрибет на 505 рублей! Он находится в твоем личном кабинете")
    elif diff == 20:
        await add_freebet(user, Freebet("За 20 дней в боте (707)", summa=707, uuid=next(key_generator)))
        await send_bonus(user, "assets/freebet_707.jpeg",
                         "Привет! Ты пользуешься ботом ровно 20 дней. За это мы дарим тебе фрибет на 707 рублей! Он находится в твоем личном кабинете")
    elif diff == 30:
        await add_freebet(user, Freebet("За 30 дней в боте (1001)", summa=1001, uuid=next(key_generator)))
        await send_bonus(user, "assets/freebet_1001.jpeg",
                         "Привет! Ты пользуешься ботом ровно 30 дней. За это мы дарим тебе фрибет на 1001 рубль! Он находится в твоем личном кабинете")
    elif diff == 40:
        await add_freebet(user, Freebet("За 40 дней в боте (1303)", summa=1303, uuid=next(key_generator)))
        await send_bonus(user, "assets/freebet_1303.jpeg",
                         "Привет! Ты пользуешься ботом ровно 40 дней. За это мы дарим тебе фрибет на 1303 рубля! Он находится в твоем личном кабинете")
    elif diff == 50:
        await add_freebet(user, Freebet("За 50 дней в боте (1505)", summa=1505, uuid=next(key_generator)))
        await send_bonus(user, "assets/freebet_1505.jpeg",
                         "Привет! Ты пользуешься ботом ровно 50 дней. За это мы дарим тебе фрибет на 1505 рублей! Он находится в твоем личном кабинете")


async def send_bonus(user: User, photo_path: str, text: str):
    await clear_chat(user)
    keyboard = kb.main_kb(user.player_id == -31415926)
    hello_message = await bot.send_message(chat_id=int(user.telegram_id), text="Привет!", reply_markup=keyboard)
    msg = await bot.send_photo(
        chat_id=int(user.telegram_id),
        photo=FSInputFile(photo_path),
        caption=text
    )
    user.last_message_id = msg.message_id
    await tg_users_data.update_user(user)
    await tg_users_data.add_to_all_messages(user, message_id=hello_message.message_id)
    await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
