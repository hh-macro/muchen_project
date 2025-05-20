# -- coding: utf-8 --
# @Author: 胡H
# @File: reques_dispose.py
# @Created: 2025/5/12 15:34
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import json

import requests

cookies = {
    'session-id': '130-4385434-5066934',
    'ubid-main': '135-1025297-2749812',
    'aws-target-data': '%7B%22support%22%3A%221%22%7D',
    'aws-target-visitor-id': '1746938000411-361671.48_0',
    'regStatus': 'pre-register',
    'AMCV_7742037254C95E840A4C98A6%40AdobeOrg': '1585540135%7CMCIDTS%7C20220%7CMCMID%7C90683267398556508902130992312058399043%7CMCAAMLH-1747542800%7C3%7CMCAAMB-1747542800%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1746945201s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0',
    'kndctr_7742037254C95E840A4C98A6_AdobeOrg_identity': 'CiYyNzcwODAzODcyMTUzMjg4ODkwMDE2ODM4OTQ0OTcxMDE0Njg1MFITCL2K-uzrMhABGAEqBEpQTjMwAPABvYr67Osy',
    'kndctr_7742037254C95E840A4C98A6_AdobeOrg_consent': 'general=in',
    'i18n-prefs': 'USD',
    'av-timezone': 'Asia/Shanghai',
    'lc-main': 'zh_CN',
    'at-main': 'Atza|IwEBIN5-szp1dNSRwSJr9AOoO80CMRKuFVmPTJCFySN9IZF83XAT3FXfl3hneR2aSybdL8fnTQMPi3p3Y4O1moq9UYuOglcK9Stzf01v85ZcZkJBo1fpsULV_YnFamRVGeGh1ZwNsCkmsAv2qaAG5JfectNhXg2J1ddJfhDuMQ0LIeIZm8f8QNmmBI80YOMXCJ2qaT1UWaVA-7kVItfacnQPne8Di6fscGXnZTB-L3ZPRhPfPg',
    'sess-at-main': '"b3eldsbm7cEQ5Pllxesf329Gd3MLRT61Vy4Gcjwii6w="',
    'sst-main': 'Sst1|PQEu9gxETxDB41zRY6Wodg_GDI3TKlL0ceTt5AHEx_5K5iqqDS0pKAp3yMg385bZo4vcEu5NivU0KM4X3H-C_MPY17A7joPPYKOzRYdGdo_miAK5Ud0jv-UlyIynFTV_9DhD0xspnb_pYR2VweCjRGA9tRFJNdlvFyBJUe7juNKz2N6zMCZiprChnyNOHNLJ93UODywmIBIrOZjaeadp9YzdaTbC2yGZBNJXaN3rwHUenN2mlGgSnf2gzBeyRHlyrPBqPAEszaLOSJa_k-dYrGoeTBBYjdGYgy9oV-LRyc5UxU-TFphLxp8ouu-2tIRdYpatt-iWT-tEIdluwn5DERFae0wOwzQtbARREPOU7I8GKJk',
    'session-id-time': '2082787201l',
    'sp-cdn': '"L5Z9:JP"',
    'av-profile': 'cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTNJS0ZPSzAyQVhRUkYmdGltZXN0YW1wPTE3NDY5NDgwODAxNjgmdmVyc2lvbj12MQ.g9i7mGm14O3xnlvQSwrwMFxRKiKqoO4SMOWqbgb386sIAAAAAQAAAABoIE_wcmF3AAAAAPgWC9WfHH8iB-olH_E9xQ',
    'session-token': 'CHEB9hC6L7BTzYX/WfN4Vx+KdagNjICuypvag1hS7sAlGv86sV4OVUkB7rj7jw+5HCSotQA4pYAnQlZKMAThqSiE6nRGJZltTwhO2zazUXeWSPUR5xCvoNv0qgFwUitsdj+OEJ2s9tNjinXsr7RhFjfJ9Ta7z7bRIRGN09754a83Q6yDL+uRlJbEdxBwYLeIboztmBHm3Znral4jjJRzjHCg/RNlkJcY2Biy6SbG5pnWGHv/g49Jqr88wWUHkGhdkE3h2OZ69mSjzYppe5SkiN+jkhG6FwnJCnOD8Mvz5JJcqmx106wSx0vIuR1D9P4tyPaXIRNuJZvTe1lchIis+a18K7JV+eYnBJYwS8pA8m4IdopJuKHqGW41fpO0kfvi',
    'x-main': '"r?Tax7JIozTX1LZO0MsQWkU2@@S5X?d9wPWLp9KCwy4ThR2A?7Ysgt3aRzK@n?Eh"',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain',
    'Origin': 'https://www.amazon.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.amazon.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'session-id=130-4385434-5066934; ubid-main=135-1025297-2749812; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1746938000411-361671.48_0; regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C20220%7CMCMID%7C90683267398556508902130992312058399043%7CMCAAMLH-1747542800%7C3%7CMCAAMB-1747542800%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1746945201s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; kndctr_7742037254C95E840A4C98A6_AdobeOrg_identity=CiYyNzcwODAzODcyMTUzMjg4ODkwMDE2ODM4OTQ0OTcxMDE0Njg1MFITCL2K-uzrMhABGAEqBEpQTjMwAPABvYr67Osy; kndctr_7742037254C95E840A4C98A6_AdobeOrg_consent=general=in; i18n-prefs=USD; av-timezone=Asia/Shanghai; lc-main=zh_CN; at-main=Atza|IwEBIN5-szp1dNSRwSJr9AOoO80CMRKuFVmPTJCFySN9IZF83XAT3FXfl3hneR2aSybdL8fnTQMPi3p3Y4O1moq9UYuOglcK9Stzf01v85ZcZkJBo1fpsULV_YnFamRVGeGh1ZwNsCkmsAv2qaAG5JfectNhXg2J1ddJfhDuMQ0LIeIZm8f8QNmmBI80YOMXCJ2qaT1UWaVA-7kVItfacnQPne8Di6fscGXnZTB-L3ZPRhPfPg; sess-at-main="b3eldsbm7cEQ5Pllxesf329Gd3MLRT61Vy4Gcjwii6w="; sst-main=Sst1|PQEu9gxETxDB41zRY6Wodg_GDI3TKlL0ceTt5AHEx_5K5iqqDS0pKAp3yMg385bZo4vcEu5NivU0KM4X3H-C_MPY17A7joPPYKOzRYdGdo_miAK5Ud0jv-UlyIynFTV_9DhD0xspnb_pYR2VweCjRGA9tRFJNdlvFyBJUe7juNKz2N6zMCZiprChnyNOHNLJ93UODywmIBIrOZjaeadp9YzdaTbC2yGZBNJXaN3rwHUenN2mlGgSnf2gzBeyRHlyrPBqPAEszaLOSJa_k-dYrGoeTBBYjdGYgy9oV-LRyc5UxU-TFphLxp8ouu-2tIRdYpatt-iWT-tEIdluwn5DERFae0wOwzQtbARREPOU7I8GKJk; session-id-time=2082787201l; sp-cdn="L5Z9:JP"; av-profile=cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTNJS0ZPSzAyQVhRUkYmdGltZXN0YW1wPTE3NDY5NDgwODAxNjgmdmVyc2lvbj12MQ.g9i7mGm14O3xnlvQSwrwMFxRKiKqoO4SMOWqbgb386sIAAAAAQAAAABoIE_wcmF3AAAAAPgWC9WfHH8iB-olH_E9xQ; session-token=CHEB9hC6L7BTzYX/WfN4Vx+KdagNjICuypvag1hS7sAlGv86sV4OVUkB7rj7jw+5HCSotQA4pYAnQlZKMAThqSiE6nRGJZltTwhO2zazUXeWSPUR5xCvoNv0qgFwUitsdj+OEJ2s9tNjinXsr7RhFjfJ9Ta7z7bRIRGN09754a83Q6yDL+uRlJbEdxBwYLeIboztmBHm3Znral4jjJRzjHCg/RNlkJcY2Biy6SbG5pnWGHv/g49Jqr88wWUHkGhdkE3h2OZ69mSjzYppe5SkiN+jkhG6FwnJCnOD8Mvz5JJcqmx106wSx0vIuR1D9P4tyPaXIRNuJZvTe1lchIis+a18K7JV+eYnBJYwS8pA8m4IdopJuKHqGW41fpO0kfvi; x-main="r?Tax7JIozTX1LZO0MsQWkU2@@S5X?d9wPWLp9KCwy4ThR2A?7Ysgt3aRzK@n?Eh"',
}

params = {
    'deviceID': '10f04796-79bf-43ba-9891-988d2bd91441',
    'deviceTypeID': 'AOAGZA014O5RE',
    'gascEnabled': 'false',
    'marketplaceID': 'ATVPDKIKX0DER',
    'uxLocale': 'zh_CN',
    'firmware': '1',
    'titleId': 'amzn1.dv.gti.41f71162-2344-4089-accf-5ce0e9c12535',
    'nerid': 'ZbDafC0v00BXTF2KsQx7NA00',
}

data_dict = {"globalParameters": {"deviceCapabilityFamily": "WebPlayer",
                                  "playbackEnvelope": "eyJ0eXAiOiJwbGVuditqd2UiLCJjdHkiOiJwbGVuditqd3MiLCJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiYTJ6K3BwX2VuYytzX3BhYWxDUXcifQ.AeVf5EUvWh0bhaY6oAffR4TOFKzDqHwCqWm8Y2b6fOGBqSmmTsNRXcNcX0Pn9NkHIYIZo_DHzb2mPyyTFh-ebt4d0t9o7iOj.AdqFliM0Owd3MKBVF56HcA.KAK4FhJKlRBsdNvrVSlVCIDMd05hbsk4074bKrh99K01zRYVDNEvqcGKMFY3ppndsevij1pLZsNc_RSBjYGmZoNfyAzRakQOkxcU_0siJ7mhxrPI9WmdpnB427c3SU9-07sE4QvRnenoONT9egahPhVcJOT8mdqzfrrADvcLSZXvMcgcoBA1SxnzKB27vDRJLI7_xdlqTEF8Mgbzvq4-L0dJWJBIz_9L0DgRoYB_WimIFU4YY7O_ZEAEEiofFy1Oly3pUBUwMEJoFMx1O9mUoT77XC2oP1SQNPQrIyoBumlgck5N9h3d7Rtsh12jgPs6CMdLxM3eT_jb05dtiCtczWp3o61Zsf4C4qA8qwybATAcoaFAmppB-PbA_N_68M4w1d5gpjB_8gLB5_ddQgAPeUsU_pHSBrOkslcMn0PUiE3ZKrSK-XztBSPD7S-Dtxp_x9tGZ6AFpuTXb6PPEf9ReQ74u1WzoiIaWpDL0zYlj48OmqC6VWG30wpwbTdZbxeXKNpUzbGBiKQ9iTIZNrji1WlxGau5Ki8lD3GPTr5aWki6NMZzo-TXgnZJH_veIbb_ikDHX88kq_8lAFz3PrjTlQ9K8wgqvgOcTe8AfQgTb1WxiRCcjB8wnYibvDkVLxk7SnsM-zcfPB_Qi486jaCDBkv4QqV4n6pyzwa9FDPb9-AuQhRC5DeJ141KzJV4t7nfUI0dCTZZDTGlV5VMc2OBvv6hAxWgfCBVYZom7wkSpsrZsh4uIA-moNAt9lacUVIFIBRoeIPvXFvSE_w0N85sz86_671Vg-XsjQ6Tsx051C6nO72LrGLr1nArMnQR0l1vmSD6VZExuauHt_zlvlOhQg9cNLr8XJV0iRs5UXNYVxuj8qtYvk8oHEVq2PSOjDK2V6G1LOBw7z6k7_yxwMeDoQa7JQap-flTFevPnpoJ8Yo18T2F6jwMwABdXRpnxZ9LI7z9wUpQdr56YLpJhswH4a_30ciZmv4_cpCeJjVuS2AFtb154WmAPSXXm835pIbxXOrIb4vj4SpbSS1iyqGDx11JIHoC1j1muA6yzz_m6kQCDfpXGJA0ukWKU_ruGbQvk5JuA-MqcmyOIRRzH07Qz7_Q8qPPf6o6hX5gGXncAceUAMCqkd2yCZe95FJm988kn7oHoBo3_QEUcDHrUkHrWbUiPCzIV23qHK20P8NABUraSUFl_fFU7TH9XM58_yOVuqv_lGRFx1pYD2N42amHh7o7vcDgOtoXjr4yyO3FHMsGExDetBJfKaG8A3aULoUnQL6gTptsEbqRX0mzjtY7Dv47AbaYZl_DzmJ6pmKjKimgVRL6iLRhkKKf6Jn0qWjBLxXQWepZrXlUb-TRiHtmqADnBfIAa9dDfXUQZyQE-ujMDffXIB0dH183L2Wvk2V6PzaM-G6RE2f_gl8l8rnwHG4fnvu4P-iwwgCvInAksF253PzyzVEVYxSzfxgnVH9AkfZc5e1GJNON6T4RrqojIcTkKH21pMi7MB_VjZg1wbyPOgNAhy7qM_evYgsGaJyzbIcdn-oveyfp3FXvTIeHGnL-O0nUB5owp_SkKPTpLMni4K5HPZXrJJLn6qNY2gdBkzMdnQ59KkJbBnT1PCgGwM0jYTccYKrt1NgAPCXwfhrNT9BV5wbTzasfRoEruFcuA3NkRHdDjlsH6oX35hLTo-gfKo92BlaVo1Lfmeu2VjU3cBMXVlDzCjs4FMheurNClLIqzUJtPtGcIiXWggGiyONTBDsXnzyrBhJXlsSbykSjWHm-AvkDLTz7BbYsY95kiek8Vy7RpIfSiU8ADzX62_HY7e8lC2cJatodMSpsvvHqJ7scNdDEgGPSWjEdfFdYZV2wAy5-vcNVm3iT3ypudGDUmX0RiY4d3MNlTTwfXSsfSbm-k2uOX3o_dEk8JADD1mdGzmptcBi7tNX3yt_TwaiC2nLquLg2gQxw68FDdfX50lTSKhRxd0Ap24gS7lLx6Tmov2nUQf5-Czp-rj3k9tnFbiUa75YAqIGA0HPn1efwlNi7s5htEj456dbfwGavA435p1yoTZyKd4bJ6zs7S77Jr8UrZALY-AdgXmTY5q8mMrhZ5xnNswMuUjQAGvb9LswqrBqP3Tc6SKQCkzPQ_wsj9VuR5lWHla7NKzYKPWKFqWbahTa7iX7gX28OmdKNGncH1h1m_oxUSv1Zy0WSSP5y_WpxQ8ADIWz-E_X_d14ZOnrw1eFpuy_zwOv3OJ7uVXlUA9WXKjtC00AJwCFXpLQcK8m-A-208Unj-kBsHeu2kKKki84btNhJgpsFP3aMWjYXJUJCbm_zCY6yTO7zQ8_-O6VRvCLydNPnbtSnCHmb5YL0XPMm_5ppeBhPe4M7z1AAi-fAJKxBLs5tCBmDvjrZDQOpQeR0DlsnU34absbVcyxiBLdR5FgdGOcoIEgFQ5aT0G5nJ06cM6Reza2Gon77yRKVUtNeGMmW3jvmLrihzhSuTX0w6St4ELToNPStHF_LZFX02h4g4s3-1Qg5u3IkQhYzpRBm2JdsIU18emxyiDkp8tgzvwg5HN_hm5spCwLk8P23Mf41J3KY1sqa0fPZXAaW2cScY7FHcNrhDKSt-SDnSXUzNeX-Gxzg-1frzqu0u1j-_RC6HYmEGGs6UBJdllN5rUESCyF6qV5rHa1IwBmoMw18Ke9cn_J1mGiq181VpwUOIvu6KSUcDW4deoNb54h7fAvMDv2B8W6YLIYvgEdEeOFG3ibcEgaOIpWUL2ucW-bIXycNsRaewCZ_EsDeDUIYNctlnzDExYUEwfcj05zyjLRaR52MqTzOLig2iZW2Syx0jSW3g5y5GzJV78XNDW_Wrwtm7tF0d7Wx7k9MudKM_L94uKFnIQlWw6JqEyRZPD9JTipwzjiH31ZlugvErH7joff6Pv-ylmMhz-lVybvvewa90548pcPINY-lGuMMFYGNBUU2Asdgt9k4JQy5JncpFG5SsUXf2B48bNk-GCq2MehhGqRPOGFJJIyDiuK3P8PIJ_2lXeNoYXayeMLlI31Z9f8vj7oqCIju_C2AQGXRMprhDORcnimjS-X_msuuh85B7wGmP5tMxyRqOKgvFLytTpz372a05E0mI_3PAwQML1occl12IkiiTAcFb4baQrvCd8UDPRSwOtFIGae1aEvoKBiAsfnpf9Pw7TLnrKl67Pp9_oka9utjWX4wIi3-XFhbuLPDc8l_mVg5EqVLtZhqPT1eMS6AdMyEvxS7J1WXlKyn_0CJmHStWQz38uBYHrtAfXtOaQ80gSjU0Ed0GEhWlKpYhDdpfRZK4B35WQp2EsXGkuMqpthoEQmw.DDtXBeH2SxWSYosqPbca3eR5RQoqBulbZ6roxk8aSqU",
                                  "capabilityDiscriminators": {
                                      "operatingSystem": {"name": "Windows", "version": "10.0"},
                                      "middleware": {"name": "Chrome", "version": "136.0.0.0"},
                                      "nativeApplication": {"name": "Chrome", "version": "136.0.0.0"},
                                      "hfrControlMode": "Legacy",
                                      "displayResolution": {"height": 1080, "width": 1920}}}, "auditPingsRequest": {},
             "playbackDataRequest": {}, "timedTextUrlsRequest": {"supportedTimedTextFormats": ["TTMLv2", "DFXP"]},
             "trickplayUrlsRequest": {}, "transitionTimecodesRequest": {}, "vodPlaybackUrlsRequest": {
        "device": {"hdcpLevel": "1.4", "maxVideoResolution": "1080p", "supportedStreamingTechnologies": ["DASH"],
                   "streamingTechnologies": {
                       "DASH": {"bitrateAdaptations": ["CBR", "CVBR"], "codecs": ["H264"], "drmKeyScheme": "DualKey",
                                "drmType": "Widevine", "dynamicRangeFormats": ["None"],
                                "fragmentRepresentations": ["ByteOffsetRange", "SeparateFile"],
                                "frameRates": ["Standard", "High"], "stitchType": "MultiPeriod",
                                "segmentInfoType": "Base",
                                "timedTextRepresentations": ["NotInManifestNorStream", "SeparateStreamInManifest"],
                                "trickplayRepresentations": ["NotInManifestNorStream"],
                                "variableAspectRatio": "supported"}}, "displayWidth": 1920, "displayHeight": 1080},
        "ads": {
            "sitePageUrl": "https://www.amazon.com/gp/video/detail/B09ML1QV1S/ref=atv_dp_season_select_s1?jic=8%7CEgRzdm9k",
            "gdpr": {"enabled": "false", "consentMap": {}}}, "playbackCustomizations": {},
        "playbackSettingsRequest": {"firmware": "UNKNOWN", "playerType": "xp", "responseFormatVersion": "1.0.0",
                                    "titleId": "amzn1.dv.gti.402c9c59-be1b-4498-8230-c8583a801d1c"}},
             "vodXrayMetadataRequest": {"xrayDeviceClass": "normal", "xrayPlaybackMode": "playback",
                                        "xrayToken": "XRAY_WEB_2023_V2"}}
data = json.dumps(data_dict)
# data = '{"globalParameters":{"deviceCapabilityFamily":"WebPlayer","playbackEnvelope":"eyJ0eXAiOiJwbGVuditqd2UiLCJjdHkiOiJwbGVuditqd3MiLCJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiYTJ6K3BwX2VuYytzX3BhYWxDUXcifQ.AeVf5EUvWh0bhaY6oAffR4TOFKzDqHwCqWm8Y2b6fOGBqSmmTsNRXcNcX0Pn9NkHIYIZo_DHzb2mPyyTFh-ebt4d0t9o7iOj.AdqFliM0Owd3MKBVF56HcA.KAK4FhJKlRBsdNvrVSlVCIDMd05hbsk4074bKrh99K01zRYVDNEvqcGKMFY3ppndsevij1pLZsNc_RSBjYGmZoNfyAzRakQOkxcU_0siJ7mhxrPI9WmdpnB427c3SU9-07sE4QvRnenoONT9egahPhVcJOT8mdqzfrrADvcLSZXvMcgcoBA1SxnzKB27vDRJLI7_xdlqTEF8Mgbzvq4-L0dJWJBIz_9L0DgRoYB_WimIFU4YY7O_ZEAEEiofFy1Oly3pUBUwMEJoFMx1O9mUoT77XC2oP1SQNPQrIyoBumlgck5N9h3d7Rtsh12jgPs6CMdLxM3eT_jb05dtiCtczWp3o61Zsf4C4qA8qwybATAcoaFAmppB-PbA_N_68M4w1d5gpjB_8gLB5_ddQgAPeUsU_pHSBrOkslcMn0PUiE3ZKrSK-XztBSPD7S-Dtxp_x9tGZ6AFpuTXb6PPEf9ReQ74u1WzoiIaWpDL0zYlj48OmqC6VWG30wpwbTdZbxeXKNpUzbGBiKQ9iTIZNrji1WlxGau5Ki8lD3GPTr5aWki6NMZzo-TXgnZJH_veIbb_ikDHX88kq_8lAFz3PrjTlQ9K8wgqvgOcTe8AfQgTb1WxiRCcjB8wnYibvDkVLxk7SnsM-zcfPB_Qi486jaCDBkv4QqV4n6pyzwa9FDPb9-AuQhRC5DeJ141KzJV4t7nfUI0dCTZZDTGlV5VMc2OBvv6hAxWgfCBVYZom7wkSpsrZsh4uIA-moNAt9lacUVIFIBRoeIPvXFvSE_w0N85sz86_671Vg-XsjQ6Tsx051C6nO72LrGLr1nArMnQR0l1vmSD6VZExuauHt_zlvlOhQg9cNLr8XJV0iRs5UXNYVxuj8qtYvk8oHEVq2PSOjDK2V6G1LOBw7z6k7_yxwMeDoQa7JQap-flTFevPnpoJ8Yo18T2F6jwMwABdXRpnxZ9LI7z9wUpQdr56YLpJhswH4a_30ciZmv4_cpCeJjVuS2AFtb154WmAPSXXm835pIbxXOrIb4vj4SpbSS1iyqGDx11JIHoC1j1muA6yzz_m6kQCDfpXGJA0ukWKU_ruGbQvk5JuA-MqcmyOIRRzH07Qz7_Q8qPPf6o6hX5gGXncAceUAMCqkd2yCZe95FJm988kn7oHoBo3_QEUcDHrUkHrWbUiPCzIV23qHK20P8NABUraSUFl_fFU7TH9XM58_yOVuqv_lGRFx1pYD2N42amHh7o7vcDgOtoXjr4yyO3FHMsGExDetBJfKaG8A3aULoUnQL6gTptsEbqRX0mzjtY7Dv47AbaYZl_DzmJ6pmKjKimgVRL6iLRhkKKf6Jn0qWjBLxXQWepZrXlUb-TRiHtmqADnBfIAa9dDfXUQZyQE-ujMDffXIB0dH183L2Wvk2V6PzaM-G6RE2f_gl8l8rnwHG4fnvu4P-iwwgCvInAksF253PzyzVEVYxSzfxgnVH9AkfZc5e1GJNON6T4RrqojIcTkKH21pMi7MB_VjZg1wbyPOgNAhy7qM_evYgsGaJyzbIcdn-oveyfp3FXvTIeHGnL-O0nUB5owp_SkKPTpLMni4K5HPZXrJJLn6qNY2gdBkzMdnQ59KkJbBnT1PCgGwM0jYTccYKrt1NgAPCXwfhrNT9BV5wbTzasfRoEruFcuA3NkRHdDjlsH6oX35hLTo-gfKo92BlaVo1Lfmeu2VjU3cBMXVlDzCjs4FMheurNClLIqzUJtPtGcIiXWggGiyONTBDsXnzyrBhJXlsSbykSjWHm-AvkDLTz7BbYsY95kiek8Vy7RpIfSiU8ADzX62_HY7e8lC2cJatodMSpsvvHqJ7scNdDEgGPSWjEdfFdYZV2wAy5-vcNVm3iT3ypudGDUmX0RiY4d3MNlTTwfXSsfSbm-k2uOX3o_dEk8JADD1mdGzmptcBi7tNX3yt_TwaiC2nLquLg2gQxw68FDdfX50lTSKhRxd0Ap24gS7lLx6Tmov2nUQf5-Czp-rj3k9tnFbiUa75YAqIGA0HPn1efwlNi7s5htEj456dbfwGavA435p1yoTZyKd4bJ6zs7S77Jr8UrZALY-AdgXmTY5q8mMrhZ5xnNswMuUjQAGvb9LswqrBqP3Tc6SKQCkzPQ_wsj9VuR5lWHla7NKzYKPWKFqWbahTa7iX7gX28OmdKNGncH1h1m_oxUSv1Zy0WSSP5y_WpxQ8ADIWz-E_X_d14ZOnrw1eFpuy_zwOv3OJ7uVXlUA9WXKjtC00AJwCFXpLQcK8m-A-208Unj-kBsHeu2kKKki84btNhJgpsFP3aMWjYXJUJCbm_zCY6yTO7zQ8_-O6VRvCLydNPnbtSnCHmb5YL0XPMm_5ppeBhPe4M7z1AAi-fAJKxBLs5tCBmDvjrZDQOpQeR0DlsnU34absbVcyxiBLdR5FgdGOcoIEgFQ5aT0G5nJ06cM6Reza2Gon77yRKVUtNeGMmW3jvmLrihzhSuTX0w6St4ELToNPStHF_LZFX02h4g4s3-1Qg5u3IkQhYzpRBm2JdsIU18emxyiDkp8tgzvwg5HN_hm5spCwLk8P23Mf41J3KY1sqa0fPZXAaW2cScY7FHcNrhDKSt-SDnSXUzNeX-Gxzg-1frzqu0u1j-_RC6HYmEGGs6UBJdllN5rUESCyF6qV5rHa1IwBmoMw18Ke9cn_J1mGiq181VpwUOIvu6KSUcDW4deoNb54h7fAvMDv2B8W6YLIYvgEdEeOFG3ibcEgaOIpWUL2ucW-bIXycNsRaewCZ_EsDeDUIYNctlnzDExYUEwfcj05zyjLRaR52MqTzOLig2iZW2Syx0jSW3g5y5GzJV78XNDW_Wrwtm7tF0d7Wx7k9MudKM_L94uKFnIQlWw6JqEyRZPD9JTipwzjiH31ZlugvErH7joff6Pv-ylmMhz-lVybvvewa90548pcPINY-lGuMMFYGNBUU2Asdgt9k4JQy5JncpFG5SsUXf2B48bNk-GCq2MehhGqRPOGFJJIyDiuK3P8PIJ_2lXeNoYXayeMLlI31Z9f8vj7oqCIju_C2AQGXRMprhDORcnimjS-X_msuuh85B7wGmP5tMxyRqOKgvFLytTpz372a05E0mI_3PAwQML1occl12IkiiTAcFb4baQrvCd8UDPRSwOtFIGae1aEvoKBiAsfnpf9Pw7TLnrKl67Pp9_oka9utjWX4wIi3-XFhbuLPDc8l_mVg5EqVLtZhqPT1eMS6AdMyEvxS7J1WXlKyn_0CJmHStWQz38uBYHrtAfXtOaQ80gSjU0Ed0GEhWlKpYhDdpfRZK4B35WQp2EsXGkuMqpthoEQmw.DDtXBeH2SxWSYosqPbca3eR5RQoqBulbZ6roxk8aSqU","capabilityDiscriminators":{"operatingSystem":{"name":"Windows","version":"10.0"},"middleware":{"name":"Chrome","version":"136.0.0.0"},"nativeApplication":{"name":"Chrome","version":"136.0.0.0"},"hfrControlMode":"Legacy","displayResolution":{"height":1080,"width":1920}}},"auditPingsRequest":{},"playbackDataRequest":{},"timedTextUrlsRequest":{"supportedTimedTextFormats":["TTMLv2","DFXP"]},"trickplayUrlsRequest":{},"transitionTimecodesRequest":{},"vodPlaybackUrlsRequest":{"device":{"hdcpLevel":"1.4","maxVideoResolution":"1080p","supportedStreamingTechnologies":["DASH"],"streamingTechnologies":{"DASH":{"bitrateAdaptations":["CBR","CVBR"],"codecs":["H264"],"drmKeyScheme":"DualKey","drmType":"Widevine","dynamicRangeFormats":["None"],"fragmentRepresentations":["ByteOffsetRange","SeparateFile"],"frameRates":["Standard","High"],"stitchType":"MultiPeriod","segmentInfoType":"Base","timedTextRepresentations":["NotInManifestNorStream","SeparateStreamInManifest"],"trickplayRepresentations":["NotInManifestNorStream"],"variableAspectRatio":"supported"}},"displayWidth":1920,"displayHeight":1080},"ads":{"sitePageUrl":"https://www.amazon.com/gp/video/detail/B09ML1QV1S/ref=atv_dp_season_select_s1?jic=8%7CEgRzdm9k","gdpr":{"enabled":false,"consentMap":{}}},"playbackCustomizations":{},"playbackSettingsRequest":{"firmware":"UNKNOWN","playerType":"xp","responseFormatVersion":"1.0.0","titleId":"amzn1.dv.gti.77650506-dee2-4b53-a87e-189f8ed5cd9c"}},"vodXrayMetadataRequest":{"xrayDeviceClass":"normal","xrayPlaybackMode":"playback","xrayToken":"XRAY_WEB_2023_V2"}}'

response = requests.post(
    'https://atv-ps.amazon.com/playback/prs/GetVodPlaybackResources',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)
print(response.json())
