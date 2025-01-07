import re
import time
import concurrent.futures

import requests
from parsel import Selector

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://pxhere.com/zh/photos?q=%E4%BA%BA&search=",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"131.0.6778.205\"",
    "sec-ch-ua-full-version-list": "\"Google Chrome\";v=\"131.0.6778.205\", \"Chromium\";v=\"131.0.6778.205\", \"Not_A Brand\";v=\"24.0.0.0\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"15.0.0\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
cookies = {
    "PHPSESSID": "s5upg4puufco2brmqq36nitf36",
    "FCNEC": "%5B%5B%22AKsRol9uOkN5EdE64dR_HjFI6iR0QWvuMAXqAZdOffblUzmy1S3XiOx34qu4MtCkKbN_8gANES9hdcT7zCT8qHwWz3b0oWGS16y7_4MFBOhRGxLPiDJ_BaIAhd0V6tla54ic5BR643EgNiGXPAVRNs501DE-51wyfA%3D%3D%22%5D%5D",
    "__gads": "ID=db957673969089fe:T=1735199906:RT=1735271106:S=ALNI_MYUjV6A_SRkXfhVS8d6JBK2RMWbJQ",
    "__gpi": "UID=00000fb90a9474db:T=1735199906:RT=1735271106:S=ALNI_Map658Cb2vGQofjiYbmMkLPyRnxBw",
    "__eoi": "ID=0f9ad230fcb0c433:T=1735199906:RT=1735271106:S=AA-AfjYKVrmxRUOaj7xVyZy9HLLp",
    "cf_clearance": "1EMJJT7.WzEVRbHHY_lvvzF1dDP.PDd9qLvHb7Ahfyk-1735277313-1.2.1.1-ZhiND8SjMJXMhSfhzxA7LD0.S.iU1HwHd0rptsRIPOqx2HrzswJG8il2sAeOFihwpZVGmjRXFc7s05y6N9qNoPJxUSBKAK0yBoBAmUWaDmkBPIVeLbUWPYjDXnbmLPADR3.hUgkCGGVY3zAnGmb8EKqMadQlRE88JA1rhXYLTQ0_YNtTIqme0nF4M5Yr0epGI9kUqyKVpPY0lUotLWCszC7wmGOZ_tloY7xpRufh1Jid1LOKwia7iUJt6lBDchH6zOrTkXym_eLNctK.NQD1raAcDfCMiE86_pDnIdWCiI0r.Fyh54D_J8H.duYBwVPoyt3OSuJerWOmRaEkGvnUTRp0n_uIShdRJtFNGymYsk97koveFBg3GA_QX7oPVNXTSCG76w5JBKOcRKjx9kU8ZP6GXJJE.6RLqqHzxSjANLDINVXO4cQ67konKYSA8OOe"
}

session = requests.Session()


def page_data(link):
    response = session.get(link, headers=headers, cookies=cookies)
    url_data = re.findall('<a_tool href="(.*?)" class="current-page-photo"', response.text)[0]
    time.sleep(0.3)
    png_save(url_data)


def png_save(rout_img):
    image_content = requests.get(rout_img).content
    time.sleep(0.3)
    png_name = int(time.time() * 1000000)
    with open(f'{png_name}.jpg', 'wb') as f:
        f.write(image_content)
    print(f'{rout_img}----保存成功')


def imge_page(i):
    time.sleep(0.3)
    params = {
        "q": "人",
        "search": "",
        "page": i,
        "format": "json"
    }
    url = "https://pxhere.com/zh/photos"
    response2 = session.get(url, headers=headers, cookies=cookies, params=params)
    print(response2.status_code)
    content_str = response2.json()['data']
    box_href_list = re.findall(' <a_tool href=\"(.*?)\" class=\"current-item-photo\">', content_str)
    for idx, box_href in enumerate(box_href_list):
        link = 'https://pxhere.com' + box_href
        page_data(link)


if __name__ == '__main__':

    start_time_1 = time.time()
    for i in range(1, 2):
        imge_page(i)
    print("线程池计算的时间：" + str(time.time() - start_time_1), "秒")
