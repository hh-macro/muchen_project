import time

import requests
import os
from urllib.parse import urljoin
import subprocess


def download_m3u8(m3u8_url, folder=''):
    """
    下载m3u8文件并保存到本地。
    """
    response = requests.get(m3u8_url)
    m3u8_content = response.text

    # 从m3u8内容中提取TS分片文件的URL
    ts_files = []
    lines = m3u8_content.splitlines()
    for line in lines:
        line = line.strip()
        if not line.startswith('#') and line:  # 跳过注释行和空行
            ts_url = urljoin(m3u8_url, line)  # 将相对路径转换为完整URL
            ts_files.append(ts_url)

    # 下载TS文件
    ts_filenames = []
    for i, ts_url in enumerate(ts_files):
        if folder:
            ts_filename = f"{folder}/segment_{i}.ts"
        else:
            ts_filename = f"segment_{i}.ts"
        response = requests.get(ts_url)
        with open(ts_filename, 'wb') as ts_file:
            ts_file.write(response.content)
        ts_filenames.append(ts_filename if not folder else ts_filename[len(folder) + 1:])

        # ts_filenames.append(ts_filename[3:])  # 去掉 '{folder}/' 前缀

    # 创建一个文件列表文件，ffmpeg需要这个文件来知道哪些文件需要合并
    with open('filelist.txt', 'w', encoding='utf-8') as f:
        for ts_file in ts_filenames:
            if folder:
                f.write(f"file '{folder}/{ts_file}'\n")
            else:
                f.write(f"file '{ts_file}'\n")

    if folder:
        output_name = f'{folder}/{int(time.time() * 100000)}.mp4'
    else:
        output_name = f'{int(time.time() * 100000)}.mp4'
    # 使用ffmpeg拼接TS文件
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'filelist.txt',
        '-c', 'copy',
        '-loglevel', 'error',
        '-hide_banner',
        output_name

    ]
    subprocess.run(command, check=True)

    # 清理临时文件
    os.remove('filelist.txt')
    for ts_file in ts_filenames:
        if folder:
            file_path = os.path.join(f'{folder}', ts_file)
        else:
            file_path = ts_file
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print(f"文件{file_path}未找到")
    print(f"视频 {output_name} ----保存成功")


if __name__ == '__main__':
    m3u8_url = "https://ltshsy.gtimg.com/B_JxNyiJmktHRgresXhfyMehFiuDrRijjuav-5ECS0M2eiOJZgT85ehPAS2_3rfHNi/svp_50001/gY6MnKdF9b-lyyFLIKXb-G9zQeyEgjJyWmMPayQ5YFg9mpj4bl5WAg3NVfZuP_GmC-iDTxJHnXcHTHsuAEF1QTwuhkI3DuzcJHM4EkF-gmXBV5fwT_OqTlakkRa10yPMDWtHd8oWR_nM340jfJdSbxqlRhbNAYqllQ3zn3W14X-ZSjXgP5f3V53OR-hlI1dcpTxGWib2TloB0wfFgFxvm1ADt7tGOMPn/szg_1749_50001_0bc3i4abmaaa4uajfidthntvcr6dczdqafsa.f306313.ts.m3u8?ver=4"
    download_m3u8(m3u8_url, folder='zl')
