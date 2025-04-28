import json

import requests


def memory_size(headers, cookies):
    params = {
        'pr': 'ucpro',
        'fr': 'pc',
        'uc_param_str': '',
        'fetch_subscribe': 'true',
        '_ch': 'home',
        'fetch_identity': 'true',
    }

    response = requests.get('https://drive-pc.quark.cn/1/clouddrive/member', params=params, cookies=cookies,
                            headers=headers)
    member_josn_data = json.loads(response.text).get('data', {})
    use_capacity = member_josn_data.get('use_capacity', 0)
    total_capacity = member_josn_data.get('total_capacity', 0)

    use_capacity = use_capacity / (1024 * 1024 * 1024)
    total_capacity = total_capacity / (1024 * 1024 * 1024)
    # 打印结果，保留两位小数
    print(f"已用容量: {use_capacity:.5f} GB")
    print(f"总容量: {total_capacity:.5f} GB")

    return {'use_capacity': use_capacity, 'total_capacity': total_capacity}


cookies = {
    'b-user-id': 'fbda1854-6aa6-0573-94d5-0122333c83ef',
    '_UP_A4A_11_': 'wb9c616100f44a539f7f79d8bda1380e',
    'isg': 'BCgon5lT22ZC0_fiyrd-ijGQ-RY6UYxbHADNOuJb66OWPcynimQk63A0MdXNVUQz',
    '_UP_D_': 'pc',
    '_UP_335_2B_': '1',
    '_UP_30C_6A_': 'st9c762011ahubqz815t55amgp1nllz0',
    '_UP_TS_': 'sg16b3c1d1b7c59e5231db68dd678981082',
    '_UP_E37_B7_': 'sg16b3c1d1b7c59e5231db68dd678981082',
    '_UP_TG_': 'st9c762011ahubqz815t55amgp1nllz0',
    '__kps': 'AAQFXbG5oNDoc8x80trxOb3s',
    '__ktd': 'JwYo/oEqHLUoE96xA8h44g==',
    '__uid': 'AAQFXbG5oNDoc8x80trxOb3s',
    'tfstk': 'grPmpE4uG-kfJtqpDulfpn64VaX-hEGsxldtXfnNU0oWHmhT7fRaXPhxQiaTqcqT5mPxkm3ajunS6mFYHRYbZkA9Mi6b7Cct_MId96UbkfGNvsr6qNtjW2uN6AlazjgTBlg2h6UblUy7vfDG9hj0w_qqblkqU3us4hlZQK7o4V0BQnrZ_aboSquZbIkqa4uiufoabf7uz0giHR6qc5Pzag8tna14vNFmoxmUumzYf77tdKZmqCRaZfHmY1mk_CPolzCmj0AhBDyIDvH74_dmszugD0EFTQcrKJatSofDgjezFSGYwMYInlmxL7DlLUcg3o2Zd8fBdxkim8PqEFRaPbyrLRqcmKi4HuDIzY8GO4EK4rN4ENtzuknmg4kRTw4rQ8FjdSIyiXyQkjeaf9pSiPyqZg5MUpWylCgPW7v6CxuSrD3pIrOVc8YtGabkLNMqPqidrav6CxuSrDQlrp5s34gjv',
    '__pus': '739b0bb5741659158524c91abcbf80a5AASdnBinUzarFJiJQDrWxrfFVVQ6qHOJ0EXWKAak6ucvBGeUbaOSSQUvjp3UocmvFzTyfCJ12kDWNingoPHuq4Ua',
    '__kp': '1be5e4d0-0ec6-11f0-902f-3bf93188e424',
    '__puus': '759f54495e2f09bb9b121a32916f6799AATnwSSQOPuUSr6HYaxmu+b/DcViKYSbvZfO1QuliP/w81l9sQY9n3hgqT/te164JtTt819tn3lRxu89tl9BbbZFVvEN+h3yD6Q1SQCD2/8V602qku+nmCaHTV0BJwp6iAkxGqXmSQm9zrYImtWqK3DaYHL7iOnkns5HjmlKQnFQa0ozsF8ThcCuzPhlncyKbhVtcJGW+NXwLdTGFPCGB7vs',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'origin': 'https://pan.quark.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://pan.quark.cn/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'b-user-id=fbda1854-6aa6-0573-94d5-0122333c83ef; _UP_A4A_11_=wb9c616100f44a539f7f79d8bda1380e; isg=BCgon5lT22ZC0_fiyrd-ijGQ-RY6UYxbHADNOuJb66OWPcynimQk63A0MdXNVUQz; _UP_D_=pc; _UP_335_2B_=1; _UP_30C_6A_=st9c762011ahubqz815t55amgp1nllz0; _UP_TS_=sg16b3c1d1b7c59e5231db68dd678981082; _UP_E37_B7_=sg16b3c1d1b7c59e5231db68dd678981082; _UP_TG_=st9c762011ahubqz815t55amgp1nllz0; __kps=AAQFXbG5oNDoc8x80trxOb3s; __ktd=JwYo/oEqHLUoE96xA8h44g==; __uid=AAQFXbG5oNDoc8x80trxOb3s; tfstk=grPmpE4uG-kfJtqpDulfpn64VaX-hEGsxldtXfnNU0oWHmhT7fRaXPhxQiaTqcqT5mPxkm3ajunS6mFYHRYbZkA9Mi6b7Cct_MId96UbkfGNvsr6qNtjW2uN6AlazjgTBlg2h6UblUy7vfDG9hj0w_qqblkqU3us4hlZQK7o4V0BQnrZ_aboSquZbIkqa4uiufoabf7uz0giHR6qc5Pzag8tna14vNFmoxmUumzYf77tdKZmqCRaZfHmY1mk_CPolzCmj0AhBDyIDvH74_dmszugD0EFTQcrKJatSofDgjezFSGYwMYInlmxL7DlLUcg3o2Zd8fBdxkim8PqEFRaPbyrLRqcmKi4HuDIzY8GO4EK4rN4ENtzuknmg4kRTw4rQ8FjdSIyiXyQkjeaf9pSiPyqZg5MUpWylCgPW7v6CxuSrD3pIrOVc8YtGabkLNMqPqidrav6CxuSrDQlrp5s34gjv; __pus=739b0bb5741659158524c91abcbf80a5AASdnBinUzarFJiJQDrWxrfFVVQ6qHOJ0EXWKAak6ucvBGeUbaOSSQUvjp3UocmvFzTyfCJ12kDWNingoPHuq4Ua; __kp=1be5e4d0-0ec6-11f0-902f-3bf93188e424; __puus=759f54495e2f09bb9b121a32916f6799AATnwSSQOPuUSr6HYaxmu+b/DcViKYSbvZfO1QuliP/w81l9sQY9n3hgqT/te164JtTt819tn3lRxu89tl9BbbZFVvEN+h3yD6Q1SQCD2/8V602qku+nmCaHTV0BJwp6iAkxGqXmSQm9zrYImtWqK3DaYHL7iOnkns5HjmlKQnFQa0ozsF8ThcCuzPhlncyKbhVtcJGW+NXwLdTGFPCGB7vs',
}

print(memory_size(headers, cookies))
