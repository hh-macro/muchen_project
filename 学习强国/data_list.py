import json

import requests


headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
cookies = {
    "__UID__": "dfe8ac60-c9a1-11ef-8137-d1c277290531",
    "_bl_uid": "npmdw5UmgFaf72110t4kb3y2d7h1",
    "csrf_token": "049703335417876861735888263331",
    "y-open-ua": "TorchApp%252F1.0%2520OSType%252FWindows%2520XueXi%252F2.19.0%2520Device%252Fxxqgpc%2520Windows%252F10(Windows%253Bzh-CN)%2520lang%252Fzh-CN%2520pc.js%252F1732601317231%2520Scene%252Fpc",
    "y-open-did": "14bab5149ae5ec1e2ca7a7ad"
}
url = "https://www.xuexi.cn/lgdata/1novbsbi47k.json"
params = {
    "_st": "28931476",
    "js_v": "1735181049229"
}
response = requests.get(url, headers=headers, cookies=cookies, params=params)
lis = json.loads(response.text)

