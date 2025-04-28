# -- coding: utf-8 --
# @Author: 胡H
# @File: tenxun_ts.py
# @Created: 2025/4/2 9:47
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import subprocess
import os

import json

import requests

cookies = {
    'RK': 'R391v4Z3NZ',
    'ptcz': '974167d978770fd2c4e8e422a8f5c74fc09917999fb5789088c8b405baac66c8',
    '_qimei_uuid42': '1910309122a100898a17759f7df11436c7ae543bf4',
    '_qimei_fingerprint': '75059786da94cf42e0e18205aaec1fcf',
    '_qimei_h38': '2db8fb138a17759f7df1143602000007519103',
    'qq_domain_video_guid_verify': 'f929b6a62256af44',
    'wap_wx_openid': 'o_lAF57bpb_tyz4q1zRtS2lM7Tss',
    'wap_wx_appid': 'wx0b6d22ad9f2c4fa0',
    'logintype': '1',
    'wap_refresh_token': '87_U9M1AcLo5OpQ8YeMXkwlzW_47-UbEoORI_2WWGcwwqYy2MS7pdcvDJGOTKkS1aYSvsIMNjyFZ3Of4-HF6O26_vwPdq_yHkxpvlqBayMxiYg',
    'wap_encrypt_logininfo': 'ASuZHXPxJsxaHE13GyDl4zI7DK0Wc6tnOd7LZ5IZS1lyMFIJ%2B8UggHICyW5i4RdaR7geynKP5S%2BMWKZ4KqGL1y3l3hqeCjxlJPUWcLMeUiiG',
    'backup_logintype': '1',
    'appuser': '93DDC16039BAB5A4',
    'pac_uid': '8QIf3nxc6YAbuD/b7gs=',
    'suid': 'user_8QIf3nxc6YAbuD%2Fb7gs%3D',
    'pgv_pvid': '7331608848',
    '_qimei_q32': '43ef7b49a9df2ec8e0354aaef880171c',
    '_qimei_q36': 'fac37627d6c63d15b44c3c37300012e18312',
    'cm_cookie': 'V1,110064&Da4Rt0K3qezB&AQEBw4hJsGSnlLXIMoTuC79QWg7X7ZW4YY5A&250106&250106',
    'lv_play_index': '58',
    'o_minduid': 'dFdzoQaLlIZIQd2_Gr41gck9Juqf5-ZJ',
    'wap_wx_access_token': '88_lj7Co72M7r-cLM3-44xpMYoVGHi1h8zBDel9uG0-OOLGD_UNj8qzvaT3zNaH9_b2iNJDeKhGQstxjS_GHVGHKK8OuyjJ4OMrDqioCwcemVo',
    'news_token': 'EoABkX8pUr73d4cf7MDxKxlpQ9ZZx4oiqW8Nk9OPtqBiAmUW5sXGfGKlHj2LiN0z9LU-q2awRU0oe2EBiK8Bgq1Bi_JZnzRUp5MG8p-FdcCwF6GQOut_rIhsCDTSgnWMoG4helMq_K-Az6aylKyG7hJRqRUljzLqZKCBy39qMK0mGJogEQ',
    'backup_news_token': 'EoABkX8pUr73d4cf7MDxKxlpQ9ZZx4oiqW8Nk9OPtqBiAmUW5sXGfGKlHj2LiN0z9LU-q2awRU0oe2EBiK8Bgq1Bi_JZnzRUp5MG8p-FdcCwF6GQOut_rIhsCDTSgnWMoG4helMq_K-Az6aylKyG7hJRqRUljzLqZKCBy39qMK0mGJogEQ',
    'ad_session_id': 'zb7atgadpozwk',
    'vversion_name': '8.2.95',
    'video_omgid': 'f929b6a62256af44',
    'pgv_info': 'ssid=s7551652382',
    'LHTturn': '699',
    'LZCturn': '718',
    'LPSJturn': '905',
    'LBSturn': '351',
    'LVINturn': '0',
    'LPHLSturn': '505',
    'LDERturn': '771',
    'LPPBturn': '381',
    'LPDFturn': '528',
    'LZTturn': '885',
    'Lturn': '267',
    'LKBturn': '588',
    'LPVLturn': '374',
    'LPLFturn': '417',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://v.qq.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://v.qq.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'RK=R391v4Z3NZ; ptcz=974167d978770fd2c4e8e422a8f5c74fc09917999fb5789088c8b405baac66c8; _qimei_uuid42=1910309122a100898a17759f7df11436c7ae543bf4; _qimei_fingerprint=75059786da94cf42e0e18205aaec1fcf; _qimei_h38=2db8fb138a17759f7df1143602000007519103; qq_domain_video_guid_verify=f929b6a62256af44; wap_wx_openid=o_lAF57bpb_tyz4q1zRtS2lM7Tss; wap_wx_appid=wx0b6d22ad9f2c4fa0; logintype=1; wap_refresh_token=87_U9M1AcLo5OpQ8YeMXkwlzW_47-UbEoORI_2WWGcwwqYy2MS7pdcvDJGOTKkS1aYSvsIMNjyFZ3Of4-HF6O26_vwPdq_yHkxpvlqBayMxiYg; wap_encrypt_logininfo=ASuZHXPxJsxaHE13GyDl4zI7DK0Wc6tnOd7LZ5IZS1lyMFIJ%2B8UggHICyW5i4RdaR7geynKP5S%2BMWKZ4KqGL1y3l3hqeCjxlJPUWcLMeUiiG; backup_logintype=1; appuser=93DDC16039BAB5A4; pac_uid=8QIf3nxc6YAbuD/b7gs=; suid=user_8QIf3nxc6YAbuD%2Fb7gs%3D; pgv_pvid=7331608848; _qimei_q32=43ef7b49a9df2ec8e0354aaef880171c; _qimei_q36=fac37627d6c63d15b44c3c37300012e18312; cm_cookie=V1,110064&Da4Rt0K3qezB&AQEBw4hJsGSnlLXIMoTuC79QWg7X7ZW4YY5A&250106&250106; lv_play_index=58; o_minduid=dFdzoQaLlIZIQd2_Gr41gck9Juqf5-ZJ; wap_wx_access_token=88_lj7Co72M7r-cLM3-44xpMYoVGHi1h8zBDel9uG0-OOLGD_UNj8qzvaT3zNaH9_b2iNJDeKhGQstxjS_GHVGHKK8OuyjJ4OMrDqioCwcemVo; news_token=EoABkX8pUr73d4cf7MDxKxlpQ9ZZx4oiqW8Nk9OPtqBiAmUW5sXGfGKlHj2LiN0z9LU-q2awRU0oe2EBiK8Bgq1Bi_JZnzRUp5MG8p-FdcCwF6GQOut_rIhsCDTSgnWMoG4helMq_K-Az6aylKyG7hJRqRUljzLqZKCBy39qMK0mGJogEQ; backup_news_token=EoABkX8pUr73d4cf7MDxKxlpQ9ZZx4oiqW8Nk9OPtqBiAmUW5sXGfGKlHj2LiN0z9LU-q2awRU0oe2EBiK8Bgq1Bi_JZnzRUp5MG8p-FdcCwF6GQOut_rIhsCDTSgnWMoG4helMq_K-Az6aylKyG7hJRqRUljzLqZKCBy39qMK0mGJogEQ; ad_session_id=zb7atgadpozwk; vversion_name=8.2.95; video_omgid=f929b6a62256af44; pgv_info=ssid=s7551652382; LHTturn=699; LZCturn=718; LPSJturn=905; LBSturn=351; LVINturn=0; LPHLSturn=505; LDERturn=771; LPPBturn=381; LPDFturn=528; LZTturn=885; Lturn=267; LKBturn=588; LPVLturn=374; LPLFturn=417',
}


data = {
    "buid": "vinfoad",
    "vinfoparam": "charge=0&otype=ojson&defnpayver=3&spau=1&spaudio=0&spwm=1&sphls=2&host=v.qq.com&refer=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2Fmzc00200rb0xufo%2Fn41006ppx9m.html&ehost=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2Fmzc00200rb0xufo%2Fn41006ppx9m.html&sphttps=1&encryptVer=9.2&cKey=56R9kkOGVQ21P81Orq2-LnCjnpb8Ocr0cPTeKABFzEul_f4uOWcvUmJNR8Gi67M9PRtBxhAJ1mrnCp7VHCeQghpmp7rG5tiHjLv_PnnatnPaZfOXktuBpd_Iiuxr75GThl3v-IIK4ccmFjOj-NmZhE-NjjawCzIdF66cdsFdzz5jk70UOmynTHDptaxqIemxrSlkg-M_BbDaBoWwiX7uSsBkDK_qlv9BvC71CgXl1BaviS_Bv-ug12yFwma4zUC404SAHbSb6M9S5S_kpd4TjsUdviqaax_wlIDr5kl4HJQkJ9Pj5oT04Oe6iqyfidIFb9E32fB489WlL76x24VC0-FWl4uoJ6ECbf2_aKBawpvo5ApcICcZxblKemQbyRd7XfE2c-1dav4pxtUstvR_yLntO5Gk9f_a5VTPhdYlg95aiJXEYVCS0MPk4CivvqYWJL7hpnWZd58JFAlk9j3OyhdL9-yJ4VkXSIK5GtX5YoPpb6Thys25BNl-TTrQHCucjUbxtgokNIptPynWbZLSAWbJl80&clip=4&guid=f929b6a62256af44&flowid=9e725ce6edf2ea2bfc10a0714fb8f5d5&platform=10201&sdtfrom=v1010&appVer=1.40.3&unid=&auth_from=&auth_ext=&vid=z4100xrpd6p&defn=hd&fhdswitch=0&dtype=3&spsrt=2&tm=1743572375&lang_code=0&logintoken=%7B%22access_token%22%3A%22%22%2C%22appid%22%3A%22phzJM3GWNjVa%22%2C%22vusession%22%3A%22AvRZuM7ZniZaMNzvYmz8pdOOiek_S7F6m4wXwKmHWW8ry-KZz7HqZ6zH0Aj2Ut3kKA.M%22%2C%22openid%22%3A%22199961645c32546e245e2c17752292be%22%2C%22vuserid%22%3A%223449288184%22%2C%22video_guid%22%3A%22f929b6a62256af44%22%2C%22main_login%22%3A%22phone%22%7D&qimei=fac37627d6c63d15b44c3c37300012e18312&spvvpay=1&spadseg=0&spav1=15&hevclv=28&spsfrhdr=0&spvideo=0&spm3u8tag=67&spmasterm3u8=3&track=null&atime=0&drm=40",
    "adparam": "lt=phone&opid=199961645c32546e245e2c17752292be&appid=phzJM3GWNjVa&atkn=&uid=3449288184&tkn=AvRZuM7ZniZaMNzvYmz8pdOOiek_S7F6m4wXwKmHWW8ry-KZz7HqZ6zH0Aj2Ut3kKA.M"
}
data = json.dumps(data)
response = requests.post('https://vd6.l.qq.com/proxyhttp', cookies=cookies, headers=headers, data=data)
print(response.text)
vi = json.loads(response.text)['vinfo']
vinfo = json.loads(vi)
ui_lis = vinfo['vl']['vi'][0].get('ul', {}).get('ui')
mu8_list = []
for ui in ui_lis:
    mu8_url = ui.get('url')
    mu8_list.append(mu8_url)
print(mu8_list)
