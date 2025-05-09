# -- coding: utf-8 --
# @Author: 胡H
# @File: main_combine.py
# @Created: 2025/5/9 11:12
# @LastModified:
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import requests


class LanguageReactorAPI:
    def __init__(self):
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.languagereactor.com',
            'pragma': 'no-cache',
            'referer': 'https://www.languagereactor.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        }

    def get_book_page(self, dioco_doc_id, page_num, auth=None):
        url = 'https://api-cdn.dioco.io/base_media_getBookPageNLP_5'
        json_data = {
            'diocoDocId': dioco_doc_id,
            'pageNum': page_num,
            'auth': auth,
        }
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            return response.json()
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def get_page_translations(self, dioco_doc_id, page_num, translation_lang, auth=None):
        url = 'https://api-cdn.dioco.io/base_media_getBookPageTranslations_5'
        json_data = {
            'diocoDocId': dioco_doc_id,
            'pageNum': page_num,
            'translationLang_G': translation_lang,
            'auth': auth,
        }
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            return response.json()
        except Exception as e:
            print(f"Request failed: {e}")
            return None


# 示例用法
if __name__ == "__main__":
    language_dict = {'中文(繁体)': 'zh-TW', '丹麦语': 'da', '乌克兰语': 'uk', '乌兹别克语': 'uz', '乌尔都语': 'ur',
                     '亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd',
                     '僧伽罗语': 'si', '克罗地亚语': 'hr', '冰岛语': 'is', '加利西亚语': 'gl', '加泰罗尼亚语': 'ca',
                     '匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢旺达语': 'rw', '卢森堡语': 'lb',
                     '印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '哈萨克语': 'kk', '土库曼语': 'tk',
                     '土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语': 'sr', '奥里亚语': 'or', '威尔士语': 'cy',
                     '孟加拉语': 'bn', '宿务语': 'ceb', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巽他语': 'su',
                     '希伯来语': 'iw', '希腊语': 'el', '库尔德语': 'ku', '德语': 'de', '意大利语': 'it',
                     '意第绪语': 'yi', '拉脱维亚语': 'lv', '挪威语': 'no', '捷克语': 'cs', '斯洛伐克语': 'sk',
                     '斯洛文尼亚语': 'sl', '斯瓦希里语': 'sw', '日语': 'ja',
                     '普什图语': 'ps', '柯尔克孜语': 'ky', '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr',
                     '波兰语': 'pl', '波斯尼亚语': 'bs', '波斯语': 'fa', '泰卢固语': 'te', '泰米尔语': 'ta',
                     '泰语': 'th', '海地克里奥尔语': 'ht', '爪哇语': 'jv', '爱尔兰语': 'ga', '爱沙尼亚语': 'et',
                     '瑞典语': 'sv', '白俄罗斯语': 'be', '祖鲁语': 'zu', '科萨语': 'xh', '立陶宛语': 'lt',
                     '索马里语': 'so', '约鲁巴语': 'yo', '绍纳语': 'sn', '维吾尔语': 'ug', '缅甸语': 'my',
                     '罗马尼亚语': 'ro', '老挝语': 'lo', '芬兰语': 'fi', '苏格兰盖尔语': 'gd', '英语': 'en',
                     '荷兰语': 'nl', '菲律宾语': 'tl', '萨摩亚语': 'sm', '葡萄牙语': 'pt', '蒙古语': 'mn',
                     '西班牙语': 'es', '豪萨语': 'ha', '越南语': 'vi', '阿塞拜疆语': 'az', '阿姆哈拉语': 'am',
                     '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '鞑靼语': 'tt', '韩语': 'ko', '马其顿语': 'mk',
                     '马拉加斯语': 'mg', '马拉地语': 'mr', '马拉雅拉姆语': 'ml', '马来语': 'ms', '马耳他语': 'mt',
                     '高棉语': 'km', '齐切瓦语': 'ny'}
    api_client = LanguageReactorAPI()

    book_page = api_client.get_book_page(
        dioco_doc_id='gb_20203',
        page_num=0
    )
    print("Book Page Content:")
    print(book_page)

    # 获取页面翻译
    translations = api_client.get_page_translations(
        dioco_doc_id='gb_20203',
        page_num=0,
        translation_lang='zh-CN'
    )
    print("\nPage Translations:")
    print(translations)
