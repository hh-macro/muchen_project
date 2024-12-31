import json
import time

import requests
import concurrent.futures


def png_save(rout_img):
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://stocksnap.io/search/people",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    image_content = requests.get(rout_img, headers=headers).content
    png_name = int(time.time() * 1000000)
    with open(f'人物/{png_name}.jpg', 'wb') as f:
        f.write(image_content)
    print(f'{rout_img}----保存成功')


def imge_page(page, category):
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://stocksnap.io/search/people",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "_hjSessionUser_2571802": "eyJpZCI6ImEyN2FhMzAxLTczNzQtNTBmNS1iYjM5LWZmZDc0Zjc4NWZkMSIsImNyZWF0ZWQiOjE3MzUxMTUwNDg0NzYsImV4aXN0aW5nIjp0cnVlfQ==",
        "_csrf": "3onTb0yUVw-Z6rwhKJoyEnzA",
        "_ga": "GA1.2.614252806.1735176655",
        "_gid": "GA1.2.299514675.1735176655",
        "_hjSession_2571802": "eyJpZCI6IjRjMTJkYzA4LTBhNDctNDgyOS05ZDI1LWY0MDg2NjJmZDBjNCIsImMiOjE3MzUxNzY2NTYwMDksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=",
        "_ga_6DPVJPQMZH": "GS1.2.1735176656.1.1.1735176774.0.0.0"
    }
    url = f"https://stocksnap.io/api/search-photos/{category}/relevance/desc/{page}"
    response = requests.get(url, headers=headers, cookies=cookies)
    json_pg = json.loads(response.text)
    image_jpg_list = json_pg['results']
    # print(image_jpg_list)
    for image_jpg in image_jpg_list:
        img_id = image_jpg['img_id']
        img_url = f'https://cdn.stocksnap.io/img-thumbs/960w/{img_id}.jpg'
        png_save(img_url)


if __name__ == '__main__':
    lei_lis = ['people', 'woman', 'man', 'child', 'baby']
    # imge_page(page=1, category='baby')

    start_time_1 = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        category = 'baby'
        for i in range(1, 300):
            executor.submit(imge_page, i, category)
    print("线程池计算的时间：" + str(time.time() - start_time_1), "秒")
