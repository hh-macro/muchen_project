# -*- coding: utf-8 -*-
import base64
import json
import re
import time
from pathlib import Path
from datetime import datetime
import requests
from protobuf_to import GetByUserInit
import pymongo
from bson.json_util import dumps

client = pymongo.MongoClient("localhost", 27017)

db = client['doubao']
collection = db['data_list']
data_list: collection = db.data_list


# 对mangodb中 data_list 表中的内容进行re正则替换----将在线地址替换成本地地址
def re_mango():
    """ 对mangodb中 data_list 表中的内容进行re正则替换----将在线地址替换成本地地址 """
    pattern1 = re.compile(r'https:(.*?).png', re.IGNORECASE)
    pattern2 = re.compile(r'!\[img\]\(https:(.*?)\)', re.IGNORECASE)

    datee_name = time_date()  # 当前时间

    # 定义替换逻辑
    def dynamic_replacement(match, pattern_type):
        if pattern_type == 1:  # 第一种格式
            rout_img = 'https:' + match.group(1) + '.png'
        else:  # 第二种格式
            rout_img = 'https:' + match.group(1)
        try:
            # print('rout_img:\t', rout_img)
            image_content = requests.get(rout_img).content
            png_name = int(time.time() * 1000000)
            with open(rf'D:/aresult/{datee_name}/images/{png_name}.png', 'wb') as f:
                f.write(image_content)
            # print(f'{rout_img} ----保存成功')

            if pattern_type == 2:
                return rf"<img src='/aresult/{datee_name}/images/{png_name}.png' />"
            return rf"/aresult/{datee_name}/images/{png_name}.png"
        except Exception as e:
            print_red(f"{e}-----------------图片下载发送异常--返回原值")

    # 遍历集合中的文档
    for document in data_list.find():
        try:
            # rich_text = document['qa_biz_params']['qa_item_result']  # 确保提取字段内容
            rich_text = document.get('stem')  # 确保提取字段内容
            # print('rich_text:\t', rich_text)
            if not rich_text:
                continue
            rich_text_str = json.dumps(rich_text, ensure_ascii=False)

            if pattern2.search(rich_text_str):
                print("-匹配到第二种格式的 URL，进行替换")
                new_text = pattern2.sub(lambda m: dynamic_replacement(m, 2), rich_text_str)
            else:
                if pattern1.search(rich_text_str):
                    print("-匹配到第一种格式的 URL，进行替换")
                    new_text = pattern1.sub(lambda m: dynamic_replacement(m, 1), rich_text_str)
                else:
                    print("-未匹配到任何 URL，跳过替换")
                    new_text = rich_text_str
        except Exception as e:
            print_red(f"-文本解析或替换时发生异常: {e} ----- 替换操作 进行跳过!!!")
            continue

        # print("原文本:")
        # print(rich_text_str)
        # print("替换后的文本:")
        # print(new_text)

        # 将替换后的内容保存回 MongoDB
        try:
            if new_text != rich_text_str:
                updated_rich_text = json.loads(new_text)
                data_list.update_one(
                    {"_id": document["_id"]},
                    {"$set": {
                        "stem": updated_rich_text
                    }}
                )
                print("文档对图片地址----已更新")
            else:
                print("文档未更改")

            print("-" * 40)
        except Exception as e:
            print_red(f"更新 MongoDB 文档时发生异常：{e}")


# 文本前面加上红色前缀
def print_red(text):
    """ 文本前面加上红色前缀"""
    RED = "\033[31m"  # 红色
    RESET = "\033[0m"  # 重置颜色
    print(f"{RED}{text}{RESET}")


# 获取当前 年-月-日
def time_date():
    """ 获取当前 年-月-日"""
    current_datetime = datetime.now()
    return f"{current_datetime.year}-{current_datetime.month}-{current_datetime.day}"


# 检查父文件夹是否存在，如果不存在则创建父文件夹和所有子文件夹。
def create_parent_and_children():
    """  检查父文件夹是否存在，如果不存在则创建父文件夹和所有子文件夹。"""
    datee_name = time_date()
    parent_folder = rf"D:/aresult/{datee_name}"
    child_folders = ["images", "timu"]
    parent_path = Path(parent_folder)

    # 检查父文件夹是否存在，如果不存在则创建
    if not parent_path.exists():
        print(f"父文件夹 {parent_folder} 不存在，正在创建父文件夹及其子文件夹...")
        parent_path.mkdir(parents=True, exist_ok=True)  # 创建父文件夹
        # 创建所有子文件夹
        for child in child_folders:
            (parent_path / child).mkdir(exist_ok=True)
            print(f"已创建子文件夹：{parent_folder}/{child}")


# 对base64_strings.json 文件里面的base64编码进行去重操作
def the_frist():
    """ 对 base64_strings.json 文件里面的 base64 编码进行去重操作，同时保留原始的键 """
    file_path = 'base64_strings.json'

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            base64_list = json.load(file)  # 加载 Base64 字符串列表（列表中套字典）

        # 提取所有键值对
        key_value_pairs = [(list(item.keys())[0], list(item.values())[0]) for item in base64_list]

        # 去重操作：根据值（value）去重，但保留第一个出现的键（key）
        unique_values = set()
        unique_key_value_pairs = []
        for key, value in key_value_pairs:
            if value not in unique_values:
                unique_values.add(value)
                unique_key_value_pairs.append((key, value))

        # 将去重后的键值对重新包装为列表中套字典的形式
        unique_base64_list = [{key: value} for key, value in unique_key_value_pairs]

        # 保存去重后的数据到文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(unique_base64_list, file, ensure_ascii=False, indent=4)

        print(f"对 {file_path} 去重结果已经重新覆盖保存")
    except FileNotFoundError:
        print_red(f"文件 {file_path} 不存在！")
    except json.JSONDecodeError:
        print_red(f"文件 {file_path} 内容为空或格式错误！")


# 读取 base64_strings.json 中的内容、遍历、筛选出字符超过10000的、调用 unpack() 方法
def circulate():
    """ 读取 base64_strings.json 中的内容、遍历、筛选出字符超过10000的、调用 unpack() 方法 """
    file_path = "base64_strings.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            base64_list = json.load(file)  # 加载 Base64 字符串列表（列表中套字典）
    except FileNotFoundError:
        print_red(f"文件 {file_path} 不存在/位置错误！")
        base64_list = []
    except json.JSONDecodeError:
        print_red(f"JSON 解析错误: 大概率是 {file_path} 内容为空")
        base64_list = []

    # 遍历列表中的每个字典
    for i, item in enumerate(base64_list, start=1):
        for key_cache, base64_str in item.items():  # 提取字典中的键和值
            if len(base64_str) > 5000:
                print(f"第 {i} 个条目(键: {key_cache})的 base64 字符串长度超过 5000，正在处理...")
                unpack(base64_str, key_cache)  # 调用 unpack 方法处理
                print("---------------------------------------------------")


# # 打开文件并清空内容
def clear_json_file(file_path):
    # 打开文件并清空内容
    with open(file_path, "w", encoding="utf-8") as file:
        file.truncate()  # 清空文件内容
    print(f"文件 {file_path} 的内容已被完全清空。")


# 对data_list'表中的内容进行去重操作
def de_weigh_json():
    # 定义聚合管道
    # pipeline = [
    #     {
    #         "$addFields": {
    #             # 判断字段是否存在，并清理嵌套字段中的 HTML 标签
    #             "clean_text": {
    #                 "$trim": {
    #                     "input": {
    #                         "$replaceAll": {
    #                             # 如果 ocr_text 存在，使用 ocr_text，否则使用 analysis
    #                             "input": {
    #                                 "$ifNull": [
    #                                     "$qa_biz_params.qa_item_result.ocr_text",
    #                                     "$qa_biz_params.qa_item_result.analysis"
    #                                 ]
    #                             },
    #                             "find": "<.*?>",  # 匹配 HTML 标签
    #                             "replacement": ""
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     },
    #     {
    #         "$group": {
    #             "_id": "$clean_text",  # 按清理后的内容分组
    #             "firstDocument": {"$first": "$$ROOT"}  # 保留每组的第一条文档
    #         }
    #     },
    #     {
    #         "$replaceRoot": {"newRoot": "$firstDocument"}  # 恢复文档的原始结构
    #     }
    # ]

    # 执行聚合管道获取去重后的文档
    pipeline = [
        {
            "$group": {
                "_id": {
                    "$ifNull": ["$analysis", "stem"]  # 如果 $analysis 不存在，使用 stem
                },
                "firstDocument": {"$first": "$$ROOT"}  # 保留每组的第一条文档
            }
        },
        {
            "$replaceRoot": {"newRoot": "$firstDocument"}  # 恢复文档的原始结构
        }
    ]
    unique_documents = list(collection.aggregate(pipeline))

    # 提取唯一文档的 _id 列表
    unique_ids = [doc["_id"] for doc in unique_documents]

    # 删除集合中不在唯一列表中的文档
    original_count = collection.count_documents({})
    result = collection.delete_many({"_id": {"$nin": unique_ids}})
    deduplicated_count = collection.count_documents({})

    # 打印去重结果
    print(f"原始集合文档数量: {original_count}")
    print(f"删除的重复文档数量: {result.deleted_count}")
    print(f"去重后集合文档数量: {deduplicated_count}")
    print("-" * 51)


# 检查字符串是否包含中文字符
def contains_chinese(s):
    """检查字符串是否包含中文字符"""
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


# 将 unpack() 方法筛选成功的list追加存入 data_list.json 文件中"
def json_save_base64(filtered_list, key_cache):
    """ 将 unpack() 方法筛选成功的list存入 data_list表中"""
    jso1_list = [json.loads(saw2) for saw2 in filtered_list]
    # print('12123', len(jso1_list), jso1_list)
    # 向每个字典中添加一个新的键值对
    for item in jso1_list:
        item["image_name"] = key_cache

    try:
        result_dict = data_list.insert_many(jso1_list)
    except TypeError as e:
        print_red(jso1_list)
        print_red(f"数据转换或插入 MongoDB 表时发生了 Type Error: {e}")
        return
    print(f"已成功向 data_list 表中插入 {len(result_dict.inserted_ids)} 条数据。")


# 将mango表中数据转json
def mango_json():
    # 将mango表中数据转json
    documents = list(data_list.find({}))
    datee_name = time_date()  # 当前时间
    try:
        # 将文档导出为 JSON 文件
        with open(f"D:/aresult/{datee_name}/data_list.json", "w", encoding="utf-8") as outfile:
            outfile.write(dumps(documents, ensure_ascii=False))
        print("data_list.json导出成功")
    except Exception as e:
        print_red(f"数据转换或导出 JSON 表时发生了 Exception: {e}")


# 核心方法unpack() 对读取的 base64码  进行转换识别操作，再通过层层筛选，得到所需josn结果
def unpack(base64_str, key_cache):
    """ 核心方法 对读取的 base64码  进行转换识别操作，再通过层层筛选，得到所需josn结果 """
    dict_result = GetByUserInit().parse(base64.b64decode(base64_str)).to_json(indent=2)

    filtered_messages = []  # 存放 dict_result 包含中文的字段
    json_data = json.loads(dict_result)

    for inner_message in json_data.get("innerList", []):
        nested = inner_message.get("nested", {})
        deep_nested = nested.get("deepNested", [])
        for dn_message in deep_nested:
            card_stem = dn_message.get("cardStem", "")
            prompt_content = dn_message.get("promptContent", [])

            # 过滤 promptContent 中包含中文字符的 conText
            filtered_prompt_content = [
                item for item in prompt_content
                if contains_chinese(item.get("conText", ""))
            ]

            # 如果 cardStem 或 filtered_prompt_content 中包含中文字符 则保留该deepNestedMessage
            if contains_chinese(card_stem) or filtered_prompt_content:
                # 更新 dn_message 中的 promptContent 为过滤后的结果
                dn_message["promptContent"] = filtered_prompt_content
                filtered_messages.append(dn_message)

    print(len(filtered_messages), end=" ")
    print(filtered_messages)
    # # 去掉每个字典中的 cardStem 字段
    # for msg in filtered_messages:
    #     msg.pop("cardStem", None)
    #
    # print(len(filtered_messages), end=" ")
    # print(filtered_messages)

    # # promptContent字符为空的先去掉，再如果promptContent下面有多个conText，进行对比，保留字符最多的conText (下面)
    # processed_messages = []
    # # 遍历 filtered_messages 列表
    # for msg in filtered_messages:
    #     # 去掉 cardStem 字段
    #     msg.pop("cardStem", None)
    #
    #     # 获取 promptContent 字段
    #     prompt_content = msg.get("promptContent", [])
    #
    #     # 去掉 promptContent 为空的项
    #     if not prompt_content:
    #         continue
    #
    #     # 如果 promptContent 下面有多个 conText，保留字符最多的 conText
    #     max_length = -1
    #     longest_con_text_item = None
    #
    #     for item in prompt_content:
    #         con_text = item.get("conText", "")
    #         if len(con_text) > max_length:
    #             max_length = len(con_text)
    #             longest_con_text_item = item
    #
    #     # 保留字符最多的 conText
    #     msg["promptContent"] = [longest_con_text_item] if longest_con_text_item else []
    #
    #     # 添加处理后的消息到 processed_messages 列表
    #     processed_messages.append(msg)
    #
    # print(len(processed_messages), end=" ")
    # print(processed_messages)

    # 提取所有 conText 到一个单独的列表
    # con_texts = [item["conText"] for msg in processed_messages for item in msg["promptContent"]]
    # print(len(con_texts), end=" ")
    # print(con_texts)

    # 去重
    # unique_data = list(set(con_texts))
    # 输出结果
    # print(len(unique_data), end=" ")
    # print(unique_data)

    # print(json.dumps(unique_data, indent=4, ensure_ascii=False))

    # 处理数据：只保留 cardStem，去除 promptContent
    processed_data = [{"cardStem": item["cardStem"]} for item in filtered_messages]
    # processed_messages = json.dumps(processed_data, indent=4, ensure_ascii=False)
    # print(len(processed_data), end=" ")
    # print(processed_data)

    # 提取 cardStem 数据并封装成列表
    con_texts = [item["cardStem"] for item in processed_data if "cardStem" in item]
    # print(len(con_texts), end=" ")
    # print(con_texts)

    filtered_data = []
    for iteam in con_texts:
        try:
            # 解析 JSON 字符串
            parsed_item = json.loads(iteam)
            content = parsed_item.get("content", "")

            # 统计中文字符数量
            chinese_count = len(re.findall(r'[\u4e00-\u9fff]', content))

            # 如果中文字符数量小于 5，则保留
            if chinese_count > 5:
                filtered_data.append(parsed_item)
        except json.JSONDecodeError as e:
            print_red(f"解析 JSON 时发生错误: {e}")

    print(len(filtered_data), end=" ")
    print(filtered_data)

    filtered_list = []
    for ie1 in filtered_data:
        try:
            # 解析 JSON 字符串
            # parsed_item = json.loads(ie1)
            content_ie1 = ie1.get("content", "")

            # 检查 avatar_text 是否为 "有问题？向豆包提问"
            if "avatar_text" in content_ie1:
                content_dict = json.loads(content_ie1)
                if content_dict.get("avatar_text") == "有问题？向豆包提问":
                    continue  # 跳过该条目

            # 如果不满足条件，则保留该条目
            filtered_list.append(content_ie1)
        except json.JSONDecodeError as e:
            print_red(f"解析 JSON 时发生错误: {e}")
    print(len(filtered_list), end=" ")
    print(filtered_list)

    json_save_base64(filtered_list, key_cache)  # 存入 data_list 表中


if __name__ == '__main__':
    # unpack(base64_str)  # 单个测试

    create_parent_and_children()  # 检查父文件夹是否存在，如果不存在则创建父文件夹和所有子文件夹。

    the_frist()  # 对base64_strings.json 文件里面的base64编码进行去重操作

    circulate()  # man

    de_weigh_json()  # 对 data_list 表中的内容进行去重操作

    clear_json_file(file_path="base64_strings.json")  # 删除并重新创建 base64_strings.json

    re_mango()  # 对mangodb中 data_list 表中的内容进行re正则替换----将在线地址替换成本地地址

    mango_json()  # mango表转json


"""
第二代版本:在筛选的时候，将cardStem保留，去掉下级conText中的内容
        与第一版区别: 题目内容较为清晰, 且题目与AI解答所有页面全在一起

"""