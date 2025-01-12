from aiogram.types import FSInputFile

import shared.keyboards.reply_keyboards.keyboards as kb
from bot import bot
from data.users.users_data import tg_users_data
from domain.entities.freebet import Freebet
from shared.methods.add_freebet import add_freebet
from shared.methods.clear_chat import clear_chat
from shared.methods.generate_freebet_key import key_generator


async def ids_frb_mailing(photo_path: str, text: str, ids_path: str, frb_name: str, frb_count: str):
    file = open(ids_path, 'r')
    content = file.readlines()
    for player_id in content:
        player_id = int(str(player_id).replace("\n", ""))
        user = await tg_users_data.get_user_by_player_id(player_id)
        await clear_chat(user)

        keyboard = kb.main_kb(user.player_id == -31415926)
        hello_message = await bot.send_message(chat_id=user.telegram_id, text="Привет!", reply_markup=keyboard)
        await add_freebet(user, Freebet(frb_name, frb_count, next(key_generator)))
        msg = await bot.send_photo(
            chat_id=user.telegram_id,
            photo=FSInputFile(photo_path),
            caption=text
        )
        user.last_message_id = msg.message_id
        await tg_users_data.update_user(user)
        await tg_users_data.add_to_all_messages(user, message_id=hello_message.message_id)
        await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
