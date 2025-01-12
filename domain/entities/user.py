import json


class User:
    def __init__(self, telegram_id, username, first_name, last_name, last_message_id, all_messages, is_admin, player_id,
                 reg_date, birthday, authorized, freebets):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.last_message_id = last_message_id
        self.all_messages = all_messages
        self.is_admin = is_admin
        self.player_id = player_id
        self.reg_date = reg_date
        self.birthday = birthday
        self.authorized = authorized
        self.freebets = freebets

    def to_string(self):
        return f"telegram_id: {self.telegram_id}\nusername: {self.username}\nfirst_name: {self.first_name}\nlast_name: {self.last_name}\nlast_message_id: {self.last_message_id}\nall_messages: {self.all_messages}\nis_admin: {self.is_admin}\nplayer_id: {self.player_id}\nreg_date: {self.reg_date}\nfreebets: {json.loads(self.freebets)}"
