# -- coding: utf-8 --
# @Author: 胡H
# @File: tp_pdf.py
# @Created: 2025/4/27 17:57
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
from PIL import Image

# 指定要拼接的 JPG 文件列表（按顺序）
image_files = [
    "image/0.png",
    "image/1.png",
    "image/2.png",
]

# 打开所有图像
images = [Image.open(img) for img in image_files]

# 保存为 PDF，第一个图像作为第一页，其余依次添加
images[0].save(
    "output.pdf",
    "PDF",
    resolution=100.0,
    save_all=True,
    append_images=images[1:]
)
