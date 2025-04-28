# -- coding: utf-8 --
# @Author: 胡H
# @File: utils_combine.py
# @Created: 2025/4/7 14:54
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:  将文件夹下整理表格去重放入新表格
import os
import pandas as pd


def process_excel_files(input_dir, output_path):
    # 初始化一个空列表，用于存储所有数据
    all_data = []

    # 遍历输入目录中的所有文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(input_dir, file_name)

            # 读取 Excel 文件
            try:
                df = pd.read_excel(file_path)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue

            # 提取文件名（去掉扩展名）
            file_name_without_ext = os.path.splitext(file_name)[0]

            # 检查是否包含 'aria_label' 和 'href' 列
            if 'aria_label' in df.columns and 'href' in df.columns:
                # 提取需要的列
                df_subset = df[['aria_label', 'href']].copy()
                # 添加文件名列
                df_subset['file_name'] = file_name_without_ext
                # 将数据追加到总列表中
                all_data.append(df_subset)
            else:
                print(f"Columns 'aria_label' or 'href' not found in {file_name}")

    # 合并所有数据
    if all_data:
        merged_df = pd.concat(all_data, ignore_index=True)
    else:
        print("No valid data found.")
        return

    # 根据 'href' 列去重，保留第一次出现的记录
    merged_df.drop_duplicates(subset=['href'], keep='first', inplace=True)

    # 调整列顺序，将 'file_name' 放在第一列
    if 'file_name' in merged_df.columns:
        merged_df = merged_df.reindex(columns=['file_name', 'aria_label', 'href'])

    # 保存到新的 Excel 文件
    merged_df.to_excel(output_path, index=False)
    print(f"处理后的数据保存到 {output_path}")


# 示例调用
input_directory = "compilations"  # 输入目录
output_file = "disney_merged_data.xlsx"  # 输出文件路径

process_excel_files(input_directory, output_file)