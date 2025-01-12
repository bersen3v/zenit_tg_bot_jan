from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InputMediaPhoto, FSInputFile, \
    CallbackQuery

from bot import bot
from data.players.players_data import get_player_by_playerid
from data.users.users_data import tg_users_data
from shared.keyboards.inline_keyboards.keyboards import lk_kb, lk_auth_kb, lk_authorized_kb, lk_freebets_kb
from shared.methods.add_freebet import get_all_user_freebets
from shared.methods.freebets_cleaning import freebets_cleaning_by_user

router = Router()


class Lk(StatesGroup):
    auth = State()


@router.message(F.text == "👤Личный кабинет")
async def command_hello_handler(message: Message, state: FSMContext) -> None:
    await message.delete()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    if user.authorized == 0:
        media = FSInputFile("assets/lk.png")
        keyboard = lk_kb()
        text = "Личный кабинет"
    else:
        media = FSInputFile("assets/lk.png")
        keyboard = lk_authorized_kb()
        text = f"Добро пожаловать в личный кабинет, {user.first_name}"
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
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)


@router.callback_query(F.data == "auth")
async def command_hello_handler(message: CallbackQuery, state: FSMContext) -> None:
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    media = FSInputFile("assets/lk.png")
    text = "Чтобы авторизоваться, отправь свой номер игрока"
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=media, caption=text),
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
                photo=media,
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
    await state.set_state(Lk.auth)


@router.message(Lk.auth)
async def registrate_account(message: Message, state: FSMContext) -> None:
    await message.delete()

    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    player = get_player_by_playerid(int(message.text))

    media = FSInputFile("assets/lk.png")

    if player == None:
        text = "Игрока с таким номером не существует"
        keyboard = lk_auth_kb()
        await state.clear()
    else:
        freebets = await get_all_user_freebets(user)
        text = f"Добро пожаловать в личный кабинет, {list(player.name)[0]}"
        user.player_id = int(list(player.player_id)[0])
        user.first_name = list(player.name)[0]
        user.birthday = player.birthday
        user.authorized = 1
        await tg_users_data.update_user(user)
        keyboard = lk_authorized_kb()
        await state.clear()

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=media, caption=text),
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
                photo=media,
                reply_markup=keyboard
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)


@router.callback_query(F.data == "freebets")
async def command_hello_handler(message: CallbackQuery, state: FSMContext) -> None:
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)

    await freebets_cleaning_by_user(user)

    media = FSInputFile("assets/lk.png")
    text = "Список фрибетов"
    freebets = await get_all_user_freebets(user)
    keyboard = lk_freebets_kb(freebets)
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=media, caption=text),
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
                photo=media,
                reply_markup=keyboard
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)


@router.callback_query(F.data.startswith("frbbtn_"))
async def command_hello_handler(message: CallbackQuery, state: FSMContext) -> None:
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    media = FSInputFile("assets/lk.png")
    _, name, uuid, summa = message.data.split("_")
    text = f"{name}\n\nПромокод: {uuid.replace("'", "")}\nСумма фрибета: {summa.replace("'", "")}"
    freebets = await get_all_user_freebets(user)
    keyboard = lk_freebets_kb(freebets)
    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=media, caption=text),
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
                photo=media,
                reply_markup=keyboard
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
