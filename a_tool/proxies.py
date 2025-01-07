import requests


def proxy_ip(url_ip):
    """
    输入代理Ip地址，获取并组成一组proxy
    """
    res = requests.get(url=url_ip).json()
    data_ip = res['data'][0]
    ip_pro = str(data_ip['ip'])
    port_pro = str(data_ip['port'])

    proxies = {
        "http": "http://" + ip_pro + ":" + port_pro,
        "https": "http://" + ip_pro + ":" + port_pro
    }

    return proxies


def locality():
    """本地局域网代理"""
    proxies = {
        "http": "127.0.0.1:7890",
        "https": "127.0.0.1:7890"
    }
    return proxies
