import time
import requests
import json

def posts_search_vk_api_groups():
    token = 'a92f413ba92f413ba92f413b39aa3f8a72aa92fa92f413bca04bf22e2703f30a8ec4c6f'
    version = 5.131
    domains = ['mashinnoe_obuchenie_ai_big_data', 'datascience_ai', 'datascience', 'datamining.team']
    count = 100
    posts = []

    for domain in domains:
        offset = 0
        while offset < 2500:
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
with open('vk_dump.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)
print(result)
