# -- coding: utf-8 --
# @Author: 胡H
# @File: ts_load.py
# @Created: 2025/4/2 11:29
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import os
import subprocess

import requests
from m3u8 import M3U8


def get_all_ts_urls(m3u8_urls):
    all_ts = []
    for url in m3u8_urls:
        playlist = M3U8(requests.get(url).text)
        ts_urls = [segment.uri for segment in playlist.segments]
        # 处理相对路径（如果 TS 地址是相对路径）
        if not ts_urls[0].startswith('http'):
            base_url = '/'.join(url.split('/')[:-1]) + '/'
            ts_urls = [base_url + ts for ts in ts_urls]
        all_ts.extend(ts_urls)
    return all_ts


def download_ts(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://example.com/'  # 根据实际情况添加
    }
    response = requests.get(url, headers=headers)
    with open(filename, 'wb') as f:
        f.write(response.content)

m3u8_urls = [
    'https://ltshwy.gtimg.com/B_fXrb0otmtGHxqhZ5HYDTdp8-LZVRr0TIxDygVJgULVk4-ybU6DrlUaoEpybJyZ3iYs_m5GcgY34j2ePpfQVMrRfTylGJ3qfUp8BUUfP8fScFyzzhwDvF1V5YyaAUUw81Sg519NWDEvBWWQGpQ5Blpw/svp_50112/AmSXh0CLKAjIZkHvB8ECoZXxnLDkTzmZ3reHaH9-4iNTKl3mtQnvtkbWsPsK2xt-EeP8kNOjuYfKdJLLQFsLYlTEcLBEhlgWFyujJgbAej23VH7iL4uEt85a1CiArOh_lOS_UCz4oMEfoU_bBnh1hajxnmwy6iPOTLhuhLiGyl9QKinkMJnBAer8kJJqZeOrFVF5DdxUVa8Bzfu7_pKuZFZr9GAyplVOKCOBAHmdzKk/gzc_1000102_0b535mavaaabdiam23pjgjt4d26dkcnqcvca.f322062.ts.m3u8?ver=4',
    'https://e958d3814b48854fd4e8a00331324107.v.smtcdns.com/moviets.tc.qq.com/AAZXM5FX8o_1q6l2xxj4wenQVr44jgEwkRF3wK_yVQdk/B_fXrb0otmtGHxqhZ5HYDTdm68Bvo8RUP7Yw0Te27p1zA4-ybU6DrlUaoEpybJyZ3iYs_m5GcgY34j2ePpfQVMrRfTylGJ3qfUp8BUUfP8fScFyzzhwDvF1V5YyaAUUw81Sg519NWDEvBWWQGpQ5Blpw/svp_50112/AmSXh0CLKAjIZkHvB8ECoZXxnLDkTzmZ3reHaH9-4iNTKl3mtQnvtkbWsPsK2xt-EeP8kNOjuYfKdJLLQFsLYlTEcLBEhlgWFyujJgbAej23VH7iL4uEt85a1CiArOh_lOS_UCz4oMEfoU_bBnh1hajxnmwy6iPOTLhuhLiGyl9QKinkMJnBAer8kJJqZeOrFVF5DdxUVa8Bzfu7_pKuZFZr9GAyplVOKCOBAHmdzKk/gzc_1000102_0b535mavaaabdiam23pjgjt4d26dkcnqcvca.f322062.ts.m3u8?ver=4',
    # ... 更多 M3U8 地址
]
# 获取所有 TS URL（同上）
all_ts = get_all_ts_urls(m3u8_urls)

# 下载所有 TS 文件
for idx, ts_url in enumerate(all_ts):
    ts_file = f"temp_{idx:04d}.ts"  # 按顺序命名（如 temp_0000.ts）
    download_ts(ts_url, ts_file)
# ===================================================================
# 按文件名顺序合并
ts_files = sorted([f for f in os.listdir() if f.startswith('temp_')])

with open('merged.ts', 'wb') as merged:
    for ts_file in ts_files:
        with open(ts_file, 'rb') as f:
            merged.write(f.read())
        os.remove(ts_file)  # 删除临时文件

# 转换为标准 MP4
subprocess.run([
    'ffmpeg',
    '-i', 'merged.ts',
    '-c', 'copy',
    'final_output.mp4'
])
os.remove('merged.ts')  # 删除中间文件