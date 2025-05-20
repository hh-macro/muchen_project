# -- coding: utf-8 --
# @Author: 胡H
# @File: manage_title.py
# @Created: 2025/5/12 9:39
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import hashlib
import json
import pickle
import random
import re
import time
from pathlib import Path

import requests
import xml.etree.ElementTree as ET

current_file = Path(__file__).parent
correspondence = []


def generate_md5():
    """生成18位随机数"""
    random_num = random.randint(10 ** 17, 10 ** 18)
    # 获取当前时间戳
    timestamp = int(time.time())
    # 将随机数和时间戳组合成字符串
    combined_str = f"{random_num}{timestamp}"
    # 计算md5
    md5 = hashlib.md5(combined_str.encode('utf-8')).hexdigest()
    return md5


def extract_subtitles(ttml_content):
    """
        从TTML内容中提取字幕文本。解析TTML XML结构，提取每个<p>标签中的文本内容，并处理<br/>标签和嵌套元素。
        ttml_content (str): TTML格式的字幕内容。
        """
    namespace = 'http://www.w3.org/ns/ttml'
    br_tag = f'{{{namespace}}}br'
    root = ET.fromstring(ttml_content)

    result = {}
    p_elements = root.findall(f'.//{{{namespace}}}p')

    for p in p_elements:
        begin_time = p.get("begin")
        if not begin_time:
            continue

        parts = []
        # 提取根文本
        if p.text and p.text.strip():
            parts.append(p.text.strip())

        # 递归处理子元素
        for child in p:
            if child.tag == br_tag:
                parts.append("<br/>")
                # 处理<br/>后的尾部文本
                if child.tail and child.tail.strip():
                    parts.append(child.tail.strip())
            else:
                # 提取嵌套元素的所有文本（如<span>）
                def extract_nested_text(element):
                    text = []
                    if element.text and element.text.strip():
                        text.append(element.text.strip())
                    for sub in element:
                        text.extend(extract_nested_text(sub))
                        if sub.tail and sub.tail.strip():
                            text.append(sub.tail.strip())
                    return text

                nested_text = extract_nested_text(child)
                parts.extend(nested_text)

        # 合并文本并格式化<br/>
        merged_text = " ".join(parts)
        merged_text = re.sub(r"\s*<br/>\s*", "<br/>", merged_text).strip()
        result[begin_time] = merged_text

    return result


def saveCorreJson():
    """
       保存data_list到josn中
    """
    file_path = Path(current_file, 'result_json', 'data.json')
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(correspondence, json_file, ensure_ascii=False, indent=4)
    print(f'数据已成功保存本地\t{file_path}')


def response_gain(_data_dict):
    """ 从字幕URLs中获取每种语言的字幕内容，并解析为字典格式 """
    subtitleUrls = _data_dict['timedTextUrls']['result']['subtitleUrls']
    typeList_All = {}
    for subtitle in subtitleUrls:
        displayName = subtitle.get('displayName')
        languageCode = subtitle.get('languageCode')
        url = subtitle.get('url')
        resp = requests.get(url).text
        # print(resp)
        subtitles = extract_subtitles(resp)
        # print(len(subtitles), subtitles)
        typeList_All.update({languageCode: subtitles})

    return typeList_All


def dispose():
    """ 获取所有字幕数据，提取中文字幕，并生成对应关系。 """
    with open('data.pkl', 'rb') as pf:
        data_list = pickle.load(pf)
    for _data_dict in data_list:

        typeDict_All = response_gain(_data_dict)
        print()
        zh_hans = typeDict_All.pop('zh-hans', None)
        if not zh_hans:
            print(f'当前字幕不存在中文!')
            return
        # print(dict_all)

        for language, type_All in typeDict_All.items():
            # print(type_All)
            for key, value in type_All.items():
                output_value = zh_hans.get(key)
                correspondence.append(
                    {'id': generate_md5(), 'input': output_value, 'output': value, 'language': language})
        print(f'数据获取成功! 当前视频的 数据量为:\t{len(correspondence)}')


if __name__ == '__main__':
    dispose()
    saveCorreJson()
