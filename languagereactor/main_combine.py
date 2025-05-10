# -- coding: utf-8 --
# @Author: 胡H
# @File: main_combine.py
# @Created: 2025/5/9 11:12
# @LastModified:
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import hashlib
import json
import os
import random
import time

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
                            '高棉语': 'km', '齐切瓦语': 'ny'}  # 总语言 -仅供参考,并不使用
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
                            '高棉语': 'km', '齐切瓦语': 'ny'}  # 需要获取的语言 -仅供参考,并不使用
        self.language_dict = {
            '斯洛文尼亚语': 'sl', '斯瓦希里语': 'sw', '日语': 'ja', '普什图语': 'ps', '柯尔克孜语': 'ky',
            '格鲁吉亚语': 'ka', '毛利语': 'mi', '法语': 'fr', '波兰语': 'pl', '波斯尼亚语': 'bs',
            '波斯语': 'fa', }  # 正式环境使用
        self.language_text = {'中文(繁体)': 'zh-TW', '日语': 'ja', '法语': 'fr', '韩语': 'ko'}  # 仅供测试使用
        self.e_books_text = [{'diocoDocId': 'gb_3015', 'pageCount': '42'}]  # 电子书信息 仅供测试使用
        self.keyword = keyword
        # self.e_books_message = self.base_media_getMediaDocs()  # 电子书信息
        self.e_books_message = [
            {'diocoDocId': 'gb_41519', 'diocoDocName': 'Thought-Culture; Or, Practical Mental Training',
             'pageCount': 33}, {'diocoDocId': 'gb_11772',
                                'diocoDocName': 'Narrative of a Voyage to Senegal in 1816\r\nUndertaken by Order of the French Government, Comprising an Account of the Shipwreck of the Medusa, the Sufferings of the Crew, and the Various Occurrences on Board the Raft, in the Desert of Zaara, at St. Louis, and at the Camp of Daccard. to Which Are Subjoined Observations Respecting the Agriculture of the Western Coast of Africa, from Cape Blanco to the Mouth of the Gambia.',
                                'pageCount': 71},
            {'diocoDocId': 'gb_7804', 'diocoDocName': 'Expressive Voice Culture, Including the Emerson System',
             'pageCount': 10}, {'diocoDocId': 'gb_16232',
                                'diocoDocName': 'The Culture of Vegetables and Flowers From Seeds and Roots\r\n16th Edition',
                                'pageCount': 182},
            {'diocoDocId': 'gb_59977', 'diocoDocName': 'Canning, Freezing, Storing Garden Produce', 'pageCount': 42},
            {'diocoDocId': 'gb_54720',
             'diocoDocName': "Three Years' Wanderings in the Northern Provinces of China\r\nIncluding a visit to the tea, silk, and cotton countries; with an account of the agriculture and horticulture of the Chinese, new plants, etc.",
             'pageCount': 100}, {'diocoDocId': 'gb_58133',
                                 'diocoDocName': 'Twentieth Century Culture and Deportment\r\nOr the Lady and Gentleman at Home and Abroad; Containing Rules of Etiquette for All Occasions, Including Calls; Invitations; Parties; Weddings; Receptions; Dinners and Teas; Etiquette of the Street; Public Places, Etc., Etc. Forming a Complete Guide to Self-Culture; the Art of Dressing Well; Conversation; Courtship; Etiquette for Children; Letter-Writing; Artistic Home and Interior Decorations, Etc.',
                                 'pageCount': 138}, {'diocoDocId': 'gb_13357',
                                                     'diocoDocName': 'Cactus Culture for Amateurs\r\nBeing Descriptions of the Various Cactuses Grown in This Country, With Full and Practical Instructions for Their Successful Cultivation',
                                                     'pageCount': 65}, {'diocoDocId': 'gb_67114',
                                                                        'diocoDocName': 'Massage & Exercises Combined\r\nA permanent physical culture course for men, women and children; health-giving, vitalizing, prophylactic, beautifying; a new system of the characteristic essentials of gymnastic and Indian Yogis concentration exercises combined with scientific massage movements; with 86 illustrations and deep breathing exercises',
                                                                        'pageCount': 18}, {'diocoDocId': 'gb_24944',
                                                                                           'diocoDocName': 'Mushrooms: how to grow them\na practical treatise on mushroom culture for profit and pleasure',
                                                                                           'pageCount': 47},
            {'diocoDocId': 'gb_43200',
             'diocoDocName': "Cornell Nature-Study Leaflets\r\nBeing a selection, with revision, from the teachers' leaflets, home nature-study lessons, junior naturalist monthlies and other publications from the College of Agriculture, Cornell University, Ithaca, N.Y., 1896-1904",
             'pageCount': 156}, {'diocoDocId': 'gb_14055',
                                 'diocoDocName': 'Food Guide for War Service at Home\r\nPrepared under the direction of the United States Food Administration in co-operation with the United States Department of Agriculture and the Bureau of Education, with a preface by Herbert Hoover',
                                 'pageCount': 17}]  # 电子书信息
        self.atlastResult = []  # 最终结果

    def generate_md5(self):
        """生成18位随机数"""
        random_num = random.randint(10 ** 17, 10 ** 18)
        # 获取当前时间戳
        timestamp = int(time.time())
        # 将随机数和时间戳组合成字符串
        combined_str = f"{random_num}{timestamp}"
        # 计算md5
        md5 = hashlib.md5(combined_str.encode('utf-8')).hexdigest()
        return md5

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

    def read_json(self):
        """读取本地 JSON 文件，如果文件不存在或为空则返回空列表"""
        if os.path.exists("result/atlastResult.json"):
            with open("result/atlastResult.json", "r", encoding='utf-8') as json_file:
                content = json_file.read()
                if content.strip():  # 检查文件是否为空或只包含空白字符
                    return json.loads(content)
                else:
                    return []
        else:
            return []

    def dict_json(self, new_data):
        """将列表嵌套的字典转换为 JSON 格式并保存到本地"""
        # 读取已有的数据
        existing_data = self.read_json()
        # 合并数据
        merged_data = existing_data + new_data
        # 将合并后的数据转换为 JSON 字符串
        json_data = json.dumps(merged_data, indent=4, ensure_ascii=False)
        # 将合并后的数据写入本地文件
        with open("result/atlastResult.json", "w", encoding='utf-8') as json_file:
            json.dump(merged_data, json_file, indent=4, ensure_ascii=False)
        return json_data

    def merge_lists(self, list1, list2):
        """ 检查两个列表的长度是否相同"""
        if len(list1) != len(list2):
            raise ValueError("两个列表的长度必须相同")
        return [
            {'input': original, 'output': translate}
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
        """ 获取页面翻译内容（带重试机制）"""
        url = 'https://api-cdn.dioco.io/base_media_getBookPageTranslations_5'
        json_data = {
            'diocoDocId': dioco_doc_id,
            'pageNum': page_num,
            'translationLang_G': translation_lang,
            'auth': auth,
        }

        # 重试配置
        max_retries = 5  # 最大重试次数
        retry_delay = 2  # 初始重试延迟秒数

        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=self.headers, json=json_data)

                if response.status_code != 200:
                    print(f"请求失败状态码: {response.status_code} (尝试 {attempt + 1}/{max_retries})")
                    if attempt == max_retries - 1:
                        return 0
                    continue

                data_resu_list = response.json()['data']
                return data_resu_list if data_resu_list else 0

            except requests.exceptions.SSLError as e:
                print(f"SSL错误发生: {e} (尝试 {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    print("SSL重试次数用尽，跳过该请求")
                    return None
                time.sleep(retry_delay * (attempt + 1))  # 递增延迟

            except Exception as e:
                print(f"其他请求异常: {e} (尝试 {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    return None
                time.sleep(retry_delay)

        return None

    def complete_response(self):
        try:
            for e_book_name in self.e_books_message:  # 遍历所有电子书
                random.uniform(1, 5)
                print(f'当前电子书 --> {e_book_name}', end=' ')
                print('=' * 61)
                # e_book_name   ----> {'diocoDocId': 'gb_3015', 'pageCount': '42'}
                pageCount = int(e_book_name['pageCount'])
                for page in range(pageCount):  # 遍历所有页数
                    try:
                        random.uniform(0, 1)
                        print(f'第{page}页', end=' ')
                        print('-' * 51)
                        book_page = self.get_book_page(
                            dioco_doc_id=e_book_name['diocoDocId'],
                            page_num=page
                        )
                        if not book_page:
                            print('book_page 内容为空,将跳过当前页')
                            continue
                            # print(book_page)
                        translations_zhCN = self.get_page_translations(
                            dioco_doc_id=e_book_name['diocoDocId'],
                            page_num=page,
                            translation_lang='zh-CN'
                        )

                        if translations_zhCN == 0:
                            print(f'当前页数{page}有问题! 将跳过当前页')
                            continue
                        self.atlastResult.extend(
                            [{**item, 'language': '英语', 'id': self.generate_md5()} for item in
                             self.merge_lists(translations_zhCN, book_page)])

                        for state, trans in self.language_dict.items():  # 遍历所有语言列表
                            try:
                                random.uniform(0, 0.5)
                                print(f'{state}', end=' ')
                                print('.' * 51)
                                # print(state, trans)  # 日语 ja
                                translations = self.get_page_translations(
                                    dioco_doc_id=e_book_name['diocoDocId'],  # gb_3015
                                    page_num=page,  # 0
                                    translation_lang=trans  # ja
                                )
                                # # 加强空值校验
                                if translations is None:
                                    print(f'获取{state}翻译时发生严重错误，跳过')
                                    continue
                                if translations == 0:
                                    print(f'当前{state} 语言不存在， 将跳过当前语言!')
                                    continue
                                    # 加强长度校验
                                if len(translations_zhCN) != len(translations):
                                    print(
                                        f"翻译长度不一致（中文:{len(translations_zhCN)} vs {state}:{len(translations)}），跳过")
                                merged_lists = [{**item, 'language': trans, 'id': self.generate_md5()} for item in
                                                self.merge_lists(translations_zhCN, translations)]  # 将一个键值对插入列表中每个字典
                                self.atlastResult.extend(merged_lists)

                            except Exception as e:
                                print(f"处理语言{state}时发生异常: {e}")
                                self.dict_json(self.atlastResult)
                    except Exception as e:
                        print(f"处理第{page}页时发生异常: {e}")
                        self.dict_json(self.atlastResult)
                        continue  # 继续处理下一页
            self.dict_json(self.atlastResult)
        except Exception as e:
            print(f"程序发生未预期异常: {e}")
            self.dict_json(self.atlastResult)
            raise  # 重新抛出异常或处理后退出


# 示例用法
if __name__ == "__main__":
    api_construction = LanguageReactorAPI(keyword='culture')
    api_construction.complete_response()  # 执行主方法
"""
{'中文(繁体)': 'zh-TW', '丹麦语': 'da', '乌克兰语': 'uk',
'乌兹别克语': 'uz','乌尔都语': 'ur','亚美尼亚语': 'hy', '伊博语': 'ig', '俄语': 'ru', '保加利亚语': 'bg', '信德语': 'sd',
'僧伽罗语': 'si', '克罗地亚语': 'hr', '冰岛语': 'is', '加利西亚语': 'gl',
'加泰罗尼亚语': 'ca','匈牙利语': 'hu', '南非荷兰语': 'af', '卡纳达语': 'kn', '卢旺达语': 'rw','卢森堡语': 'lb',
'印地语': 'hi', '印度尼西亚语': 'id', '古吉拉特语': 'gu', '哈萨克语': 'kk',
'土库曼语': 'tk','土耳其语': 'tr', '塔吉克语': 'tg', '塞尔维亚语': 'sr', '奥里亚语': 'or',
'威尔士语': 'cy','孟加拉语': 'bn', '宿务语': 'ceb', '尼泊尔语': 'ne', '巴斯克语': 'eu', '巽他语': 'su',
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
'高棉语': 'km', '齐切瓦语': 'ny'}

"""
