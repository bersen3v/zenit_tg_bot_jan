import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot import bot
from data.users.users_data import tg_users_data
from shared.methods.add_birthday_bonus import add_birthday_bonus
from shared.methods.bonus_freebet import add_freebet_bonus
from shared.methods.to_admin_chat_info import send_stat_to_admins
from shared.routers import router

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def send_mes():
    users = await tg_users_data.get_all_users()

    for user in users:
        try:
            await add_freebet_bonus(user)
            if user.birthday != " ":
                await add_birthday_bonus(user)
        except Exception as e:
            print(e)

    await send_stat_to_admins()


async def periodic_send():
    while True:
        await send_mes()
        await asyncio.sleep(86400)


async def main() -> None:
    await tg_users_data.create_table()
    asyncio.create_task(periodic_send())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
