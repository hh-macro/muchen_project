# -- coding: utf-8 --
# @Author: 胡H
# @File: 草稿二.py
# @Created: 2025/4/2 11:20
# @LastModified:
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:  将正常 m3u8链接列表，发起请求。最终保存为.mp4

import subprocess

import requests
from m3u8 import M3U8


def m3u8_single(output_file="output_mp4/output.mp4",
                m3u8_url="https://ltshwy.gtimg.com/B_fXrb0otmtGHxqhZ5HYDTdp8-LZVRr0TIxDygVJgULVk4-ybU6DrlUaoEpybJyZ3iYs_m5GcgY34j2ePpfQVMrRfTylGJ3qfUp8BUUfP8fScFyzzhwDvF1V5YyaAUUw81Sg519NWDEvBWWQGpQ5Blpw/svp_50112/AmSXh0CLKAjIZkHvB8ECoZXxnLDkTzmZ3reHaH9-4iNTKl3mtQnvtkbWsPsK2xt-EeP8kNOjuYfKdJLLQFsLYlTEcLBEhlgWFyujJgbAej23VH7iL4uEt85a1CiArOh_lOS_UCz4oMEfoU_bBnh1hajxnmwy6iPOTLhuhLiGyl9QKinkMJnBAer8kJJqZeOrFVF5DdxUVa8Bzfu7_pKuZFZr9GAyplVOKCOBAHmdzKk/gzc_1000102_0b535mavaaabdiam23pjgjt4d26dkcnqcvca.f322062.ts.m3u8?ver=4"):
    """
    output_file： mp4目标结果路径
    m3u8_url: m3u8 的URL
    单个 m3u8 保存 mp4
    """
    command = [
        'ffmpeg',
        '-i', m3u8_url,  # 输入m3u8地址
        '-c', 'copy',  # 直接复制流，不重新编码（速度快）
        '-bsf:a', 'aac_adtstoasc',  # 修复AAC音频流
        output_file
    ]

    subprocess.run(command, check=True)
    print("转换完成！")


class get_save_ts:
    """
    m3u8_urls: 可用的m3u8列表
    将m3u8列表中的ts提取到txt中
    """

    def __init__(self, m3u8_urls):
        self.m3u8_urls = m3u8_urls
        # self.m3u8_urls = [
        #     'https://ltshwy.gtimg.com/B_fXrb0otmtGHxqhZ5HYDTdp8-LZVRr0TIxDygVJgULVk4-ybU6DrlUaoEpybJyZ3iYs_m5GcgY34j2ePpfQVMrRfTylGJ3qfUp8BUUfP8fScFyzzhwDvF1V5YyaAUUw81Sg519NWDEvBWWQGpQ5Blpw/svp_50112/AmSXh0CLKAjIZkHvB8ECoZXxnLDkTzmZ3reHaH9-4iNTKl3mtQnvtkbWsPsK2xt-EeP8kNOjuYfKdJLLQFsLYlTEcLBEhlgWFyujJgbAej23VH7iL4uEt85a1CiArOh_lOS_UCz4oMEfoU_bBnh1hajxnmwy6iPOTLhuhLiGyl9QKinkMJnBAer8kJJqZeOrFVF5DdxUVa8Bzfu7_pKuZFZr9GAyplVOKCOBAHmdzKk/gzc_1000102_0b535mavaaabdiam23pjgjt4d26dkcnqcvca.f322062.ts.m3u8?ver=4',
        #     'https://e958d3814b48854fd4e8a00331324107.v.smtcdns.com/moviets.tc.qq.com/AAZXM5FX8o_1q6l2xxj4wenQVr44jgEwkRF3wK_yVQdk/B_fXrb0otmtGHxqhZ5HYDTdm68Bvo8RUP7Yw0Te27p1zA4-ybU6DrlUaoEpybJyZ3iYs_m5GcgY34j2ePpfQVMrRfTylGJ3qfUp8BUUfP8fScFyzzhwDvF1V5YyaAUUw81Sg519NWDEvBWWQGpQ5Blpw/svp_50112/AmSXh0CLKAjIZkHvB8ECoZXxnLDkTzmZ3reHaH9-4iNTKl3mtQnvtkbWsPsK2xt-EeP8kNOjuYfKdJLLQFsLYlTEcLBEhlgWFyujJgbAej23VH7iL4uEt85a1CiArOh_lOS_UCz4oMEfoU_bBnh1hajxnmwy6iPOTLhuhLiGyl9QKinkMJnBAer8kJJqZeOrFVF5DdxUVa8Bzfu7_pKuZFZr9GAyplVOKCOBAHmdzKk/gzc_1000102_0b535mavaaabdiam23pjgjt4d26dkcnqcvca.f322062.ts.m3u8?ver=4',
        #
        # ]

    def get_all_ts_urls(self):
        all_ts = []
        for url in self.m3u8_urls:
            playlist = M3U8(requests.get(url).text)
            ts_urls = [segment.uri for segment in playlist.segments]
            # print(ts_urls)
            if not ts_urls[0].startswith('http'):
                base_url = '/'.join(url.split('/')[:-1]) + '/'
                ts_urls = [base_url + ts for ts in ts_urls]
            all_ts.extend(ts_urls)
        return all_ts

    def save_ts(self):
        all_ts = self.get_all_ts_urls()

        # 保存 TS 地址到文件（供 FFmpeg 使用）
        with open('ts_list.txt', 'w') as f:
            for ts in all_ts:
                f.write(f"file '{ts}'\n")
                print('ts_list.txt 已成功保存到其中')


def ffmpeg_save(input_file, output_file):
    """
    output_file :mp4结果路径
    将ts文件列表(ts_list.txt) 保存为mp4
    """
    command = [
        'ffmpeg',
        '-f', 'concat',  # 使用 concat 协议合并
        '-safe', '0',  # 避免安全检查报错
        '-protocol_whitelist', 'file,http,https,tcp,tls',  # 允许所有协议
        '-i', input_file,
        '-c', 'copy',  # 直接复制流，不重新编码
        '-bsf:a', 'aac_adtstoasc',  # 修复音频格式
        output_file
    ]
    subprocess.run(command, check=True)

    print("已成功将 m3u8 转为 mp4 ")


if __name__ == '__main__':
    m3u8_urls = [
        'https://defaultts.tc.qq.com/moviets.tc.qq.com/AJSdQY-pybQLCmt4nQxUno93Y2MglGBBv7lcX3q1wxHs/B_fXrb0otmtGHxqhZ5HYDTdgNcKvofz6phQngU6Of3-C_vUy4IiEiqodQ2C1GN8LOpGvrzU_xZYb2n3BCGv-LMrolzZi2SwYLcmpNkUm_bn60FyzzhwDvF1V5YyaAUUw81Sg519NWDEvBWWQGpQ5Blpw/svp_50112/sWhJY3dcI8KVQMOuwc0MBiPg3IMRc_lC-sY3Q2gmpyM-IIAK_9drjd7Ahi_tRT3EmBG9uigtmPGJkdVXUNqTC7Zl1yNM49OxKMTr7XKiYOks3og5kn4CA7T_HS2lan14R_0xaEQOPlhZlqNc1iZY8ExoHtGWlP2fy_w3Tkw5ElEI-inGf3TxQYZtCXipFgTYoWlZcpkrciIUQKbRfRfaIYCZR1TZ1j82jCOJ4DH2P5c/gzc_1000102_0b53euavaaabr4apnb7jgrt4cjodkbkqcvca.f322062.ts.m3u8?ver=4',
        'https://apd-vlive.apdcdn.tc.qq.com/defaultts.tc.qq.com/B_fXrb0otmtGHxqhZ5HYDTdpaVKpLEyUfm2-beHHamm3jvUy4IiEiqodQ2C1GN8LOpGvrzU_xZYb2n3BCGv-LMrolzZi2SwYLcmpNkUm_bn60FyzzhwDvF1V5YyaAUUw81Sg519NWDEvBWWQGpQ5Blpw/svp_50112/sWhJY3dcI8KVQMOuwc0MBiPg3IMRc_lC-sY3Q2gmpyM-IIAK_9drjd7Ahi_tRT3EmBG9uigtmPGJkdVXUNqTC7Zl1yNM49OxKMTr7XKiYOks3og5kn4CA7T_HS2lan14R_0xaEQOPlhZlqNc1iZY8ExoHtGWlP2fy_w3Tkw5ElEI-inGf3TxQYZtCXipFgTYoWlZcpkrciIUQKbRfRfaIYCZR1TZ1j82jCOJ4DH2P5c/gzc_1000102_0b53euavaaabr4apnb7jgrt4cjodkbkqcvca.f322062.ts.m3u8?ver=4']

    SavaTs = get_save_ts(m3u8_urls)
    SavaTs.save_ts()
    ffmpeg_save(input_file='ts_list.txt', output_file="merged_output.mp4")
