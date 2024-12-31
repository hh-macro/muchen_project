import requests


headers = {
    "accept": "*/*",
    "accept-language": "en-US",
    "client-geo-region": "global",
    "priority": "u=1, i",
    "referer": "https://unsplash.com/t/people",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
cookies = {
    "require_cookie_consent": "false",
    "xp-simplified-join-form": "experiment",
    "uuid": "76b07319-7b25-4e7a-aaa2-08597622ac6a",
    "azk": "76b07319-7b25-4e7a-aaa2-08597622ac6a",
    "azk-ss": "true",
    "_sp_ses.0295": "*",
    "_sp_id.0295": "8ebd85f7-adf7-4c2f-ac2e-4220cdfa96ca.1735095896.2.1735103162.1735098732.29118549-3248-4a7f-9ec9-d62be7e8eae4.42d4dbfe-4b82-4e57-a1dc-c4a6a4f48e53.b87d6b6f-f6f7-4e65-8c65-7dc48ed224dc.1735102641185.26",
    "_dd_s": "logs=1&id=8ec72760-6db0-4a08-8483-65b1c70b083a&created=1735102631797&expire=1735104067857"
}
url = "https://unsplash.com/napi/topics/people/photos"
params = {
    "page": "17",
    "per_page": "10"
}
response = requests.get(url, headers=headers, cookies=cookies, params=params)

print(response.text)
print(response)