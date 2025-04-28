import json
import time
import concurrent.futures

import requests


def png_save(rout_img):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "authorization;": "",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.pexels.com/zh-cn/search/%E4%BA%BA%E7%89%A9/",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "secret-key": "H2jk9uKnhRmL6WPwh89zBezWvr",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-client-type": "react",
        "x-forwarded-cf-connecting-ip;": "",
        "x-forwarded-cf-ipregioncode;": "",
        "x-forwarded-http_cf_ipcountry;": ""
    }
    image_content = requests.get(rout_img, headers=headers).content
    png_name = int(time.time() * 1000000)
    with open(f'人物/{png_name}.jpg', 'wb') as f:
        f.write(image_content)
    print(f'{rout_img}----保存成功')


def imge_page(page):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "authorization;": "",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.pexels.com/zh-cn/search/%E4%BA%BA%E7%89%A9/",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "secret-key": "H2jk9uKnhRmL6WPwh89zBezWvr",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-client-type": "react",
        "x-forwarded-cf-connecting-ip;": "",
        "x-forwarded-cf-ipregioncode;": "",
        "x-forwarded-http_cf_ipcountry;": ""
    }
    cookies = {
        "_ga": "GA1.1.682930128.1735097201",
        "_cfuvid": "JMo9yCb8.ZMM8i0vXUCMiiFS4.w_3gxlKOsAAlxmf30-1735104607695-0.0.1.1-604800000",
        "__cf_bm": "MSmxKqlyaRZcU5tpvqdzOk9pjs2aBI3ctrYGeujlTQI-1735105733-1.0.1.1-QpdnhpJZc78txVmLWnyAudEKaBnVwLtX2z8Iifq2q0GG_Rtm4GSo4mAxhukmYTEh9XQBqPsnOK8IiQ5fkWPFhg",
        "country-code-v2": "CN",
        "_sp_ses.9ec1": "*",
        "cf_clearance": "dAk0FH3Y2mQGQ46cun9asqRiXLP1j9ubQl0POWfv7Ps-1735105752-1.2.1.1-yjdEYbVe42UHxD.MSWhATlaklvuwU4lO7E48LTS7hntPMtpk6.vhk3b_ToWEdrLAdyz8.Q8X8kWipiHS8gGHH.3w6UpwN1WEucA.fRykmhct8dYArmAF_5OYRCsCawH2xBLZU2FNAKJZsxyo7NYRKc_S4Na0zXw6zPvP9263mIUqVsIzqQPNkEkOWduvQU1pCZqdN9JrwKd2q.sV5JR84Hfsz9BBWb0F17.FZh.uxwTX8qHmV2kd79u77g48kq8I0fQx_EG6YKyaR7JgMQ6heBqDp2jYA885MvXmHC_SnnQfqWy1hb0ezptsw5tlTy5gK7e5GZaGtGzytzkwR3lBASEUlL0ZqBPysMleK_LNFYTwLk.FE05cmiVzZH.mbqdk",
        "_sp_id.9ec1": "1362b4b8-ff3d-4022-ae1d-d77706621e20.1735097188.2.1735105754.1735097454.9d9a7d65-e903-46ca-99ad-bf2ab23ee3a0.9d606a14-a8d9-4a40-91bf-9579ef64ec6a.1dc562b3-223e-4199-9df9-7be3cb7da248.1735105746106.6",
        "OptanonAlertBoxClosed": "2024-12-25T05:49:17.136Z",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+Dec+25+2024+13%3A49%3A17+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202301.1.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=CN%3BCQ&AwaitingReconsent=false",
        "_ga_8JE65Q40S6": "GS1.1.1735105725.2.1.1735105770.0.0.0"
    }
    url = "https://www.pexels.com/zh-cn/api/v3/search/photos"
    params = {
        "query": "人像",
        "page": page,
        "per_page": "24",
        "orientation": "all",
        "size": "all",
        "color": "all",
        "sort": "popular",
        "seo_tags": "true"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    json_pg = json.loads(response.text)
    image_jpg_list = json_pg['a_data']
    for image_jpg in image_jpg_list:
        rout_img = image_jpg['attributes']['user']['avatar']['medium']
        rout_img = rout_img.replace('h=256', 'h=3840').replace('w=256', 'w=3840')
        png_save(rout_img)


if __name__ == '__main__':

    start_time_1 = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        for i in range(1, 300):
            executor.submit(imge_page, i)
    print("线程池计算的时间：" + str(time.time() - start_time_1), "秒")
