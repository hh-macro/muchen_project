# -- coding: utf-8 --
# @Author: 胡H
# @File: id_one.py
# @Created: 2025/5/10 19:35
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import json
import os

def reorder_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 重新排序，将 id 放在第一位
    ordered_data = [{"id": item["id"], **{k: item[k] for k in item if k != "id"}} for item in data]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(ordered_data, f, ensure_ascii=False, indent=4)

# 指定目录路径
directory_path = 'output_one'

# 遍历目录下的所有 JSON 文件
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        reorder_json(file_path)