# -- coding: utf-8 --
# @Author: 胡H
# @File: get_full.py
# @Created: 2025/6/9 16:32
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import hashlib
import json
import os
import uuid
from pathlib import Path

import requests
import urllib3
from bs4 import BeautifulSoup

from decorators import retry_request

current_file = Path(__file__).parent  # E:\AAA-project\muchen_project\projecteuclid

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PageFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }

        self.cookies = {
            "cookieconsent_status": "dismiss",
            "AdvancedSearchSave": "{\"AdvLogicTextFields\":[{\"logic\":\"AND\",\"text\":\"\",\"field\":\"ALL\"},{\"logic\":\"AND\",\"text\":\"\",\"field\":\"ALL\"},{\"logic\":\"AND\",\"text\":\"\",\"field\":\"ALL\"},{\"logic\":\"AND\",\"text\":\"\",\"field\":\"ALL\"},{\"logic\":\"AND\",\"text\":\"\",\"field\":\"ALL\"},{\"logic\":\"AND\",\"text\":\"\",\"field\":\"ALL\"},{\"logic\":\"AND\",\"text\":\"\",\"field\":\"ALL\"},{\"logic\":\"AND\",\"text\":\"\",\"field\":\"ALL\"}],\"AdvSearchWithin\":{\"Publications\":[],\"Collections\":[]},\"AdvSearchYears\":{\"Start\":\"\",\"End\":\"\",\"Single\":\"\"}}",
            "visid_incap_2482420": "OS32axZOTZKXQsESOMQrog2ZRmgAAAAAQUIPAAAAAACXqb/tbmj4nXFCXdBO3UbE",
            "ASP.NET_SessionId": "atngcuevsjidcnjespwhx2w5",
            "__RequestVerificationToken": "X9XAp7cs5FxXAQjqrJOjGiM_ABjrimDm1ZLgyshgzCH5eKJNlQlEP5gRQ4OPUS0Fv_IQIeBih4-rz6SMcF3bHcg3O501",
            "nlbi_2482420": "HzAVH2c5/Xjxj8ac6OT8qQAAAAB8SLQ1fdNUdJmo7EXRDiaa",
            "incap_ses_1838_2482420": "6F+TdG2CNhpjSo1Gi+OBGYmDR2gAAAAA8nZhSCx2WRkk0TvxxKOyLQ==",
            "incap_ses_84_2482420": "WbpiNzHqvXzs1sXX9m0qAfuGR2gAAAAApVAkGr5jea9XSUGqbjqMrQ==",
            "reese84": "3:CNoCsQ0NRwrMeBwGo7gRgA==:U5uo51OKgOZIB1fupYG/9qkDWHJJMd7maSZN5o5xeIfaTvdHVlj+Fgfi1C7R4ylvpbm0rKlIeVZfAxCQO1v9ntwxahVKz82IGIOrmZeY+WV0gPQrrQ0L1qXtIqOw31OJhn762XDL75nplyheoWhkebCKDt/X9hTpt96WWLn8E8ebBaW5WC7MV+v7vmmz0Nw6rl1a5kXJHMH5i78yzPpbmtFxyBUkd2dYbc04JcfA80OqBVxyaaER/t65tXZorhIQYz8iEIdgcdjDULZm32QXtg4pbJMy0n7hASdbChjjsIoRCkhtLpqnCwWp6iVxHGVpT4GWzhCl6FflB+v58jCS1ynuvFxkYIb0+GedCFzqddB7aDjarLVtKhBm8n7rOmrYu8UoaHuJS/TDEV6OmU4qZJ22KooNrZCVhjk9VChOBE6nvXqbhk6K15HqvfNkyRohDY/LGygPUCD9i7w6OBsZcg==:X9VElwsHZMvEBUvX10gF+MDiH3w6uNtrBXsXcQcvNj4=",
            "nlbi_2482420_2147483392": "bnxObCECiSlUD6b+6OT8qQAAAABuLY1fIGjxpf2xaP+JqNgh"
        }
        self.base_url = 'https://projecteuclid.org'

    @retry_request()
    def fetch_page(self, url):
        """
        发送 GET 请求并返回 BeautifulSoup 对象
        """
        response = self.session.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            timeout=10,
            verify=False
        )
        if response.status_code != 200:
            raise f'{response.status_code} \t请求错误! 请重试'
        response.encoding = 'utf-8'
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def save_json(self, data_dict, json_path):
        """
        追加保存字典到 JSON 文件中，格式为 list[dict]
        """
        if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON 文件内容不是列表")
        else:
            data = []

        data.append(data_dict)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def download_pdf(self, url, save_path):
        """
        下载 PDF 文件并以 URL 的 MD5 为文件名保存
        :param url: PDF 下载链接
        :param save_dir: 保存目录，如 'pdfs/'
        """
        response = self.session.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            timeout=20,
            stream=True,
            verify=False
        )
        response.raise_for_status()

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"PDF 已保存至: {save_path}")

    @retry_request(max_retries=5, delay=3, backoff=5)
    def gain_data(self, url, issn, save_path) -> dict:
        soup_data = fetcher.fetch_page(url)
        # print(soup_data)
        title = soup_data.select_one(".ProceedingsArticleOpenAccessHeaderText").text
        # down_href = self.base_url + soup_data.select_one('.ui-button.btn-DownloadPaper')['href']
        content_length = os.path.getsize(Path(current_file, save_path))  # 单位是字节
        proceedings_text = soup_data.select_one('.ProceedingsArticleOpenAccessText')
        author = '|'.join([span.text for span in proceedings_text.select('span')])
        doi_str = soup_data.select_one('.TocLineItemAnchorStyle').select('span')[-1].text
        # print(doi_str)
        doi = doi_str.replace("DOI:", "").strip()

        meta_tag = soup_data.find('meta', attrs={'name': 'dc.Language'})
        if meta_tag and 'content' in meta_tag.attrs:
            language = meta_tag['content']
        else:
            language = 'en'
        try:
            abstract = soup_data.select_one('.ArticleContentText div p').text
        except AttributeError as e:
            abstract = ""
            print(f'被反爬了 {e}')
            print(soup_data)
        crumbs_div = soup_data.select_one('.crumbs')
        category_strs = [crumbs.text for crumbs in crumbs_div.select('a')]
        category_str = [category.strip() for category in category_strs]
        span_tags = crumbs_div.select_one('.on').text
        print(category_str, span_tags)
        category_str.append(span_tags)
        category = '|'.join(category_str)
        immersives = soup_data.select('.KeyWordsPanel div')
        magazine = soup_data.select_one('.KeyWordsPanel div div a b').text
        volume = immersives[1].text

        pub_time = soup_data.select_one('.DetailDate span').text
        result_dict = {
            "track_id": str(uuid.uuid4()),
            "url": url,
            "relative_path": save_path,
            "file_type": "pdf",
            "file_format": "pdf",
            "content_length": content_length,
            "title": title,
            "author": author,
            "doi": doi,
            "language": language,
            "abstract": abstract,
            "category": category,
            "classification_code": "",
            "keyword": "",
            "magazine": magazine,
            "issn": issn,
            "volume": volume.strip(),
            "pub_time": pub_time,
        }
        return result_dict

    def get_browse(self, title_url: str = 'https://projecteuclid.org/browse/title/A') -> list:
        """ 获取当前类型的所有年份书籍大类
        :param: 传入一个链接：https://projecteuclid.org/browse/title/A
        :return: 返回当前类型的所有年份书籍大类 url列表
        """
        browse_list = []
        soup_browse = self.fetch_page(title_url)
        links_elements = soup_browse.select('[class="links"]')
        for links_element in links_elements:
            children = links_element.find_all(recursive=False)
            if children:
                last_child = children[-1]['href']
                browse_list.append(self.base_url + last_child)
        return browse_list

    def get_mathematica(self, brows: str) -> list:
        """获取大类下，所有年份的具体每年的url
        :param: brows: https://projecteuclid.org/journals/abstract-and-applied-analysis/issues
        :return:返回每个年份书籍的url列表
        """
        particulars_list = []
        soup_bro = self.fetch_page(brows)
        InnerTexts = soup_bro.select('.IssueByYearInnerText')
        for InnerText in InnerTexts:
            particulars_list.append(self.base_url + InnerText['href'])
        return particulars_list

    def large_number(self):
        part_url = 'https://projecteuclid.org/journals/abstract-and-applied-analysis/volume-2014/issue-SI23'
        soup_issue = self.fetch_page(part_url)
        down_urls = [self.base_url + group['href'] for group in soup_issue.select('.form-group.DownloadSaveButton1')]
        page_urls = [self.base_url + issue['href'] for issue in soup_issue.select('.TocLineItemAnchorText1')]

        self.fetch_page(f'{part_url}')

        for down_url, page_url in zip(down_urls, page_urls):
            md5_filename = hashlib.md5(down_url.encode('utf-8')).hexdigest() + ".pdf"
            # save_dir = r'E:\AAA-project\muchen_project\projecteuclid\save_pdf'
            save_dir = Path(current_file, 'save_pdf')
            os.makedirs(save_dir, exist_ok=True)
            save_path = Path('save_pdf', md5_filename)
            print(page_url, save_path)
            self.download_pdf(down_url, Path(current_file, save_path))  #
            issn = "1687-0409"
            result_dict = self.gain_data(f'{page_url}?tab=ArticleLink', issn, save_path)  #
            json_path = Path(current_file, 'projecteuclid1.json')
            print(result_dict)
            self.save_json(result_dict, json_path)  # 读取再存入


if __name__ == "__main__":
    fetcher = PageFetcher()
    # fetcher.large_number()
    print(fetcher.get_mathematica('https://projecteuclid.org/journals/abstract-and-applied-analysis/issues'))
