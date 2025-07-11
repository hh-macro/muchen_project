# -- coding: utf-8 --
# @Author: 胡H
# @File: doubport.py
# @Created: 2025/7/4 18:13
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc: 调用豆包AI接口 并执行OCR识别
import json
from typing import List, Dict

from openai import OpenAI, OpenAIError
import base64


class DoubaoAiPort:
    def __init__(self, encrypted_api_key: str, key: int):
        self.key = key
        self.api_key = self._decrypt_orf(encrypted_api_key)
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=self.api_key,
        )

    def _decrypt_orf(self, encrypted_text: str) -> str:
        return ''.join([chr(ord(char) ^ self.key) for char in encrypted_text])

    def _encrypt_ord(self, text, key):
        return ''.join(chr(ord(c) ^ key) for c in text)

    def image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode("utf-8")

    def recognize_image(self, image_path: str) -> str:
        """ 识别单张图，返回 JSON 字符串
        :param image_path:编码后的图片
        """

        try:
            base64_image = self.image_to_base64(image_path)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "现在我有手写书法文字图片，你需要将图片里面的文字内容识别下来，并按照顺序排列，返回json给我,两个项，一个图片路径(先为空)iamge_path，一个为图片结果内容content。记住是返回json格式。其中需要完全按照原图中内容，不能多字，不能少字"),
                        },
                    ],
                }
            ]
            response = self.client.chat.completions.create(
                model="doubao-seed-1-6-250615",
                messages=messages,
            )
            return response.choices[0].message.content
        except FileNotFoundError:
            return json.dumps({"error": f"文件未找到: {image_path}"}, ensure_ascii=False)
        except OpenAIError as e:
            return json.dumps({"error": f"OpenAI 接口错误: {str(e)}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": f"未知错误: {str(e)}"}, ensure_ascii=False)

    def recognize_batch(self, image_paths: List[str]) -> List[Dict[str, str]]:
        """ 批量识别图片，返回结果列表
        :param image_paths:
        :return:
        """
        """"""
        results = []
        for path in image_paths:
            result = self.recognize_image(path)
            results.append({
                "image_path": path,
                "result": result
            })
        return results

    def save_results_to_json(self, results: List[Dict[str, str]], output_path: str):
        """保存识别结果到 JSON 文件"""
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存 JSON 文件出错: {e}")


if __name__ == "__main__":
    key = int(input("请输入: "))
    encrypted_key = "ĤħųųĠŰŹŹŬĢŲųűŬŵŸŹųŬĠŵģųŬŴųŷŰŵŶģĤŶĥĠĠ"

    dbport = DoubaoAiPort(encrypted_key, key)
    result = dbport.recognize_image("89defae676abd3e3a42b41df17c40096.jpg")
    print(result)

    # image_files = ["img1.jpg", "img2.jpg", "img3.jpg"]
    # batch_results = dbport.recognize_batch(image_files)
    # dbport.save_results_to_json(batch_results, "output.json")
