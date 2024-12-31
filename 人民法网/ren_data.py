import random
import time
from datetime import datetime
import requests

import json

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://rmfyalk.court.gov.cn",
    "Pragma": "no-cache",
    "Referer": "https://rmfyalk.court.gov.cn/view/content.html?id=wZyJGLbzhQFECRjGPHIR0upcGRPiH57ZIktF5UEDRf0%253D&lib=ck&cf=06",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "faxin-cpws-al-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzU2MjYxNzEsInVzZXJuYW1lIjoiZ215Q2ZDMWRRVk0yRnc3Z1I0NE0wd0xsUUExdHg5b2JTTkNIenUvdWZmNGNlQ3g5b2owK2xobEhsaEZMMHJJM1hIYXFKZ0UwejJBPSJ9.M7rIJPq0lzsmzheqEFhp8K3LXRegvPc4Sl3J2HGKrSU",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "Hm_lvt_d78a621da6111a54cda8ed0e717115b9": "1735611658",
    "wzws_sessionid": "gWY1MWJiNIAxMTMuMjQ4LjI1NC4xNzCCY2FiYTg0oGdzVQ8=",
    "HMACCOUNT": "78DFBE33FB144353",
    "faxin-cpws-al-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzU2MjYxNzEsInVzZXJuYW1lIjoiZ215Q2ZDMWRRVk0yRnc3Z1I0NE0wd0xsUUExdHg5b2JTTkNIenUvdWZmNGNlQ3g5b2owK2xobEhsaEZMMHJJM1hIYXFKZ0UwejJBPSJ9.M7rIJPq0lzsmzheqEFhp8K3LXRegvPc4Sl3J2HGKrSU",
    "Hm_lpvt_d78a621da6111a54cda8ed0e717115b9": "1735611909"
}

session = requests.Session()


def time_bi(cpws_al_rk_time):
    time1 = datetime.strptime(cpws_al_rk_time, '%Y-%m-%d %H:%M:%S')
    time2 = datetime.strptime('2024-12-06', '%Y-%m-%d')
    return time1 >= time2


def json_file(data_j):
    with open('人民法院案例库/data.json', 'a', encoding='utf-8') as file:
        json_string = json.dumps(data_j, indent=4, ensure_ascii=False) + ',\n'
        file.write(json_string)
    print("数据插入成功！")


def search_page(page, category):
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
            "lib": "cpwsAl_qb",
            "sort_field": "",
            "case_sort_id_cpwsAl": category
        }
    }

    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=headers, cookies=cookies, data=data)
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
                      cpws_al_ajzh, cpws_al_slcx_name, cpws_al_rk_time, cpws_al_ts_name, filename)
        else:
            print(cpws_url, end='\t')
            print('日期不符合')


def rmfy_data(cpws_url, cpws_id, cpws_al_case_sort_name, cpws_al_sort_name, cpws_al_slfy_name, cpws_al_ajzh,
              cpws_al_slcx_name, cpws_al_rk_time, cpws_al_ts_name, filename):
    time.sleep(random.uniform(1.2, 3))
    url = "https://rmfyalk.court.gov.cn/cpws_al_api/api/cpwsAl/content"
    data = {
        "gid": cpws_id
    }

    data = json.dumps(data, separators=(',', ':'))
    response = session.post(url, headers=headers, cookies=cookies, data=data)
    # print(response.text)
    josn_page = json.loads(response.text)
    title = josn_page['data']['data']['cpws_al_title']  # 标题
    cpws_al_cpyz = josn_page['data']['data']['cpws_al_cpyz']  # 裁判要旨
    cpws_al_keyword = josn_page['data']['data']['cpws_al_keyword']  # 关键字(列表)
    cpws_al_jbaq = josn_page['data']['data']['cpws_al_jbaq']  # 基本案情
    cpws_al_glsy = josn_page['data']['data']['cpws_al_glsy']  # 关联索
    cpws_al_no = josn_page['data']['data']['cpws_al_no']  # 入库编号
    # cpws_al_sub_title = josn_page['data']['data']['cpws_al_sub_title']
    cpws_al_cply = josn_page['data']['data']['cpws_al_cply']  # 裁判理由

    cpws_al_case_sort_name = cpws_al_case_sort_name  # 案例类型
    filename = filename  # 文件名
    cpws_al_sort_name = cpws_al_sort_name  # 案由/罪名
    cpws_al_slfy_name = cpws_al_slfy_name  # 审理法院
    cpws_al_zs_date = josn_page['data']['data']['cpws_al_zs_date']  # 裁判日期
    cpws_al_ajzh = cpws_al_ajzh  # 案号
    cpws_al_slcx_name = cpws_al_slcx_name  # 审理程序
    cpws_al_rk_time = cpws_al_rk_time  # 入库时间
    cpws_al_ts_name = cpws_al_ts_name  # 文书类型
    biaodi = ''  # 标的
    biaodiwu = ''  # 标的物
    shulifei = ''  # 受理费
    file_content = {  # 文件内容
        'title': title,  # 标题
        'cpws_al_keyword': cpws_al_keyword,  # 关键字
        'cpws_al_jbaq': cpws_al_jbaq,  # 基本案情
        'cpws_al_cply': cpws_al_cply,  # 裁判结果/裁判理由
        'cpws_al_cpyz': cpws_al_cpyz,  # 裁判要旨
        'cpws_al_glsy': cpws_al_glsy,  # 关联索

    }
    laiyuan = '人民法院案例库'  # 来源
    cpws_url = cpws_url  # 来源链接
    data_j = {
        'cpws_al_case_sort_name': cpws_al_case_sort_name,  # 案例类型
        'filename': filename,  # 文件名
        'cpws_al_no': cpws_al_no,  # 入库编号
        'cpws_al_sort_name': cpws_al_sort_name,  # 案由/罪名
        'cpws_al_slfy_name': cpws_al_slfy_name,  # 审理法院
        'cpws_al_zs_date': cpws_al_zs_date,  # 裁判日期
        'cpws_al_ajzh': cpws_al_ajzh,  # 案号
        'cpws_al_slcx_name': cpws_al_slcx_name,  # 审理程序
        'cpws_al_rk_time': cpws_al_rk_time,  # 入库时间
        'cpws_al_ts_name': cpws_al_ts_name,  # 文书类型
        'biaodi': biaodi,  # 标的
        'biaodiwu': biaodiwu,  # 标的物
        'shulifei': shulifei,  # 受理费
        'file_content': file_content,  # 文件内容
        'laiyuan': laiyuan,  # 来源
        'cpws_url': cpws_url,  # 来源链接
    }
    json_file(data_j)


if __name__ == '__main__':
    list_category = ['02', '01', '03', '05', '06', '11']  # ['176', '198', '51', '5', '32', '1']
    category = '11'
    for i in range(1, 2):
        print(f'第{i}页--------------------------')
        search_page(i, category)

    # for i in range(1, 177):
    #     search_page(i, category)

    # start_time_1 = time.time()
    # with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    #     for i in range(1, 177):
    #         executor.submit(search_page, i, category)
    # print("线程池计算的时间：" + str(time.time() - start_time_1), "秒")
