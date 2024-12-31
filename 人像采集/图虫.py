import json
import time

import requests
import concurrent.futures


def png_save(rout_img):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://stock.tuchong.com/search?page=1&platform=image&relevance_guarantee=false&search_id=7454007702289678619&size=100&sort=0&sortBy=0&source=tc_pc_home_search&term=%E4%BA%BA%E5%83%8F&topic_id=",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    image_content = requests.get(rout_img, headers=headers).content
    png_name = int(time.time() * 1000000)
    with open(f'人物/{png_name}.jpg', 'wb') as f:
        f.write(image_content)
    print(f'{rout_img}----保存成功')


def imge_page(page):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://stock.tuchong.com/search?page=1&platform=image&relevance_guarantee=false&search_id=7454007702289678619&size=100&sort=0&sortBy=0&source=tc_pc_home_search&term=%E4%BA%BA%E5%83%8F&topic_id=",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    cookies = {
        "webp_enabled": "1",
        "lang": "zh",
        "source": "tc_pc_home_search",
        "creative_device_id": "5e7159f7-b183-4558-a614-883ff8bae551",
        "Hm_lvt_f212e14a5ffb8199fd0e64061c054314": "1735487808,1735521422",
        "dialog_show_times": "17",
        "creative_token": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzU1MjY0MzcsInZhbCI6IjJEVjVaNElLWE5GUklZSU1TNTRVTFFPUUc0NFVXRlVOREtLWVkzUERTTVFKNUMzQk5QUUEifQ.gsRP2h2Ee7m0Icc6wdNf1YXLruIwuUqfGhyb5grsUxPoXFh3JZX07GUQRiEZB1go",
        "Hm_lpvt_f212e14a5ffb8199fd0e64061c054314": "1735526445"
    }
    url = "https://stock.tuchong.com/api/search/image"
    params = {
        "enable_rewrite": "true",
        "page": page,
        "platform": "",
        "search_id": "7454007702289678619",
        "size": "100",
        "sort_by": "0",
        "term": "人像"
    }
    proxies = {
        'http': '119.132.69.75:40021',
        'https': '119.132.69.75:40021'

    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    # print(response.text)
    # print(response.status_code)
    json_pg = json.loads(response.text)
    json_pg_list = json_pg['data']['hits']
    for json_pg in json_pg_list:
        image_id = json_pg['image_id']
        image_url = f'https://cdn9-banquan.ituchong.com/weili/image/ml/{image_id}.webp'
        time.sleep(0.3)
        png_save(image_url)


if __name__ == '__main__':
    imge_page(page=1)

    start_time_1 = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        for i in range(1, 150):
            print(f'第{i}页---------------------')
            executor.submit(imge_page, i)
    print("线程池计算的时间：" + str(time.time() - start_time_1), "秒")
