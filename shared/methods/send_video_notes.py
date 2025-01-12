from aiogram.types import FSInputFile

import shared.keyboards.reply_keyboards.keyboards as kb
from bot import bot
from data.users.users_data import tg_users_data
from shared.methods.clear_chat import clear_chat


async def send_video_notes(video_path: str):
    users = await tg_users_data.get_all_users()

    for user in users:
        await clear_chat(user)

        keyboard = kb.main_kb(user.player_id == -31415926)
        hello_message = await bot.send_message(chat_id=user.telegram_id, text="Привет!", reply_markup=keyboard)

        video = FSInputFile(video_path)

        msg = await bot.send_video_note(
            video_note=video,
            chat_id=user.telegram_id
        )

        user.last_message_id = msg.message_id
        await tg_users_data.update_user(user)
        await tg_users_data.add_to_all_messages(user, message_id=hello_message.message_id)
        await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
