import time
import requests

def posts_search_vk_api_groups():
    token = 'a92f413ba92f413ba92f413b39aa3f8a72aa92fa92f413bca04bf22e2703f30a8ec4c6f'
    version = 5.131
    domains = ['bmstu1830', 'miptru', 'msu_official', 'mephi_official', 'hse',
               'mgimo', 'theacademy', 'finuniversity', 'reu', 'nust_misis',
               'mpei_ru', 'gubkin.university', 'i.m.sechenov', 'rudn_university', 'rnimu',
               'spb1724', 'nsu24', 'tomskuniversity', 'kazan_federal_university', 'ural.federal.university']
    count = 100
    posts = []

    for domain in domains:
        offset = 0
        while offset < 500:
            response = requests.get('https://api.vk.com/method/wall.search',
                                    params={
                                        'access_token': token,
                                        'v': version,
                                        'domain': domain,
                                        'query': 'большие данные',
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
print(result)
