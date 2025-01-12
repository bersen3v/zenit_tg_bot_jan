import json

from data.users.users_data import tg_users_data
from domain.entities.freebet import Freebet
from domain.entities.user import User


async def add_freebet(user: User, freebet: Freebet):
    frb = json.loads(user.freebets)
    frb.append(freebet.to_json())
    user.freebets = json.dumps(frb)
    await tg_users_data.update_user(user)


async def remove_freebet(user: User, freebet_uuid):
    frb = json.loads(user.freebets)
    index = 0
    for freebet in frb:
        if freebet['uuid'] == freebet_uuid:
            frb.pop(index)
            break
        index += 1
    user.freebets = json.dumps(frb)
    await tg_users_data.update_user(user)


async def get_all_user_freebets(user: User):
    frb = json.loads(user.freebets)
    answer = []
    for freebet in frb:
        frbt = Freebet(freebet['name'], freebet['summa'], freebet['uuid'])
        answer.append(frbt)
    return answer
