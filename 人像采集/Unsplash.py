import requests



headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
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
    "uuid": "c3909c9a-0191-4cf2-ac0e-6f5ebc2e4aef",
    "require_cookie_consent": "false",
    "xp-simplified-join-form": "control",
    "azk-ss": "true",
    "auth_user_id": "17642124",
    "_ga": "GA1.2.243980653.1735176284",
    "_ga_21SLH4J369": "GS1.2.1735181824.2.0.1735181824.0.0.0",
    "_sp_ses.0295": "*",
    "azk": "71d017e7-53aa-41ee-b23e-43ff13c2fdfe",
    "_gid": "GA1.2.175549471.1735203705",
    "un_sesh": "Yy9rM2xoK01JWVVzMFFBQTErb1RsWGVUVzlCVnVBTWJvTndacGNaaTE4aGlIZjN1LzdXekxCL2tqVVVTV2xRT3pNb1NUUGxuWTBZZTVVQjJJQ2FzYk9meVJUcVNxOEdTdGZMYS83dmFZRVVpTWVtTTQyeTFrNjFrMkUyTC9vUS9mZDI0YUZVTzFrV3VLc0RPSVlQK2VFczJDUWVtTDVCdE04em96RS9USkpiYXZpMEdIWFBQRzlzKzJndndZbDVveU5wWjJ5cCtyYVdZaC9tdXU0bU9IdUdUQjVQYWVCNGVnUXNURU45VC92S0lwVm90WWU2TDRxZWMydmh6WnJmakJNMXhkWlVBYWZ6bXhZYnBWRXJES0hwcExXRU92YzRXQzRmTHVPMDIzb2dTQkM2Q1JZVDcvWG95UHFQa1V2ZGtMTTFUYmhYYmF6NmpqMjNZcVVDejNRWHJoQVpMdkROczV2eFdkSmVqQzduUDloRGxCTmlVYnVNT2hqUitRTGFvSmp2bElzdVhXR2JYZG5Wdk9pRWJIOW9sZXpYanhzL29HQjBNb01ocXJsSkk4TzhZekdvSVA4OTRuRnJxNSs2MDFrZVhrWVJTck5QTXNNUlpmejlqTzZwWXZXK0h6TEhOcGJOd0pYMHBJeS9PTDVFaUttaUhHUnB0THUwMEZ5cm5LVnBBRnowdHZ1R1RFRnRSbDFBcnF5cldwVThBc0g2Vi95N1dDWjBTNHN4a0pVTXVTdGFJb0ZxRmwzSXA3UFB1clo4dk9KaW1uS3R1cFpUYStZVUQxVW5KYzJnUE9PWUFuM2pqVlgzT1dZVUhiV09kb0xGTkhWWjJndndodTN6Ty0tcSs5WDRadE1FeVhWRGZYVjZMVkg5dz09--0a4aadad49f25f8f6c07e9f261867e2f8f706cba",
    "_sp_id.0295": "eb3de7ab-ee81-453e-8083-c535c54361da.1735095907.9.1735204306.1735180458.59a4e422-2872-4615-91cf-6508c555c8c2..b80cfae6-e383-4b8c-a112-bd57a49c3660.1735203715374.40",
    "_dd_s": "logs=1&id=7c4e631b-0874-494d-89c5-d9d234631e02&created=1735203232644&expire=1735205201219"
}
url = "https://unsplash.com/t/people"
response = requests.get(url, headers=headers, cookies=cookies)

print(response.text)
print(response)
