# -- coding: utf-8 --
# @Author: 胡H
# @File: json_combine.py
# @Created: 2025/5/9 23:49
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import json
import os
import glob
from collections import defaultdict


def merge_json_files(input_dir):
    """
    功能：合并指定目录下的所有JSON文件
    参数：
        input_dir - 包含JSON文件的目录路径
    返回：
        list - 合并后的所有JSON数据
    """
    merged_data = []

    # 遍历目录下所有.json文件
    for file_path in glob.glob(os.path.join(input_dir, "*.json")):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    print(f"警告：文件 {file_path} 根元素不是数组，已跳过")
            except json.JSONDecodeError:
                print(f"错误：文件 {file_path} 不是有效的JSON，已跳过")

    return merged_data


def normalize_languages(data):
    """
    功能：标准化language字段
    参数：
        data - 需要处理的JSON数据列表
    返回：
        list - 处理后的数据列表
    """
    for item in data:
        if "language" in item and item["language"] == "英语":
            item["language"] = "en"
    return data


def split_by_language(data, output_dir):
    """
    功能：按language字段分割数据并保存
    参数：
        data - 需要处理的数据列表
        output_dir - 输出目录路径
    """
    # 创建按language分类的字典
    lang_dict = defaultdict(list)

    for item in data:
        lang = item.get("language", "unknown")
        lang_dict[lang].append(item)

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 为每个language创建独立文件
    for lang, items in lang_dict.items():
        output_path = os.path.join(output_dir, f"{lang}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)


def main_process(input_dir, output_dir):
    """
    完整处理流程
    参数：
        input_dir - 输入目录（包含要合并的JSON文件）
        output_dir - 输出目录（用于保存分类后的JSON文件）
    """
    # 1. 合并所有JSON文件
    merged_data = merge_json_files(input_dir)
    print(f"成功合并 {len(merged_data)} 条记录")

    # 2. 标准化language字段
    normalized_data = normalize_languages(merged_data)

    # 3. 按language分割并保存
    split_by_language(normalized_data, output_dir)
    print("文件已按语言分类保存")


if __name__ == "__main__":
    # 使用示例
    main_process(
        input_dir="input_json",  # 替换为实际输入目录
        output_dir="output"  # 替换为实际输出目录
    )