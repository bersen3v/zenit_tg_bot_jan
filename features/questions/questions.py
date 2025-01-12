from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, FSInputFile, \
    CallbackQuery

from bot import bot
from data.users.users_data import tg_users_data
from shared import constants
from shared.keyboards.inline_keyboards.keyboards import questions_kb

router = Router()


@router.message(F.text == "❓Частые вопросы")
async def command_hello_handler(message: Message) -> None:
    await message.delete()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    keyboard = questions_kb()
    media = FSInputFile("assets/questions.png")
    text = 'Выбери нужный вопрос'

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
                text=text,
                photo=media,
                reply_markup=keyboard
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, msg.message_id)


@router.callback_query(F.data.startswith('questions_'))
async def helloworld(callback: CallbackQuery):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    keyboard = questions_kb()
    text = f"{callback.data.replace("questions_", "")}\n\n{constants.questions_map[callback.data]}"
    photo = FSInputFile("assets/questions.png")
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=text),
            chat_id=user.telegram_id,
            message_id=user.last_message_id,
            reply_markup=keyboard
        )
    except TelegramBadRequest as e:
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=user.telegram_id,
                caption=text,
                photo=photo,
                reply_markup=keyboard
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, msg.message_id)
