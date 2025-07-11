import random
import re
import time
from datetime import datetime
import requests

import json


def extract_relevant_part(text):
    """将 text 文本取最后一段，再从取年月日开始取到最后 """
    # 分割段落并获取最后一段
    paragraphs = [p.strip() for p in text.split('<br/>') if p.strip()]
    if not paragraphs:
        return ""
    last_paragraph = paragraphs[-1]

    # 匹配“YYYY年M月D日”格式的日期
    date_pattern = re.compile(r'\d{4}年\d{1,2}月\d{1,2}日')
    matches = list(date_pattern.finditer(last_paragraph))

    if matches:
        # 取最后一个出现的日期
        last_match = matches[-1]
        date_start = last_match.start()

        # 找到这句话的起始：回溯到前一个“。”、“，”或英文逗号“,”之后
        idx_dot = last_paragraph.rfind('。', 0, date_start)
        idx_cn_comma = last_paragraph.rfind('，', 0, date_start)
        idx_en_comma = last_paragraph.rfind(',', 0, date_start)
        last_punct = max(idx_dot, idx_cn_comma, idx_en_comma)
        sentence_start = last_punct + 1 if last_punct != -1 else 0

        # 从句子起始取到段落末尾
        return last_paragraph[sentence_start:]
    else:
        # 如果没找到日期，则返回整段
        return last_paragraph


def clean_html_tags(text):
    # 去掉<p>标签
    text = re.sub(r'<p>', '', text)
    text = re.sub(r'</p>', '', text)
    # 将<br/>替换成\n
    text = re.sub(r'<br\s*/?>', '\n', text)
    # 去掉多余的空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text


cookies = {
    "UM_distinctid": "0",
    "wzws_sessionid": "gTdkZGVkYaBoazS8gDExMy4yNTEuOTAuMjUxgmNhYmE4NA==",
    "HMACCOUNT": "0",
    "Hm_lvt_d78a621da6111a54cda8ed0e717115b9": "1751871913",
    "Hm_lpvt_d78a621da6111a54cda8ed0e717115b9": "1751871913",
    "faxin-cpws-al-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NTE4ODYyMDAsInVzZXJuYW1lIjoiL3VOMzJiQkdrN0tBRTZFYVJJQlVFVGlRZGxVTWxQUm9OTGtudlNtZ2IycC95VDN0SjJvc3JoSFJYcVphYlBnZCtwelVoNEZiMXBnPSJ9.RqCq7mTvFILOWH6pmwc6HE-OA-Uw-gieZoQQNZ6tkok"
}

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://rmfyalk.court.gov.cn",
    "Pragma": "no-cache",
    "Referer": "https://rmfyalk.court.gov.cn/view/content.html?id=wi%252FKl6U3LKdGtiKXVu3kUyXJ4HGb%252F5abs84RR8h1uDU%253D&lib=ck&cf=01",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
session = requests.Session()


def time_bi(cpws_al_rk_time):
    time1 = datetime.strptime(cpws_al_rk_time, '%Y-%m-%d %H:%M:%S')
    time2 = datetime.strptime('2025-04-23', '%Y-%m-%d')
    return time1 >= time2


def json_file(data_j):
    with open('人民法院案例库/data.json', 'a', encoding='utf-8') as file:
        json_string = json.dumps(data_j, indent=4, ensure_ascii=False) + ',\n'
        file.write(json_string)
    print("数据插入成功！")


def search_page(page, category, lib):
    time.sleep(random.uniform(1.2, 3))
    url = "https://rmfyalk.court.gov.cn/cpws_al_api/api/cpwsAl/search"
    data = {
        "page": page,
        "size": 10,
        "lib": "qb",
        "searchParams": {
            "userSearchType": 1,
            "isAdvSearch": "0",
            "selectValue": "qw",
            "lib": lib,
            "sort_field": "",
            "case_sort_id_cpwsAl": category
        }
    }

    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=headers, cookies=cookies, data=data, timeout=50)

    json_data_lis = json.loads(response.text)['data']['datas']
    for json_data in json_data_lis:
        cpws_al_rk_time = json_data['cpws_al_rk_time']  # 入库日期
        cpws_id = json_data['id']  # id -- kVfF%2BLhOxQsrgOfIc4ElerXYC%2FKliD5YIFNGiN9AGwE%3D
        cpws_al_case_sort_name = json_data['cpws_al_case_sort_name']  # 案例类型
        cpws_al_sort_name = json_data['cpws_al_sort_name']  # 案由/罪名
        cpws_al_slfy_name = json_data['cpws_al_slfy_name']  # 审理法院
        cpws_al_ajzh = json_data['cpws_al_ajzh']  # 案号
        try:
            cpws_al_slcx_name = json_data['cpws_al_slcx_name']  # 审理程序
        except:
            cpws_al_slcx_name = ''
        cpws_al_ts_name = json_data['cpws_al_ts_name']  # 文书类型
        filename = json_data['cpws_al_title']  # 文件名
        cpws_url = f'https://rmfyalk.court.gov.cn/view/content.html?id={cpws_id}&lib=ck&cf=02'
        if time_bi(cpws_al_rk_time):
            # print(cpws_url, end='\t')
            rmfy_data(cpws_url, cpws_id, cpws_al_case_sort_name, cpws_al_sort_name, cpws_al_slfy_name,
                      cpws_al_ajzh, cpws_al_slcx_name, cpws_al_rk_time, cpws_al_ts_name, filename, lib)
        else:
            print(cpws_url, end='\t')
            print('日期不符合')


def rmfy_data(cpws_url, cpws_id, cpws_al_case_sort_name, cpws_al_sort_name, cpws_al_slfy_name, cpws_al_ajzh,
              cpws_al_slcx_name, cpws_al_rk_time, cpws_al_ts_name, filename, lib):
    time.sleep(random.uniform(1.2, 3))
    url = "https://rmfyalk.court.gov.cn/cpws_al_api/api/cpwsAl/content"
    data = {
        "gid": cpws_id
    }

    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=headers, cookies=cookies, data=data, timeout=50)
    try:
        # print(response.text)
        josn_page = json.loads(response.text)
        # print('josn_page:\t', josn_page)
        title = josn_page['data']['data']['cpws_al_title']  # 标题
        cpws_al_cpyz = josn_page['data']['data']['cpws_al_cpyz']  # 裁判要旨
        cpws_al_keyword = josn_page['data']['data']['cpws_al_keyword']  # 关键字(列表)
        cpws_al_jbaq = josn_page['data']['data']['cpws_al_jbaq']  # 基本案情
        cpws_al_glsy = josn_page['data']['data']['cpws_al_glsy']  # 关联索
        cpws_al_no = josn_page['data']['data']['cpws_al_no']  # 入库编号
        # cpws_al_sub_title = josn_page['a_data']['a_data']['cpws_al_sub_title']
        cpws_al_cply = josn_page['data']['data']['cpws_al_cply']  # 裁判理由

        cpws_al_case_sort_name = cpws_al_case_sort_name  # 案例类型

        if "：" in filename:
            split_text = filename.split("：")
            alh = split_text[0]
            pcmc = split_text[1]
        else:
            alh = 'null'
            pcmc = filename
        cpws_al_sort_name = cpws_al_sort_name  # 案由/罪名
        cpws_al_slfy_name = cpws_al_slfy_name  # 审理法院
        try:
            cpws_al_zs_date = josn_page['data']['data']['cpws_al_zs_date']  # 裁判日期
            cpws_al_zs_date = cpws_al_zs_date.replace('.', '-')  # 时间处理 | "2021-04-15"
            spnf = cpws_al_zs_date[:4]  # 2021
        except Exception as e:
            cpws_al_zs_date = "null"
            spnf = "null"
        cpws_al_ajzh = cpws_al_ajzh  # 案号
        cpws_al_slcx_name = cpws_al_slcx_name  # 审理程序
        cpws_al_rk_time = cpws_al_rk_time  # 入库时间
        cpws_al_ts_name = cpws_al_ts_name  # 文书类型
        cpws_al_sf = josn_page['data']['data']['cpws_al_sf']  # 地域
        file_content = {  # 文件内容
            'title': title,  # 标题
            'cpws_al_keyword': cpws_al_keyword,  # 关键字
            'cpws_al_jbaq': cpws_al_jbaq,  # 基本案情
            'cpws_al_cply': cpws_al_cply,  # 裁判结果/裁判理由
            'cpws_al_cpyz': cpws_al_cpyz,  # 裁判要旨
            'cpws_al_glsy': cpws_al_glsy,  # 关联索

        }
        cpws_url = cpws_url  # 来源链接
        if lib == 'cpwsAl_01':
            allx = '指导性案例'
        elif lib == 'cpwsAl_02':
            allx = '参考案例'
        # cpjg = clean_html_tags(extract_relevant_part(cpws_al_cply))

        data_j = {
            'pcmc': pcmc,  # 批次名称
            'allx': allx,  # 案例类型
            "alzt": "null",  # 案例主题
            'fbjg': '中华人民共和国最高人民法院',  # 发布机构
            # 'fbsj': cpws_al_rk_time,  # 发布时间
            'fbsj': 'null',  # 发布时间
            'sjlx': '参考案例',  # 数据类型
            'gklx': '信息公开',  # 公开类型
            'almc': filename,  # 案例名称
            'alh': alh,  # 案例号
            'gjc': '/'.join(cpws_al_keyword),  # 关键字
            'cpyd': clean_html_tags(cpws_al_cpyz),  # 裁判要点
            'xgft': clean_html_tags(cpws_al_glsy),  # 相关法条
            'jbaq': clean_html_tags(cpws_al_jbaq),  # 基本案情
            'cpjg': 'null',  # 裁判结果
            'cply': clean_html_tags(cpws_al_cply),  # 裁判理由
            'spzzcy': 'null',  # 审判组织成员
            'ah': cpws_al_ajzh,  # 案号
            'ajlx': cpws_al_case_sort_name,  # 案例类型
            'alsy': clean_html_tags(cpws_al_glsy),  # 案例索引
            'ay': cpws_al_sort_name,  # 罪由/罪名
            'wslx': 'null',  # 文书类型
            'cprq': cpws_al_zs_date,  # 裁判日期
            'slfy': cpws_al_slfy_name,  # 审理法院
            'slcx': cpws_al_slcx_name,  # 审理程序
            'sxx': '现行有效',  # 时效性
            'bd': 'null',  # 标的
            'slf': 'null',  # 受理费
            'dsrmc': f'{title}',  # 当事人名称
            'gsjg': 'null',  # 公诉机关
            'ksjg': 'null',  # 抗诉机关
            'ssdlrmc': 'null',  # 诉讼代理人名
            'ls': 'null',  # 律师
            'lssws': 'null',  # 律师事务所
            'orglist/url': cpws_url,  # 数据来源链接
            'wsid': 'null',  # 唯一标识
            'code': cpws_al_no,  # 入库编码
            'spnf': f'{spnf}年',  # 审判年份
            'dy': cpws_al_sf,  # 地域
            'fycj': '中级人民法院',  # 法院层级
            'bde': 'null',  # 标的额
            'jdlx': 'null',  # 结果类型
        }
        json_file(data_j)
    except Exception as e:
        print(f"发生错误 {e}")
        print('响应体:\t', response.text)
        print('响应状态:\t', response.status_code)
        print('文章ID:\t', cpws_id)


if __name__ == '__main__':
    list_category = ['02', '01', '03', '05', '04']  # ['176', '198', '51', '5', '32', '1']
    libs = ['cpwsAl_01', 'cpwsAl_02']  # cpwsAl_01-->指导性案例   cpwsAl_02-->参考案例

    category = '04'
    lib = 'cpwsAl_01'
    for i in range(1, 15):
        time.sleep(random.uniform(1, 3))
        print(f'第{i}页--------------------------')
        search_page(i, category, lib)

"""
2024-04-23 ~ 2025-07-07
02  cpwsAl_01   1页  4
02  cpwsAl_02   9页  93
01  cpwsAl_01   1页  1
01  cpwsAl_02   7页  68
03  cpwsAl_01   0页  0
03  cpwsAl_02   3页  29
05  cpwsAl_01   0页  0   
05  cpwsAl_02   2页  17
04  cpwsAl_01   0页  0
04  cpwsAl_02   1页  5
总计-----------------217
===================================================
2024-12-31 ~ 2025-04-24
02  cpwsAl_01  1页 。 2
02  cpwsAl_02  5页 。 48
01  cpwsAl_01  1页 。 1
01  cpwsAl_02  8页 。 89 
03  cpwsAl_01  0页 。 0
03  cpwsAl_02  1页 。 7
05  cpwsAl_01  1页 。 6 
05  cpwsAl_02  1页 。 7 
04  cpwsAl_01  0页 。 0
04  cpwsAl_02  1页 。 3    


"""

# for i in range(1, 177):
#     search_page(i, category)

# start_time_1 = time.time()
# with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
#     for i in range(1, 177):
#         executor.submit(search_page, i, category)
# print("线程池计算的时间：" + str(time.time() - start_time_1), "秒")
