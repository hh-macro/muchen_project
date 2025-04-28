# -*- coding: utf-8 -*-
import base64
import json
from pathlib import Path
from protobuf_to import GetByUserInit


# 对base64_strings.json 文件里面的base64编码进行去重操作
def the_frist():
    """ 对base64_strings.json 文件里面的base64编码进行去重操作 """
    file_path = '../base64_strings.json'

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            base64_list = json.load(file)  # 加载 Base64 字符串列表
        unique_base64_list = list(set(base64_list))
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(unique_base64_list, file, ensure_ascii=False, indent=4)

        print(f"对 {file_path} 去重结果已经重新覆盖保存")
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在！")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的 JSON 格式!")


# 读取 base64_strings.json 中的内容、遍历、筛选出字符超过10000的、调用 unpack() 方法
def circulat():
    """  读取 base64_strings.json 中的内容、遍历、筛选出字符超过10000的、调用 unpack() 方法"""
    file_path = "../base64_strings.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            base64_list = json.load(file)  # 加载 Base64 字符串列表
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在/位置错误！")
        base64_list = []

    for i, base64_str in enumerate(base64_list, start=1):
        if len(base64_str) > 10000:
            # print(base64_str)
            unpack(base64_str)
            print("---------------------------------------------------")
            continue


def clear_json_file(file_path):
    # 打开文件并清空内容
    with open(file_path, "w", encoding="utf-8") as file:
        file.truncate()  # 清空文件内容
    print(f"文件 {file_path} 的内容已被完全清空。")


# 对data_list.json'中的内容进行去重操作
def de_weigh_json(item):
    """ 对data_list.json'中的内容进行去重操作  item为文件选择"""
    file_path = rf'E:\AAA-project\muchen_project\豆包爱学\aitutor_pro\result\data_list_{item}.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"出现错误: {file_path} 文件为空！")
    # 如果列表中的元素是字符串或数字，可以直接使用 set
    if all(isinstance(item, (str, int, float)) for item in data):
        unique_data = list(set(data))
    else:
        # 如果列表中的元素是字典或列表，需要先将其转换为不可变类型（如元组）
        unique_data = []
        seen = set()
        for item in data:
            # 将字典或列表转换为元组
            item_tuple = tuple(item.items()) if isinstance(item, dict) else tuple(item)
            if item_tuple not in seen:
                seen.add(item_tuple)
                unique_data.append(item)

    # 输出去重后的列表
    print(len(unique_data), end=' ')
    print('去重后', unique_data)

    # 可以选择将去重后的列表写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)
        print(f"去重后的列表已重新保存")


# 检查字符串是否包含中文字符
def contains_chinese(s):
    """检查字符串是否包含中文字符"""
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


# 将 unpack() 方法筛选成功的list追加存入 data_list.json 文件中"
def json_save_base64(filtered_list, max_items_per_file=50000):
    """ 将 unpack() 方法筛选成功的list存入 data_list.json 文件中"""
    item = 0
    file_path = rf"E:\AAA-project\muchen_project\豆包爱学\aitutor_pro\result\data_list_{item}.json"

    while True:
        try:
            # 尝试读取现有 JSON 文件
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)  # 加载现有数据
            item_count = len(existing_data)
            print(f"文件 {file_path} 中的列表数量为：{item_count}")

            # 如果文件已满，切换到下一个文件
            if item_count >= max_items_per_file:
                print(f"文件 {file_path} 已满，切换到下一个文件。")
                item += 1
                file_path = rf"E:\AAA-project\muchen_project\豆包爱学\aitutor_pro\result\data_list_{item}.json"
                continue

            # 如果文件未满，追加数据
            existing_data.extend(filtered_list)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)
            print(f"数据已成功追加到 {file_path} 文件中。")
            break

        except (FileNotFoundError, json.JSONDecodeError):
            print(f"文件 {file_path} 不存在或内容为空，将初始化为空列表。")
            existing_data = []

        # 如果文件为空或格式错误，写入新数据
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(filtered_list, file, ensure_ascii=False, indent=4)
        print(f"数据已成功写入到新文件 {file_path} 中。")
        break


# 核心方法unpack() 对读取的 base64码  进行转换识别操作，再通过层层筛选，得到所需josn结果
def unpack(base64_str):
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

    # 去掉每个字典中的 cardStem 字段
    for msg in filtered_messages:
        msg.pop("cardStem", None)

    print(len(filtered_messages), end=" ")
    print(filtered_messages)

    # promptContent字符为空的先去掉，再如果promptContent下面有多个conText，进行对比，保留字符最多的conText (下面)
    processed_messages = []
    # 遍历 filtered_messages 列表
    for msg in filtered_messages:
        # 去掉 cardStem 字段
        msg.pop("cardStem", None)

        # 获取 promptContent 字段
        prompt_content = msg.get("promptContent", [])

        # 去掉 promptContent 为空的项
        if not prompt_content:
            continue

        # 如果 promptContent 下面有多个 conText，保留字符最多的 conText
        max_length = -1
        longest_con_text_item = None

        for item in prompt_content:
            con_text = item.get("conText", "")
            if len(con_text) > max_length:
                max_length = len(con_text)
                longest_con_text_item = item

        # 保留字符最多的 conText
        msg["promptContent"] = [longest_con_text_item] if longest_con_text_item else []

        # 添加处理后的消息到 processed_messages 列表
        processed_messages.append(msg)

    print(len(processed_messages), end=" ")
    print(processed_messages)

    # 提取所有 conText 到一个单独的列表
    con_texts = [item["conText"] for msg in processed_messages for item in msg["promptContent"]]
    # print(len(con_texts), end=" ")
    # print(con_texts)

    # 去重
    unique_data = list(set(con_texts))
    # 输出结果
    # print(len(unique_data), end=" ")
    # print(unique_data)

    # print(json.dumps(unique_data, indent=4, ensure_ascii=False))

    filtered_list = []
    for item in unique_data:
        try:
            data = json.loads(item)
            if 'a:prompt_replace' not in data or len(data['a:prompt_replace']) > 10:
                filtered_list.append(item)
        except json.JSONDecodeError:
            continue
    print(len(filtered_list), end=" ")
    print(filtered_list)

    json_save_base64(filtered_list)  # 存入 data_list.json 文件中


if __name__ == '__main__':
    base64_str = """
CMgBELHeBxgAIgJPSygAMsEYwgy9GAqnAwoTNzQ2MDQ0Njg5ODYyMTU5NTk1NhACGKOQmIDfpbXEZyAAKLSChdDVnbXEZzDRhgM4o72gvYTN0wVCgQF7ImNvbW1hbmRfdHlwZSI6NCwiY29udmVyc2F0aW9uX2lkIjoiNzQ2MDQ0Njg5ODYyMTU5NTk1NiIsImNvbnZlcnNhdGlvbl90eXBlIjoyLCJjb252ZXJzYXRpb25fdmVyc2lvbiI6MTczNzAyMDcyMSwiaW5ib3hfdHlwZSI6MH1KOwoTczpjbGllbnRfbWVzc2FnZV9pZBIkNzUyZWFlZTUtZGY1My00ZWViLWE2YzUtNWI3NTUyYjU5MDM0Si0KHHM6c2VydmVyX21lc3NhZ2VfY3JlYXRlX3RpbWUSDTE3MzcwMjA3MjE0NDVKHQoJczp2aXNpYmxlEhAzMTgyNDM0NTI5NTgyNzU1UKSSg/TGMlgAYABoAHJMTVM0d0xqQUJBQUFBc0tJc2RaVEcxRGk1NXFKZE9mekw0WEJZUnZYNmp1WjhFN3RpY2psSGpwQjhTZ0ZVbnJxZWhJbTg4el9qRWZtQYgBAAqFFQoTNzQ2MDQ0Njg5ODYyMTU5NTk1NhACGI+QoLDcpbXEZyAAKLSChdDVnbXEZzDShgM4h/EeQqgKeyJjYXJkX3R5cGUiOjIwLCJjb250ZW50Ijoie1wiYXZhdGFyX3RleHRcIjpcIuaciemXrumimO+8n+WQkeixhuWMheaPkOmXrlwiLFwiYXZhdGFyX2ltYWdlXCI6e1widXJpXCI6XCJcIixcInVybFwiOlwiaHR0cHM6Ly9wMy1oaXBwby11c2VyLmJ5dGVpbWcuY29tL3Rvcy1jbi1pLWo0ZnIxdDY3bDYvYXZhdG9yX2ZpeC5wbmd+dHBsdi1qNGZyMXQ2N2w2LWltYWdlLmltYWdlXCJ9fSIsInRyYW5zZmVyX3R5cGUiOjIsIm1vdW50X3VuaXQiOlt7Im1vdW50X3R5cGUiOjEsIm9wdCI6eyJvcHRfaWQiOjAsIm9wdF90eXBlIjoxLCJvcHRfY29udCI6IuWIhuW8j+S4jeetieW8j+acieS7gOS5iOeJueeCuSIsImFmdGVyX2NsaWNrX3R5cGUiOjIsImhhc19jaG9vc2VuIjpmYWxzZSwiYXNzb2NpYXRlZF9pdGVtIjp7ImFzc29jaWF0ZWRfaXRlbV90eXBlIjozLCJhc3NvY2lhdGVkX2l0ZW1faWQiOjAsImFzc29jaWF0ZWRfaXRlbV9pbmZvIjoie1wiZmFxX2lkXCI6MCxcInF1ZXN0aW9uX3R5cGVcIjowLFwiZmFxX3NvdXJjZVwiOjgsXCJpc19maXJzdFwiOnRydWV9In0sImludGVuZCI6MywiY2FuX3Nob3dfaW5fcGxhY2Vob2xkZXIiOnRydWV9fSx7Im1vdW50X3R5cGUiOjEsIm9wdCI6eyJvcHRfaWQiOjEsIm9wdF90eXBlIjoxLCJvcHRfY29udCI6IuWmguS9leWIpOaWreWIhuWtkOWIhuavjeeahOato+i0n+aApyIsImFmdGVyX2NsaWNrX3R5cGUiOjIsImhhc19jaG9vc2VuIjpmYWxzZSwiYXNzb2NpYXRlZF9pdGVtIjp7ImFzc29jaWF0ZWRfaXRlbV90eXBlIjozLCJhc3NvY2lhdGVkX2l0ZW1faWQiOjAsImFzc29jaWF0ZWRfaXRlbV9pbmZvIjoie1wiZmFxX2lkXCI6MCxcInF1ZXN0aW9uX3R5cGVcIjowLFwiZmFxX3NvdXJjZVwiOjgsXCJpc19maXJzdFwiOnRydWV9In0sImludGVuZCI6MywiY2FuX3Nob3dfaW5fcGxhY2Vob2xkZXIiOnRydWV9fSx7Im1vdW50X3R5cGUiOjEsIm9wdCI6eyJvcHRfaWQiOjIsIm9wdF90eXBlIjoxLCJvcHRfY29udCI6IuS4uuS7gOS5iOW9k1xcKHgrMVx1MDAzYzBcXCnkuJRcXCh4IC0gMVx1MDAzZTBcXCnml7bml6Dop6MiLCJhZnRlcl9jbGlja190eXBlIjoyLCJoYXNfY2hvb3NlbiI6ZmFsc2UsImFzc29jaWF0ZWRfaXRlbSI6eyJhc3NvY2lhdGVkX2l0ZW1fdHlwZSI6MywiYXNzb2NpYXRlZF9pdGVtX2lkIjowLCJhc3NvY2lhdGVkX2l0ZW1faW5mbyI6IntcImZhcV9pZFwiOjAsXCJxdWVzdGlvbl90eXBlXCI6MCxcImZhcV9zb3VyY2VcIjo4LFwiaXNfZmlyc3RcIjp0cnVlfSJ9LCJpbnRlbmQiOjMsImNhbl9zaG93X2luX3BsYWNlaG9sZGVyIjpmYWxzZX19XSwic3RyZWFtX2tleSI6IiJ9ShEKDHM6ZWRpdF9jb3VudBIBMUqtAwoLYTpiaXpfcGFyYW0SnQN7ImJpel9hcHBfaWQiOjUyMDk0NywiYml6X3NjZW5lcyI6NSwicWFfYml6X3BhcmFtcyI6eyJzZWFyY2hfaWQiOjE4MjEzOTgxNjY0OTIyMDgsInJlc19pZCI6MTgyMTM5ODE3MzcxMTQwOCwiaXRlbV9pZCI6MCwiZGVwYXJ0bWVudCI6Mywic3ViamVjdCI6MiwicWFfaXRlbV9yZXN1bHQiOnsic2VhcmNoX2lkIjoxODIxMzk4MTY2NDkyMjA4LCJyZXNfaWQiOjE4MjEzOTgxNzM3MTE0MDgsIml0ZW1faWQiOjAsInJpY2hfdGV4dCI6IiIsIm9jcl90ZXh0IjoiIiwiYW5zd2VyIjoiIiwiaXNfb3JpZ2luIjp0cnVlLCJjYW5fbGxtX3NvbHZlZCI6ZmFsc2UsIm1hcmtkb3duX2dyYXlfcHVibGlzaCI6dHJ1ZSwiaGFzX2hpbnQiOnRydWUsImRldGVjdGlvbl90eXBlIjoyLCJzZWFyY2hfdHlwZSI6MX0sImVudHJhbmNlX3R5cGUiOjh9fUoqChNzOnNlcnZlcl9tZXNzYWdlX2lkEhM3NDYwNDQ3MTE5MjAwMjQxNjk5SjQKEGE6ZXZlbnRfdHJhY2tpbmcSIHsibXNnX3N1Yl90eXBlIjoicWFfbGxtX3Jlc3VsdCJ9SgsKBnM6bW9kZRIBMEp3ChNzOmNsaWVudF9tZXNzYWdlX2lkEmBhcHBfaWQ6NTIwOTQ3OmJvdDpDb21iaW5lUWFCb3Q6cmVwbHlfdG9fbXNnOjA6ZXh0cmE6Y29udmVyc2F0aW9uOjc0NjA0NDY4OTg2MjE1OTU5NTY6dHlwZTphdmF0YXJK6QEKCXM6YWRkX2V4dBLbAXsiYTplbW90aW9uIjoie1wiZW1vdGlvbl9pbnRlbnNpdHlcIjoxLFwiZW1vdGlvbl90eXBlXCI6OH0iLCJhOmV2ZW50X3RyYWNraW5nIjoie1wibXNnX3N1Yl90eXBlXCI6XCJxYV9sbG1fcmVzdWx0XCJ9IiwiYTppbnRlbmQiOiIxIiwiYTpxYV9zZWFyY2hfcmVzdWx0X2lkIjoiMTgyMTM5ODE2NjQ5MjIwODoxODIxMzk4MTczNzExNDA4IiwiYTpzY2hvb2xfZGVwYXJ0bWVudCI6IjMifUoYChNhOnNjaG9vbF9kZXBhcnRtZW50EgEzSjUKCWE6ZW1vdGlvbhIoeyJlbW90aW9uX2ludGVuc2l0eSI6MSwiZW1vdGlvbl90eXBlIjo4fUo6ChVhOnFhX3NlYXJjaF9yZXN1bHRfaWQSITE4MjEzOTgxNjY0OTIyMDg6MTgyMTM5ODE3MzcxMTQwOEotChxzOnNlcnZlcl9tZXNzYWdlX2NyZWF0ZV90aW1lEg0xNzM3MDIwNzIxNDQzSg0KCGE6aW50ZW5kEgExShMKCXM6Yml6X2FpZBIGNTIwOTQ3Sl4KC3M6ZWRpdF9pbmZvEk97ImNvbnRlbnRfaXNfZWRpdGVkIjp0cnVlLCJjb250ZW50X2VkaXRvciI6MCwiY29udGVudF9lZGl0X3RpbWUiOjE3MzcwMjA3MjE0MjV9UKOSg/TGMliRkoP0xjJgAGgAcjdNUzR3TGpBQkFBQUEycUExeEdpNmI4cmhqeWotM1RvNk9fMEgzdm5OV0ZIUTJVNTh4OTVWRElniAEAEPil2bj6+YoDGAA6IjIwMjUwMTE2MTc0NjU4QUJFMTk5MDFEQjg3MzIwRDFCMzRQmIyJ9MYyWK2MifTGMg==
    """
    # unpack(base64_str)  # 单个测试
    the_frist()  # 对base64_strings.json 文件里面的base64编码进行去重操作
    circulat()
    dir_path = ""
    path_a = Path(dir_path)

    file_count = sum(1 for entry in path_a.iterdir() if entry.is_file())

    de_weigh_json(item=0)  # 对data_list.json'中的内容进行去重操作, item为

    clear_json_file(file_path="../base64_strings.json")  # 删除并重新创建 base64_strings.json
