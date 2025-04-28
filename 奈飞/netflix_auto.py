# -- coding: utf-8 --
# @Author: 胡H
# @File: auto_text.py
# @Created: 2025/4/3 13:36
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:  根据url遍历获取所有视频名和链接，并保存到表格中

import random

import pandas as pd
from DrissionPage import ChromiumPage
import time

page = ChromiumPage()

page.get('https://www.netflix.com/login')
time.sleep(4)
try:
    page.ele('css::r0:').input('san6x3@nf189.com')
    page.ele('css::r3:').input('asd768')

    page.ele(
        'css:.pressable_styles__a6ynkg0.button_styles__1kwr4ym0.default-ltr-cache-18x5i-StyledBaseButton.e1ax5wel2').click()
    page.ele('css:.profile-icon').click()
except:
    print('已登陆')
# elements_tab = page.eles('css:.navigation-tab a')  # 节目
# elements_tab[1].click()
# time.sleep(2)
# page.ele('css:.nfDropDown.theme-lakira').click()
# time.sleep(2)
# page.eles('css:.sub-menu-link')[6].click()
# time.sleep(2)
# page.ele('css:.aro-grid-toggle').click()
# time.sleep(2)
page.get('https://www.netflix.com/browse/m/genre/2690435?so=az')
time.sleep(8)

# -----------------------------------------------------------------------------------
max_scroll_attempts = 1000
scroll_attempts = 0
max_stagnant_rolls = 10  # 允许的最大停滞滚动次数
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
# -----------------------------------------------------------------------------------

time.sleep(2)

rowContainer_title_card = page.eles('css:.galleryLockups .rowContainer.rowContainer_title_card')
print(rowContainer_title_card)
data_content_list = []

for rowContainer in rowContainer_title_card:  # 遍历每行内容
    title_card_list = rowContainer.eles('css:.title-card')  # 获取当前行的所有标题卡片
    row_data = []  # 用于存储当前行的所有视频信息
    for title_card in title_card_list:  # 遍历子视频
        try:
            slider_refocus = title_card.ele('css:.slider-refocus')  # 单行视频下子视频
            href = slider_refocus.attr('href')  # 视频链接
            aria_label = slider_refocus.attr('aria-label')  # 视频名
            full_url = 'https://www.netflix.com/' + slider_refocus.attr('href')  # 视频链接
            video_info = {
                'aria_label': aria_label,
                'href': full_url
            }
            row_data.append(video_info)  # 将当前视频信息添加到行数据中
        except Exception as e:
            print(f"处理标题卡错误: {e}")
            continue

    data_content_list.extend(row_data)  # 将当前行的所有视频信息添加到总列表中

print('data_content_list:\t', data_content_list)
df = pd.DataFrame(data_content_list)

df.to_excel(f"./compilations/netflixList-{int(time.time())}.xlsx", index=False)

print(f"netflixList-{int(time.time())}.xlsx")
