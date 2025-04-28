# -- coding: utf-8 --
# @Author: 胡H
# @File: xiaohognshu_page.py
# @Created: 2025/3/31 10:23
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import json
import time
import random
import execjs
import requests
from loguru import logger
import re
from fetch_details import fetch_xiaohongshu_data
import pandas as pd
import os
from datetime import datetime

img_path = 'result'
output_file_path = "result.csv"

# 初始化 CSV 文件并写入表头
if not os.path.exists(output_file_path):
    with open(output_file_path, mode="w", encoding="utf-8-sig", newline="") as f:
        f.write("note_url,last_update_time,note_id,xsec_token,type,title,text,topics,likes,comments,collects,shares\n")


def base36encode(number, digits='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    base36 = ""
    while number:
        number, i = divmod(number, 36)
        base36 = digits[i] + base36
    return base36.lower()


def generate_search_id():
    timestamp = int(time.time() * 1000) << 64
    random_value = int(random.uniform(0, 2147483646))
    return base36encode(timestamp + random_value)


def parse_data(data):
    items = data.get('data', {}).get('items', [])
    parsed_info = []

    for item in items:
        note = item.get('note_card', {})
        title = note.get('title', '')
        desc = note.get('desc', '')

        # 提取并清理话题
        topics = [word.strip('#').replace('[话题]', '').strip() for word in desc.split() if '[话题]' in word]
        desc_cleaned = ' '.join([word for word in desc.split() if '[话题]' not in word]).strip()

        interact_info = note.get('interact_info', {})
        liked_count = interact_info.get('liked_count', 0)
        comment_count = interact_info.get('comment_count', 0)
        collected_count = interact_info.get('collected_count', 0)
        share_count = interact_info.get('share_count', 0)

        parsed_info.append({
            '标题': title,
            '内容': desc_cleaned,
            '点赞数': liked_count,
            '评论数': comment_count,
            '收藏数': collected_count,
            '转发数': share_count,
            '话题': topics
        })

    return parsed_info


def convert_to_int(value):
    if '万' in value:
        value = value.replace('万', '')
        return float(value) * 10000  # 转换为万单位的整数
    else:
        return value


search_data = {
    "keyword": "关键词",
    "page": 1,  # 爬的页数游标，需要不断更改
    "page_size": 20,  # 不用修改
    "search_id": generate_search_id(),
    "sort": "general",  # 排序的方式 综合，最热，最新
    "note_type": 0
}
cookies = {
    'abRequestId': '39a73910-2452-5903-a228-10c7a82ba11f',
    'webBuild': '4.61.1',
    'xsecappid': 'xhs-pc-web',
    'a1': '195e9f335bdpnvw38ozqmjhjz64wj9txl39g34z6f50000876516',
    'webId': '6d0bae642111efe50c0a31b8e6debd61',
    'acw_tc': '0ad6fb0417433867857456385e282c059bd0558ea3c7520dd2d75e9bd58b46',
    'gid': 'yj2djiq40y18yj2djiqq2q4uDfUIhEqYluA6jKiVxVuK4k28EVj9Cq888YWK2yK8YqDDy8Jy',
    'web_session': '040069b4f42beba52063d3b0dc354b4c9ac007',
    'unread': '{%22ub%22:%2267c832e6000000002903815b%22%2C%22ue%22:%2267e75adf000000001c00b5c8%22%2C%22uc%22:33}',
    'loadts': '1743386979966',
    'websectiga': '7750c37de43b7be9de8ed9ff8ea0e576519e8cd2157322eb972ecb429a7735d4',
    'sec_poison_id': 'be72e0e0-3b10-40df-833c-64199c1862cd',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'origin': 'https://www.xiaohongshu.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.xiaohongshu.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-b3-traceid': '19312f336007841a',
    'x-mns': 'awc2K2davRRfPg4JY9ZZM9yKO/yufDwMM53baCD1iFmfzS1xpwkaeRyf0G4XvaF3veavDg4+TbtQCcmk9/h0GCJPW30M9ipHQM/SKiTEXuCQEP5xuL7t0gzzweYZviJygvWpEYHOBLJJ3kiO2a0IDipvRTDQc8uN377+4IjIf4MytpdxNcXMvcn/0Id3aMWCyf7NOtjCCLxZhz0QOWDdgioQ9Zv3yId77CiBBcZNEfvMLInZaIvuoNPHH1IoHm4xLzZF7TRm3LTPxzE5ib+uDuHSab1xncZD8nctGnaPdwzQIHudTBIxkzy8eG9BNQW8Dy9EFn7HnnKfOuSjjhIu7Y2iYT1n3vE3bGogLBf2Qm+m+gZp5+W5dR2aRWQSX1HGcYxNXbYf7EKXhOuzCMS1a1k30Y7bN1cjtZ/4Rc6ekhk5EWD4WxyJZ28G9DYdX29IOWxJ0kHYb5mQv6Z3mp03+WokPNF95dHcmgjzh0lvzevPxHyFR/1RQgEcJcov',
    'x-s': 'XYW_eyJzaWduU3ZuIjoiNTYiLCJzaWduVHlwZSI6IngyIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6IjM2NjVlNmFjYmI2MzhkMjFkMWRmNTZiYjkyMGM2ZDFjMTRlZmNhYTQxNmM0NDU5ZmU2NTExNmYyNmU0OTgwZjhkMjI2NzM0YTI2NjQwZGEwNTJjY2FhMDc1ZTE1NTkzNTQ2OWJmZTgwY2YzMDAyOTNmZjY2YWM1OTVhZGVhOTMyYzc2NmYzNTllMWMzMjY0ZDljMTgyZTY2OWUxOTUyMTNlNTcxODU1YTI5OTAwMWFhMTYwYjA0N2MyYjUzODVlMGFjZTUxOWIzODRiNDhhZTEyOTg1NGQxZjhhMTMyMDg4MzM2MWUyOTIwMGYzOGZiYjlhZThmYjc5NTY4NzY2YjI5NzU0ZmFlMDMwNDhjNzI1MzU4YzU4YmJlZjMwNmJjMWNlY2ViY2I5YWQ2N2NhN2JkMzQzMDkxYTZiOWYyODc1NmFkMTNjYzdkNmE4NTM4NmYxMGUwOTdmZTk3NjQyMDAzZGU5N2I0ZmZhMzQyOGMyNjYwMDg3NWZhNzlhYmRiMTRhZDQ2NjVlOWQxNGUyOTY1Y2M0N2JhODdhOWM5Y2E3In0=',
    'x-s-common': '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',
    'x-t': '1743387104183',
    'x-xray-traceid': 'caf4fc09db00794173bd53b6a1a72ba7',
    # 'cookie': 'abRequestId=39a73910-2452-5903-a228-10c7a82ba11f; webBuild=4.61.1; xsecappid=xhs-pc-web; a1=195e9f335bdpnvw38ozqmjhjz64wj9txl39g34z6f50000876516; webId=6d0bae642111efe50c0a31b8e6debd61; acw_tc=0ad6fb0417433867857456385e282c059bd0558ea3c7520dd2d75e9bd58b46; gid=yj2djiq40y18yj2djiqq2q4uDfUIhEqYluA6jKiVxVuK4k28EVj9Cq888YWK2yK8YqDDy8Jy; web_session=040069b4f42beba52063d3b0dc354b4c9ac007; unread={%22ub%22:%2267c832e6000000002903815b%22%2C%22ue%22:%2267e75adf000000001c00b5c8%22%2C%22uc%22:33}; loadts=1743386979966; websectiga=7750c37de43b7be9de8ed9ff8ea0e576519e8cd2157322eb972ecb429a7735d4; sec_poison_id=be72e0e0-3b10-40df-833c-64199c1862cd',
}

url = 'https://edith.xiaohongshu.com/api/sns/web/v1/search/notes'
api_endpoint = '/api/sns/web/v1/search/notes'
a1_value = cookies['a1']

for page in range(1, 12):
    search_data['page'] = str(page)
    with open('1.js', 'r', encoding='utf-8') as f:
        js_script = f.read()
        context = execjs.compile(js_script)
        sign = context.call('getXs', api_endpoint, search_data, a1_value)

    GREEN = "\033[1;32;40m  %s  \033[0m"

    headers['x-s'] = sign['X-s']
    headers['x-t'] = str(sign['X-t'])
    headers['X-s-common'] = sign['X-s-common']
    response = requests.post(url, headers=headers,
                             data=json.dumps(search_data, separators=(",", ":"), ensure_ascii=False).encode('utf-8'))
    logger.info(f'{response.json()}')
    if response.status_code == 200:

        data = response.json()
        notes = data.get('data', {}).get('items', [])
        for note in notes:
            try:
                xsec_token = note.get('xsec_token')
                note_id = note.get('id')
                note_url = 'https://www.xiaohongshu.com/explore/' + note_id + '?xsec_token=' + xsec_token + '&xsec_source=pc_feed'
                note_data, status_code_result, headers_result = fetch_xiaohongshu_data(note_id, xsec_token, cookies)
                print(note_data)
                time = note_data['data']['items'][0]['note_card'].get('last_update_time', 'N/A')
                datetime_obj = datetime.utcfromtimestamp(time / 1000)
                last_update_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
                note_type = note_data['data']['items'][0]['note_card'].get('type', 'N/A')
                img_urls = []
                image_urls = [img['url_default'] for img in note_data['data']['items'][0]['note_card']['image_list'] if
                              'url_default' in img]

                output_dir = f"./{img_path}/{note_id}"
                os.makedirs(output_dir, exist_ok=True)

                # 下载并保存图片
                for i, url in enumerate(image_urls):
                    image_path = os.path.join(output_dir, f"image_{i + 1}.jpg")
                    try:
                        response = requests.get(url)
                        response.raise_for_status()
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        print(f"图片已保存: {image_path}")
                    except requests.exceptions.RequestException as e:
                        print(f"图片下载失败 {url}: {e}")
                result = parse_data(note_data)
                display_title = result[0]['标题'].replace("\n", "").strip()
                text = result[0]['内容'].replace("\n", "").strip()
                likes = convert_to_int(result[0]['点赞数'])
                comments = convert_to_int(result[0]['评论数'])
                collects = convert_to_int(result[0]['收藏数'])
                shares = convert_to_int(result[0]['转发数'])
                topics = ", ".join(result[0]['话题']).replace("\n", "").strip()
                data_row = {
                    'note_url': note_url,
                    'last_update_time': last_update_time,
                    'note_id': note_id,
                    'xsec_token': xsec_token,
                    'type': note_type,
                    "title": display_title,
                    "desc": text,
                    "tag_list": topics,
                    "likes": likes,
                    "comments": comments,
                    "collects": collects,
                    "shares": shares
                }
                df = pd.DataFrame([data_row])
                df.to_csv(output_file_path, mode="a", index=False, header=False, encoding="utf-8-sig", quoting=1)
            except:
                pass
    else:
        print('请求过于频繁，请稍后再试')