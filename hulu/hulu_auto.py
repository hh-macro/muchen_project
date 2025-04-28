# -- coding: utf-8 --
# @Author: 胡H
# @File: hulu_auto.py
# @Created: 2025/4/8 12:13
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import random

import pandas as pd
from DrissionPage import ChromiumPage
import time

page = ChromiumPage()

page.get('https://auth.hulu.com/web/login/enter-email')
time.sleep(3)
try:
    try:
        page.ele('css:#email-field').input('arxqdmogy@zohomail.com')
        page.ele('css:.leading-lg.text-lg.font-semibold.overflow-hidden.text-ellipsis.whitespace-nowrap').click()
        time.sleep(2)
    except:
        page.ele('css:#password').input('ds369369')
        page.ele('css:.leading-lg.text-lg.font-semibold.overflow-hidden.text-ellipsis.whitespace-nowrap').click()
except:
    print('已登陆')
time.sleep(2)

page.get('https://www.hulu.com/hub/anime-tv/collection/4559')

time.sleep(4)
# -----------------------------------------------------------------------------------
# max_scroll_attempts = 1000
# scroll_attempts = 0
# max_stagnant_rolls = 10  # 允许的最大停滞滚动次数
# stagnant_rolls = 0  # 当前停滞滚动次数
# last_pos = 0  # 初始化 last_pos，记录上次滚动位置
#
# while scroll_attempts < max_scroll_attempts:
#     # 滚动页面
#     page.scroll.down(random.randint(400, 650))  # 随机向下滚动 100-500 像素
#     scroll_attempts += 1
#     print(f"滚动次数: {scroll_attempts}")
#     time.sleep(1.5)  # 等待页面加载
#
#     # 检查是否滚动到页面底部
#     current_pos = page.run_js('return window.pageYOffset;')
#     max_pos = page.run_js('return document.documentElement.scrollHeight - window.innerHeight;')
#
#     # 检查是否滚动停滞
#     if current_pos == last_pos:
#         stagnant_rolls += 1
#         print(f"滚动停滞次数: {stagnant_rolls}")
#     else:
#         stagnant_rolls = 0  # 重置停滞计数器
#         last_pos = current_pos  # 更新上次滚动位置
#
#     # 如果连续10次滚动位置没有变化，认为已经滚动到底部
#     if stagnant_rolls >= max_stagnant_rolls:
#         print("连续10次滚动位置没有变化，认为已经滚动到底部")
#         break
#
#     # 如果滚动到底部，停止滚动
#     if current_pos >= max_pos:
#         print("已到达物理页面底部，停止滚动")
#         break
input('回车以开始:')
# -----------------------------------------------------------------------------------

generics_tile = page.eles('css:.AllUpGrid__generic-tile')
print(len(generics_tile), generics_tile)
data_content_list = []
for generic_tile in generics_tile:
    try:
        baspu2a = generic_tile.ele('css:._6bueqfd._1fbaspu1c._1fbaspuv._1fbaspuu._1fbaspu1a._1fbaspu2a')
        aria_label = baspu2a.attr('aria-label')  # 视频名
        full_url = baspu2a.attr('href')  # 视频链接

        video_info = {
            'aria_label': aria_label,
            'href': full_url
        }
        data_content_list.append(video_info)  # 将当前视频信息添加到行数据中
    except Exception as e:
        print(f"处理标题卡错误: {e}")
        continue

print('data_content_list:\t', data_content_list)
df = pd.DataFrame(data_content_list)

df.to_excel(f"./compilations/huluList-{int(time.time())}.xlsx", index=False)

print(f"huluList-{int(time.time())}.xlsx")
