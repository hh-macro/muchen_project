# -*- coding: utf-8 -*-
# @Time    : 2025/5/10 13:55
# @Author  : Soin
# @File    : json合并.py
# @Software: PyCharm
from pathlib import Path
import json
import re
import time
import random
import hashlib
from loguru import logger
"""
此代码实现的是合并json内容，将input的字符保持在40+当然这里看你实例化的时候传参
min_len就是字符长度

"""
y_num = 0
e_num = 0
class JsonMerger:

    def __init__(self, min_len, path):
        """

        :param min_len: 文本长度
        :param path: json所在的文件夹
        """

        logger.info(f"<---------------开始处理文件夹 {path} 中的 JSON 文件...--------------->")
        self.min_len = min_len
        self.folder_path = path


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

    def process_text(self, text):

        new_text = re.sub(r'[<（\[].*?[）>\]]', '', text)

        return new_text

    def process_data(self, json_data):
        global y_num,e_num
        new_json_data = []
        """
        这个函数实现的是，处理json的内容
        :return:
        """
        i = 0
        while i < len(json_data):
            # logger.debug(f"现在是：{json_data[i]}")
            lang = json_data[i].get('language', '')
            """
                这个while循环的目的就是通过循环的方法去搞，去遍历。
            """
            # 存在空值
            if not json_data[i]['input'] or not json_data[i]['output']:
                # print(f"这个被跳过了：{json_data[i]},因为是长度为0的")
                i += 1
                continue
            if 'NETFLIX' in json_data[i]['input'] or '-' in json_data[i]['input']:  # 如果有NETFLIX，或者- 则跳过  这个是废话
                # print(f"这个被跳过了：{json_data[i]},因为是废话")
                i += 1
                continue

            input_text = self.process_text(json_data[i]['input'])
            output_text = self.process_text(json_data[i]['output'])

            if len(input_text) == 0 or len(output_text) == 0:
                # print(f"这个被跳过了：{json_data[i]},因为是长度为0的")
                i += 1
                continue
            i += 1
            # 这里判断input_text 的长度也是通过while循环实现追加
            while i < len(json_data) and len(input_text) < self.min_len:
                # logger.debug(f"现在是：{json_data[i]}")
                # logger.debug(f"现在是：{json_data[i]}")


                # 存在空值
                if not json_data[i]['input'] or not json_data[i]['output']:
                    # print(f"这个被跳过了：{json_data[i]},因为是长度为0的")
                    i += 1
                    continue
                if len(json_data[i]['input']) == 0 or len(json_data[i]['output']) == 0:
                    # print(f"这个被跳过了：{json_data[i]},因为是长度为0的")
                    i += 1
                    continue
                if 'NETFLIX' in json_data[i]['input'] or '-' in json_data[i]['input']:  # 如果有NETFLIX，或者- 则跳过  这个是废话
                    # print(f"这个被跳过了：{json_data[i]},因为是废话")
                    i += 1

                    continue

                if json_data[i]['input'][-1] in ['.', '!', '?', '！', '？', '，', '。', ',']:
                    input_text += self.process_text(json_data[i]['input'])
                else:
                    input_text += "," + self.process_text(json_data[i]['input'])
                if json_data[i]['output'][-1] in ['.', '!', '?', '！', '？', '，', '。', ',']:
                    output_text += self.process_text(json_data[i]['output'])
                else:
                    output_text += "," + self.process_text(json_data[i]['output'])
                i += 1
            new_json_data.append({
                "input": input_text,
                "output": output_text,
                "language": lang,
                'id': self.generate_md5()
            })
            # i += 1
        logger.success(f"初始的句对数量:{len(json_data)}---->->-->处理后的句对数量:{len(new_json_data)}")
        y_num+=len(json_data)
        e_num+=len(new_json_data)
        return new_json_data

    def merge_json_files(self):
        """
        合并指定文件夹内的所有 JSON 文件，确保每条数据的 input 字符长度达到 min_length，并将处理后的数据替换原文件内容。
        拼接时使用逗号分隔每段内容，但避免重复逗号和符号。
        跳过含有 "-" 的数据，并移除 input 和 output 中被“（）”和“[]”包裹住的内容。

        :param min_length: 每条合并后的 input 字符串最小长度
        :param folder_path: 存放 JSON 文件的文件夹路径
        """

        # 配置：文件夹路径
        folder_path = Path(self.folder_path)

        # 读取并处理所有 json 文件内容
        for file in folder_path.glob('*.json'):
            all_data = []
            try:
                with file.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        all_data.append(data)
                    elif isinstance(data, list):
                        all_data.extend(data)
            except json.JSONDecodeError:
                logger.error(f"文件 {file.name} 解码失败，跳过")
                continue

            # 合并逻辑
            # merged = []
            # print(file.name)
            logger.debug(f">>>>>========正在处理文件 {file.name}========<<<<<")
            new_json_data = self.process_data(all_data)
            output_path_folder = Path(r'E:\Python\205-4\语料\网飞字幕筛选',Path(self.folder_path).name)

            output_path_folder.mkdir(parents=True, exist_ok=True)
            output_path = Path(output_path_folder,file.name)
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(new_json_data, f, ensure_ascii=False, indent=2)
            logger.success(f"处理成功,数据存储位置:{output_path}")
    # logger
            # break


if __name__ == '__main__':
    """
    这里是多文件夹的调用展示
    """
    # input_folder = Path(r"E:\Python\205-4\语料\合并")
    # # 获取到input_folder里面的全部的一级文件夹
    # for folder in input_folder.iterdir():
    #     if folder.is_dir():
    #         jm = JsonMerger(40, str(Path(input_folder, folder.name)))
    #         # print(folder.name)
    #         # output_file = Path(r"E:\Python\205-4\nexfy\yl\matched_subtitles.json")
    #         jm.merge_json_files()
    #         logger.success(f"全部处理完成！{y_num}=====>{e_num}")
    # 单文件夹调用:
    input_folder = Path(r"result_json")

    jm = JsonMerger(40, Path(input_folder))
    jm.merge_json_files()
            # break
    # jm = JsonMerger(40, r'D:\新建文件夹\WXWork\1688857125672560\Cache\File\2025-05\output')
    # # print(folder.name)
    # # output_file = Path(r"E:\Python\205-4\nexfy\yl\matched_subtitles.json")
    # jm.merge_json_files()
    # logger.success(f"全部处理完成！{y_num}=====>{e_num}")