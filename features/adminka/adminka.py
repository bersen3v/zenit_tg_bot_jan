from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, FSInputFile

from bot import bot
from data.users.users_data import tg_users_data
from shared.keyboards.inline_keyboards.keyboards import admin_kb

router = Router()

from aiogram.fsm.state import State, StatesGroup


class AdminkaLoadData(StatesGroup):
    need_data = State()


@router.message(F.text == "ПАНЕЛЬ АДМИНИСТРАТОРА")
async def command_hello_handler(message: Message) -> None:
    await message.delete()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    media = FSInputFile("assets/adminka.jpeg")
    keyboard = admin_kb()
    text = "ПАНЕЛЬ АДМИНИСТРАТОРА"
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=media, caption=text),
            chat_id=message.chat.id,
            message_id=user.last_message_id,
            reply_markup=keyboard
        )
    except TelegramBadRequest as e:
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=message.chat.id,
                caption=text,
                photo=media,
                reply_markup=admin_kb()
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, msg.message_id)
