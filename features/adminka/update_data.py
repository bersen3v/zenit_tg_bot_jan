from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, FSInputFile, CallbackQuery

from bot import bot
from data.users.users_data import tg_users_data
from shared.keyboards.inline_keyboards.keyboards import load_data_kb

router = Router()

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class AdminkaLoadData(StatesGroup):
    need_data = State()


@router.callback_query(F.data.startswith("load_data"))
async def helloworld(callback: CallbackQuery, state: FSMContext):
    user = await tg_users_data.get_user_by_tg_id(callback.from_user.id)
    keyboard = load_data_kb()
    text = f"Скинь базу в формате .csv"
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
    await state.set_state(AdminkaLoadData.need_data)


@router.message(AdminkaLoadData.need_data, F.document)
async def helloworld(message: Message, state: FSMContext):
    await message.delete()

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    if message.document.file_name.endswith('.csv'):
        text = f"База обновлена"
        file = await bot.download_file(file_path=file_path, destination="data/databases/players.csv")
        await state.clear()
    else:
        text = "Ошибка"
        await state.clear()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
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
    await state.set_state(AdminkaLoadData.need_data)
