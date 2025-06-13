# -- coding: utf-8 --
# @Author: 胡H
# @File: gain_display.py
# @Created: 2025/6/12 15:56
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import hashlib
import json
import os
import random
import time
import requests
from bs4 import BeautifulSoup
import urllib3
from pathlib import Path

from logg_init import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 消除证书不安全警告显示

current_file = Path(__file__).parent  # E:\AAA-project\muchen_project\karlsruhe


class ICSDClient:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "Origin": "https://icsd.fiz-karlsruhe.de",
            "Pragma": "no-cache",
            "Referer": "https://icsd.fiz-karlsruhe.de/display/list.xhtml",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.cookies2 = {
            "ICSDCHECK": "1749715159692",
            "JSESSIONID": "0904E580A55491728D1D2ECA0E354A11",
            "FIZ-Cookie": "289161869.16671.0000",
            "_pk_id.4.b153": "9f12b672c8c2c1e9.1749715170.",
            "_pk_ses.4.b153": "1",
            "mtm_consent_removed": "true",
            "piwikNoticeClosed": "true"
        }
        self.cookies1 = {
            '_pk_id.4.b153': 'dc235a62294ff2ed.1749637930.',
            'ICSDCHECK': '1749699576133',
            'FIZ-Cookie': '289161869.16671.0000',
            '_pk_ses.4.b153': '1',
            'mtm_consent_removed': 'true',
            'piwikNoticeClosed': 'true',
            'JSESSIONID': '6E5C3BA3D08D26D99148D0703D804334',
            'csfcfc': 'YEBqXBH4gYfWtkFgVbkCGdrsmVIamShAB6P1tXfYCeMCWO%2BIZQ%3D%3D',
        }

    def string_to_md5(self, string):
        md5_hash = hashlib.md5(string.encode()).hexdigest()
        return md5_hash

    def save_cif_file(self, down_url: str, down_path):
        """ 保存cif到本地
        :param down_url:
        :param down_path:
        :return:
        """
        response = requests.get(down_url, headers=self.headers, cookies=self.cookies1, verify=False)
        if response.status_code == 200:
            with open(down_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"CIF 文件已保存到: {down_path}")
        else:
            logger.error(f"下载失败，状态码: {response.status_code}")

    def save_to_json(self, data_list, file_path: Path, fileName):
        """ 将列表保存为本地 JSON 文件
        :param data_list: 列表数据
        :param file_path: 保存的文件路径
        """
        try:
            with open(f'{file_path}/{str(fileName)}.json', 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
            logger.success(f"数据成功保存到 {file_path}")
        except Exception as e:
            logger.error(f" 保存 JSON 文件出错: {e}")

    def fetch_page(self, url, data: dict = None, type_ver: str = None):
        """ 获取并解析页面内容 | 如果响应内容太短(小于1000字符), 尝试使用cookies2再次请求
        :param url:
        :param data:
        :param type_ver
        """

        def _make_request(current_cookies):
            if data:
                return self.session.post(
                    url,
                    headers=self.headers,
                    cookies=current_cookies,
                    timeout=10,
                    data=data,
                    verify=False
                )
            else:
                return self.session.get(
                    url,
                    headers=self.headers,
                    cookies=current_cookies,
                    timeout=10,
                    verify=False
                )

        response = _make_request(self.cookies1)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            logger.warning(f"状态码非200: {response.status_code}")
            return response.status_code

        if len(response.text) < 1000:
            logger.warning(" 响应内容过短，尝试使用备用 cookies2 重新请求...")
            response = _make_request(self.cookies2)
            response.encoding = 'utf-8'
            if response.status_code != 200:
                logger.error(f" 使用 cookies2 请求失败，状态码: {response.status_code}")
                return response.status_code

        response.raise_for_status()

        if type_ver and type_ver == 'xml':
            return BeautifulSoup(response.text, 'lxml')
        return BeautifulSoup(response.text, 'html.parser')

    def post_list_view(self, page: int, view_state: str, file_path: Path) -> list or int:
        """
        提交分页查询请求，抓取初始列表页
        :return: 请求响应文本
        """
        data = {
            'jakarta.faces.partial.ajax': 'true',
            'jakarta.faces.source': 'display_form:listViewTable',
            'jakarta.faces.partial.execute': 'display_form:listViewTable',
            'jakarta.faces.partial.render': 'display_form:listViewTable display_form:selectedRowsLabel',
            'jakarta.faces.behavior.event': 'page',
            'jakarta.faces.partial.event': 'page',
            'display_form:listViewTable_pagination': 'true',
            'display_form:listViewTable_first': f'{page}',
            'display_form:listViewTable_rows': '10',
            'display_form:listViewTable_skipChildren': 'true',
            'display_form:listViewTable_encodeFeature': 'true',
            'display_form': 'display_form',
            'display_form:j_idt46:shareLinkBackUrl': '#',
            'display_form:listViewTable_rppDD': '10',
            'display_form:listViewTable_selection': '',
            'display_form:listViewTable_columnOrder': 'display_form:listViewTable:j_idt71,display_form:listViewTable:listViewTableCollCodeColumn,display_form:listViewTable:j_idt74,display_form:listViewTable:j_idt82,display_form:listViewTable:j_idt90,display_form:listViewTable:j_idt96,display_form:listViewTable:j_idt110,display_form:listViewTable:j_idt118,display_form:listViewTable:listViewTableQualityTagColumn,display_form:listViewTable:downloadColumn',
            'display_form:listViewTable_resizableColumnState': '',
            'display_form:expName': 'YourCustomFileName',
            'display_form:expCelltype:input_input': 'experimental',
            'jakarta.faces.ViewState': f'{view_state}',
        }
        url = 'https://icsd.fiz-karlsruhe.de/display/list.xhtml'
        soup = self.fetch_page(url=url, data=data, type_ver='xml')
        if isinstance(soup, int):
            logger.warning(soup)
        # print(soup)
        tr_lis = soup.find_all('tr', attrs={"aria-selected": "false"})
        tr_list = []
        for _tr in tr_lis:

            td = _tr.select('td')
            icsd_code = td[1].text.strip()
            struct_from = td[3].text.strip()
            struct_type = td[4].text.strip()
            title = td[5].text.strip()
            reference = td[7].text.strip()
            try:
                data_rk = _tr.get('data-rk')
                down_url = f"https://icsd.fiz-karlsruhe.de/ws/cif/{data_rk}?celltype=experimental&windowsclient=true&filename=EntryWithCollCode{icsd_code}.cif"
                down_path = Path(file_path, f'EntryWithCollCode{icsd_code}.cif')
                self.save_cif_file(down_url, down_path)
                tr_list.append(
                    {"icsd_code": icsd_code, "struct_from": struct_from, "struct_type": struct_type, "title": title,
                     "reference": reference, "down_path": f'resultJson/EntryWithCollCode{icsd_code}.cif'})
            except Exception as e:
                logger.error(f"下载失败! -> {e}")
                tr_list.append(
                    {"icsd_code": icsd_code, "struct_from": struct_from, "struct_type": struct_type, "title": title,
                     "reference": reference, "down_path": ''})

        # print(tr_list)
        if len(tr_list) < 3:
            return tr_list == 0
        return tr_list

    def dispose_message(self):
        message_data = []
        view_state = '7595524056105717739:-4048064795409396653'
        fileName = self.string_to_md5(view_state)  # 转换md5
        file_path = Path(current_file, 'resultJson', fileName)
        os.makedirs(file_path, exist_ok=True)
        for page in range(0, 10, 10):
            time.sleep(random.uniform(0.9, 1.9))

            logger.info(f'正在获取 \t{view_state} \t第{page}页')
            tr_data_list = self.post_list_view(page, view_state, file_path)  # 核心获取
            if not tr_data_list:
                logger.info(f"{view_state}: \t已取完所有内容")
                break
            message_data.extend(tr_data_list)

        logger.success(f'已全部获取完毕! | 数据量为{len(message_data)}')

        self.save_to_json(message_data, file_path, fileName)  # 保存


if __name__ == "__main__":
    client = ICSDClient()
    html_text = client.dispose_message()
