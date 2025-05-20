# -- coding: utf-8 --
# @Author: 胡H
# @File: replace_json.py
# @Created: 2025/5/13 16:46
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:用新JSON替换原JSON中的对应数据
import json


def update_original_with_new_data(original_file, new_data_file, output_file, key_field):
    """通过关键字段更新原JSON数据"""
    # 读取原数据和新数据
    with open(original_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    with open(new_data_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    # 建立新数据映射（以关键字段为索引）
    new_data_map = {item[key_field]: item for item in new_data}

    # 更新原数据
    for item in original_data:
        key_value = item.get(key_field)
        if key_value in new_data_map:
            item.update(new_data_map[key_value])

    # 保存更新后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(original_data, f, ensure_ascii=False, indent=2)


# 用法示例（以 orglist/url 为关键字段）
update_original_with_new_data(
    original_file="2024-12-31~2025-04-24rmfy案例库.json",
    new_data_file="rmfy案例库子_merged.json",
    output_file="new-2024-12-31~2025-04-24rmfy案例库.json",
    key_field="orglist/url"
)
