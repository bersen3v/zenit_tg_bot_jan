from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, FSInputFile, CallbackQuery

from bot import bot
from data.users.users_data import tg_users_data
from shared.keyboards.inline_keyboards.keyboards import mailing_kb, mailing_final_kb

router = Router()

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.methods.mailing import mailing


class MailingData(StatesGroup):
    need_photo = State()
    need_text = State()
    need_ids = State()


@router.callback_query(F.data == "mailing")
async def helloworld(callback: CallbackQuery, state: FSMContext):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    keyboard = mailing_kb()
    text = f"Выбери вид рассылок"
    photo = FSInputFile("assets/adminka.jpeg")
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


@router.callback_query(F.data.startswith('mailing_'))
async def helloworld(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type=callback.data)

    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    photo = FSInputFile("assets/adminka.jpeg")
    text = "Скинь фото для рассылки"
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=text
            ),
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
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
    await state.set_state(MailingData.need_photo)


@router.message(MailingData.need_photo, F.document)
async def helloworld(message: Message, state: FSMContext):
    await message.delete()

    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = message.document.file_name

    await bot.download_file(file_path=file_path, destination=f"assets/cache/{file_name}")
    await state.update_data(photo_path=f"assets/cache/{file_name}")

    text = "Фото получено. Теперь введи текст"
    photo = FSInputFile(f"assets/cache/{file_name}")

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=text
            ),
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
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
    await state.set_state(MailingData.need_text)


@router.message(MailingData.need_text)
async def helloworld(message: Message, state: FSMContext):
    await message.delete()

    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)

    await state.update_data(text=message.text)
    data = await state.get_data()

    photo = FSInputFile(data['photo_path'])

    keyboard = mailing_final_kb()

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=f"{data['text']}"
            ),
            chat_id=user.telegram_id,
            message_id=user.last_message_id,
            reply_markup=keyboard
        )

    except TelegramBadRequest as e:
        print(e)
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=user.telegram_id,
                caption="message.text",
                photo=photo,
                reply_markup=keyboard
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)


@router.callback_query(F.data == "send")
async def helloworld(callback: CallbackQuery, state: FSMContext):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    photo = FSInputFile("assets/adminka.jpeg")
    data = await state.get_data()

    await mailing(photo_path=data['photo_path'], text=data['text'], type=data['type'])
    await state.clear()

    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(
                media=photo,
                caption=f"Сообщения разосланы"
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
                caption="Сообщения разосланы",
                photo=photo,
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
