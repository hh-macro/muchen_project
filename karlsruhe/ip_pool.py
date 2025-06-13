# -- coding: utf-8 --
# @Author: 胡H
# @File: ip_pool.py
# @Created: 2025/6/12 13:44
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import requests
import random
import time


class DynamicIPPool:
    def __init__(self, fetch_api: str, max_pool_size: int = 10, test_url: str = "https://httpbin.org/ip"):
        """
        初始化 IP 池
        :param fetch_api: 动态代理获取接口 (返回格式为 IP:PORT 的列表)
        :param max_pool_size: IP 池最大容量
        :param test_url: 测试 IP 是否可用的 URL
        """
        self.fetch_api = fetch_api
        self.max_pool_size = max_pool_size
        self.test_url = test_url
        self.pool = []

    def fetch_ip_list(self) -> list:
        """
        从代理提供商获取一批代理 IP
        :return: IP 列表
        """
        try:
            response = requests.get(self.fetch_api, timeout=10)
            if response.ok:
                ip_list = response.text.strip().split('\n')
                return [ip.strip() for ip in ip_list if ip.strip()]
        except Exception as e:
            print(f"[!] 获取代理失败: {e}")
        return []

    def test_proxy(self, proxy: str) -> bool:
        """
        测试代理是否可用
        :param proxy: "ip:port" 形式的代理
        :return: True 可用, False 不可用
        """
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        try:
            r = requests.get(self.test_url, proxies=proxies, timeout=4)
            return r.status_code == 200
        except Exception as e:
            print(e)
            return False

    def refill_pool(self):
        """
        填充 IP 池至最大容量
        """
        print("[+] 正在填充 IP 池...")
        new_ips = self.fetch_ip_list()
        for ip in new_ips:
            if len(self.pool) >= self.max_pool_size:
                break
            if self.test_proxy(ip):
                print(f"[√] 有效代理：{ip}")
                self.pool.append(ip)
            else:
                print(f"[×] 无效代理：{ip}")
        print(f"[✓] 当前 IP 池容量：{len(self.pool)} / {self.max_pool_size}")

    def get_proxy(self) -> str:
        """
        随机获取一个可用代理 IP
        :return: 代理 IP 字符串
        """
        if not self.pool:
            self.refill_pool()
        if not self.pool:
            raise Exception("IP 池为空，无法获取代理")
        return random.choice(self.pool)

    def remove_proxy(self, proxy: str):
        """
        删除失效代理
        """
        if proxy in self.pool:
            self.pool.remove(proxy)
            print(f"[-] 移除失效代理：{proxy}")


# 示例用法
if __name__ == "__main__":
    # 示例：芝麻代理的提取链接（此处需要你换成自己的）
    FETCH_API = "http://api.ipipgo.com/ip?cty=00&c=10&pt=1&ft=json&pat=\n&rep=1&key=835a6bbd"  # 返回 IP:PORT 的纯文本
    ip_pool = DynamicIPPool(fetch_api=FETCH_API, max_pool_size=10)

    # 获取一个代理
    try:
        proxy = ip_pool.get_proxy()
        print(f"使用代理：{proxy}")
        # 用于 requests 示例：
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
        print(r.json())
    except Exception as e:
        print(f"[!] 获取代理失败: {e}")
