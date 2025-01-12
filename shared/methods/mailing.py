from aiogram.types import FSInputFile

import shared.keyboards.reply_keyboards.keyboards as kb
from bot import bot
from data.users.users_data import tg_users_data
from domain.entities.user import User
from shared.methods.clear_chat import clear_chat


async def mailing(photo_path: str, text: str, type: str):
    users = await tg_users_data.get_all_users()

    for user in users:
        if user_validate_by_type(type, user):
            await clear_chat(user)

            keyboard = kb.main_kb(user.player_id == -31415926)
            hello_message = await bot.send_message(chat_id=user.telegram_id, text="Привет!", reply_markup=keyboard)

            msg = await bot.send_photo(
                chat_id=user.telegram_id,
                photo=FSInputFile(photo_path),
                caption=text
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=hello_message.message_id)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)


async def ids_mailing(photo_path: str, text: str, ids_path: str):
    file = open(ids_path, 'r')
    content = file.readlines()
    for id in content:
        user = await tg_users_data.get_user_by_player_id(id)
        await clear_chat(user)

        keyboard = kb.main_kb(user.player_id == -31415926)
        hello_message = await bot.send_message(chat_id=user.telegram_id, text="Привет!", reply_markup=keyboard)

        msg = await bot.send_photo(
            chat_id=user.telegram_id,
            photo=FSInputFile(photo_path),
            caption=text
        )
        user.last_message_id = msg.message_id
        await tg_users_data.update_user(user)
        await tg_users_data.add_to_all_messages(user, message_id=hello_message.message_id)
        await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)


def user_validate_by_type(type: str, user: User):
    if type == "mailing_to_all":
        return True
    elif type == "mailing_to_authorized":
        if user.authorized == 1:
            return True
