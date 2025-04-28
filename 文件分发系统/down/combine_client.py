import json
import re
import os

import psutil
from loguru import logger
from pathlib import Path

from minio import Minio
import yaml
import shutil
from tqdm.auto import tqdm  # 新增进度条库

import signal

# ================= 日志配置 =================
logger.add(
    "../download.log",  # 日志文件
    rotation="10 MB",  # 按大小轮转
    retention="30 days",  # 保留周期
    enqueue=True,  # 线程安全
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # 简化格式
    level="DEBUG",  # 日志级别
    encoding="utf8"  # 指定文件编码为 UTF-8
)

# 同时输出到控制台（带颜色和表情符号）
logger.add(
    lambda msg: print(msg, end=""),
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    level="DEBUG",
    filter=lambda record: "🚀" in record["message"] or "🎉" in record["message"] or "❌" in record["message"]
)


# ====================从 YAML 文件加载配置=======================

def load_config():
    with open("config.yaml", "r", encoding='utf-8') as file:
        return yaml.safe_load(file)


CONFIG = load_config()

WHITELIST_FILE = CONFIG['confWay']['WHITELIST_FILE']  # 白名单关联
PROGRAM_KEY = CONFIG['confWay']['PROGRAM_KEY']


# ===========================================

class ProgressCallback:
    def __init__(self, object_name, total_size, progress_bar):
        self.object_name = object_name
        self.total_size = total_size
        self.progress_bar = progress_bar  # 使用 tqdm 进度条

    def update(self, downloaded_bytes):
        """处理进度更新"""
        self.progress_bar.update(downloaded_bytes)  # 更新进度条

    def set_meta(self, *args, **kwargs):
        pass  # 兼容 MinIO 内部调用


# ===========================================

def create_minio_client():
    """创建MinIO客户端"""
    return Minio(
        CONFIG["minio"]["endpoint"],
        access_key=CONFIG["minio"]["access_key"],
        secret_key=CONFIG["minio"]["secret_key"],
        secure=CONFIG["minio"]["secure"]
    )


def ensure_folder_exists(local_folder):
    """
    检查本地文件夹是否存在，如果不存在则创建。
    """
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)
        # print(f"文件夹已创建: {local_folder}")
    else:
        print(f" ")


def get_local_files_and_folders(local_dir):
    """获取本地指定路径下的所有文件和文件夹名（仅当前层级）"""
    items = []
    try:
        for item in os.listdir(local_dir):
            items.append(item)
    except Exception as e:
        logger.error(f"❌ 获取本地文件和文件夹时出错: {str(e)}")
    return items


def get_minio_objects(client, bucket_name, prefix):
    """获取MinIO存储桶中指定前缀下的所有文件和文件夹名（仅当前层级）"""
    items = []
    try:
        for obj in client.list_objects(bucket_name, prefix=prefix, recursive=False):
            # 去掉前缀并排除路径中的前导/后导斜杠
            relative_path = obj.object_name[len(prefix):].strip("/")
            if "/" in relative_path:
                # 是文件夹
                name = relative_path.split("/")[0]
                items.append(name)
            else:
                # 是文件
                items.append(relative_path)
    except Exception as e:
        logger.error(f"❌ 获取MinIO对象时出错: {str(e)}")
    return items


def compare_names(local_items, minio_items):
    """比较本地和MinIO的文件和文件夹名，返回名字不一样的项"""
    local_set = set(local_items)
    minio_set = set(minio_items)
    different_items = minio_set - local_set  # 存储桶有而本地没有的项
    return different_items


def delete_local_item(local_path):
    """删除本地文件或文件夹"""
    try:
        if os.path.isdir(local_path):
            shutil.rmtree(local_path)
            logger.info(f"刪除本地文件夹: {local_path}")
        else:
            os.remove(local_path)
            logger.info(f"刪除本地文件: {local_path}")
    except Exception as e:
        logger.error(f"❌ 刪除本地文件或文件夹时出错: {str(e)}")


def download_item(client, bucket_name, minio_item, local_dir, bucket_dir):
    """下载MinIO中的文件或文件夹"""
    try:
        minio_path = os.path.join(bucket_dir, minio_item).replace('\\', '/')

        try:
            obj = client.stat_object(bucket_name, minio_path)
            is_file = not obj.is_dir
        except Exception as e:
            if e.code == "NoSuchKey":
                # 当对象不存在时，尝试作为虚拟文件夹处理
                is_file = False
            else:
                raise

        local_path = os.path.join(local_dir, minio_item)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        if is_file:
            # 文件下载流程
            try:
                obj_info = client.stat_object(bucket_name, minio_path)
                total_size = obj_info.size

                with tqdm(total=total_size, unit_scale=True, unit_divisor=1024, unit="B",
                          desc=f"📥 下载文件: {minio_item}") as progress_bar:
                    client.fget_object(
                        bucket_name,
                        minio_path,
                        local_path,
                        progress=ProgressCallback(minio_item, total_size, progress_bar)
                    )
                logger.success(f"✅ 文件下载成功 | 路径: {local_path}")
            except Exception as e:
                logger.error(f"🚨 文件下载失败 {minio_path} -> {local_path}: {str(e)}")
                if os.path.exists(local_path):
                    os.remove(local_path)  # 清理不完整文件
        else:
            # 文件夹下载流程
            try:
                if not os.path.exists(local_path):
                    os.makedirs(local_path, exist_ok=True)
                    logger.info(f"📁 创建本地目录 | 路径: {local_path}")

                # 获取文件夹中所有文件的总数
                objects = [obj for obj in client.list_objects(bucket_name, prefix=minio_path, recursive=True) if
                           not obj.is_dir]
                total_files = len(objects)

                with tqdm(total=total_files, desc=f"🚀 下载文件夹: {minio_item}", unit="file") as progress_bar:
                    for obj in objects:
                        relative_path = obj.object_name[len(minio_path):].lstrip('/')
                        nested_local = os.path.join(local_path, relative_path)
                        os.makedirs(os.path.dirname(nested_local), exist_ok=True)
                        client.fget_object(bucket_name, obj.object_name, nested_local)
                        progress_bar.update(1)
                        # 每下载一个文件更新进度条

                logger.success(f"📦 目录下载完成 | 路径: {local_path}")
            except Exception as e:
                logger.error(f"🚨 目录下载失败 {minio_path}: {str(e)}")
                if os.path.exists(local_path) and not os.listdir(local_path):
                    os.rmdir(local_path)  # 清理空目录

    except Exception as e:
        logger.error(f"🔍 MinIO访问异常 | 路径: {minio_path} | 错误: {str(e)}")


def download_folder(client, bucket_name, minio_folder, local_folder):
    """下载MinIO中的文件夹及其内容"""
    os.makedirs(local_folder, exist_ok=True)
    objects = client.list_objects(bucket_name, prefix=minio_folder, recursive=True)
    for obj in objects:
        local_path = os.path.join(local_folder, obj.object_name[len(minio_folder):].strip("/"))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        client.fget_object(bucket_name, obj.object_name, local_path)
        logger.success(f"🎉 下载完成! 📁 文件: {local_path}")


def download_main():
    minio_config = CONFIG['minio']
    buckets = CONFIG.get('buckets', [])
    local_dir_template = CONFIG['local']['local_dir']  # 本地目录模板

    # client = create_minio_client()

    for bucket_config in buckets:
        client = create_minio_client()  # 再次创建 MinIO 客户端

        bucket_name = bucket_config['name']
        bucket_dir = bucket_config['bucket_dir']
        local_dir = local_dir_template.format(bucket_name=bucket_name, bucket_dir=bucket_dir)  # 动态生成本地目录
        # print(local_dir)
        logger.info(f"🔄🔄🔄 启动同步存储桶: {bucket_name} (本地路径: {local_dir})")

        file_exist(local_dir)  #

        ensure_folder_exists('D:/bucket')
        ensure_folder_exists(f'D:/bucket/{bucket_name}')

        # 获取本地文件和文件夹名
        local_items = get_local_files_and_folders(local_dir)
        local_set = set(local_items)

        # 获取存储桶中文件和文件夹名
        minio_items = get_minio_objects(client, bucket_name, bucket_dir)
        minio_set = set(minio_items)

        # 比较名字
        different_items = compare_names(local_items, minio_items)
        # print(different_items)
        if different_items:
            logger.info("以下文件和文件夹名在本地和存储桶中不一致:")
            for item in different_items:
                logger.info(f" - {item}")

        # 删除本地多余的文件和文件夹
        for item in local_set - minio_set:
            # kill_all_python_processes()
            kill_all_java_processes()
            kill_white_list_all_python_processes(WHITELIST_FILE, PROGRAM_KEY)

            local_path = os.path.join(local_dir, item)
            delete_local_item(local_path)

        # 下载存储桶中缺少的文件和文件夹
        for item in minio_set - local_set:
            download_item(client, bucket_name, item, local_dir, bucket_dir)

        logger.success(f"🎉 同步完成! 📂 存储桶: {bucket_name} ✅ 成功同步文件夹: {local_dir}")
        # 清理 MinIO 客户端（可选）
        del client

    logger.success("🎉 所有存储桶同步完成!")


# ========================= v2 =============================

def get_minio_files(client, bucket_name, prefix):
    """获取存储桶中所有文件完整路径（递归）"""
    file_paths = []
    try:
        # 标准化前缀格式
        prefix = prefix.rstrip('/') + '/' if prefix else ''
        objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)

        for obj in objects:
            if obj.is_dir:
                continue
            # 保留完整路径（包含前缀）
            full_path = obj.object_name
            file_paths.append(full_path)
    except Exception as e:
        logger.error(f"❌ 获取MinIO文件列表失败: {str(e)}")
    return file_paths


def get_local_files(local_dir, bucket_dir):
    """获取本地所有文件相对路径（基于存储桶目录结构）"""
    local_files = []
    try:
        base_path = Path(local_dir)
        for file_path in base_path.rglob('*'):
            if file_path.is_file():
                # 计算相对于存储桶目录的路径
                rel_path = str(file_path.relative_to(base_path))
                local_files.append(rel_path.replace('\\', '/'))
    except Exception as e:
        logger.error(f"❌ 获取本地文件列表失败: {str(e)}")
    return local_files


# ==================== 文件同步操作 ====================
def sync_files(client, bucket_name, prefix, local_dir):
    """执行文件同步的核心逻辑"""
    # 获取文件列表
    minio_full_paths = get_minio_files(client, bucket_name, prefix)

    # 生成相对路径映射
    minio_relative_map = {
        p[len(prefix):]: p  # 保留原始完整路径
        for p in minio_full_paths
        if p.startswith(prefix)
    }
    # print('minio_relative_map:', minio_relative_map)

    local_files = set(get_local_files(local_dir, prefix))
    # print(local_files)
    # 计算需要删除的本地文件
    # obsolete_files = local_files - set(minio_relative_map.keys())
    obsolete_files = set(minio_relative_map.keys()) - local_files
    for rel_path in obsolete_files:
        local_path = os.path.join(local_dir, rel_path)
        try:
            if not os.path.exists(local_path):  # 新增存在性检查
                logger.warning(f"⚠️ 本地文件不存在，跳过删除: {local_path}")
                continue
            if not os.path.isfile(local_path):  # 防止误删目录
                logger.warning(f"⚠️ 路径不是文件，跳过删除: {local_path}")
                continue
            os.remove(local_path)
            logger.info(f"🗑️ 已删除本地文件: {local_path}")
        except Exception as e:
            logger.error(f"❌ 删除文件失败 {local_path}: {str(e)}")

    # 下载所有minio文件
    for rel_path, full_path in minio_relative_map.items():
        local_path = os.path.join(local_dir, rel_path)

        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            obj_info = client.stat_object(bucket_name, full_path)

            # 下载文件（带进度条）
            with tqdm(
                    total=obj_info.size,
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"📥 下载 {os.path.basename(local_path)}"
            ) as pbar:
                client.fget_object(
                    bucket_name,
                    full_path,
                    local_path,
                    progress=ProgressCallback(full_path, obj_info.size, pbar)
                )
            logger.success(f"✅ 已同步文件: {local_path}")
        except Exception as e:
            logger.error(f"🚨 文件同步失败 {full_path} -> {local_path}: {str(e)}")
            # 清理不完整文件
            if os.path.exists(local_path):
                os.remove(local_path)


# ===================================================================
def check_and_clean_versions(client, bucket_name, bucket_prefix, local_base_path):
    """
    版本检测与清理函数
    返回是否需要执行同步（True需要同步，False跳过）
    """

    # 获取存储桶最新版本目录名
    def get_bucket_version():
        try:
            objects = client.list_objects(bucket_name, prefix=bucket_prefix, recursive=False)
            for obj in objects:
                # print(f"Object Name: {obj.object_name}")
                dir_name = obj.object_name[len(bucket_prefix):].strip('/')
                # print('dir_name:\t', dir_name)  # zuoyebang-SQ-3/
                if re.match(r'version-\d+\.\d+\.\d+', dir_name):
                    return dir_name
        except Exception as e:
            logger.error(f"❌ 获取存储桶版本失败: {str(e)}")
        return None

    def get_local_version():
        try:
            # print(local_base_path)
            for entry in Path(local_base_path).iterdir():
                # print(entry.name)
                if re.match(r'version-\d+\.\d+\.\d+', entry.name):
                    return entry.name
            return None
        except Exception as e:
            logger.error(f"❌ 获取本地版本失败: {str(e)}")
            return None

    bucket_ver = get_bucket_version()
    # print('bucket_ver:\t', bucket_ver)
    local_ver = get_local_version()
    # print('local_ver:\t', local_ver)

    if not bucket_ver:
        logger.warning("⚠️ 存储桶中没有找到版本文件, 将进行跳过")
        return False  # 需要同步

    if not local_ver:
        logger.warning("⚠️ 本地中没有找到版本文件, 将进行跳过")
        return False  # 需要同步

    if bucket_ver == local_ver:
        logger.info(f"✅ 版本一致 ({local_ver}) 无需操作")
        return False  # 跳过同步

    if local_ver:
        old_path = os.path.join(local_base_path, local_ver)
        # print('old_path:\t', old_path)
        try:
            if os.path.isfile(old_path):
                os.remove(old_path)  # 删除文件
                logger.info(f"🗑️ 已删除旧版本: {old_path}")
        except Exception as e:
            logger.error(f"❌ 删除旧版本失败: {str(e)}")
            return False

    return True  # 需要同步


def down_main():
    client = create_minio_client()

    for bucket_config in CONFIG["buckets"]:
        bucket_name = bucket_config["name"]
        bucket_dir = bucket_config["bucket_dir"]
        local_dir = CONFIG["local"]["local_dir"].format(
            bucket_name=bucket_name,
            bucket_dir=bucket_dir
        )

        logger.info(f"🔄🔄🔄 开始同步存储桶 [{bucket_name}] 到目录 {local_dir}")

        file_exist(f'D:/bucket/{bucket_name}/{bucket_dir}')  #

        local_dir = os.path.normpath(local_dir)
        # 确保本地目录存在
        Path(local_dir).mkdir(parents=True, exist_ok=True)

        # 新增版本检测
        need_sync = check_and_clean_versions(
            client,
            bucket_name,
            bucket_dir,  # 示例：zyb/zuoyebang-SQ-3/
            Path(local_dir)  # 示例：D:/bucket/zyb/zuoyebang-SQ-3
        )
        # print('need_sync:\t', need_sync)
        # need_sync = False
        if not need_sync:
            continue

        try:
            kill_all_java_processes()
            # kill_all_python_processes()

            kill_white_list_all_python_processes(WHITELIST_FILE, PROGRAM_KEY)

            sync_files(client, bucket_name, bucket_dir, local_dir)
            logger.success(f"🎉 存储桶 [{bucket_name}] 同步完成 ")
        except Exception as e:
            logger.error(f"❌ 存储桶 [{bucket_name}] 同步失败: {str(e)}")

    logger.success("🎉🎉🎉 所有存储桶同步完成！")


def file_exist(path):
    # CONFIG = load_config()
    # path = CONFIG['local']['local_dir']
    # path = "D:at1/at2/at3"
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"目录不存在已创建: {path}")


def kill_all_python_processes():
    try:
        for proc in psutil.process_iter(attrs=['name']):
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                pid = proc.pid
                os.kill(pid, signal.SIGTERM)
                print(f"已终止进程: {pid}")
    except Exception as e:
        print(f"发生错误: {e}")


def kill_all_java_processes():
    try:
        for proc in psutil.process_iter(attrs=['name']):
            if proc.info['name'] and 'java' in proc.info['name'].lower():
                pid = proc.pid
                os.kill(pid, signal.SIGTERM)
                print(f"已终止进程: {pid}")
    except Exception as e:
        print(f"发生错误: {e}")


def save_pid_to_whitelist(current_pid, WHITELIST_FILE, PROGRAM_KEY):
    try:
        with open(WHITELIST_FILE, "r") as f:
            whitelist = json.load(f)
    except FileNotFoundError:
        whitelist = []

    found = False
    for entry in whitelist:
        if PROGRAM_KEY in entry:
            entry[PROGRAM_KEY] = current_pid
            found = True
            break
    if not found:
        whitelist.append({PROGRAM_KEY: current_pid})

    with open(WHITELIST_FILE, "w") as f:
        json.dump(whitelist, f, indent=2)


def get_whitelist_pids(WHITELIST_FILE, PROGRAM_KEY):
    try:
        with open(WHITELIST_FILE, "r") as f:
            whitelist = json.load(f)
        return {pid for entry in whitelist for pid in entry.values()}
    except FileNotFoundError:
        return set()


def kill_white_list_all_python_processes(WHITELIST_FILE, PROGRAM_KEY):
    """终止所有非白名单py进程"""
    whitelist_pids = get_whitelist_pids(WHITELIST_FILE, PROGRAM_KEY)

    try:
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if (
                    proc.info['name']
                    and 'python' in proc.info['name'].lower()
                    and proc.info['pid'] not in whitelist_pids
            ):
                os.kill(proc.info['pid'], signal.SIGTERM)
                print(f"已终止非白名单进程: {proc.info['pid']}")
    except Exception as e:
        print(f"发生错误: {e}")


def pail_mo():
    # WHITELIST_FILE = CONFIG['confWay']['WHITELIST_FILE']
    # PROGRAM_KEY = CONFIG['confWay']['PROGRAM_KEY']

    current_pid = os.getpid()
    print('current_pid:\t', current_pid)
    save_pid_to_whitelist(current_pid, WHITELIST_FILE, PROGRAM_KEY)

    if CONFIG['settings']['schema'] == 'v1':
        for buck_dict in CONFIG['buckets']:
            buck_name = buck_dict['name']
            if '-' in buck_name:
                # print(f'桶`{buck_name}` 不支持当前v1模式! 请更换其他模式')
                logger.critical(f'\t桶`{buck_name}` 不支持当前v1模式! 请更换其他模式')

                return
        down_main()

    elif CONFIG['settings']['schema'] == 'v2':
        for buck_dict in CONFIG['buckets']:
            buck_name = buck_dict['name']
            if '-' not in buck_name:
                # print(f'桶`{buck_name}` 不支持当前v2模式! 请更换其他模式')
                logger.critical(f'\t桶`{buck_name}` 不支持当前v2模式! 请更换其他模式!')
                return
        download_main()

    # print("按任意键关闭程序......")
    # os.system('pause')


if __name__ == '__main__':
    pail_mo()
