import time
from datetime import datetime
import requests
import json
import psycopg2
import tqdm


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
        while offset < 2:  # 2500
            # Запрос wall.get
            response = requests.get('https://api.vk.com/method/wall.get',
                                    params={
                                        'access_token': token,
                                        'v': version,
                                        'domain': domain,
                                        # 'query': 'большие данные',
                                        'count': count,
                                        'offset': offset
                                    }
                                    )
            data = response.json()['response']['items']
            offset += 100
            posts.extend(data)
            time.sleep(0.1)
    return posts


def main():
    # Подключение к БД
    conn = psycopg2.connect(
        host="localhost",
        port=5511,
        database="intro_bd",
        user="postgres",
        password="KJKSZPJ")

    result = posts_search_vk_api_groups()

    # Формирование json файла (закомментить, если файл не нужен)
    with open('vk_dump.json', 'w', encoding='utf8') as outfile:
        json.dump(result, outfile, ensure_ascii=False)

    # with open('vk_dump.json', 'r', encoding='utf8') as f:
    #     result_json = json.load(f)

    # Фиксация времени
    c = conn.cursor()
    start_time = datetime.now()
    c.execute("begin")

    # Запись в БД
    for entry in tqdm(result):
        origin_id = entry["from_id"] + '_' + entry["id"]
        url = f'vk.com/wall{origin_id}'
        c.execute(
            "INSERT INTO data (platform, origin_id, content, origin_name, origin_url, raw_content) VALUES (3, %s, %s, 'Null', %s, 'Null')",
            (origin_id, entry['text'], url))

    c.execute("commit")
    print(datetime.now() - start_time)


main()
