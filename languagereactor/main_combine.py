# -- coding: utf-8 --
# @Author: 胡H
# @File: main_combine.py
# @Created: 2025/5/9 11:12
# @LastModified:
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import json
import random

import requests


class LanguageReactorAPI:
    def __init__(self, keyword=None):
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
        }  # 请求头
        self.languageAll = {'中文(简体)': 'zh-CN', '中文(繁体)': 'zh-TW', '丹麦语': 'da', '乌克兰语': 'uk',
                            '乌兹别克语': 'uz',
                            '乌尔都语': 'ur',
                            '亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd',
                            '僧伽罗语': 'si', '克罗地亚语': 'hr', '冰岛语': 'is', '加利西亚语': 'gl',
                            '加泰罗尼亚语': 'ca',
                            '匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢旺达语': 'rw',
                            '卢森堡语': 'lb',
                            '印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '哈萨克语': 'kk',
                            '土库曼语': 'tk',
                            '土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语': 'sr', '奥里亚语': 'or',
                            '威尔士语': 'cy',
                            '孟加拉语': 'bn', '宿务语': 'ceb', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巽他语': 'su',
                            '希伯来语': 'iw', '希腊语': 'el', '库尔德语': 'ku', '德语': 'de', '意大利语': 'it',
                            '意第绪语': 'yi', '拉脱维亚语': 'lv', '挪威语': 'no', '捷克语': 'cs', '斯洛伐克语': 'sk',
                            '斯洛文尼亚语': 'sl', '斯瓦希里语': 'sw', '日语': 'ja',
                            '普什图语': 'ps', '柯尔克孜语': 'ky', '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr',
                            '波兰语': 'pl', '波斯尼亚语': 'bs', '波斯语': 'fa', '泰卢固语': 'te', '泰米尔语': 'ta',
                            '泰语': 'th', '海地克里奥尔语': 'ht', '爪哇语': 'jv', '爱尔兰语': 'ga',
                            '爱沙尼亚语': 'et',
                            '瑞典语': 'sv', '白俄罗斯语': 'be', '祖鲁语': 'zu', '科萨语': 'xh', '立陶宛语': 'lt',
                            '索马里语': 'so', '约鲁巴语': 'yo', '绍纳语': 'sn', '维吾尔语': 'ug', '缅甸语': 'my',
                            '罗马尼亚语': 'ro', '老挝语': 'lo', '芬兰语': 'fi', '苏格兰盖尔语': 'gd', '英语': 'en',
                            '荷兰语': 'nl', '菲律宾语': 'tl', '萨摩亚语': 'sm', '葡萄牙语': 'pt', '蒙古语': 'mn',
                            '西班牙语': 'es', '豪萨语': 'ha', '越南语': 'vi', '阿塞拜疆语': 'az', '阿姆哈拉语': 'am',
                            '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '鞑靼语': 'tt', '韩语': 'ko', '马其顿语': 'mk',
                            '马拉加斯语': 'mg', '马拉地语': 'mr', '马拉雅拉姆语': 'ml', '马来语': 'ms',
                            '马耳他语': 'mt',
                            '高棉语': 'km', '齐切瓦语': 'ny'}  # 仅供参考,并不使用
        self.language_dict = {'中文(繁体)': 'zh-TW', '丹麦语': 'da', '乌克兰语': 'uk',
                              '乌兹别克语': 'uz',
                              '乌尔都语': 'ur',
                              '亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd',
                              '僧伽罗语': 'si', '克罗地亚语': 'hr', '冰岛语': 'is', '加利西亚语': 'gl',
                              '加泰罗尼亚语': 'ca',
                              '匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢旺达语': 'rw',
                              '卢森堡语': 'lb',
                              '印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '哈萨克语': 'kk',
                              '土库曼语': 'tk',
                              '土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语': 'sr', '奥里亚语': 'or',
                              '威尔士语': 'cy',
                              '孟加拉语': 'bn', '宿务语': 'ceb', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巽他语': 'su',
                              '希伯来语': 'iw', '希腊语': 'el', '库尔德语': 'ku', '德语': 'de', '意大利语': 'it',
                              '意第绪语': 'yi', '拉脱维亚语': 'lv', '挪威语': 'no', '捷克语': 'cs', '斯洛伐克语': 'sk',
                              '斯洛文尼亚语': 'sl', '斯瓦希里语': 'sw', '日语': 'ja',
                              '普什图语': 'ps', '柯尔克孜语': 'ky', '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr',
                              '波兰语': 'pl', '波斯尼亚语': 'bs', '波斯语': 'fa', '泰卢固语': 'te', '泰米尔语': 'ta',
                              '泰语': 'th', '海地克里奥尔语': 'ht', '爪哇语': 'jv', '爱尔兰语': 'ga',
                              '爱沙尼亚语': 'et',
                              '瑞典语': 'sv', '白俄罗斯语': 'be', '祖鲁语': 'zu', '科萨语': 'xh', '立陶宛语': 'lt',
                              '索马里语': 'so', '约鲁巴语': 'yo', '绍纳语': 'sn', '维吾尔语': 'ug', '缅甸语': 'my',
                              '罗马尼亚语': 'ro', '老挝语': 'lo', '芬兰语': 'fi', '苏格兰盖尔语': 'gd',
                              '荷兰语': 'nl', '菲律宾语': 'tl', '萨摩亚语': 'sm', '葡萄牙语': 'pt', '蒙古语': 'mn',
                              '西班牙语': 'es', '豪萨语': 'ha', '越南语': 'vi', '阿塞拜疆语': 'az', '阿姆哈拉语': 'am',
                              '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '鞑靼语': 'tt', '韩语': 'ko', '马其顿语': 'mk',
                              '马拉加斯语': 'mg', '马拉地语': 'mr', '马拉雅拉姆语': 'ml', '马来语': 'ms',
                              '马耳他语': 'mt',
                              '高棉语': 'km', '齐切瓦语': 'ny'}  # 正式环境使用
        self.language_text = {'中文(繁体)': 'zh-TW', '日语': 'ja', '法语': 'fr', '韩语': 'ko'}  # 仅供测试使用
        self.e_books_text = [{'diocoDocId': 'gb_3015', 'pageCount': '42'}]  # 电子书信息 仅供测试使用
        self.keyword = keyword
        self.e_books_message = self.base_media_getMediaDocs()  # 电子书信息
        self.atlastResult = []  # 最终结果

    def base_media_getMediaDocs(self, freq95_min=0, freq95_max=100000, page_min=None, page_max=None):
        """ 获取搜索页信息并返回标准的数据格式"""
        json_data = {
            'auth': None,
            'translationLang_G': 'zh-CN',
            'freq95': {
                'min': freq95_min,
                'max': freq95_max,
            },
            'lang_G': 'en',
            'filters': {
                'mediaTab': 'TAB_BOOKS',
                'searchText': self.keyword,
                'pageCount': {
                    'min': page_min,
                    'max': page_max,
                },
            },
            'pinnedDiocoPlaylistIds': [],
            'diocoPlaylistId': 't_tx_all_en',
            'forceIncludeDiocoDocId': None,
        }

        response = requests.post('https://api-cdn.dioco.io/base_media_getMediaDocs_5', headers=self.headers,
                                 json=json_data)
        if response.status_code != 200: raise '请注意! 您已经被该网站反爬检测! 请稍后启动'
        docs_metadata_list = response.json()['data']['docs_metadata']

        # 提取指定的键并创建新的列表
        e_books_message = []
        for docs_metadata in docs_metadata_list:
            new_item = {
                "diocoDocId": docs_metadata.get("diocoDocId"),
                "diocoDocName": docs_metadata.get("diocoDocName"),
                "pageCount": docs_metadata.get("pageCount")
            }
            e_books_message.append(new_item)
        if not e_books_message: raise '数据为空!'
        return e_books_message

    def dict_json(self, data):
        """ 将列表嵌套的字典转换为json格式并保存本地"""
        json_data = json.dumps(data, indent=4)  # indent 参数用于美化输出
        with open("result/atlastResult.json", "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        return json_data

    def merge_lists(self, list1, list2):
        """ 检查两个列表的长度是否相同"""
        if len(list1) != len(list2):
            raise ValueError("两个列表的长度必须相同")
        return [
            {'originalTranslation': original, 'translate': translate}
            for original, translate in zip(list1, list2)
        ]

    def get_book_page(self, dioco_doc_id, page_num, auth=None):
        # 获取书籍本体内容
        url = 'https://api-cdn.dioco.io/base_media_getBookPageNLP_5'
        json_data = {
            'diocoDocId': dioco_doc_id,
            'pageNum': page_num,
            'auth': auth,
        }
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            data_subs = response.json()['data']['nlpDataBlob']['subs']
            text_list = [item.get('text', '') for item in data_subs]
            return text_list
        except Exception as e:
            print(f"请求失败: {e}")
            return None

    def get_page_translations(self, dioco_doc_id, page_num, translation_lang, auth=None):
        # 获取页面翻译内容
        url = 'https://api-cdn.dioco.io/base_media_getBookPageTranslations_5'
        json_data = {
            'diocoDocId': dioco_doc_id,
            'pageNum': page_num,
            'translationLang_G': translation_lang,
            'auth': auth,
        }
        try:
            response = requests.post(url, headers=self.headers, json=json_data)
            if response.status_code != 200:
                return 0
            data_resu_list = response.json()['data']
            # data_resu_str = ' '.join(data_resu_list)
            return data_resu_list
        except Exception as e:
            print(f"请求失败: {e}")
            return None

    def complete_response(self):
        for e_book_name in self.e_books_message:  # 遍历所有电子书
            random.uniform(1, 5)
            print(f'当前电子书 --> {e_book_name}', end=' ')
            print('=' * 61)
            # e_book_name   ----> {'diocoDocId': 'gb_3015', 'pageCount': '42'}
            pageCount = int(e_book_name['pageCount'])
            for page in range(pageCount):  # 遍历所有页数
                random.uniform(0, 1)
                print(f'第{page}页', end=' ')
                print('-' * 51)
                book_page = self.get_book_page(
                    dioco_doc_id=e_book_name['diocoDocId'],
                    page_num=page
                )
                # print(book_page)
                translations_zhCN = self.get_page_translations(
                    dioco_doc_id=e_book_name['diocoDocId'],
                    page_num=page,
                    translation_lang='zh-CN'
                )

                self.atlastResult.extend([{**item, 'language': '英语'} for item in
                                          self.merge_lists(translations_zhCN, book_page)])
                for state, trans in self.language_dict.items():  # 遍历所有语言列表
                    random.uniform(0, 0.5)
                    print(f'{state}', end=' ')
                    print('.' * 51)
                    # print(state, trans)  # 日语 ja
                    translations = self.get_page_translations(
                        dioco_doc_id=e_book_name['diocoDocId'],  # gb_3015
                        page_num=page,  # 0
                        translation_lang=trans  # ja
                    )
                    if translations == 0:
                        print(f'当前{state} 语言不存在， 将跳过当前语言!')
                        continue
                    merged_lists = [{**item, 'language': state} for item in
                                    self.merge_lists(translations_zhCN, translations)]  # 将一个键值对插入列表中每个字典
                    self.atlastResult.extend(merged_lists)


# 示例用法
if __name__ == "__main__":
    api_client = LanguageReactorAPI(keyword='culture')
    api_client.complete_response()  # 执行主方法

    atlastResult = api_client.atlastResult
    api_client.dict_json(atlastResult)
