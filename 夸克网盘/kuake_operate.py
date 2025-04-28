# -- coding: utf-8 --
# @Author: 胡H
# @File: a.py
# @Created: 2025/3/31 16:11
# @LastModified:
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:

import json
import time
import socket

from loguru import logger
import pandas as pd
import requests
from functools import wraps
from requests.exceptions import RequestException, JSONDecodeError

# 日志配置保持不变
logger.add(
    "../夸克网盘日志.log",
    rotation="10 MB",
    retention="30 days",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    encoding="utf8"
)


# ===================================群机器人=======================================================
def bot(content):
    try:
        json_data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": ["王泽泽"],
            }
        }
        headers = {
            'Content-Type': 'application/json',
        }
        params = {
            'key': '5a5411e4-92bc-4484-be86-d49c81e2fc9f',
        }
        response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send', params=params, headers=headers,
                                 json=json_data)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"发送机器人消息失败: {e}")
        return False


# =================================================================================================

def retry(max_retries=3, delay=5, allowed_exceptions=(Exception,)):
    """通用重试装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _retries = max_retries
            while _retries > 0:
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    _retries -= 1
                    logger.warning(f"操作重试中，剩余尝试次数 {_retries}，错误信息：{str(e)}")
                    time.sleep(delay)
                    if _retries == 0:
                        logger.error(f"操作失败，已达最大重试次数 | 函数：{func.__name__} | 错误：{str(e)}")
                        raise

        return wrapper

    return decorator


@retry(max_retries=3, delay=10)
def get_files_list(headers, targe_exts,phone=None):
    """获取文件列表（带重试机制）"""
    total_fid_list = []
    try:
        for targe in targe_exts:
            logger.info(f'正在匹配后缀 {targe}......')
            time.sleep(1.2)
            for page in range(1, 100):
                url_get = f'https://drive-pc.quark.cn/1/clouddrive/file/search?pr=ucpro&fr=pc&uc_param_str=&q={targe}&_page={page}&_size=10000&_fetch_total=1&_sort=file_type:desc,updated_at:desc&_is_hl=1'
                # url_get = 'https://drive-pc.quark.cn/1/clouddrive/file/search?pr=ucpro&fr=pc&uc_param_str=&q=MP4&_page=1&_size=50&_fetch_total=1&_sort=file_type:desc,updated_at:desc&_is_hl=1'
                # print(url_get)
                # print(headers)

                response = requests.get(
                    url=url_get,
                    headers=headers,
                    timeout=15  # 增加超时设置
                )

                if response.status_code != 200:
                    if response.status_code == 400:
                        pass
                        # print()
                    else:
                        logger.warning(f"请求异常 | 状态码:{response.status_code}")
                    break

                time.sleep(6)
                search_dict = json.loads(response.text)
                result_list = search_dict.get('data', {}).get('list', [])

                if not result_list:
                    break

                for result in result_list:
                    if fid := result.get('fid'):
                        total_fid_list.append(fid)

                if total_fid_list:
                    logger.success(f'{targe} 后缀已成功匹配到 {len(total_fid_list)} 个文件')
                if len(total_fid_list)>1000:
                    for i in range(0, len(total_fid_list), 1000):
                        delete_files(headers, total_fid_list[i:i+1000], phone)
                        time.sleep(2)
                else:
                    delete_files(headers, total_fid_list, phone)
        return total_fid_list
    except (JSONDecodeError, KeyError) as e:
        logger.error(f"解析响应数据失败: {str(e)}")
        raise


@retry(max_retries=3, delay=10)
def delete_files(headers, total_fid_list, phone):
    """删除文件（带重试机制）"""
    try:
        if not total_fid_list:
            logger.warning("没有需要删除的文件")
            return

        params = {'pr': 'ucpro', 'fr': 'pc', 'uc_param_str': ''}
        json_data = {'action_type': 2, 'filelist': total_fid_list, 'exclude_fids': []}

        response = requests.post(
            'https://drive-pc.quark.cn/1/clouddrive/file/delete',
            params=params,
            headers=headers,
            json=json_data,
            timeout=15
        )

        if response.status_code == 200:
            logger.success(f" 任务: 夸克网盘 | 主机: {gethostname()} 手机号: {phone}\t已成功删除 {len(total_fid_list)}个文件")
        #     bot(f" 任务: 夸克网盘 \n 主机: {gethostname()}\n手机号: {phone}\n 已成功删除 {len(total_fid_list)}个文件 \n当前剩余内存 {use_capacity:.5f}GB/{total_capacity:.5f}GB")
        #     logger.success(
        #         f" 任务: 夸克网盘 | 主机: {gethostname()} 手机号: {phone}\t已成功删除 {len(total_fid_list)}个文件 | 当前剩余内存 {use_capacity:.5f}GB/{total_capacity:.5f}GB")
        # else:
        #     bot(f"主机:{gethostname()}\t 手机号:{phone}\t 删除失败!!! | 状态码：{response.status_code} | 响应内容：{response.text} | 当前剩余内存{use_capacity:.5f}GB/{total_capacity:.5f}GB")
        #     logger.error(
        #         f"主机:{gethostname()}\t 手机号:{phone}\t 删除失败!!! | 状态码：{response.status_code} | 响应内容：{response.text} | 当前剩余内存{use_capacity:.5f}GB/{total_capacity:.5f}GB")
    except RequestException as e:
        logger.error(f"删除请求失败: {str(e)}")
        raise


def table_data():
    try:
        file_path = 'map.xlsx'
        df = pd.read_excel(file_path, engine='openpyxl', header=0, usecols=['手机号', 'cookie'])

        if df.empty:
            logger.error("Excel 文件为空或格式不正确")
            return []

        return [{'name': row['手机号'], 'cookie': row['cookie']} for _, row in df.iterrows()]
    except Exception as e:
        logger.error(f"读取Excel文件失败: {str(e)}")
        return []


def page_main():
    try:
        EmailsNames_list = table_data()
        if not EmailsNames_list:
            logger.error("未读取到有效数据")
            return

        for EmailsNames in EmailsNames_list:
            user_cookies = EmailsNames.get('cookie', '').strip()
            phone = EmailsNames.get('name', '未知用户')

            if not user_cookies:
                logger.warning(f"手机号 {phone} 的cookie为空")
                continue

            user_headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'origin': 'https://pan.quark.cn',
                'priority': 'u=1, i',
                'referer': 'https://pan.quark.cn/',
                'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
                'cookie': user_cookies,
            }

            try:
                # 测试cookie有效性
                response_test = requests.get('https://pan.quark.cn/list',
                                             headers=user_headers,
                                             timeout=10)
                if response_test.status_code != 200:
                    bot(f'当前手机号为 {phone} 的cookie已失效， 请及时更换!!!')
                    logger.error(f'当前手机号为 {phone} 的cookie已失效,已进行跳过 | 请及时更换!!!')
                    continue

                # 目标后缀列表
                targe_exts = ["zip", "rar", "mp4", "mp3", "jpg", "png", "7z",
                              "jpeg", "gif", "dll", "pak", "sig", "json", "bin",
                              "sys", "md", "bat", "wbpz", "djvu", "inf", "ssk",
                              "uvz", "db", "lnk", "doc", "docx", "wma", "pps"]
                total_fid_list = get_files_list(user_headers, targe_exts, phone)
                # 获取并删除文件
                # total_fid_list = get_files_list(user_headers, targe_exts)
                # if total_fid_list:
                #     delete_files(user_headers, total_fid_list, phone)
                # else:
                #     logger.info(f"手机号 {phone} 没有匹配到目标文件")
                use_capacity = memory_size(user_headers)['use_capacity']
                total_capacity = memory_size(user_headers)['total_capacity']
                bot(f" 任务: 夸克网盘 \n 主机: {gethostname()}\t手机号: {phone}\t 已成功删除 {len(total_fid_list)}个文件 \n当前剩余内存 {use_capacity:.2f}GB/{total_capacity:.2f}GB")
            except Exception as e:
                bot(f"主机{gethostname()}\n在处理用户 {phone} \n 时发生异常: {str(e)}\n注意查看原因")
                logger.error(f"主机{gethostname()}\n在处理用户 {phone} \n 时发生异常: {str(e)}\n注意查看原因")
                continue

    except Exception as e:
        logger.critical(f"主流程发生未捕获异常: {str(e)}")
        raise


def gethostname():
    return socket.gethostname()


def memory_size(headers):
    params = {
        'pr': 'ucpro',
        'fr': 'pc',
        'uc_param_str': '',
        'fetch_subscribe': 'true',
        '_ch': 'home',
        'fetch_identity': 'true',
    }

    response = requests.get('https://drive-pc.quark.cn/1/clouddrive/member', params=params,
                            headers=headers)
    member_josn_data = json.loads(response.text).get('data', {})
    use_capacity = member_josn_data.get('use_capacity', 0)
    total_capacity = member_josn_data.get('total_capacity', 0)

    use_capacity = use_capacity / (1024 * 1024 * 1024)
    total_capacity = total_capacity / (1024 * 1024 * 1024)

    return {'use_capacity': use_capacity, 'total_capacity': total_capacity}


if __name__ == "__main__":
    try:
        page_main()

    except KeyboardInterrupt:
        logger.info("用户手动终止程序")
    except Exception as e:
        bot(f"主机: {gethostname()}\t 程序异常终止: {str(e)} \t 请及时检查!!!")
        logger.critical(f"主机: {gethostname()}\t 程序异常终止: {str(e)} \t 请及时检查!!!")
