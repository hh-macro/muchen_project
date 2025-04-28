import os
import signal
import psutil
import subprocess


def get_pid_by_cmd_name(cmd_name):
    try:
        # 获取所有进程
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            print(proc)
            # 检查进程的命令行参数
            if proc.info['cmdline'] and cmd_name in proc.info['cmdline']:
                return proc.info['pid']
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None


def kill_process_by_pid(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"已终止进程: {pid}")
    except Exception as e:
        print(f"发生错误: {e}")


def kill_all_other_python_processes():
    try:
        # 遍历所有进程
        for proc in psutil.process_iter(attrs=['name', 'cmdline']):
            # 检查进程名称是否包含 "python"
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                # 检查进程的命令行参数是否包含当前脚本名
                if proc.info['cmdline'] and __file__ in proc.info['cmdline']:
                    continue  # 跳过当前脚本
                # 终止其他 Python 进程
                os.kill(proc.pid, signal.SIGTERM)
                print(f"已终止进程: {proc.pid}")
    except Exception as e:
        print(f"发生错误: {e}")


def main():
    # 假设当前脚本的窗口名称是 "my_script"
    cmd_name = "zyb-sign-server"
    pid = get_pid_by_cmd_name(cmd_name)
    if pid:
        kill_process_by_pid(pid)
    else:
        print(f"未找到名称为 {cmd_name} 的进程")

    # 停止其他 Python 程序占用的端口
    kill_all_other_python_processes()


if __name__ == "__main__":
    main()
