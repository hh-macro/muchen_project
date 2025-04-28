import os
import subprocess

import uiautomator2 as u2


def push_directory(destination_folder_on_pc, target_folder):
    """ 将 destination_folder_on_pc 路径内容传入到手机端 target_folder """
    push_command = ["adb", "push", destination_folder_on_pc, target_folder]
    result_1 = subprocess.run(push_command, capture_output=True, text=True, encoding="utf-8")
    refresh_command = ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d",
                       f"file://{target_folder}"]
    if result_1.returncode == 0:
        subprocess.run(refresh_command, capture_output=True, text=True, encoding="utf-8")
        print("文件推送成功！")
        print(result_1.stdout)


d = u2.connect('2080e939')

destination_folder_on_pc = r"D:/atimu/01_04_02_aliyun@2a8dc48a-13dd-4dad-bb83-a89e43f05698_234696.jpg"
target_path = "/sdcard/Pictures/cache/a1.jpg"

push_command = ["adb", "push", destination_folder_on_pc, target_path]
result_1 = subprocess.run(push_command, capture_output=True, text=True, encoding="utf-8")
if result_1.returncode == 0:
    print("文件推送成功！")

command = f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{target_path}"
result = d.shell(command)
print("媒体库扫描命令执行结果:", result.output.strip())

d(resourceId='com.baidu.homework:id/zyb').click()
# adb shell am broadcast \ -a android.intent.action.MEDIA_SCANNER_SCAN_FILE \ -d "file:///sdcard/DCIM/Camera/01_04_02_aliyun@1a40dbc7-599a-4124-ae7d-1a5e56023607_844623.jpg"