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

    def _get_node_wiki(self) -> dict:
        """获取知识空间节点信息"""
        headers = {
            "Authorization": f"Bearer {self.access_token}"  # 使用动态获取的令牌
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

    def _get_access_token(self) -> str:
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

        # def get_row_count(self):
        #     """获取表格元数据 """
        #     obj_token = self._get_node_wiki()['obj_token']
        #     # url = f"https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{obj_token}/sheets/{self.sheet_id}/meta"
        #     url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{obj_token}/metainfo"
        #     headers = {"Authorization": f"Bearer {self.access_token}"}
        #     response = requests.get(url, headers=headers)
        #     # print(response.text)
        #     data = response.json()['data']
        #     sheets = data['sheets']
        #
        #     target_sheet = [sheet for sheet in sheets if sheet['sheetId'] == self.sheet_id]
        #     print(target_sheet)
        #     row_count = target_sheet[0].get("rowCount")

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
            raise Exception(f"写入表格失败: {response.text}")
        return response.json()


if __name__ == "__main__":
    APP_ID = "cli_a8a140d29425d00b"
    APP_SECRET = "rOcyjHfKwhz6n5EFvXtKAdQIMwWKLJE2"
    SPREADSHEET_TOKEN = "O9upwWDiViOHMlkaqZJc47uJncg"
    SHEET_ID = "caaa6e"

    writer = FeishuTableWriter(APP_ID, APP_SECRET, SPREADSHEET_TOKEN, SHEET_ID)

    title = ["Name", "Age", "gender"]
    data = ["Alice", "25", "man"]

    # 这里直接写入标题（根据需求调整）
    writer.write_to_table("A1:C1", [title])

    empty_row = 3
    # 写入数据
    result = writer.write_to_table(f"A{empty_row}:C{empty_row}", [data])
    print("写入成功:", result)
