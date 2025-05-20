# -- coding: utf-8 --
# @Author: 胡H
# @File: intercept.py
# @Created: 2025/5/12 14:48
# @LastModified:
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import json
import pickle
import time

from DrissionPage import Chromium
import pyautogui

data_list = []


def mlddle_move(tab, element):
    elements = tab.eles(element)
    if elements:
        target_element = elements[0]
        print('目标元素存在')

        tab.actions.move_to(ele_or_loc=target_element)
        print('鼠标已悬停在目标元素上')
    else:
        print('未找到目标元素')


def mlddle_click():
    # 定义点击位置（例如，页面中心）
    click_x = 2800
    click_y = 400

    # 使用 pyautogui 直接点击指定位置
    pyautogui.click(click_x, click_y)


def pkl_sava(pickle_file_path="data.pkl"):
    with open(pickle_file_path, "wb") as pf:
        pickle.dump(data_list, pf)
    print(f'已成功截取到的所有 --> GetVodPlaybackResources 覆盖保存到本地')


def main_auto():
    tab = Chromium().latest_tab
    # tab.get('https://www.amazon.com/gp/video/')

    tab.get('https://www.amazon.com/gp/video/detail/B0DNRCX9WM/ref=atv_tv_hom_c_uDZhwG_brws_2_2?jic=8%7CEgRzdm9k')

    # 显式等待剧集列表加载
    episode_container = tab.ele('.GG33WY', timeout=10)
    episode_much = episode_container.eles('.c5qQpO')

    tab.listen.start('GetVodPlaybackResources')

    time.sleep(1)
    tab.listen.start('GetVodPlaybackResources')  # 开始监听，指定获取包含该文本的数据包

    for count, episode in enumerate(episode_much):
        if count == 0:
            # 确保悬停元素可见
            mlddle_move(tab, element='css:.OUwe3b')
            # 等待剧集元素完全加载
            episode.wait.displayed(timeout=10)
            # 使用更精准的选择器定位播放按钮
            play_btn = episode.ele('css:.bPQjm1', timeout=10)
            # 使用JS点击避免依赖元素坐标
            play_btn.run_js('this.click()')
        tab.wait(3, 5)
        # mlddle_click()
        # next_btn = tab.ele(
        #     'css:.fqye4e3.f1ly7q5u.fk9c3ap.fz9ydgy.f1xrlb00.f1hy0e6n.fgbpje3.f1uteees.f1h2a8xb.atvwebplayersdk-nexttitle-button.f1qa0by8.f1dvg9i6.f45h',
        #     timeout=15)  # 下一集
        # if not next_btn:
        #     print(f'已经是最后一集了 | 一共{count}集')
        #     break
        print(f'第{count + 1}集', end='\t')

        res = tab.listen.wait()  # 等待并获取一个数据包
        print('res.url', res.url)
        data_list.append(res.response.body)

        tab.wait(0.5, 1.0)
        # 处理翻页按钮
        mlddle_click()
        next_btn = tab.ele(
            'css:.fqye4e3.f1ly7q5u.fk9c3ap.fz9ydgy.f1xrlb00.f1hy0e6n.fgbpje3.f1uteees.f1h2a8xb.atvwebplayersdk-nexttitle-button.f1qa0by8.f1dvg9i6.f45h',
            timeout=15)  # 下一集
        if next_btn:
            next_btn.run_js('this.click()')  # 使用JS点击
        else:
            print('无法找到翻页按钮')
            break

    pkl_sava()


if __name__ == '__main__':
    main_auto()
