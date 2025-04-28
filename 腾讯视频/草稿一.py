import json
import re

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
    'pgv_info': 'ssid=s296051362',
    'LPVLturn': '445',
    'LPLFturn': '441',
    'LPSJturn': '976',
    'LVINturn': '71',
    'LPHLSturn': '536',
    'LDERturn': '843',
    'LPPBturn': '400',
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
    # 'cookie': 'RK=R391v4Z3NZ; ptcz=974167d978770fd2c4e8e422a8f5c74fc09917999fb5789088c8b405baac66c8; _qimei_uuid42=1910309122a100898a17759f7df11436c7ae543bf4; _qimei_fingerprint=75059786da94cf42e0e18205aaec1fcf; _qimei_h38=2db8fb138a17759f7df1143602000007519103; qq_domain_video_guid_verify=f929b6a62256af44; wap_wx_openid=o_lAF57bpb_tyz4q1zRtS2lM7Tss; wap_wx_appid=wx0b6d22ad9f2c4fa0; logintype=1; wap_refresh_token=87_U9M1AcLo5OpQ8YeMXkwlzW_47-UbEoORI_2WWGcwwqYy2MS7pdcvDJGOTKkS1aYSvsIMNjyFZ3Of4-HF6O26_vwPdq_yHkxpvlqBayMxiYg; wap_encrypt_logininfo=ASuZHXPxJsxaHE13GyDl4zI7DK0Wc6tnOd7LZ5IZS1lyMFIJ%2B8UggHICyW5i4RdaR7geynKP5S%2BMWKZ4KqGL1y3l3hqeCjxlJPUWcLMeUiiG; backup_logintype=1; appuser=93DDC16039BAB5A4; pac_uid=8QIf3nxc6YAbuD/b7gs=; suid=user_8QIf3nxc6YAbuD%2Fb7gs%3D; pgv_pvid=7331608848; _qimei_q32=43ef7b49a9df2ec8e0354aaef880171c; _qimei_q36=fac37627d6c63d15b44c3c37300012e18312; cm_cookie=V1,110064&Da4Rt0K3qezB&AQEBw4hJsGSnlLXIMoTuC79QWg7X7ZW4YY5A&250106&250106; lv_play_index=58; o_minduid=dFdzoQaLlIZIQd2_Gr41gck9Juqf5-ZJ; wap_wx_access_token=88_lj7Co72M7r-cLM3-44xpMYoVGHi1h8zBDel9uG0-OOLGD_UNj8qzvaT3zNaH9_b2iNJDeKhGQstxjS_GHVGHKK8OuyjJ4OMrDqioCwcemVo; news_token=EoABkX8pUr73d4cf7MDxKxlpQ9ZZx4oiqW8Nk9OPtqBiAmUW5sXGfGKlHj2LiN0z9LU-q2awRU0oe2EBiK8Bgq1Bi_JZnzRUp5MG8p-FdcCwF6GQOut_rIhsCDTSgnWMoG4helMq_K-Az6aylKyG7hJRqRUljzLqZKCBy39qMK0mGJogEQ; backup_news_token=EoABkX8pUr73d4cf7MDxKxlpQ9ZZx4oiqW8Nk9OPtqBiAmUW5sXGfGKlHj2LiN0z9LU-q2awRU0oe2EBiK8Bgq1Bi_JZnzRUp5MG8p-FdcCwF6GQOut_rIhsCDTSgnWMoG4helMq_K-Az6aylKyG7hJRqRUljzLqZKCBy39qMK0mGJogEQ; ad_session_id=zb7atgadpozwk; vversion_name=8.2.95; video_omgid=f929b6a62256af44; pgv_info=ssid=s296051362; LPVLturn=445; LPLFturn=441; LPSJturn=976; LVINturn=71; LPHLSturn=536; LDERturn=843; LPPBturn=400',
}

data = '{"buid":"vinfoad","vinfoparam":"charge=0&otype=ojson&defnpayver=3&spau=1&spaudio=0&spwm=1&sphls=2&host=v.qq.com&refer=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2Fd968qjcaw9pdld0%2Fo001470awrf.html&ehost=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2Fd968qjcaw9pdld0%2Fo001470awrf.html&sphttps=1&encryptVer=9.2&cKey=EHoOYbRYJv61EM1Orq2-LnCjnpb8Ocr0cPTeK6GKzEul_f4uOWcvUmJNR8G377I8OVQD1wNNwGoKCp7VHCeQghpmp7rG5tiHjLv_PnnatnPaZfrUx9PA-YzZj7cr84iR2V3u_IML5cZmFjOj-NmZhE-NjjawCzIdF66cdsFdzz5jk70UOmynTHDptaxqIemxrSlkg-M_BbDaBoWksGXkUJYnQqXKgvocvCDoQBra3Bby3kOuy43cimXGmTO2ml3AhMLGSLSNuYcFi3m5pvAjoPAdvjeBPEfwmNLx9gg9S9d4Iprj18f4srmonrvmrcFLf9172-Nn84r3Le-qhtp4vqgEhJf4crMKM6WgP_EWl56z9lwdKyYQnLktXEYy0xJzXbZhIeEcf_c7ndcm4o47kq-nNtWbucyy4VKc0Id50YsO3ZDNNlOXg-Hy4nz9tvdBJLTo93euTd5VHF1l-njSiE0ZoqEEDyvjKgd3pccgp-jugReQBAQEBEWabX4&clip=4&guid=f929b6a62256af44&flowid=2fea5a93d08759cd8080b49a036d6565&platform=10201&sdtfrom=v1010&appVer=1.40.3&unid=&auth_from=&auth_ext=&vid=o001470awrf&defn=hd&fhdswitch=0&dtype=3&spsrt=2&tm=1743744088&lang_code=0&logintoken=%7B%22access_token%22%3A%22%22%2C%22appid%22%3A%22phzJM3GWNjVa%22%2C%22vusession%22%3A%22Al94ppCEy5WZnShXNZcYCx25sv5CT9dU1vXcK623wnpN-iZKXfByPLuy8WQgcWbhVA.M%22%2C%22openid%22%3A%22199961645c32546e245e2c17752292be%22%2C%22vuserid%22%3A%223449288184%22%2C%22video_guid%22%3A%22f929b6a62256af44%22%2C%22main_login%22%3A%22phone%22%7D&qimei=fac37627d6c63d15b44c3c37300012e18312&spvvpay=1&spadseg=3&spav1=15&hevclv=28&spsfrhdr=0&spvideo=0&spm3u8tag=67&spmasterm3u8=3&track=undefined&atime=7&drm=40","sspAdParam":"{\\"ad_scene\\":1,\\"pre_ad_params\\":{\\"ad_scene\\":1,\\"user_type\\":2,\\"video\\":{\\"base\\":{\\"vid\\":\\"o001470awrf\\",\\"cid\\":\\"d968qjcaw9pdld0\\"},\\"is_live\\":false,\\"type_id\\":1,\\"referer\\":\\"\\",\\"url\\":\\"https://v.qq.com/x/cover/d968qjcaw9pdld0/o001470awrf.html\\",\\"flow_id\\":\\"2fea5a93d08759cd8080b49a036d6565\\",\\"refresh_id\\":\\"e1581e9590bd49cb0ea6c17c6a6a9554_1743743976\\",\\"fmt\\":\\"hd\\"},\\"platform\\":{\\"guid\\":\\"f929b6a62256af44\\",\\"channel_id\\":0,\\"site\\":\\"web\\",\\"platform\\":\\"in\\",\\"from\\":0,\\"device\\":\\"pc\\",\\"play_platform\\":10201,\\"pv_tag\\":\\"\\",\\"support_click_scan_integration\\":true,\\"qimei32\\":\\"43ef7b49a9df2ec8e0354aaef880171c\\"},\\"player\\":{\\"version\\":\\"1.40.3\\",\\"plugin\\":\\"4.1.30\\",\\"switch\\":1,\\"play_type\\":\\"0\\"},\\"token\\":{\\"type\\":3,\\"vuid\\":3449288184,\\"vuser_session\\":\\"Al94ppCEy5WZnShXNZcYCx25sv5CT9dU1vXcK623wnpN-iZKXfByPLuy8WQgcWbhVA.M\\",\\"app_id\\":\\"phzJM3GWNjVa\\",\\"open_id\\":\\"199961645c32546e245e2c17752292be\\",\\"access_token\\":\\"\\"},\\"req_extra_info\\":{\\"now_timestamp_s\\":1743744088,\\"ad_frequency_control_time_list\\":{\\"full_pause_short_bid_forbid_cid\\":{\\"ad_frequency_control_time_list\\":[1743573723,1743573727]},\\"full_pause_short_bid_forbid_vid\\":{\\"ad_frequency_control_time_list\\":[1743573723,1743573727]},\\"full_pause_feed_back_bid\\":{\\"ad_frequency_control_time_list\\":[1743573731,1743573734]},\\"full_pause_feedback_bid_successive\\":{\\"ad_frequency_control_time_list\\":[1743573731,1743573734]},\\"full_pause_feed_back\\":{\\"ad_frequency_control_time_list\\":[1743587222]},\\"full_pause_feedback_successive\\":{\\"ad_frequency_control_time_list\\":[1743587222]}},\\"ad_request_id\\":\\"48202885-9ec7-4ad3-9833-665ab55f7100\\",\\"exp_ids\\":[\\"100000\\",\\"11892116\\"],\\"video_played_time_ms\\":0,\\"playback_novelty_contexts\\":[]},\\"extra_info\\":{}}}","adparam":"adType=preAd&vid=o001470awrf&sspKey=mcrr"}'

response = requests.post('https://vd6.l.qq.com/proxyhttp', cookies=cookies, headers=headers, data=data)
data_dict = json.loads(response.text)
vinfo = data_dict.get('vinfo')
if not vinfo:
    print(response.status_code)
    print("当前包已失效\t: ", response.text)
vinfo = json.loads(vinfo)
m3u8List = vinfo['vl']['vi'][0]['ul']['m3u8']
ui_url = vinfo['vl']['vi'][0]['ul']['ui'][0]['url']

uel_header_v2 = ui_url.split('gzc_', 1)[0]

print(uel_header_v2)
print(m3u8List)


# from  ts_mp4 import ts_convert
# ts_convert(m3u8List, uel_header_v2)