import json
from domain.entities.user import User
from bot import bot
from data.users.users_data import tg_users_data

async def clear_chat(user: User):
  try:
    await bot.delete_messages(chat_id=user.telegram_id, message_ids=json.loads(user.all_messages))
    user.all_messages = json.dumps([])
    await tg_users_data.update_user(user)
  except Exception as e: 
    print(e)