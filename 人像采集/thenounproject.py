import time

import requests
import json
import concurrent.futures


def png_save(rout_img):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://thenounproject.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://thenounproject.com/search/photos/?q=people&page=2",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    image_content = requests.get(rout_img, headers=headers).content
    import time
    png_name = int(time.time() * 1000000)
    with open(f'人物/{png_name}.jpg', 'wb') as f:
        f.write(image_content)
    print(f'{rout_img}----保存成功')


def imge_page(page):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://thenounproject.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://thenounproject.com/search/photos/?q=people&page=2",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    cookies = {
        "csrftoken": "po30iDMN9U8EeBwOTmXAzjGlokJTXtNC",
        "_ga": "GA1.1.1954111196.1735179514",
        "_hjSession_5004138": "eyJpZCI6ImVjNzFmMzg0LWNiZjAtNDNiNy05MTA5LWI4ZTM3OTVhNDdiYSIsImMiOjE3MzUxNzk1NDA5MDIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=",
        "_hjSessionUser_5004138": "eyJpZCI6IjAwZTU4YzE3LTYwNGQtNTllYi05NWYxLTM2YmRjODYwNjc3NSIsImNyZWF0ZWQiOjE3MzUxNzk1NDA5MDEsImV4aXN0aW5nIjp0cnVlfQ==",
        "cookie_consent": "%7B%22dateOfConsent%22%3A1735179564330%2C%22functionality%22%3Atrue%2C%22analytics%22%3Atrue%2C%22advertising%22%3Atrue%7D",
        "_ga_TEXVFE05D4": "GS1.1.1735179513.1.1.1735179718.53.0.0"
    }
    url = "https://thenounproject.com/graphql/"
    data = {
        "operationName": "photoSearch",
        "variables": {
            "query": "people",
            "offset": page,
            "limit": 50
        },
        "query": "query photoSearch($query: String!, $creator: String, $limit: Int, $offset: Int) {\n  photoSearch(query: $query, creator: $creator, limit: $limit, offset: $offset) {\n    totalCount\n    items {\n      id\n      slugWithId\n      title\n      isPremium\n      assets {\n        thumbnailSmall\n        thumbnailMedium\n        __typename\n      }\n      ratio\n      tags {\n        name\n        slug\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    json_pg = json.loads(response.text)
    image_jpg_list = json_pg['a_data']['photoSearch']['items']
    for image_jpg in image_jpg_list:
        img_id = image_jpg['assets']['thumbnailMedium']
        png_save(img_id)


if __name__ == '__main__':
    start_time_1 = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        for i in range(50, 10000, 50):
            executor.submit(imge_page, i)
    print("线程池计算的时间：" + str(time.time() - start_time_1), "秒")
