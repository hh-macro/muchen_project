import base64
import json
import time
from datetime import datetime
from mitmproxy.tools.main import mitmdump

from mitmproxy import http

# 用于存储所有 base64 编码的字符串
base64_list = []


def image_cache_r():
    # 从缓存文件读取图片名
    with open("image_cache", "r") as cache_file:
        cached_image_name = cache_file.read()
    return cached_image_name


def response(flow: http.HTTPFlow) -> None:
    if "zijieapi.com" not in flow.request.url: return
    target_url = "https://imapi-oth.zijieapi.com/v1/message/get_by_conversation"
    # print(flow.request.url)
    if target_url in flow.request.url:

        flow_res = flow.response.content
        base64_str = base64.b64encode(flow_res).decode('utf-8')
        # print(base64_str)
        key = image_cache_r()
        if key:
            # 创建字典并添加到列表中
            base64_list.append({key: base64_str})
            # print(base64_str)
            save_base64_strings_to_file('base64_strings.json')  # 保存
        else:
            print("截取到包，但程序并未运行---为错误包")


# 保存 base64_strings 到文件
def save_base64_strings_to_file(file_path):
    with open(file_path, 'w') as file:
        json.dump(base64_list, file, indent=4)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{image_cache_r()}\t {now_time}:\t 文件覆盖保存成功！ ----  {file_path}")


def mit_main():
    # 启动 mitmdump 并加载当前脚本
    mitmdump(["-q", "-s", __file__])


"""
mitmdump -q -s intercept.py  ----启动截包
"""

if __name__ == '__main__':
    open("image_cache", "w").close()
    mit_main()
