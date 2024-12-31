import requests


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    "authorization;": "",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.pexels.com/zh-cn/search/people/",
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
    "OptanonAlertBoxClosed": "2024-12-25T05:49:17.136Z",
    "country-code-v2": "US",
    "_gid": "GA1.2.1675409294.1735489114",
    "_fbp": "fb.1.1735489121545.178350229839789409",
    "__cf_bm": "Bo33o3RZWoqGSCAMuQPXUMU5yRvTW0O6A75JNJORkbE-1735520543-1.0.1.1-mbtF5oeoRuL.RHAJRSOp.U3Qgo.UdnsI6le5V_HVzOqgRKBDL.dLIyUH_ZNoN32mCRe8dprTXoKohQozYSQgOw",
    "_cfuvid": "Drn7rOmrBYj9U4cF8lKecRizn07LA1Ypa0z1iLiig7A-1735520543849-0.0.1.1-604800000",
    "_sp_ses.9ec1": "*",
    "cf_clearance": "5k_7EikeZKDPk6LtAwljU7xeU1aRM4fAtqXYU7gTC8s-1735520545-1.2.1.1-rLSBfg7TijbwqcdDh5VyXzS6.B01TYZ_iBiI9FWx8MHVIS_OBdkINGGw..2hXiqGGKoJvvTH92rvOdrXcfo3_m2I.PqKBpMuRhesDp3tiB18Arj2xasvktbfnAwEMz0EJ7Ahleg1_8gBhhPAYUJcQYngffAtXDob8C9OV.qHOfjyp1HmDgK8OBZIZRscwUUt.2VdLvNBkOmpd89FppcnizyVU4kJNXEIj1wLJJD1iSa5_WI9ZAN45HbgjzBH6FKf9zBcRc3_1xXdtMRZWmOXVud93imKIrcDak_IpIwWHfxQMpILEnVDcGvAQlS2YKiNfWEVVhqhN2ITkNVhZ1jTJa91wUgEz.C4zR6fsNmd7s9sWKawOl7ajO6GTCFV6Taq",
    "locale": "zh-CN",
    "_ga": "GA1.1.682930128.1735097201",
    "_sp_id.9ec1": "1362b4b8-ff3d-4022-ae1d-d77706621e20.1735097188.7.1735521054.1735489171.b5731688-3965-4c2c-bc31-88475a67e24d.9b302389-5c2f-4b43-aa26-8785d5fefb96.3f031c10-6cac-4a11-b6f4-a0f5dbf670bd.1735520545978.59",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Mon+Dec+30+2024+09%3A10%3A54+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202301.1.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=CN%3BCQ&AwaitingReconsent=false",
    "_ga_8JE65Q40S6": "GS1.1.1735520546.9.1.1735521065.0.0.0"
}
url = "https://www.pexels.com/en-us/api/v3/search/photos"
params = {
    "query": "people",
    "page": "6",
    "per_page": "24",
    "orientation": "all",
    "size": "all",
    "color": "all",
    "sort": "popular",
    "seo_tags": "true"
}
response = requests.get(url, headers=headers, cookies=cookies, params=params)

print(response.text)
print(response)