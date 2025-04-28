import time
import subprocess
from pathlib import Path

from datetime import date
import uiautomator2 as u2
import shutil


def time_date():
    #  获取今天的 年-月-日
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    return f'{year}-{month}-{day}'


def print_red(text):
    """ 文本前面加上红色前缀"""
    RED = "\033[31m"  # 红色
    RESET = "\033[0m"  # 重置颜色
    print(f"{RED}{text}{RESET}")


# 将一个文件复制到另一个文件或目录
def copy_file(source_name):
    """ 将一个文件复制到另一个文件或目录。"""
    # 源文件路径
    source_folder = Path(r"D:/atimu")
    source = source_folder / source_name  # 源文件的完整路径

    # 目标文件路径
    target_folder = Path(rf"D:/aresult/{time_date()}/timu")
    target = target_folder / source_name  # 目标文件的完整路径

    try:
        shutil.copy(source, target)
    except Exception as e:
        print_red(f"复制文件时发生错误：{e}")


def image_cache_w(image_name):
    # 写入缓存文件
    with open("image_cache", "w") as cache_file:
        cache_file.write(image_name)
    print(image_name + ' --加入缓存成功!')


def image_cache_r():
    # 从缓存文件读取图片名
    with open("image_cache", "r") as cache_file:
        cached_image_name = cache_file.read()
    return cached_image_name


def clear_directory(target_folder):
    """ 删除target_folder路径下的所有内容 """
    command = f"adb shell rm -rf {target_folder}/*"
    subprocess.run(command, shell=True, capture_output=True, text=True)
    refresh_command = ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d",
                       f"file://{target_folder}"]
    subprocess.run(refresh_command, capture_output=True, text=True, encoding="utf-8")
    print("正在删除所有文件...")


def push_directory(destination_folder_on_pc, target_folder):
    """ 将 destination_folder_on_pc 路径内容传入到手机端 target_folder """
    push_command = ["adb", "push", destination_folder_on_pc, target_folder]
    result_1 = subprocess.run(push_command, capture_output=True, text=True, encoding="utf-8")
    refresh_command = ["adb", "shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d",
                       f"file://{target_folder}"]
    # print('refresh_command:\t', refresh_command)
    if result_1.returncode == 0:
        subprocess.run(refresh_command, capture_output=True, text=True, encoding="utf-8")
        print("文件推送成功!")
        # print(result_1.stdout)


def create_parent_and_children():
    """  检查父文件夹是否存在，如果不存在则创建父文件夹和所有子文件夹。"""
    datee_name = time_date()
    parent_folder = rf"D:/aresult/{datee_name}"
    child_folders = ["images", "timu"]
    parent_path = Path(parent_folder)

    # 检查父文件夹是否存在，如果不存在则创建
    if not parent_path.exists():
        print(f"父文件夹 {parent_folder} 不存在，正在创建父文件夹及其子文件夹...")
        parent_path.mkdir(parents=True, exist_ok=True)  # 创建父文件夹
        # 创建所有子文件夹
        for child in child_folders:
            (parent_path / child).mkdir(exist_ok=True)
            print(f"已创建子文件夹：{parent_folder}/{child}")


def hold_folder(device_code='4310d42b'):
    d = u2.connect(device_code)
    d.implicitly_wait(3)

    target_folder = "/sdcard/DCIM/Camera"
    directory_file = r"D:/atimu"

    create_parent_and_children()  # 创建文件夹
    clear_directory(target_folder)  # 第一次清空手机目录

    path = Path(directory_file)
    # 遍历目录及其所有子目录
    for item in path.rglob("*"):  # rglob("*") 递归所有
        if item.is_file():  # 只处理文件
            print('')
            print(f"图片:\t{item} 正在处理...")

            file_name = item.name  # 获取文件名
            copy_file(file_name)  # 复制图片
            d(text='拍题答疑').click_exists()
            d(text='再拍一页').click_exists(timeout=2)
            push_directory(item, target_folder)  # 传入图片
            time.sleep(2)
            # print(item.stem)  # 文件名无后缀
            image_cache_w(item.stem)  # 写入缓存
            try:
                d(resourceId='com.aitutor.hippo:id/mj').click(timeout=5)
                d(resourceId='com.aitutor.hippo:id/1g')[0].click(timeout=5)
            except Exception as e:
                print_red(f"图片加载异常，将重新搜索题目 : {e}")
                time.sleep(2)
                d(resourceId='com.aitutor.hippo:id/aj9').click_exists(timeout=10)
                d(text='再拍一页').click_exists(timeout=2)

                d(resourceId='com.aitutor.hippo:id/mj').click(timeout=5)
                d(resourceId='com.aitutor.hippo:id/1g')[0].click(timeout=5)

            clear_directory(target_folder)  # 清空手机目录
            time.sleep(6)
            d(text='重试').click_exists()
            if not d(resourceId='com.aitutor.hippo:id/aog', text='1').exists(timeout=120):
                print_red(f"网络请求异常\t---- {item.stem}\t 题目无法加载!!! 进行跳过")
                d(resourceId='com.aitutor.hippo:id/aj9').click(timeout=5)
                continue
            try:
                for io in range(1, 30):
                    time.sleep(0.5)
                    d(text='重试').click_exists()
                    max_duration = 15
                    start_time = time.time()
                    while True:
                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        if elapsed_time > max_duration:
                            break
                        elif d(text='识别题目').exists() or d(resourceId='com.aitutor.hippo:id/sl').exists():
                            break
                        elif d(text='满意').exists():
                            break

                    aog_page = d(resourceId='com.aitutor.hippo:id/aog', text=f'{io}').click_exists()
                    if not aog_page:
                        time.sleep(3)
                        print(f'页面题目结果一共{io - 1}道题目')
                        break
            except Exception as e:
                print_red(f"翻页过程出现故障, 将中断翻页搜索下一个题目---- {e}")
                d(text='再拍一页').click_exists(timeout=10)
                continue
            con_page = d(text='再拍一页').click_exists(timeout=10)

            # if not con_page:
            #     for i in range(7):
            #         print(i)
            #         d(text='重试').click_exists(timeout=3)
            #         time.sleep(1)
            #
            #     for io in range(1, 20):
            #         time.sleep(0.3)
            #         aog_page = d(resourceId='com.aitutor.hippo:id/aog', text=f'{io}').click_exists()
            #         if not aog_page:
            #             break


if __name__ == '__main__':
    hold_folder()
