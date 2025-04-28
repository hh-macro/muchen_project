# -- coding: utf-8 --
# @Author: 胡H
# @File: link_getPage.py
# @Created: 2025/4/3 11:39
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import json

import pandas as pd
import requests

import time

cookies = {
    'flwssn': '89e116d8-dcd8-4dd6-8a67-b59cd26aa60c',
    'gsid': '7ef0b277-6b3b-4765-9a87-9a3798df2413',
    'netflix-sans-normal-3-loaded': 'true',
    'netflix-sans-bold-3-loaded': 'true',
    'sawContext': 'true',
    'nfvdid': 'BQFmAAEBECg6EhKgnWrjiCzyKBVIR_hgDwZBieH0wWLAyO7J_DxW2VKuA8BPzUMN3OkFmQxT3c5s893faLVInP86Fb6bwrJzEnoQz8_mclFYmYCAHjqVpeALRh2T_hd-kfqWjTQx3QiRy-FBOTh-Thv_36kQS9WG',
    'SecureNetflixId': 'v%3D3%26mac%3DAQEAEQABABR2J2KmicCWVs6A38aTrqokr2iOdjgaaoE.%26dt%3D1743650425710',
    'NetflixId': 'v%3D3%26ct%3DBgjHlOvcAxL8AtWFqhY8tgKxCAprpShiz2el9KXQ1qL9-GK6HOeD_Vprjgi2tmOUiRnN4BjsqT2YFD_4e-3RvpAm5n4rfwpOt179HKH2ykRKxG8utq3IC6X8Zkh-3jhocNUMI5vchBEXGPaCvZbmxZwwZRfSeOUV_tE4kHaczZ_JiLd1BHLuAzsxcPBUka0XC-Y7BmSQAPZ7iS1PyME2Uq15t_q2KTyll64dxnvxIc8VuPPKQCIBHwhAD0Sksbg2i6u3-A8B2TnXK8CpybOz2Ib-lxKFp4QzVctVI6uacel6Pzg7AahLSEs9piaJQlHRKutJ-luBw87UNNHNuOegG8YxzbM6AF4SFApr65MDAbqztTfku03JKyniUgJl8UZWPM7l9HTCobHTeL2ycEXB7jkukm2m7c0Bre-hX-4Kjd-p2nz3rEvMY1H1FaYcG5I2AFkIkpgIWWgEP8b_tLk7eCD8MWQADMFsaldsCK_fTctjAk_ztqvpiS66zrHBy0n5TOe7eQYMGAYiDgoM8sszBih-PMdWvOOG%26ch%3DAQEAEAABABTvxxWzf2cOEkNhKsrJPf3rnZNJCoBE0pY.',
    'profilesNewSession': '0',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Apr+03+2025+11%3A32%3A35+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8ee4ef4d-ac19-4519-825e-c7b81ec85b4e&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.netflix.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.netflix.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-netflix.context.app-version': 'v5db5418b',
    'x-netflix.context.locales': 'zh-tr',
    'x-netflix.context.operation-name': 'MiniModalQuery',
    'x-netflix.context.ui-flavor': 'akira',
    'x-netflix.request.attempt': '1',
    'x-netflix.request.client.context': '{"appstate":"foreground"}',
    'x-netflix.request.id': 'd833d634e4d1443bae736288f6570252',
    'x-netflix.request.originating.url': 'https://www.netflix.com/search?q=%E7%BA%AA%E5%BD%95%E7%89%87',
    'x-netflix.request.toplevel.uuid': '1cf874c8-bd58-4baa-945d-854f63fc62c6',
    # 'cookie': 'flwssn=89e116d8-dcd8-4dd6-8a67-b59cd26aa60c; gsid=7ef0b277-6b3b-4765-9a87-9a3798df2413; netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; sawContext=true; nfvdid=BQFmAAEBECg6EhKgnWrjiCzyKBVIR_hgDwZBieH0wWLAyO7J_DxW2VKuA8BPzUMN3OkFmQxT3c5s893faLVInP86Fb6bwrJzEnoQz8_mclFYmYCAHjqVpeALRh2T_hd-kfqWjTQx3QiRy-FBOTh-Thv_36kQS9WG; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABR2J2KmicCWVs6A38aTrqokr2iOdjgaaoE.%26dt%3D1743650425710; NetflixId=v%3D3%26ct%3DBgjHlOvcAxL8AtWFqhY8tgKxCAprpShiz2el9KXQ1qL9-GK6HOeD_Vprjgi2tmOUiRnN4BjsqT2YFD_4e-3RvpAm5n4rfwpOt179HKH2ykRKxG8utq3IC6X8Zkh-3jhocNUMI5vchBEXGPaCvZbmxZwwZRfSeOUV_tE4kHaczZ_JiLd1BHLuAzsxcPBUka0XC-Y7BmSQAPZ7iS1PyME2Uq15t_q2KTyll64dxnvxIc8VuPPKQCIBHwhAD0Sksbg2i6u3-A8B2TnXK8CpybOz2Ib-lxKFp4QzVctVI6uacel6Pzg7AahLSEs9piaJQlHRKutJ-luBw87UNNHNuOegG8YxzbM6AF4SFApr65MDAbqztTfku03JKyniUgJl8UZWPM7l9HTCobHTeL2ycEXB7jkukm2m7c0Bre-hX-4Kjd-p2nz3rEvMY1H1FaYcG5I2AFkIkpgIWWgEP8b_tLk7eCD8MWQADMFsaldsCK_fTctjAk_ztqvpiS66zrHBy0n5TOe7eQYMGAYiDgoM8sszBih-PMdWvOOG%26ch%3DAQEAEAABABTvxxWzf2cOEkNhKsrJPf3rnZNJCoBE0pY.; profilesNewSession=0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Apr+03+2025+11%3A32%3A35+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8ee4ef4d-ac19-4519-825e-c7b81ec85b4e&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
}

json_data = {
    'operationName': 'MiniModalQuery',
    'variables': {
        'opaqueImageFormat': 'WEBP',
        'transparentImageFormat': 'WEBP',
        'videoMerchEnabled': True,
        'fetchPromoVideoOverride': False,
        'hasPromoVideoOverride': False,
        'promoVideoId': 0,
        'videoMerchContext': 'BROWSE',
        'isLiveEpisodic': False,
        'artworkContext': {},
        'textEvidenceUiContext': 'BOB',
        'unifiedEntityIds': [
            'Video:81026142',
            'Video:81607869',
            'Video:80133187',
            'Video:80192098',
            'Video:81736884',
            'Video:81590652',
            'Video:70204970',
            'Video:81746667',
            'Video:81325501',
            'Video:80117552',
            'Video:81168282',
            'Video:81564905',
            'Video:81516491',
            'Video:80215147',
            'Video:81117189',
            'Video:81074662',
            'Video:81728365',
            'Video:81211003',
            'Video:80049832',
            'Video:81711982',
            'Video:81075536',
            'Video:80135674',
            'Video:81652564',
            'Video:81554996',
            'Video:81507383',
            'Video:81239224',
            'Video:81155081',
            'Video:80175351',
            'Video:81086133',
            'Video:81351263',
            'Video:81721676',
            'Video:81030202',
            'Video:81036559',
            'Video:81780831',
            'Video:81681485',
            'Video:81720808',
            'Video:81322606',
        ],
    },
    'extensions': {
        'persistedQuery': {
            'id': '85f714bc-d42f-40d4-bd6f-9a9c046a8936',
            'version': 102,
        },
    },
}


response = requests.post('https://web.prod.cloud.netflix.com/graphql', cookies=cookies, headers=headers, json=json_data)
print(response.status_code)
print(response.text)
# =====================================================
data_dict = json.loads(response.text).get('data', {})
if not data_dict:
    print('请求异常')
unifiedEntities = data_dict['unifiedEntities']
data_list_message = []
for unified in unifiedEntities:
    dict_message = {}
    title = unified.get('title', '')  # 标题
    videoId = 'https://www.netflix.com/watch/' + str(unified.get('videoId'))  # id
    textEvidence = unified.get('textEvidence')[0].get('text', '')  # 类别

    dict_message['title'] = title
    dict_message['videoId'] = videoId
    dict_message['textEvidence'] = textEvidence

    data_list_message.append(dict_message)

print(data_list_message)

# 将列表转换为DataFrame
df = pd.DataFrame(data_list_message)

# 将DataFrame导出为Excel文件
df.to_excel(f"./compilations/netflix-{int(time.time())}.xlsx", index=False)

print(f"netflix-{int(time.time())}.xlsx")