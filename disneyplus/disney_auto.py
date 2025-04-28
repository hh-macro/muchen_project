# -- coding: utf-8 --
# @Author: 胡H
# @File: disney_auto.py
# @Created: 2025/4/8 14:36
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import random

import pandas as pd
from DrissionPage import ChromiumPage
import time

page = ChromiumPage()

page.get('https://www.disneyplus.com/identity/login/enter-email')
time.sleep(5)
try:
    page.ele('css:#email').input('arxqdmogy@zohomail.com')
    page.ele('css:.leading-lg.text-lg.font-semibold.overflow-hidden.text-ellipsis.whitespace-nowrap').click()
    time.sleep(2)
    page.ele('css:#password').input('ds369369')
    page.ele('css:.leading-lg.text-lg.font-semibold.overflow-hidden.text-ellipsis.whitespace-nowrap').click()

    time.sleep(2)
    page.ele('css:.sc-bmyXtO.sc-jqIZGH.eawCjh.profile-avatar')

except:
    print('已登陆')
time.sleep(5)
page.get('https://www.disneyplus.com/zh-hans/browse/movies')  # 类别  -电影
time.sleep(4)
page.eles('css:.jrlc7j1.xgfbc18c.xgfbc18p.xgfbc1n3.xgfbc1rr.xgfbc1d3.xgfbc1hr.xgfbc16.xgfbc18x.xgfbc189.xgfbc184.xgfbc11al.xgfbc11x3.xgfbc15p.xgfbc13i')[2].click()
time.sleep(2)
# -----------------------------------------------------------------------------------
max_scroll_attempts = 1000
scroll_attempts = 0
max_stagnant_rolls = 15  # 允许的最大停滞滚动次数
stagnant_rolls = 0  # 当前停滞滚动次数
last_pos = 0  # 初始化 last_pos，记录上次滚动位置

while scroll_attempts < max_scroll_attempts:
    # 滚动页面
    page.scroll.down(random.randint(400, 650))  # 随机向下滚动 100-500 像素
    scroll_attempts += 1
    print(f"滚动次数: {scroll_attempts}")
    time.sleep(1.5)  # 等待页面加载

    # 检查是否滚动到页面底部
    current_pos = page.run_js('return window.pageYOffset;')
    max_pos = page.run_js('return document.documentElement.scrollHeight - window.innerHeight;')

    # 检查是否滚动停滞
    if current_pos == last_pos:
        stagnant_rolls += 1
        print(f"滚动停滞次数: {stagnant_rolls}")
    else:
        stagnant_rolls = 0  # 重置停滞计数器
        last_pos = current_pos  # 更新上次滚动位置

    # 如果连续10次滚动位置没有变化，认为已经滚动到底部
    if stagnant_rolls >= max_stagnant_rolls:
        print("连续10次滚动位置没有变化，认为已经滚动到底部")
        break

    # 如果滚动到底部，停止滚动
    if current_pos >= max_pos:
        print("已到达物理页面底部，停止滚动")
        break
# input('回车以开始:')
# -----------------------------------------------------------------------------------
_1srq7ki1_divs = page.eles('css:._1srq7ki1 div a')
print(len(_1srq7ki1_divs), _1srq7ki1_divs)
data_content_list = []
for _1srq7ki1_div in _1srq7ki1_divs:
    try:
        aria_label = _1srq7ki1_div.attr('aria-label').replace('选择以获取此作品的详情。', '')  # 视频名
        full_url = _1srq7ki1_div.attr('href')  # 链接
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

df.to_excel(f"./compilations/hdisneyList-{int(time.time())}.xlsx", index=False)

print(f"hdisneyList-{int(time.time())}.xlsx")
