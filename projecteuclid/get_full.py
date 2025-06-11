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
import random
import time
import uuid
from pathlib import Path
import requests
import urllib3
from bs4 import BeautifulSoup
from pymongo import MongoClient
from fake_useragent import UserAgent

from decorators import retry_request
from logger_init import logger
from mgPaginator import MongoPaginator

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
current_file = Path(__file__).parent  # E:\AAA-project\muchen_project\projecteuclid

client = MongoClient(
    'mongodb://root:Aliyun_Mongo_20250218@dds-2vc3c96a7e797ee41197-pub.mongodb.cn-chengdu.rds.aliyuncs.com:3717,dds-2vc3c96a7e797ee42971-pub.mongodb.cn-chengdu.rds.aliyuncs.com:3717/admin?replicaSet=mgset-1150525521')
db = client['projecteuclid']
projecteuclidResult = db['projecteuclidResult']
awaitResult = db['awaitResult']
ua = UserAgent()


def proxy_pool(max_retries=3):
    """
    管理代理池，提供随机代理选择和简单的失败重试机制。
    :return dict: 随机选择的代理，或None如果所有代理都不可用
    """
    proxies = [
        {'http': 'socks5://182.42.139.81:11752', 'https': 'socks5://182.42.139.81:11752'},
        {'http': 'socks5://124.236.46.230:18362', 'https': 'socks5://124.236.46.230:18362'},
        {'http': 'socks5://106.227.48.126:12811', 'https': 'socks5://106.227.48.126:12811'}
    ]
    if not proxies:
        return None
    for _ in range(max_retries):
        proxy = random.choice(proxies)
        try:
            # 可添加代理验证逻辑
            return proxy
        except Exception:
            continue
    return None


class PageFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "user-agent": ua.random
        }
        self.base_url = 'https://projecteuclid.org'

    def init_cookie(self):
        # 第一次访问主页或某个页面来让网站设置 cookie
        self.headers["User-Agent"] = ua.random
        resp = self.session.get(self.base_url, headers=self.headers, timeout=15)
        resp.raise_for_status()
        logger.info(f"动态获取 cookie: {self.session.cookies.get_dict()}")

    @retry_request(max_retries=5, delay=2, backoff=4)
    def fetch_page(self, url):
        """
        发送 GET 请求并返回 BeautifulSoup 对象
        """
        response = self.session.get(
            url,
            headers=self.headers,
            # cookies=self.cookies,
            timeout=10,
            verify=False,
            # proxies=proxy_pool()
        )
        if response.status_code != 200:
            raise Exception(f'{response.status_code} 请求错误!')
        response.encoding = 'utf-8'
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def save_json(self, data_dict, json_path):
        """
        追加保存字典到 JSON 文件中，格式为 list[dict]
        """
        try:
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
        except Exception as e:
            logger.error(f"[save_json] 保存失败: {e}")  #

    def download_pdf(self, url, save_path):
        """
        下载 PDF 文件并以 URL 的 MD5 为文件名保存
        :param url: PDF 下载链接
        :param save_dir: 保存目录，如 'pdfs/'
        """
        try:
            response = self.session.get(
                url,
                headers=self.headers,
                # cookies=self.cookies,
                timeout=20,
                stream=True,
                verify=False,
                # proxies=proxy_pool()
            )
            # print(response.status_code)
            response.raise_for_status()

            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logger.info(f"PDF 已保存至: {save_path}")
        except Exception as e:
            logger.error(f"[download_pdf] 下载失败: {url} 错误: {e}")  #
            raise

    @retry_request(max_retries=5, delay=3, backoff=5)
    def gain_data(self, url, issn, save_path) -> dict:
        soup_data = self.fetch_page(url)
        # print(soup_data)
        title_type = soup_data.select_one(".ProceedingsArticleOpenAccessHeaderText")
        if not title_type:
            raise f'{title_type} 为空，ip被封或者触发网站反爬机制'
        title = title_type.text
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
            logger.warning(f"[gain_data] 抽取摘要失败! 可能被反爬: {e}")
            # print(soup_data)
        crumbs_div = soup_data.select_one('.crumbs')
        category_strs = [crumbs.text for crumbs in crumbs_div.select('a')]
        category_str = [category.strip() for category in category_strs]
        span_tags = crumbs_div.select_one('.on').text
        # print(category_str, span_tags)
        category_str.append(span_tags)
        category = '|'.join(category_str)
        immersives = soup_data.select('.KeyWordsPanel div div')
        magazine = soup_data.select_one('.KeyWordsPanel div div a b').text
        volume = immersives[1].text

        pub_time = soup_data.select_one('.DetailDate span').text
        result_dict = {
            "track_id": str(uuid.uuid4()),
            "url": url,
            "relative_path": save_path.as_posix(),
            "file_type": "pdf",
            "file_format": "paper",
            "content_length": content_length,
            "title": title,
            "author": author,
            "doi": doi,
            "language": language,
            "abstract": abstract,
            "category": category,
            # "classification_code": "",
            # "keyword": "",
            "magazine": magazine,
            "issn": issn,
            "volume": volume.strip(),
            "pub_time": pub_time,
        }
        return result_dict

    def get_browse(self, title_url: str) -> list:
        """ 获取当前类型的所有年份书籍大类
        :param: 传入一个链接：https://projecteuclid.org/browse/title/A
        :return: 返回当前类型的所有年份书籍大类 url列表
        """
        try:
            browse_list = []
            soup_browse = self.fetch_page(title_url)
            links_elements = soup_browse.select('[class="links"]')
            for links_element in links_elements:
                children = links_element.find_all(recursive=False)
                if children:
                    last_child = children[-1]['href']
                    browse_list.append(self.base_url + last_child)
            return browse_list

        except Exception as e:
            logger.error(f"[get_browse] 获取失败: {e}")

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

    def get_details_dict(self, brows: str) -> dict:
        """处理url并将url格式改为其他视图并继续请求获取 ISSN | 注：只处理单个url
        :param: 处理后的 -> brows_url: https://projecteuclid.org/journals/abstract-and-applied-analysis/scope-and-details
        :return: 返回所需字符信息字典
        """
        brows_url = brows.split('/issue')[0] + '/scope-and-details'
        soup_detail = self.fetch_page(brows_url)
        issn_b = soup_detail.select('b')
        Print_issn = issn_b[0].next_sibling
        online_issn = issn_b[1].next_sibling
        return {
            'Print-issn': Print_issn.strip(),
            'issn': online_issn.strip()
        }

    def large_down_main(self):
        """读取 mango 并遍历详细页链接和下载链接 | 下载该页所有 PDF 文件，提取信息并保存 JSON
        :return:
        """
        paginator = MongoPaginator(db)
        page = 1
        page_size = 100   # 此数量必须大于最大数量
        while True:
            message_result = paginator.paginate(
                collection_name="awaitResult",
                page=page,
                page_size=page_size, )
            data_results = message_result["data"]
            if page >= message_result["total_pages"]:  #
                break
            for data_re in data_results:
                time.sleep(random.uniform(0.9, 2))
                down_url = data_re.get('down_url')
                page_url = data_re.get('page_url')
                # print('down_url:\t', down_url)
                # print('page_url:\t', page_url)
                issn = data_re.get('issn')

                try:  # 核心处理部分
                    md5_filename = hashlib.md5(down_url.encode('utf-8')).hexdigest() + ".pdf"
                    # save_dir = r'E:\AAA-project\muchen_project\projecteuclid\save_pdf'
                    save_dir = Path(current_file, 'save_pdf')
                    os.makedirs(save_dir, exist_ok=True)
                    save_path = Path('save_pdf', md5_filename)
                    # print(page_url, save_path)
                    self.download_pdf(down_url, Path(current_file, save_path))  #
                    result_dict = self.gain_data(f'{page_url}?tab=ArticleLink', issn, save_path)  #
                    json_path = Path(current_file, 'projecteuclid2.json')
                    # print(result_dict)
                    self.save_json(result_dict, json_path)  # 读取再存入
                    logger.info(f"处理完成: {page_url}")
                    projecteuclidResult.insert_one(result_dict)  # 将完成的内容保存到mango中
                    awaitResult.delete_one({"page_url": page_url})  # 从 awaitResult 中删除已完成项
                except Exception as e:
                    logger.error(f"[large_number] 处理失败: {page_url}\t 错误: {e}")

            page += 1
            time.sleep(random.uniform(5, 10))

    def large_number(self, part_url: str, issn: str) -> int:
        """将符合的详情链接和下载链接保存到mango中
        :param part_url  详细页面url
        :param issn  父页获取到的issn
        """
        soup_issue = self.fetch_page(part_url)
        try:
            down_urls = [self.base_url + group['href'] for group in
                         soup_issue.select('.form-group.DownloadSaveButton1')]
        except KeyError as e:
            logger.warning(f"当前论题 下载需要25$  \t-->{e}")
            return 0
        page_urls = [self.base_url + issue['href'] for issue in soup_issue.select('.TocLineItemAnchorText1')]
        for down_url, page_url in zip(down_urls, page_urls):
            awaitResult.insert_one({
                "down_url": down_url,
                "page_url": page_url,
                "issn": issn
            })
            logger.info(f'{page_url} 插入成功!')

    def gain_main(self):
        """调用其他方法 | 将所有可下载链接保存到 mango 中
        :return:
        """
        logger.info("程序启动，开始抓取 ProjectEuclid 数据")
        browse_list = self.get_browse('https://projecteuclid.org/browse/title/A')  # 获取当前大类别的所有年份书籍url 列表 -> list
        logger.info(f"获取到 {len(browse_list)} 个大类页面")

        for brow_url in browse_list:
            logger.info(f'正在请求书籍链接 ->  {brow_url}')
            time.sleep(random.uniform(5, 30))
            issn_dict = self.get_details_dict(brows=brow_url)  # 获取当前页面的issn -> dict
            issn = issn_dict.get('issn')
            mathematica_list = self.get_mathematica(brows=brow_url)  # 获取当前书籍类别下的所有数据url 列表 -> list
            new_mathematica_list = [ma.replace('/issues/', '/volume-') + '/issue-none' for ma in mathematica_list]
            for mathe_url in new_mathematica_list:
                time.sleep(random.uniform(2, 5.5))
                condition = self.large_number(part_url=mathe_url,
                                              issn=issn)  # 下载页面内容所有pdf | 获取子链接中所有的详情信息 | 保存信息到本地json中
                if condition == 0:
                    logger.warning(f'将对当前整个年份论题进行跳过 \t->跳过{mathe_url}')
            break


if __name__ == "__main__":
    fetcher = PageFetcher()
    fetcher.init_cookie()  # 自动管理cookie
    # fetcher.gain_main()  # 获取链接
    fetcher.large_down_main()  # 下载
