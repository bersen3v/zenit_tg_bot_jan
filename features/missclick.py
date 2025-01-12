from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def command_hello_handler(message: Message) -> None:
    await message.delete()
