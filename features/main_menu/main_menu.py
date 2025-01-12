import datetime
import json

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto

import shared.keyboards.reply_keyboards.keyboards as kb
from bot import bot
from data.users.users_data import tg_users_data
from domain.entities.freebet import Freebet
from domain.entities.user import User
from shared.methods.clear_chat import clear_chat
from shared.methods.generate_freebet_key import key_generator
from shared.methods.update_last_message import update_last_message

router = Router()


@router.message(Command('start'))
async def command_hello_handler(message: Message) -> None:
    await message.delete()

    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)

    def isAdmin():
        if message.from_user.id == 5965231899:
            return 1
        else:
            return 0

    keyboard = kb.main_kb(0)

    if user:
        if user.player_id == -31415926:
            keyboard = kb.main_kb(1)

    hello_message = await message.answer(text="Привет!", reply_markup=keyboard)

    if not user:
        freebet = Freebet(name='Фрибет за вход в бота', summa=111, uuid=next(key_generator))
        user = await tg_users_data.add_user(
            User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                last_message_id=message.message_id + 1,
                all_messages=json.dumps([hello_message.message_id]),
                is_admin=isAdmin(),
                player_id=-1,
                reg_date=datetime.datetime.now(),
                birthday='',
                authorized=0,
                freebets=json.dumps([freebet.to_json()])
            ))
    else:
        await clear_chat(user)
        await tg_users_data.add_to_all_messages(user, hello_message.message_id)

    msg = await bot.send_photo(
        chat_id=message.chat.id,
        caption=f"Все функции расположены в нижнем меню",
        photo=FSInputFile("assets/main_menu.png")
    )
    await tg_users_data.add_to_all_messages(user, msg.message_id)
    await update_last_message(user, msg.message_id)


@router.callback_query(F.data.startswith("main_menu"))
async def helloworld(callback: CallbackQuery):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)

    if callback.data == "main_menu_exit":
        user.authorized = 0
        await tg_users_data.update_user(user)

    text = f"Все функции расположены в нижнем меню"
    photo = FSInputFile("assets/main_menu.png")
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=text),
            chat_id=user.telegram_id,
            message_id=user.last_message_id,
        )
    except TelegramBadRequest as e:
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=user.telegram_id,
                caption=text,
                photo=photo,
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, msg.message_id)
