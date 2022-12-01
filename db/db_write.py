import psycopg2
import tqdm
import json


with open('vk_dump.json', encoding='utf8') as f:
    result_json = json.load(f)

conn = psycopg2.connect(
    host="localhost",
    port=5511,
    database="intro_bd",
    user="postgres",
    password="KJKSZPJ")

# Cursor setting
for entry in tqdm(result_json):
    c = conn.cursor()
    c.execute("begin")
    origin_id = entry["from_id"] + '_' + entry["id"]
    url = f'vk.com/wall{origin_id}'
    c.execute(
        "INSERT INTO data (platform, origin_id, content, origin_name, origin_url, raw_content) VALUES (3, %s, %s, 'Null', %s, 'Null')",
        (origin_id, entry['text'], url))
    c.execute("commit")
