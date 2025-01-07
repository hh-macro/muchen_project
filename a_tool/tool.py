# 万能工具包
import time

import chardet
import requests


def encode_conver(wrong_encoded_str):
    """
    ----编码功能----
    编码错误检测替换--将编码错误的字符串进行重新编码转换，尝试将其转换为正确的编码形式
    """
    detected = chardet.detect(wrong_encoded_str.encode('latin1'))
    try:
        corrected_str = wrong_encoded_str.encode('latin1').decode(detected['encoding'])
        return corrected_str
    except UnicodeDecodeError:
        print("")


def pdf_save(pdffile_url, filename=''):
    """
    ----pdf保存功能----
    将pdf地址保存本地，filename默认为空，意思是在当前目录下，加上则是保存当前{目录名}下
    """
    response = requests.get(pdffile_url)
    png_name = int(time.time() * 1000000)
    if filename:
        with open(f"{filename}/{png_name}.pdf", "wb") as file:
            file.write(response.content)
    else:
        with open(f"{png_name}.pdf", "wb") as file:
            file.write(response.content)
    print(f'{pdffile_url} ----保存成功')


def png_save(rout_img, filename=''):
    """
    ----保存图片png功能----
    """
    image_content = requests.get(rout_img).content
    png_name = int(time.time() * 1000000)
    if filename:
        with open(f'{filename}/{png_name}.jpg', 'wb') as f:
            f.write(image_content)
    else:
        with open(f'{png_name}.jpg', 'wb') as f:
            f.write(image_content)
    print(f'{rout_img} ----保存成功')


def mp3_save(audio_url, filename=''):
    """
    ----保存音频----
    """
    response = requests.get(audio_url)
    audio_name = int(time.time() * 1000000)
    if filename:
        with open(f"{filename}/{audio_name}.mp3", "wb") as file:
            file.write(response.content)
    else:
        with open(f"{audio_name}.mp3", "wb") as file:
            file.write(response.content)
    print(f'{audio_url} ----保存成功')
