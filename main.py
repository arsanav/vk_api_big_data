import time
import requests
import json


# Выкачка данных из групп тематики Big Data
def posts_search_vk_api_groups():
    # Токен для подключения к VK API
    token = 'a92f413ba92f413ba92f413b39aa3f8a72aa92fa92f413bca04bf22e2703f30a8ec4c6f'
    version = 5.131

    # Список доменов групп для выкачки
    domains = ['mashinnoe_obuchenie_ai_big_data', 'datascience_ai', 'datascience', 'datamining.team']

    # Количество выкачиваемых записей за итерацию (у VK API лимит до 100)
    count = 100
    posts = []

    for domain in domains:
        # Смещение для обхода лимита
        offset = 0
        while offset < 2500:
            # Запрос wall.get
            response = requests.get('https://api.vk.com/method/wall.get',
                                    params={
                                        'access_token': token,
                                        'v': version,
                                        'domain': domain,
                                        #'query': 'большие данные',
                                        'count': count,
                                        'offset': offset
                                    }
                                    )
            data = response.json()['response']['items']
            offset += 100
            posts.extend(data)
            time.sleep(0.1)
    return posts


result = posts_search_vk_api_groups()

# Формирование json файла
with open('vk_dump.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)

