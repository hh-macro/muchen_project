import requests
import json


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    "cache-control": "no-cache",
    "content-type": "text/plain;charset=UTF-8",
    "origin": "https://news.qq.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://news.qq.com/",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
cookies = {
    "RK": "R391v4Z3NZ",
    "ptcz": "974167d978770fd2c4e8e422a8f5c74fc09917999fb5789088c8b405baac66c8",
    "_qimei_uuid42": "1910309122a100898a17759f7df11436c7ae543bf4",
    "_qimei_fingerprint": "75059786da94cf42e0e18205aaec1fcf",
    "_qimei_h38": "2db8fb138a17759f7df1143602000007519103",
    "qq_domain_video_guid_verify": "f929b6a62256af44",
    "wap_wx_openid": "o_lAF57bpb_tyz4q1zRtS2lM7Tss",
    "wap_wx_appid": "wx0b6d22ad9f2c4fa0",
    "logintype": "1",
    "wap_refresh_token": "87_U9M1AcLo5OpQ8YeMXkwlzW_47-UbEoORI_2WWGcwwqYy2MS7pdcvDJGOTKkS1aYSvsIMNjyFZ3Of4-HF6O26_vwPdq_yHkxpvlqBayMxiYg",
    "wap_encrypt_logininfo": "ASuZHXPxJsxaHE13GyDl4zI7DK0Wc6tnOd7LZ5IZS1lyMFIJ%2B8UggHICyW5i4RdaR7geynKP5S%2BMWKZ4KqGL1y3l3hqeCjxlJPUWcLMeUiiG",
    "backup_logintype": "1",
    "appuser": "93DDC16039BAB5A4",
    "pac_uid": "8QIf3nxc6YAbuD/b7gs=",
    "suid": "user_8QIf3nxc6YAbuD%2Fb7gs%3D",
    "current-city-name": "cq",
    "pgv_pvid": "7331608848",
    "_qimei_q32": "43ef7b49a9df2ec8e0354aaef880171c",
    "_qimei_q36": "fac37627d6c63d15b44c3c37300012e18312",
    "wap_wx_access_token": "88_lj7Co72M7r-cLM3-44xpMSFHUStdhEI5mhBCTPu6Snhp9a8FANIAjyR9oMTMnfmivAxHDabh5sKYOfSKOlKHuWt_VDnsi75xHVO_n5Q4WF4",
    "cm_cookie": "V1,110064&Da4Rt0K3qezB&AQEBw4hJsGSnlLXIMoTuC79QWg7X7ZW4YY5A&250106&250106",
    "LPVLturn": "25",
    "LZTturn": "852",
    "news_token": "EoABzSPj4g88D4Vd4b768jPKQqmvw90WzX_e-z8TSvYNh7KTYF6k0sy_EbaZ5DA45aLoPK6IPbWJSAxAz3OQUwYReo2L6DLM1WBPXJ2uDXhXbwdhsObs9JUS0xtYXGNQ-G5hpNtYUguZWOPoHkkgUorZSp5EFvwt97Hay3GaQcOUXVggEQ",
    "backup_news_token": "EoABzSPj4g88D4Vd4b768jPKQqmvw90WzX_e-z8TSvYNh7KTYF6k0sy_EbaZ5DA45aLoPK6IPbWJSAxAz3OQUwYReo2L6DLM1WBPXJ2uDXhXbwdhsObs9JUS0xtYXGNQ-G5hpNtYUguZWOPoHkkgUorZSp5EFvwt97Hay3GaQcOUXVggEQ",
    "LZCturn": "113",
    "LPHLSturn": "27",
    "LPDFturn": "22",
    "Lturn": "207",
    "LPLFturn": "436",
    "LPPBturn": "899",
    "lv_play_index": "57",
    "next_refresh_time": "1736218235",
    "o_minduid": "_X0ihKyvAcJ060qjiPlhyOO079F-4q8d",
    "LPSJturn": "546",
    "LBSturn": "979",
    "LVINturn": "113",
    "LDERturn": "303"
}
url = "https://vd6.l.qq.com/proxyhttp"
data = {
    "buid": "vinfoad",
    "vinfoparam": "charge=0&otype=ojson&defnpayver=2&spau=1&spaudio=0&spwm=1&sphls=2&host=news.qq.com&refer=https%3A%2F%2Fnews.qq.com%2Frain%2Fa%2F20250106V0494W00&ehost=https%3A%2F%2Fnews.qq.com%2Frain%2Fa%2F20250106V0494W00&sphttps=1&encryptVer=8.5&cKey=--01CEEE0598ED5AAC39A441303F78A63060A4348455CD26AAC3A19030AB0B17571DDF61B72DA2C620A89966D93635E8D017A11214F21E31267BD75A2A23FCC8FB27AF88395D6986A98DCFD578C487ABD12D372F8D6B2DA40A4137823B8C3EEEB0A018F160701F496DD24CE82F18BDAC394B0AE0CCF023D5CA99C66D8F7279182243A951D8687D0611DC210104B4F5CFEA983A3CC0036313CE1D7A443AB9A49A12309BF668FFB376B66B20D450D396C8E4F9D2D51E7EC3027846C63CBF0EAF3C34424B6068B7EBB3C9ACF51F43B4B065921F17AD76F16C7FE2221B47CAC4F4259398A132AD8CA1E0F031BAD4C2BC67F82CAF&clip=4&guid=8QIf3nxc6YAbuD%2Fb7gs%3D&flowid=93dc75382aecd9f20d7cf8822544e62f&platform=6740201&sdtfrom=v1104&appVer=1.33.6&unid=&auth_from=&auth_ext=&vid=t1495r68g37&defn=shd&fhdswitch=0&dtype=3&spsrt=2&tm=1736215646&lang_code=0&logintoken=&spvvpay=1&spadseg=3&spav1=15&hevclv=28&spsfrhdr=0&spvideo=0&spm3u8tag=67&spmasterm3u8=3&scene=news_defn_sc_rule%3D-1&drm=40",
    "sspAdParam": "{\"ad_scene\":1,\"pre_ad_params\":{\"ad_scene\":1,\"user_type\":-1,\"video\":{\"base\":{\"vid\":\"a1492y9a1w5\"},\"is_live\":false,\"type_id\":0,\"referer\":\"https://news.qq.com/ch/history\",\"url\":\"https://news.qq.com/rain/a/20241231V05F7W00\",\"flow_id\":\"c88b2d77210d625d4a8a95afee11d44f\",\"refresh_id\":\"\",\"fmt\":\"shd\"},\"platform\":{\"guid\":\"8QIf3nxc6YAbuD/b7gs=\",\"channel_id\":2020,\"site\":\"web\",\"platform\":\"out\",\"from\":0,\"device\":\"pc\",\"play_platform\":6740201,\"pv_tag\":\"news_qq_com\",\"support_click_scan_integration\":false,\"qimei32\":\"43ef7b49a9df2ec8e0354aaef880171c\",\"qimei36\":\"fac37627d6c63d15b44c3c37300012e18312\"},\"player\":{\"version\":\"1.33.5\",\"plugin\":\"4.1.13\",\"switch\":1,\"play_type\":\"0\",\"img_type\":\"webp\"},\"token\":{\"type\":0,\"vuid\":0,\"vuser_session\":\"\",\"app_id\":\"\",\"open_id\":\"\",\"access_token\":\"\"},\"req_extra_info\":{\"now_timestamp_s\":1736215207,\"ad_frequency_control_time_list\":{}},\"extra_info\":{\"news_frequency_info\":{\"watch_complete_timestamp_ms\":0,\"refresh_video_num\":0,\"free_ad_time_ms\":0,\"refresh_free_ad_num\":0}}}}",
    "adparam": "adType=preAd&vid=t1495r68g37&sspKey=bcbr"
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)
mu8_list = json.loads(response.text)['vinfo']
# print(mu8_list)
mu8_url = json.loads(mu8_list)['vl']['vi'][0]['ul']['ui'][0]['url']
print(mu8_url)
