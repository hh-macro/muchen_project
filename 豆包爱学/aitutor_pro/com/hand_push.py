import os
import subprocess


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


def hang_image():
    """  将电脑文件destination_folder_on_pc 推入手机目录 target_folder """
    destination_folder_on_pc = r"D:/atimu"
    target_folder = "/sdcard/DCIM/Camera"
    # 遍历文件夹中的所有文件
    for root, _, files in os.walk(destination_folder_on_pc):
        for file in files:
            file_path = os.path.join(root, file)
            # 构造目标路径（去掉文件夹本身的路径）
            relative_path = os.path.relpath(file_path, destination_folder_on_pc)
            target_path = os.path.join(target_folder, relative_path)

            # 调用 push_directory 函数推送单个文件
            push_directory(file_path, os.path.dirname(target_path))


if __name__ == '__main__':
    hang_image()
