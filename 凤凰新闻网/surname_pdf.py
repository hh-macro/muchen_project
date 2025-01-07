import random
import time

import requests
import chardet
import pdfkit
from bs4 import BeautifulSoup
from parsel import Selector

import re
import os


def encode_conver(wrong_encoded_str):
    detected = chardet.detect(wrong_encoded_str.encode('latin1'))
    try:
        corrected_str = wrong_encoded_str.encode('latin1').decode(detected['encoding'])
        return corrected_str
    except UnicodeDecodeError:
        print("")


def file_create(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    else:
        # print(f"目录{dir_path}--已存在")
        print('', end='')


def sanitize_filename(filename):
    # Windows系统中不允许的字符
    invalid_chars = r'[<>:"/\\|?*]'
    # 替换不允许的字符为下划线
    sanitized_filename = re.sub(invalid_chars, '_', filename)
    # 去除文件名开头和结尾的空格
    sanitized_filename = sanitized_filename.strip()
    return sanitized_filename


def news_list(category_id):
    for i in range(1, 100):

        print(f"第{i}页---------------------------------------------------")
        if i == 1:
            response = requests.get(f'https://www.fhxww.cn/channel/{category_id}.html')
        else:
            response = requests.get(f'https://www.fhxww.cn/channel/{category_id}_{i}.html')
        if response.status_code == 200:
            selector = Selector(text=response.text)
            li_elements = selector.css('.news_list.m_t_40 li')
            for li in li_elements:
                news_title = li.css('.f_left::text').get()  # 使用xpath获取文本内容
                news_url = li.css('a_tool::attr(href)').get()
                news_title = encode_conver(news_title)
                print(news_title, news_url)
                news_single(news_title, news_url)  # 具体文章爬取
        else:
            print(f'-----------一共爬取了{i - 1}页--------------------')
            break


def news_single(news_title, news_url):
    config = pdfkit.configuration(wkhtmltopdf=r'D:\plug\wkhtmltopdf\bin\wkhtmltopdf.exe')
    response = requests.get(news_url)
    # print(response.text)
    if response.status_code == 200:
        try:
            detected = chardet.detect(response.content)
            encoding = detected['encoding']
            page_content = response.content.decode(encoding)
            # print(page_content)
            selector = Selector(text=page_content)
            box_left_content = selector.css('.box_left.f_left').get()
            if box_left_content is None:
                box_left_content = selector.css('.box-left1.f-left').get()
            html_header = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>title</title>
            </head>
            <body>
            """
            html_footer = """
            </body>
            </html>
            """
            complete_html = html_header + box_left_content + html_footer
            # print(complete_html)  # 文章断块html

            soup = BeautifulSoup(complete_html, 'html.parser')
            elements_to_remove1 = soup.select('.b-bottom-2gray3')
            if elements_to_remove1:
                for element in elements_to_remove1:
                    element.decompose()
            elements_to_remove2 = soup.select('.p_t_20.overf')
            if elements_to_remove2:
                for element in elements_to_remove2:
                    element.decompose()
            elements_to_remove3 = soup.select('.b-top-2gray3')
            if elements_to_remove3:
                for element in elements_to_remove3:
                    element.decompose()
            elements_to_remove4 = soup.select('.plyr.plyr--full-ui')
            if elements_to_remove4:
                for element in elements_to_remove4:
                    element.decompose()
            elements_to_remove5 = soup.select('.favNum.starCount')
            if elements_to_remove5:
                for element in elements_to_remove5:
                    element.decompose()
            cleaned_html = str(soup)
            # print(cleaned_html)
            new_title = sanitize_filename(news_title)
            try:
                pdfkit.from_string(cleaned_html, f'凤凰旅游/{new_title}.pdf', configuration=config)
            except:
                temporary = int(time.time())
                pdfkit.from_string(cleaned_html, f'凤凰旅游/{temporary}.pdf', configuration=config)
        except:
            print(f"文章--{news_title}--已不存在！！！")

    else:
        print(f"文章--{news_title}--爬取失败")


if __name__ == '__main__':
    # category_id_list = ['1072', '1073', '1074', '1075', '1077', '1076', '1079', '1078']
    # category_name_list = ['凤凰概览', '凤凰旅游', '理论园地', '文艺频道', '专题专栏', '凤凰政务', '影像凤凰',
    #                       '新闻中心']
    # for category_id, category_name in zip(category_id_list, category_name_list):
    #     time.sleep(random.uniform(0.5, 1.2))
    #     print(category_id, category_name)

    category_id = '1073'
    category_name = '凤凰旅游'
    file_create(category_name)  # 文件夹检测
    # news_list(category_id)  # 文章列表信

    # 以下为单个测试----------------------
    news_title = 'text'
    news_url = 'https://www.fhxww.cn/content/2018/07/19/5123776.html'
    news_single(news_title, news_url)  # 具体文章爬取
