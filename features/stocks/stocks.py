from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, FSInputFile, \
    CallbackQuery

from bot import bot
from data.users.users_data import tg_users_data
from shared import constants
from shared.keyboards.inline_keyboards.keyboards import stocks_kb

router = Router()


@router.message(F.text == "🎁Акции")
async def command_hello_handler(message: Message) -> None:
    await message.delete()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    keyboard = stocks_kb()
    media = FSInputFile("assets/stocks.png")
    text = 'Наши акции'

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
                reply_markup=keyboard
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, msg.message_id)


@router.callback_query(F.data.startswith('stocks_'))
async def helloworld(callback: CallbackQuery):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    keyboard = stocks_kb()
    text = f"{constants.stocks_map[callback.data]['description']}"
    photo = FSInputFile(constants.stocks_map[callback.data]['photo'])
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
