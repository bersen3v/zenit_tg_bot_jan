from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InputMediaPhoto, FSInputFile, CallbackQuery

from bot import bot
from data.users.users_data import tg_users_data
from shared.keyboards.inline_keyboards.keyboards import complaints_kb

router = Router()


class ComplaintData(StatesGroup):
    need_complaint = State()


@router.message(F.text == "🚨Жалобы")
async def command_hello_handler(message: Message) -> None:
    await message.delete()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    media = FSInputFile("assets/jaloba.png")

    text = 'Жалобы'

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=media, caption=text),
            chat_id=message.chat.id,
            message_id=user.last_message_id,
            reply_markup=complaints_kb()
        )
    except TelegramBadRequest as e:
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=message.chat.id,
                caption=text,
                photo=media,
                reply_markup=complaints_kb()
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, msg.message_id)


@router.callback_query(F.data == "send_complaint_irm")
async def helloworld(callback: CallbackQuery, state: FSMContext):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    photo = FSInputFile("assets/jaloba.png")

    await bot.send_message(
        chat_id=-1002487832753,
        text=f"Новая жалоба\n@{callback.from_user.username}\n{callback.from_user.id}\n{user.first_name}\n{user.birthday}\n\nНЕ РАБОТАЕТ ИРМ"
    )

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=f"Жалоба принята"
            ),
            chat_id=user.telegram_id,
            message_id=user.last_message_id,
        )

    except TelegramBadRequest as e:
        print(e)
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=user.telegram_id,
                caption="Жалоба принята",
                photo=photo,
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)


@router.callback_query(F.data == "send_complaint")
async def helloworld(callback: CallbackQuery, state: FSMContext):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    photo = FSInputFile("assets/jaloba.png")

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=f"Напиши жалобу"
            ),
            chat_id=user.telegram_id,
            message_id=user.last_message_id,
        )

    except TelegramBadRequest as e:
        print(e)
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=user.telegram_id,
                caption="Напиши жалобу",
                photo=photo,
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
    await state.set_state(ComplaintData.need_complaint)


@router.message(ComplaintData.need_complaint)
async def helloworld(message: Message, state: FSMContext):
    await message.delete()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    photo = FSInputFile("assets/jaloba.png")

    await bot.send_message(
        chat_id=-1002487832753,
        text=f"Новая жалоба\n@{message.from_user.username}\n{message.from_user.id}\n{user.first_name}\n{user.birthday}\n\n{message.text}"
    )
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=f"Жалоба принята"
            ),
            chat_id=user.telegram_id,
            message_id=user.last_message_id,
        )

    except TelegramBadRequest as e:
        print(e)
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=user.telegram_id,
                caption="Жалоба принята",
                photo=photo,
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
    await state.clear()
