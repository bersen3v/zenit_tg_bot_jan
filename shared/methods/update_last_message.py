from domain.entities.user import User
from data.users.users_data import tg_users_data


async def update_last_message(user: User, message_id: int):
  user.last_message_id = message_id
  await tg_users_data.update_user(user)