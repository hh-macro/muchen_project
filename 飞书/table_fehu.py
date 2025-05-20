# -- coding: utf-8 --
# @Author: 胡H
# @File: table_fehu.py
# @Created: 2025/5/20 14:15
# @LastModified:
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:

import requests
import json


class FeishuTableWriter:
    def __init__(self, app_id, app_secret, spreadsheet_token, sheet_id):
        """Initialize the FeishuTableWriter with credentials and table identifiers."""
        self.app_id = app_id
        self.app_secret = app_secret
        self.spreadsheet_token = spreadsheet_token
        self.sheet_id = sheet_id
        self.access_token = self._get_access_token()

    def _get_node_wiki(self):
        """获取知识空间节点信息"""
        headers = {
            "Authorization": "Bearer u-cNRtUk0Zdc3FqupXl.y0SLg13J.wkg2NjgG0kl6a2B.v"
        }
        url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node"
        params = {
            "obj_type": "wiki",
            "token": self.spreadsheet_token
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"GET间节点信息失败:  {response.text}")
        return response.json()["data"]["node"]

    def _get_access_token(self):
        """通过APP_ID和APP_SECRET获取租户访问令牌"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"POST访问令牌失败:  {response.text}")
        return response.json()["tenant_access_token"]

    # 获取当前行数
    def get_row_count(self, token):
        url = f"https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{SPREADSHEET_TOKEN}/sheets/{SHEET_ID}/meta"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("data", {}).get("rowCount", 0)

    def write_to_table(self, range, values):
        """批量写入Feishu表中指定范围的内容"""
        obj_token = self._get_node_wiki()['obj_token']
        url = f"https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{obj_token}/values"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "valueRange": {
                "range": f"{self.sheet_id}!{range}",
                "values": values
            }
        }
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        # print(response.text)
        if response.status_code != 200:
            raise Exception(f"Failed to write to table: {response.text}")
        return response.json()


if __name__ == "__main__":
    APP_ID = "cli_a8a140d29425d00b"
    APP_SECRET = "rOcyjHfKwhz6n5EFvXtKAdQIMwWKLJE2"
    SPREADSHEET_TOKEN = "O9upwWDiViOHMlkaqZJc47uJncg"
    SHEET_ID = "caaa6e"

    writer = FeishuTableWriter(APP_ID, APP_SECRET, SPREADSHEET_TOKEN, SHEET_ID)

    range_to_write = "A1:B2"
    values_to_write = [
        ["Name", "Age"],
        ["Alice", "25"]
    ]

    # 将数据写入表
    result = writer.write_to_table(range_to_write, values_to_write)
    print("Write result:", result)
