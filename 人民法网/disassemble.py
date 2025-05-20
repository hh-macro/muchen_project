# -- coding: utf-8 --
# @Author: 胡H
# @File: disassemble.py
# @Created: 2025/5/13 16:45
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:将JSON文件拆分为两个
import json


def split_json_file(input_file, output_file1, output_file2, split_index=None):
    """拆分JSON为两个文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 自动计算拆分点（如果未指定）
    if split_index is None:
        split_index = len(data) // 2

    # 拆分数据
    part1 = data[:split_index]
    part2 = data[split_index:]

    # 保存拆分结果
    with open(output_file1, 'w', encoding='utf-8') as f:
        json.dump(part1, f, ensure_ascii=False, indent=2)
    with open(output_file2, 'w', encoding='utf-8') as f:
        json.dump(part2, f, ensure_ascii=False, indent=2)


def merge_json_files(input_file1, input_file2, output_file):
    """合并两个JSON文件为一个"""
    # 读取第一个文件
    with open(input_file1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)

    # 读取第二个文件
    with open(input_file2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)

    # 合并数据
    merged_data = data1 + data2

    # 保存合并结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)


# # 用法示例（自动从中间拆分）
# split_json_file(
#     input_file="rmfy案例库子.json",
#     output_file1="rmfy案例库子1.json",
#     output_file2="rmfy案例库子2.json"
# )

# 用法示例（合并两个文件）
merge_json_files(
    input_file1="rmfy案例库子1.json",
    input_file2="rmfy案例库子2.json",
    output_file="rmfy案例库子_merged.json"
)