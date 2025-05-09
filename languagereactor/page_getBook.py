# -- coding: utf-8 --
# @Author: 胡H
# @File: page_getBook.py
# @Created: 2025/5/9 11:05
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.languagereactor.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.languagereactor.com/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

json_data = {
    'diocoDocId': 'gb_20203',
    'pageNum': 0,
    'auth': None,
}

response = requests.post('https://api-cdn.dioco.io/base_media_getBookPageNLP_5', headers=headers, json=json_data)

print(response.json())