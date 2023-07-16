import requests
import json
import time
import itertools


# типы игр (id, название категории)
category_types_url = 'https://api.tesera.ru/tags/types?Offset=0&IsCancellationRequested=false&CanBeCanceled=false&WaitHandle.Handle=%7B%7D'
# типы сеттингов (id, название категории)   
category_settings_url = 'https://api.tesera.ru/tags/settings?Offset=0&IsCancellationRequested=false&CanBeCanceled=false&WaitHandle.Handle=%7B%7D'

def parse_cat(url):
    types_list = requests.get(url).json()
    with open('category_types_list', 'w') as json_file:
        json.dump(types_list, json_file, indent=4)

#df_types = pd.DataFrame(parse_cat(category_types_list)).append(pd.DataFrame(parse_cat(category_settings_list))



games = []

for ids in df_types['id']:
    url_tag = f'https://api.tesera.ru/games?Tags={ids}&Limit=100&WaitHandle.Handle=%7B%7D'
    response = requests.get(url_tag)
    count_offset = response.headers['x-total-pages']
    
    for offset in range(int(count_offset)):
        url = f'https://api.tesera.ru/games?Tags={ids}&Offset={offset}&Limit=100&WaitHandle.Handle=%7B%7D'
        games_data = requests.get(url).json()
        
        for row in games_data:
            row['id_type'] = ids
        
        games.append(games_data)


games = list(itertools.chain(*games))
#games_df = pd.DataFrame(games)



users = []

for alias in games['alias']:
    url_tag = f'https://api.tesera.ru/games/{alias}/ratings?Limit=100&WaitHandle.Handle=%7B%7D'
    response = requests.get(url_tag)
    count_offset = response.headers['x-total-pages']
    
    for offset in range(int(count_offset)):
        url = f'https://api.tesera.ru/games/{alias}/ratings?Offset={offset}&Limit=100&WaitHandle.Handle=%7B%7D'
        data = requests.get(url).json()
        
        for row in data:
            row['game_alias'] = alias

        users.append(data)

users = list(itertools.chain(*users))
#users_df = pd.DataFrame(users)