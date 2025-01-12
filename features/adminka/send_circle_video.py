from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, FSInputFile, CallbackQuery

from bot import bot
from data.users.users_data import tg_users_data
from shared.keyboards.inline_keyboards.keyboards import send_circle_video_final_kb
from shared.methods.send_video_notes import send_video_notes

router = Router()

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class MailingVideoData(StatesGroup):
    need_photo = State()
    need_text = State()
    need_ids = State()


@router.callback_query(F.data == "send_circle_video")
async def helloworld(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type=callback.data)

    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    photo = FSInputFile("assets/adminka.jpeg")
    text = "Скинь видео для рассылки"
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
    await state.set_state(MailingVideoData.need_photo)


@router.message(MailingVideoData.need_photo, F.video)
async def helloworld(message: Message, state: FSMContext):
    await message.delete()

    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)

    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = message.video.file_name

    await bot.download_file(file_path=file_path, destination=f"assets/cache/{file_name}")
    await state.update_data(photo_path=f"assets/cache/{file_name}")

    video = FSInputFile(f"assets/cache/{file_name}")
    keyboard = send_circle_video_final_kb()

    msg = await bot.send_video_note(
        video_note=video,
        chat_id=user.telegram_id,
        reply_markup=keyboard
    )
    user.last_message_id = msg.message_id
    await tg_users_data.update_user(user)
    await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)


@router.callback_query(F.data == "send_circle_video_final")
async def helloworld(callback: CallbackQuery, state: FSMContext):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    photo = FSInputFile("assets/adminka.jpeg")
    data = await state.get_data()

    await send_video_notes(video_path=data['photo_path'])
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
