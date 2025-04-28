import os

import uiautomator2 as u2
import time


def file_exists(d):
    target_folder = "/sdcard/DCIM/Screenshots/"  #
    destination_folder_on_pc = r"E:\AAA-project\muchen_project\豆包爱学\result"  # 电脑上的目标文件夹路径
    # 确保目标文件夹存在
    if not os.path.exists(destination_folder_on_pc):
        os.makedirs(destination_folder_on_pc)

    refresh_command = f"am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://{target_folder}"
    d.shell(refresh_command).output.strip()

    result1 = d.shell(f"ls {target_folder}").output.strip()
    if result1:
        pull_command = f"adb pull {target_folder} {destination_folder_on_pc}"
        os.system(pull_command)  # 执行命令

    command = f"rm -rf {target_folder}/*"
    d.shell(command).output.strip()

    refresh_command = f"am broadcast -a android.intent.action.MEDIA_MOUNTED -d file://{target_folder}"
    d.shell(refresh_command).output.strip()


def resou_auto(d):
    # 获取 index 为 0 的子元素

    children = d(resourceId="com.aitutor.hippo:id/an=").child(className="android.widget.LinearLayout")
    lines = children.child(resourceId="com.aitutor.hippo:id/aog")
    # print("1111", lines)
    time.sleep(2)
    for line in lines:

        print('line:\t', line)
        line.click()
        tr_zk = d(resourceId="com.aitutor.hippo:id/tr").click_exists()

        d(text="展开全部").click_exists(timeout=2)

        d(packageName="com.miui.touchassistant").click()  # 点圆圈
        d(packageName="com.miui.touchassistant", index=3).click()  # 截图
        time.sleep(3)
        d(text='截长屏').click_exists(timeout=3)

        g_beck = d(resourceId='com.miui.mediaeditor:id/save_iv')
        start_time = time.time()
        while not g_beck.exists:
            g_beck = d(resourceId='com.miui.mediaeditor:id/save_iv')
            if time.time() - start_time > 50:
                print("超时")
                break
            time.sleep(1)
        d(resourceId='com.miui.mediaeditor:id/save_iv').click()

        file_exists(d)


def main_outer(d):
    d(resourceId='com.aitutor.hippo:id/arj').click()

    d(resourceId='com.aitutor.hippo:id/mj').click()
    parents = d(resourceId="com.aitutor.hippo:id/afq")
    lg_lis = parents.child(resourceId='com.aitutor.hippo:id/1g')
    for lg in lg_lis:
        # print(lg)
        lg.click()

        resou_auto(d)

        time.sleep(2)
        d(text='再拍一页').click()
        d(resourceId='com.aitutor.hippo:id/mj').click()


if __name__ == '__main__':
    d = u2.connect('2080e939')
    d.implicitly_wait(3)

    # resou_auto(d)
    main_outer(d)
