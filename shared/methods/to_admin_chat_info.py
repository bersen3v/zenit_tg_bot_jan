from aiogram.types import FSInputFile

from bot import bot
from data.users.users_data import tg_users_data


async def send_stat_to_admins():
    await tg_users_data.create_txt_data()
    await bot.send_document(
        chat_id=-1002487832753,
        document=FSInputFile("data/databases/main.db")
    )
    await bot.send_document(
        chat_id=-1002487832753,
        document=FSInputFile("data/databases/users.txt")
    )
