import os

import pandas as pd

from domain.entities.player import Player

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
project_root = os.path.abspath(os.path.join(current_directory, "../"))


def get_player_by_playerid(player_id: int):
    df = pd.read_csv(f"{project_root}/databases/players.csv")

    player_data = df[df['Номер клиента'] == player_id]
    if len(player_data.index) != 0:
        if pd.isnull(player_data['Отметка'].values[0]) and pd.isnull(player_data['Приложение'].values[0]):
            player = Player(
                player_data['Номер клиента'].values[0],
                str(player_data['Имя'].values[0]),
                player_data['Пол'].values[0],
                player_data['Дата рождения'].values[0],
            )
            return player
    else:
        return None
