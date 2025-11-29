import json

import aiosqlite

from data.databases.db_config import DB, C, T
from domain.entities.user import User


class TelegramUsersData:

    def __init__(self) -> None:
        self.database_path = DB.main

    async def create_table(self) -> None:
        async with aiosqlite.connect(self.database_path) as connection:
            await connection.execute(f'''
                CREATE TABLE IF NOT EXISTS {T.telegram_users_table} (
                    {C.tg_id} INTEGER PRIMARY KEY,
                    {C.tg_username} TEXT, 
                    {C.tg_first_name} TEXT,
                    {C.tg_last_name} TEXT,
                    {C.last_message_id} INTEGER,
                    {C.all_messages} TEXT,
                    {C.is_admin} INTEGER,
                    {C.player_id} INTEGER,
                    {C.reg_date} TEXT,
                    {C.birthday} TEXT,
                    {C.authorized} INTEGER,
                    {C.freebets} TEXT
                )
            ''')
            await connection.commit()

    async def get_user_by_player_id(self, player_id: int):
        async with aiosqlite.connect(self.database_path) as connection:
            cursor = await connection.execute(
                F'SELECT * FROM {T.telegram_users_table} WHERE {C.player_id} = {player_id}')
            row = await cursor.fetchone()
        if row:
            user = User(*row)
            return user
        else:
            return None

    async def get_user_by_tg_id(self, tg_id: int):
        async with aiosqlite.connect(self.database_path) as connection:
            cursor = await connection.execute(F'SELECT * FROM {T.telegram_users_table} WHERE {C.tg_id} = {tg_id}')
            row = await cursor.fetchone()

        if row:
            user = User(*row)
            return user
        else:
            return None

    async def get_all_users(self) -> list[User]:
        users = []
        async with aiosqlite.connect(self.database_path) as connection:
            cursor = await connection.execute(F'SELECT * FROM {T.telegram_users_table}')
            rows = await cursor.fetchall()
        for row in rows:
            if row:
                users.append(User(*row))
        return users

    async def add_user(self, user: User) -> None:
        async with aiosqlite.connect(self.database_path) as connection:
            await connection.execute(f'''
                   INSERT INTO {T.telegram_users_table} 
                   ({C.tg_id}, {C.tg_username}, {C.tg_first_name}, {C.tg_last_name}, {C.last_message_id}, {C.all_messages}, {C.is_admin}, {C.player_id}, {C.reg_date}, {C.birthday}, {C.authorized}, {C.freebets}) 
                   VALUES ({user.telegram_id}, '{user.username}', '{user.first_name}', '{user.last_name}', {user.last_message_id}, '{user.all_messages}', {user.is_admin}, {user.player_id}, '{user.reg_date}', '{user.birthday}', {user.authorized}, '{user.freebets}')
               ''')
            await connection.commit()

        async with aiosqlite.connect(self.database_path) as connection:
            cursor = await connection.execute(
                F'SELECT * FROM {T.telegram_users_table} WHERE {C.tg_id} = {user.telegram_id}')
            row = await cursor.fetchone()

        if row:
            user = User(*row)
            return user
        else:
            return None

    async def update_user(self, user: User) -> None:
        async with aiosqlite.connect(self.database_path) as connection:
            await connection.execute(f'''
                    UPDATE {T.telegram_users_table}
                    SET {C.tg_username} = '{user.username}', {C.tg_first_name} = '{user.first_name}', {C.tg_last_name} = '{user.last_name}', {C.last_message_id} = {user.last_message_id}, {C.all_messages} = '{user.all_messages}', {C.is_admin} = {user.is_admin}, {C.reg_date} = '{user.reg_date}', {C.birthday} = '{user.birthday}', {C.authorized} = {user.authorized}, {C.freebets} = '{user.freebets}', {C.player_id} = {user.player_id}
                    WHERE {C.tg_id} = {user.telegram_id}
               ''')
            await connection.commit()

    async def add_to_all_messages(self, user: User, message_id: int):
        all_messages = json.loads(user.all_messages)
        all_messages.append(message_id)
        user.all_messages = json.dumps(all_messages)
        await tg_users_data.update_user(user)

    async def create_txt_data(self):
        i = 0
        users = await tg_users_data.get_all_users()
        with open('data/databases/users.txt', 'w') as file:
            for user in users:
                i += 1
                file.write(f"{i}\n")
                file.write(f"{user.to_string()}\n\n")


tg_users_data = TelegramUsersData()
