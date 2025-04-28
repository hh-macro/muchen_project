# -- coding: utf-8 --
# @Author: 胡H
# @File: drission_cookie.py
# @Created: 2025/3/31 15:17
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import random
from DrissionPage import ChromiumPage, ChromiumOptions
import json
import time

# 设置浏览器选项
options = ChromiumOptions()
# 如果需要指定浏览器路径，可以设置如下：
# options.set_browser_path(r"/opt/google/chrome/google-chrome")
options.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
options.set_argument('--disable-automation-extensions')
page = ChromiumPage()

try:
    page.get('https://pan.quark.cn/')
    time.sleep(random.uniform(1, 2))

    element_ByiLK3y = page.ele('xpath://*[@id="ice-container"]/div/div[1]/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]')
    # element_ByiLK3y = page.ele('css:.LoginComponent--other-mode-item--ByiLK3y .text:nth-child(1)')
    if element_ByiLK3y:
        element_ByiLK3y.click()
        time.sleep(random.uniform(1, 2))

        username = input(":")
        page.ele('#login_name').input(username)  # 手机号
        page.ele('#send_sms_code').click()  # 获取短信验证码

        verify = input(":")
        page.ele('#u_sms_code').input(verify)  # 验证码

        page.ele('#submit_btn').click()  # 登录

        print(page.cookies().as_dict())

        slider = page.ele('css:.slider')  # 滑块的 CSS 选择器
        slider_track = page.ele('css:.slider-track')  # 滑槽的 CSS 选择器
        slider_rect = slider.rect
        slider_track_rect = slider_track.rect
        distance = slider_track_rect.width - slider_rect.width

        # 拖动滑块
        slider.drag(distance)

    time.sleep(10)

    # 获取Cookie
    cookies = page.cookies(as_dict=True)

    # 打印Cookie
    print(json.dumps(cookies, indent=4))

    # 保存Cookie到文件
    with open('quark_cookies.json', 'w', encoding='utf-8') as file:
        json.dump(cookies, file, indent=4)

finally:
    # 关闭浏览器
    page.quit()