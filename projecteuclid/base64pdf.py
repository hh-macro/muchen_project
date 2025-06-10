# -- coding: utf-8 --
# @Author: 胡H
# @File: base64pdf.py
# @Created: 2025/6/9 11:13
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:
import base64
import os
import time
import uuid

random_uuid = uuid.uuid4()
file_path = "save_pdf/968384.pdf"
print('file_path:\t', file_path)
print('random_uuid:\t', random_uuid)

with open(file_path, "rb") as pdf_file:
    pdf_data = pdf_file.read()
base64_encoded = base64.b64encode(pdf_data).decode("utf-8")

print('base64_encoded:\t', base64_encoded[:100])


file_size = os.path.getsize(file_path)  # 单位是字节
print('file_size:\t', file_size)

print('int(time.time()):\t', int(time.time()))
