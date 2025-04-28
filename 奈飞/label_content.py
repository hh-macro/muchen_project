# -- coding: utf-8 --
# @Author: 胡H
# @File: label_content.py
# @Created: 2025/4/3 17:01
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import requests

cookies = {
    'gsid': '7ef0b277-6b3b-4765-9a87-9a3798df2413',
    'netflix-sans-normal-3-loaded': 'true',
    'netflix-sans-bold-3-loaded': 'true',
    'sawContext': 'true',
    'nfvdid': 'BQFmAAEBECg6EhKgnWrjiCzyKBVIR_hgDwZBieH0wWLAyO7J_DxW2VKuA8BPzUMN3OkFmQxT3c5s893faLVInP86Fb6bwrJzEnoQz8_mclFYmYCAHjqVpeALRh2T_hd-kfqWjTQx3QiRy-FBOTh-Thv_36kQS9WG',
    'SecureNetflixId': 'v%3D3%26mac%3DAQEAEQABABR2J2KmicCWVs6A38aTrqokr2iOdjgaaoE.%26dt%3D1743650425710',
    'NetflixId': 'v%3D3%26ct%3DBgjHlOvcAxL8AtWFqhY8tgKxCAprpShiz2el9KXQ1qL9-GK6HOeD_Vprjgi2tmOUiRnN4BjsqT2YFD_4e-3RvpAm5n4rfwpOt179HKH2ykRKxG8utq3IC6X8Zkh-3jhocNUMI5vchBEXGPaCvZbmxZwwZRfSeOUV_tE4kHaczZ_JiLd1BHLuAzsxcPBUka0XC-Y7BmSQAPZ7iS1PyME2Uq15t_q2KTyll64dxnvxIc8VuPPKQCIBHwhAD0Sksbg2i6u3-A8B2TnXK8CpybOz2Ib-lxKFp4QzVctVI6uacel6Pzg7AahLSEs9piaJQlHRKutJ-luBw87UNNHNuOegG8YxzbM6AF4SFApr65MDAbqztTfku03JKyniUgJl8UZWPM7l9HTCobHTeL2ycEXB7jkukm2m7c0Bre-hX-4Kjd-p2nz3rEvMY1H1FaYcG5I2AFkIkpgIWWgEP8b_tLk7eCD8MWQADMFsaldsCK_fTctjAk_ztqvpiS66zrHBy0n5TOe7eQYMGAYiDgoM8sszBih-PMdWvOOG%26ch%3DAQEAEAABABTvxxWzf2cOEkNhKsrJPf3rnZNJCoBE0pY.',
    'profilesNewSession': '0',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Apr+03+2025+16%3A56%3A53+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8ee4ef4d-ac19-4519-825e-c7b81ec85b4e&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.netflix.com/NotFound?prev=https%3A%2F%2Fwww.netflix.com%2Fbrowse%2Fgenre%3Fbc%3D83',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"19.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'gsid=7ef0b277-6b3b-4765-9a87-9a3798df2413; netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; sawContext=true; nfvdid=BQFmAAEBECg6EhKgnWrjiCzyKBVIR_hgDwZBieH0wWLAyO7J_DxW2VKuA8BPzUMN3OkFmQxT3c5s893faLVInP86Fb6bwrJzEnoQz8_mclFYmYCAHjqVpeALRh2T_hd-kfqWjTQx3QiRy-FBOTh-Thv_36kQS9WG; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABR2J2KmicCWVs6A38aTrqokr2iOdjgaaoE.%26dt%3D1743650425710; NetflixId=v%3D3%26ct%3DBgjHlOvcAxL8AtWFqhY8tgKxCAprpShiz2el9KXQ1qL9-GK6HOeD_Vprjgi2tmOUiRnN4BjsqT2YFD_4e-3RvpAm5n4rfwpOt179HKH2ykRKxG8utq3IC6X8Zkh-3jhocNUMI5vchBEXGPaCvZbmxZwwZRfSeOUV_tE4kHaczZ_JiLd1BHLuAzsxcPBUka0XC-Y7BmSQAPZ7iS1PyME2Uq15t_q2KTyll64dxnvxIc8VuPPKQCIBHwhAD0Sksbg2i6u3-A8B2TnXK8CpybOz2Ib-lxKFp4QzVctVI6uacel6Pzg7AahLSEs9piaJQlHRKutJ-luBw87UNNHNuOegG8YxzbM6AF4SFApr65MDAbqztTfku03JKyniUgJl8UZWPM7l9HTCobHTeL2ycEXB7jkukm2m7c0Bre-hX-4Kjd-p2nz3rEvMY1H1FaYcG5I2AFkIkpgIWWgEP8b_tLk7eCD8MWQADMFsaldsCK_fTctjAk_ztqvpiS66zrHBy0n5TOe7eQYMGAYiDgoM8sszBih-PMdWvOOG%26ch%3DAQEAEAABABTvxxWzf2cOEkNhKsrJPf3rnZNJCoBE0pY.; profilesNewSession=0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Apr+03+2025+16%3A56%3A53+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8ee4ef4d-ac19-4519-825e-c7b81ec85b4e&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
}

params = {
    'so': 'az',
}

response = requests.get('https://www.netflix.com/browse/m/genre/1165152', params=params, cookies=cookies, headers=headers)
print(response.text)