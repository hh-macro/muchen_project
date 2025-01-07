import requests


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://www.xuexi.cn/",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "__UID__": "dfe8ac60-c9a1-11ef-8137-d1c277290531",
    "csrf_token": "049703335417876861735888263331",
    "y-open-ua": "TorchApp%252F1.0%2520OSType%252FWindows%2520XueXi%252F2.19.0%2520Device%252Fxxqgpc%2520Windows%252F10(Windows%253Bzh-CN)%2520lang%252Fzh-CN%2520pc.js%252F1732601317231%2520Scene%252Fpc",
    "y-open-did": "14bab5149ae5ec1e2ca7a7ad"
}
url = "https://boot-source.xuexi.cn/data/app/14829498764170892529.js"
params = {
    "callback": "callback",
    "_st": "1735888627034"
}
response = requests.get(url, headers=headers, cookies=cookies, params=params)

print(response.text)
print(response)