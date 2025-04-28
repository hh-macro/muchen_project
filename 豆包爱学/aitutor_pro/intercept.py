import base64
import json
import time
from datetime import datetime
from mitmproxy.tools.main import mitmdump
import subprocess  # 导入 subprocess 模块用于启动和关闭 mitmdump
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
    target_url = "https://imapi-oth.zijieapi.com/v1/message/get_by_user"
    # print(flow.request.url)
    if target_url in flow.request.url:
        # 获取响应内容
        # print(flow.response.text)
        # print("第一次响应")
        # time.sleep(5)  # 等待 5 秒
        # response = requests.get(flow.request.url, timeout=10)
        # flow_res = response.content
        time.sleep(10)
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
    print(f"{now_time}:\t 文件覆盖保存成功！ ----  {file_path}")


# 新增函数：启动 mitmdump
def start_mitmdump():
    # 启动 mitmdump 并加载当前脚本
    mitmdump_cmd = ["mitmdump", "-q", "-s", __file__]
    mitmdump_process = subprocess.Popen(mitmdump_cmd)
    print("mitmdump 已启动\t PID:", mitmdump_process.pid)
    return mitmdump_process


# 新增函数：关闭 mitmdump
def stop_mitmdump(process):
    process.terminate()  # 发送终止信号
    process.wait()  # 等待进程结束
    print("mitmdump 已关闭")


"""
mitmdump -q -s intercept.py  ----启动截包
"""

if __name__ == '__main__':
    open("image_cache", "w").close()  # 清空缓存文件
    mitmdump_process = start_mitmdump()  # 启动 mitmdump

    time.sleep(120)
    stop_mitmdump(mitmdump_process)  # 关闭 mitmdump
