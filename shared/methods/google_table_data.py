import pandas as pd
import requests


async def get_google_table_data():
    url = "https://docs.google.com/spreadsheets/u/0/d/1Uc2vypVtz4Umc87kPpWRF9UjsP-kgWQi_QfXaVKoT7g/export?format=csv"
    response = requests.get(url)
    with open("assets/cache/google_table.csv", "w") as file:
        file.write(response.content.decode('utf-8'))
    df = pd.read_csv("assets/cache/google_table.csv")
    data = []
    for c in [3, 8, 13, 18, 23, 28, 33]:
        for frbt_id in list(df[f'Unnamed: {c}']):
            if str(frbt_id).isdigit():
                data.append(int(frbt_id))
    return data
