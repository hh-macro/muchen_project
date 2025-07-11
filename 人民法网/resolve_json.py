# -- coding: utf-8 --
# @Author: 胡H
# @File: resolve_json.py
# @Created: 2025/5/13 16:45
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc: 提取指定字段生成新JSON
import json

def extract_fields_to_new_json(input_file, output_file, fields_to_keep):
    """提取指定字段生成新JSON"""
    with open(input_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    # 提取目标字段
    new_data = []
    for item in original_data:
        new_item = {key: item.get(key) for key in fields_to_keep}
        new_data.append(new_item)

    # 保存新JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

# 用法示例
fields_to_extract = ["alsy", "dsrmc", "spnf", "dy", "fycj", "alh", "sjlx", "orglist/url"]
extract_fields_to_new_json("人民法院案例库/2025-04-23~2025-07-07rmfy案例库.json", "rmfy案例库子.json", fields_to_extract)