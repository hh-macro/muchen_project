"""
查找模拟器或者手机的CPU类型：adb shell getprop ro.product.cpu.abi
    frida -U -f com.aitutor.hippo -l byteDance.js
    运行应用后再附加脚本，避免过早注入： frida -U -n com.aitutor.hippo -l byteDance.js

打开软件com.aitutor.hippo -- adb shell monkey -p com.aitutor.hippo -c android.intent.category.LAUNCHER 1

./fri666 -l 0.0.0.0:1234

python r0capture.py -U -f com.aitutor.hippo -p soul3.pcap

将证书从windows系统移动到模拟器安卓系统下:  adb push 证书路径 /system/etc/security/cacerts/
"""

import os
import subprocess

import uiautomator2 as u2

# 指定目标文件夹路径
d = u2.connect('2080e939')

target_folder = "/sdcard/DCIM/Screenshots/"  #
destination_folder_on_pc = r"E:\AAA-project\muchen_project\豆包爱学\result"  # 电脑上的目标文件夹路径
# 确保目标文件夹存在
if not os.path.exists(destination_folder_on_pc):
    os.makedirs(destination_folder_on_pc)

# 执行 shell 命令列出文件夹内容
result1 = d.shell(f"ls {target_folder}").output.strip()
print(result1)


# if result1:
#     # os.makedirs(destination_folder_on_pc)
#     pull_command = f"adb pull {target_folder} {destination_folder_on_pc}"
#     result = os.system(pull_command)  # 执行命令

# command = f"rm -rf {target_folder}/*"
# result2 = d.shell(command).output.strip()

# refresh_command = f"am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://{target_folder}"
# refresh_result = d.shell(refresh_command).output.strip()
source_folder_on_pc = r"E:\jpg_a\Snipaste_2025-01-13_17-21-03.jpg"
target_folder_on = '/sdcard/DCIM/Camera'
push_command = f"adb push {source_folder_on_pc} {target_folder_on}"
result = os.system(push_command)
target_folder_on = "/sdcard/DCIM/Camera"

command = f"adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{target_folder_on}"
result1 = subprocess.run(command, shell=True, capture_output=True)


