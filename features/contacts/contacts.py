from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, FSInputFile

from bot import bot
from data.users.users_data import tg_users_data

router = Router()


@router.message(F.text == "📞Контакты")
async def command_hello_handler(message: Message) -> None:
    await message.delete()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    media = FSInputFile("assets/contacts.png")

    text = (
        "Контакты:\n"
        "1. Телеграмм: [zenit_bk_krsk](https://t.me/zenit_bk_krsk)\n"
        "2. ВКонтакте: [bet_zenit24](https://vk.com/bet_zenit24)\n"
        "3. Справочный телефон: +7 (391) 200-81-84\n"
        "4. Телефон для связи по вопросам качества обслуживания:\n +7 963 260-58-71\n"
        "5. Сайт: [Смотриспорт24.рф](http://смотриспорт24.рф)"
    )

    try:
        await bot.edit_message_media(
            media=InputMediaPhoto(media=media, caption=text),
            chat_id=message.chat.id,
            message_id=user.last_message_id,
        )
    except TelegramBadRequest as e:
        if "the same as a current content" in str(e):
            return
        else:
            msg = await bot.send_photo(
                chat_id=message.chat.id,
                caption=text,
                photo=media,
            )
            user.last_message_id = msg.message_id
            await tg_users_data.update_user(user)
            await tg_users_data.add_to_all_messages(user, msg.message_id)
