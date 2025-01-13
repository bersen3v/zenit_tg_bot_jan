from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, FSInputFile

from bot import bot
from data.users.users_data import tg_users_data

router = Router()


@router.message(F.text == "📍Адреса")
async def command_hello_handler(message: Message) -> None:
    await message.delete()
    user = await tg_users_data.get_user_by_tg_id(message.from_user.id)
    media = FSInputFile("assets/adresses.png")

    text = (
        "Наши адреса:\n"
        "[ул. Ладо Кецховели 26/1](https://yandex.ru/maps/-/CDXOiPLP)\n"
        "[ул. Карла Маркса 51](https://yandex.ru/maps/-/CDXOiGnq)\n"
        "[ул. Взлетная ба](https://yandex.ru/maps/-/CDXOmUoR)\n"
        "[пр-т Красноярский Рабочий 176д/1](https://yandex.ru/maps/-/CDXOqN8a)\n"
        "[пр-т Красноярский Рабочий 91](https://yandex.ru/maps/-/CDXOqZYi)\n"
        "[ул. Павлова 11](https://yandex.ru/maps/-/CDXOqG2e)\n"
        "[ул. 26 Бакинских Комиссаров 44](https://yandex.ru/maps/-/CDXOqSmQ)\n"
        "[ул. Авиаторов 68а](https://yandex.ru/maps/-/CDXOq09z)\n"
        "[ул. Крупской 1г](https://yandex.ru/maps/-/CDXOqHyP)\n"
        "[пр-т Комсомольский 1, к.1](https://2gis.ru/krasnoyarsk/geo/985798073695894?m=92.935014%2C56.060415%2F15.95)\n"
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
            await tg_users_data.add_to_all_messages(user, message_id=msg.message_id)
