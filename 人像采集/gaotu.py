import re
import time

import requests
import json
import concurrent.futures


def png_save(rout_img):
    image_content = requests.get(rout_img).content
    png_name = int(time.time() * 1000000)
    with open(f'人物/{png_name}.jpg', 'wb') as f:
        f.write(image_content)
    print(f'{rout_img}----保存成功')


def imge_page(page):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://gaoimg.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://gaoimg.com/?s=%E4%BA%BA%E7%89%A9&post_type=item",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    cookies = {
        "wordpress_sec_064724d75af14744414a7b51ab4fcfbd": "WB_97215029438921BCB292370A4505C277%7C1736307346%7CSN9W3LsoIsgb5nIJGNiXDUlhxg2eoilEwkPHPioPMgw%7C67386b4007eed8c88360fe162ca90c61e23e4d758184c38f944f11c67d70236b",
        "wordpress_test_cookie": "WP%20Cookie%20check",
        "Hm_lvt_3f8e828cd325c7ba4659472bcf3795af": "1735097724",
        "Hm_lpvt_3f8e828cd325c7ba4659472bcf3795af": "1735097724",
        "HMACCOUNT": "1B24FA033D89266E",
        "PHPSESSID": "10l8bme9tqm0ef3hp4hgoa3k0l",
        "wordpress_logged_in_064724d75af14744414a7b51ab4fcfbd": "WB_97215029438921BCB292370A4505C277%7C1736307346%7CSN9W3LsoIsgb5nIJGNiXDUlhxg2eoilEwkPHPioPMgw%7Ccd72e14aea9fb092b2cc5e9ab00b9331d9bff8aa82d9f8d2533e62dfdcaa76a7"
    }
    url = "https://gaoimg.com/wp-admin/admin-ajax.php"
    data = {
        "action": "wb_lazy_load",
        "do": "the_posts",
        "col": "1",
        "cnf": "{\"s\":\"\\u4eba\\u7269\",\"location\":\"spc\"}",
        "paged": page
    }
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    json_pg = json.loads(response.text)
    image_jpg_list = json_pg['data'][1:]
    # print(len(image_jpg_list))
    # print(image_jpg_list)
    for image_jpg in image_jpg_list:
        # print(image_jpg)
        rout_img = re.findall('<a_tool class="act-btn" href="(.*?)" target=', image_jpg)[0]
        png_save(rout_img)


if __name__ == '__main__':

    start_time_1 = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        for i in range(1, 50):
            executor.submit(imge_page, i)
    print("线程池计算的时间：" + str(time.time() - start_time_1), "秒")
