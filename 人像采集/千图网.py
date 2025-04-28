import re

import requests


def png_save(rout_img):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.58pic.com/tupian/renxiang.html",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
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
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.58pic.com/tupian/renxiang.html",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    cookies = {
        "qt_visitor_id": "%2253e7a4d2ae7bb6e834fe0d3c018f504a%22",
        "user-browser": "%22baidu%22",
        "did": "%223038ab08ef1f0a3a%22",
        "history_did_data_3038ab08ef1f0a3a": "%22eyJkaXN0aW5jdF9pZCI6IjMwMzhhYjA4ZWYxZjBhM2EiLCJ1dG1fY2FtcGFpZ24iOjAsInV0bV9zb3VyY2UiOjAsInV0bV9tZWRpdW0iOjAsInV0bV90ZXJtIjowLCJ1dG1fY29udGVudCI6MCwidGlkIjowfQ%3D%3D%22",
        "qiantudata2018jssdkcross": "%7B%22distinct_id%22%3A%22193fbe1807a897-00d73561534f31-26011851-1327104-193fbe1807b1507%22%7D",
        "FIRSTVISITED": "1735097680.168",
        "originUrl": "https%3A%2F%2Fwww.58pic.com%2Flogin",
        "history_uid_data_82445718": "%22eyJ1aWQiOjgyNDQ1NzE4LCJkaXN0aW5jdF9pZCI6IjMwMzhhYjA4ZWYxZjBhM2EiLCJ1dG1fY2FtcGFpZ24iOjAsInV0bV9zb3VyY2UiOjAsInV0bV9tZWRpdW0iOjAsInV0bV90ZXJtIjowLCJ1dG1fY29udGVudCI6MCwiZmlyc3RfdHJhZmZpY19zb3VyY2VfdHlwZSI6MCwidGlkIjowfQ%3D%3D%22",
        "auth_id_list": "bNAjBl3EB7aTG34ABg-BrBD1hTx-obs7RjbqxE0eUjHB1V5KmMA6ejxpEb_djQZ4_UAcGoEeybMqUqzoAwxwS38nTqeYhcccCPu7dVGsu1xDq09qmhu1TvQlN11e__lCel-5Z0SDZxi73Q7jHMdZ4_TlZ9PWEfUCULekBQolsGdQpJ5mpeC3pdDLLtfwFkZHLjQukXhZmLiAx9REMd74jNCxdz9IVVVHzHg5oLidzOHxrwKriQ3nGELaSQkH2zWkbp6XD5s79yVeYt6UswQGft1UXM3O2gpXzeIg4obFVeH1JaRAls8Z9LMwqXVECt8tHXPpNmYieKGS7uUaoYfnJzEYdOXQFMJzkPsP9POqOxcL63yp469ou1OamhSPQRnY7rRnz-yhi56WE7VsdA0ax7GN3wlMdsOSQ9AIwp1Ncri9yyfih26rXUPM2KCYP17g7SB9mH1R_xi1BmmBMNIB_jmXYWU4AYPQrp1DUR9tFiFPRvbJ0w_BENQkROo0-UX4kdXU9kfNFEezi6t9AvDVhLyye6zhFl1JPIcDDkm-p5CyMN0OxRMX05QBqoULYXKm6hpzXXyvTHMpM0rZvn1NMY65_ndcMA3-7a5cHdkXeR5-M7KtwMXQ1FR4VQp1UHhc",
        "success_target_path": "%22https%3A%5C%2F%5C%2Fwww.58pic.com%5C%2Flogin%22",
        "sns": "%7B%22token%22%3A%7B%22access_token%22%3A%225C21858BF5CEE7C87AD21DD1ED1ABF41%22%2C%22expires_in%22%3A%22604800%22%2C%22refresh_token%22%3A%221255B22DF4458132F324EFD7E2F5203F%22%2C%22openid%22%3A%226AF62A15B5742F46B10AFE761C13838C%22%7D%2C%22type%22%3A%22qq%22%7D",
        "ssid": "%22676ba31cc6ac10.66572387%22",
        "last_login_type": "1",
        "qt_risk_visitor_id": "%228a2dd11f12b70396779180a86f7bce55%22",
        "newbieTask": "%22%7B%5C%22is_login%5C%22%3A1%2C%5C%22is_search%5C%22%3A0%2C%5C%22is_download%5C%22%3A0%2C%5C%22is_keep%5C%22%3A0%2C%5C%22login_count%5C%22%3A1%2C%5C%22upload_material%5C%22%3A0%2C%5C%22is_task_complete%5C%22%3A0%2C%5C%22task1%5C%22%3A0%2C%5C%22task2%5C%22%3A0%2C%5C%22task3%5C%22%3A0%7D%22",
        "_is_pay": "0",
        "auth_id_v2": "wAqq2D254eAxLFTjBcrgal7JQzoVbamLzPF6huoxHYPo5a7pU93c1VrGJ1WvtzxwKJX8ZAx6crMx04FQyKieU-T0-TZh5F-fSInAoV_sPekYklh_i94iYzi1oAnlrd1Ztn0KwwyRgo_7S8C7nH2VsNkbd2-ik3IXq_figDdlFnDnFooyU6kX_gZ8uicKTIf4NKoHkulcDTuCRXIdPho5uYpPH_-7QSJqhhg4PCKEFxhGcFYXJEzKXBKIBSIXPMANp8-uiE5KFMgnByuFD5MBLS34Aqk-1KwVygYrEhwTJE552OguzwR-Gu28iDC_dKnE",
        "auth_id": "%2282445718%7C5Y2D5Zu%2B55So5oi3XzU3MTg%3D%7C1736316967%7C489defa635171cb56b44fbcd75b8d566%22",
        "login_status": "1",
        "qt_uid": "%2282445718%22",
        "ISREQUEST": "1",
        "WEBPARAMS": "is_pay=0",
        "favorites:author:v1:82445718": "0",
        "qt_ur_type": "2",
        "qt_type": "2",
        "is_show_login": "1",
        "sem:party:day:": "1228487",
        "sem_tid": "1228487",
        "sem_tid_expire": "1735184589",
        "sem_roi": "1",
        "tid_today_data_3038ab08ef1f0a3a_20241226": "%22eyJ0b2RheV90aWQiOiIxMjI4NDg3IiwidG9kYXlfdXRtX3NvdXJjZSI6ImJhaWR1MiIsInRvZGF5X3V0bV9tZWRpdW0iOiJjcGMiLCJ0b2RheV91dG1fdGVybSI6IiVDNyVBNyVDRCVCQyVDRCVGOCIsInRvZGF5X3V0bV9jYW1wYWlnbiI6IiVDNiVCNyVDNSVDNiVCNCVDQSglRDAlQzIpIiwidG9kYXlfdXRtX2NvbnRlbnQiOiIlQzclQTclQ0QlQkMifQ%3D%3D%22",
        "Hm_lvt_41d92aaaf21b7b22785ea85eb88e7cea": "1735097680,1735184590",
        "HMACCOUNT": "1B24FA033D89266E",
        "Hm_lvt_644763986e48f2374d9118a9ae189e14": "1735097680,1735184591",
        "_clck": "1ig1q77%7C2%7Cfs1%7C0%7C1820",
        "search_risk": "%22MjAyNDEyMjY%3D%22",
        "Hm_lpvt_41d92aaaf21b7b22785ea85eb88e7cea": "1735184620",
        "Hm_lpvt_644763986e48f2374d9118a9ae189e14": "1735184621",
        "searchParam": "%227198_3%22",
        "_clsk": "q3isda%7C1735192376839%7C1%7C0%7Co.clarity.ms%2Fcollect",
        "public_property": "%22eyJ1aWQiOiI4MjQ0NTcxOCIsImxpYiI6InBocCIsImxpYl92ZXJzaW9uIjoiMS4wIiwiZXF1aXAiOjEsImRpc3RpbmN0X2lkIjoiMzAzOGFiMDhlZjFmMGEzYSIsImV2ZW50X25hbWUiOiIiLCJzZXJ2ZXJfYWdlbnQiOiJNb3ppbGxhXC81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXRcLzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZVwvMTMxLjAuMC4wIFNhZmFyaVwvNTM3LjM2IiwidXJsIjoiaHR0cDpcL1wvd3d3LjU4cGljLmNvbVwvdHVwaWFuXC9yZW54aWFuZy5odG1sIiwidGltZSI6MTczNTE5MjM3NiwiY2xpZW50X2lwIjoiMTEzLjI0OC4yNTQuMTcwIiwib3MiOiJXaW5kb3dzIDEwIiwiYnJvd3NlciI6IkNocm9tZSIsImJyb3dzZXJfdmVyc2lvbiI6IjEzMS4wLjAuMCIsInJlZmVycmVyIjoiaHR0cHM6XC9cL3d3dy41OHBpYy5jb21cLz90aWQ9MTIyODQ4NyZ1dG1fc291cmNlPWJhaWR1MiZ1dG1fbWVkaXVtPWNwYyZ1dG1fY2FtcGFpZ249JUM2JUI3JUM1JUM2JUI0JUNBKCVEMCVDMikmdXRtX2NvbnRlbnQ9JUM3JUE3JUNEJUJDJnV0bV90ZXJtPSVDNyVBNyVDRCVCQyVDRCVGOCZzZGNsa2lkPUFMMnMxNWZHeHJENmJMLXBBTGVfIiwibGF0ZXN0X3RyYWZmaWNfc291cmNlX3R5cGUiOm51bGwsImxhdGVzdF9yZWZlcnJlciI6bnVsbCwibGF0ZXN0X3JlZmVycmVyX2hvc3QiOm51bGwsImxhdGVzdF9zZWFyY2hfa2V5d29yZCI6bnVsbCwibGF0ZXN0X3V0bV9tZWRpdW0iOm51bGwsImxhdGVzdF91dG1fY2FtcGFpZ24iOm51bGwsImxhdGVzdF91dG1fdGVybSI6bnVsbCwibGF0ZXN0X3V0bV9zb3VyY2UiOm51bGwsImxhdGVzdF90aWQiOm51bGwsImxhdGVzdF91dG1fY29udGVudCI6bnVsbCwicXlfaWQiOjAsInVzZXJfc3RhdHVzIjoxLCJ0b2RheV90aWQiOiIxMjI4NDg3IiwidG9kYXlfdXRtX3NvdXJjZSI6ImJhaWR1MiIsInRvZGF5X3V0bV9tZWRpdW0iOiJjcGMiLCJ0b2RheV91dG1fdGVybSI6IiVDNyVBNyVDRCVCQyVDRCVGOCIsInRvZGF5X3V0bV9jb250ZW50IjoiJUM3JUE3JUNEJUJDIiwidG9kYXlfdXRtX2NhbXBhaWduIjoiJUM2JUI3JUM1JUM2JUI0JUNBKCVEMCVDMikiLCJ0aWQiOjAsInV0bV9zb3VyY2UiOjAsInV0bV9tZWRpdW0iOjAsInV0bV9jYW1wYWlnbiI6MCwidXRtX2NvbnRlbnQiOjAsInV0bV90ZXJtIjowfQ%3D%3D%22",
        "qt_utime": "1735192564",
        "big_data_visit_time": "1735192564"
    }
    url = f"https://www.58pic.com/tupian/renxiang-0-0-{page}.html"
    response = requests.get(url, headers=headers, cookies=cookies)
    # print(response.text)
    image_ur_list = re.findall('<img class="lazy"a_data-original="(.*?)"src=""alt="', response.text)
    # print(image_ur_list)
    for image_ur in image_ur_list:
        image_url = 'https:' + image_ur
        # print(image_url)
        cut_url = image_url.split('.jpg', 1)[0] + '.jpg'
        new_url = cut_url + "!w1024_webp"
        png_save(new_url)


if __name__ == '__main__':
    imge_page(page=1)
