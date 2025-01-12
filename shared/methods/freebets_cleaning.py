import json

from data.users.users_data import tg_users_data
from domain.entities.user import User
from shared.methods.add_freebet import remove_freebet
from shared.methods.google_table_data import get_google_table_data


async def freebets_cleaning_by_user(user: User):
    done_freebets = await get_google_table_data()
    freebets = json.loads(user.freebets)
    for freebet in freebets:
        freebet_id = int(freebet['uuid'][0])
        if freebet_id in done_freebets:
            done_freebets.remove(freebet_id)
            await remove_freebet(user, freebet['uuid'])


async def freebets_cleaning():
    done_freebets = await get_google_table_data()
    users = await tg_users_data.get_all_users()
    for user in users:
        freebets = json.loads(user.freebets)
        for freebet in freebets:
            freebet_id = int(freebet['uuid'])
            if freebet_id in done_freebets:
                done_freebets.remove(freebet_id)
                await remove_freebet(user, freebet['uuid'])
