# -- coding: utf-8 --
# @Author: 胡H
# @File: 草稿一.py
# @Created: 2025/3/31 17:46
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import base64

import requests
import execjs

with open('草稿一.js', encoding='utf-8') as f:
    js_code = f.read()
    ctx = execjs.compile(js_code)
    result_data = ctx.call("getResult")

    print("Result:", result_data["result"])
    print("t:", result_data["t"])


cookies = {
    'sessionid': '14o9jrg2ce2aan2zorxx0u8swe4dxvcn',
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1743132214,1743413279',
    'HMACCOUNT': '78DFBE33FB144353',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1743413881',
    's': '51b351b351b351b370b0d030d070d030907051b030',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'm': 'dedededededea0a6a3a2a3a69fa5a7a6a8a09f',
    'origin': 'https://stu.tulingpyton.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://stu.tulingpyton.cn/problem-detail/8/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    't': result_data["t"],
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'sessionid=14o9jrg2ce2aan2zorxx0u8swe4dxvcn; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1743132214,1743413279; HMACCOUNT=78DFBE33FB144353; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1743413881; s=51b351b351b351b370b0d030d070d030907051b030',
}

json_data = {
    'page': 2,
}

response = requests.post('https://stu.tulingpyton.cn/api/problem-detail/8/data/', cookies=cookies, headers=headers, json=json_data)
print(response.status_code)
print(response.text)
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"page":2}'
#response = requests.post('https://stu.tulingpyton.cn/api/problem-detail/8/data/', cookies=cookies, headers=headers, data=data)