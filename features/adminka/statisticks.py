from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, FSInputFile, CallbackQuery

from bot import bot
from data.users.users_data import tg_users_data
from shared.methods.to_admin_chat_info import send_stat_to_admins

router = Router()

from aiogram.fsm.context import FSMContext


@router.callback_query(F.data.startswith("statistics"))
async def helloworld(callback: CallbackQuery, state: FSMContext):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    await send_stat_to_admins()

    users = await tg_users_data.get_all_users()
    text = (f"Статистика\n\n"
            f"Пользователей всего: {len(users)}\n\n"
            f"Авторизированных пользователей: {len([user for user in users if user.authorized == 1])}")
    photo = FSInputFile("assets/adminka.jpeg")
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
