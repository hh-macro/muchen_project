import re
import shutil

from minio import Minio
import os
from loguru import logger
import yaml
from tqdm.auto import tqdm
from pathlib import Path
from packaging import version as pkg_version

# ================= 日志配置 =================
logger.add(
    "../download.log",
    rotation="10 MB",
    retention="30 days",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    encoding="utf8"
)
logger.add(
    lambda msg: print(msg, end=""),
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    level="DEBUG"
)


# ==================== 配置加载 ====================
def load_config():
    with open("config.yaml", "r", encoding='utf-8') as file:
        return yaml.safe_load(file)


CONFIG = load_config()


# ==================== 进度回调类 ====================
class ProgressCallback:
    def __init__(self, object_name, total_size, progress_bar):
        self.object_name = object_name
        self.total_size = total_size
        self.progress_bar = progress_bar

    def update(self, downloaded_bytes):
        self.progress_bar.update(downloaded_bytes)

    def set_meta(self, *args, **kwargs):
        pass


# ==================== MinIO 客户端 ====================
def create_minio_client():
    return Minio(
        CONFIG["minio"]["endpoint"],
        access_key=CONFIG["minio"]["access_key"],
        secret_key=CONFIG["minio"]["secret_key"],
        secure=CONFIG["minio"]["secure"]
    )


# ==================== 文件路径处理 ====================
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


def file_exist(path):
    # CONFIG = load_config()
    # path = CONFIG['local']['local_dir']
    # path = "D:at1/at2/at3"
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"目录不存在已创建: {path}")


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

    # 下载所有MinIO文件
    for rel_path, full_path in minio_relative_map.items():
        local_path = os.path.join(local_dir, rel_path)

        try:
            # 创建父目录（自动生成完整层级）
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # 获取文件信息
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
        print('old_path:\t', old_path)
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

        file_exist(CONFIG['local']['local_dir'])  #

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
            sync_files(client, bucket_name, bucket_dir, local_dir)
            logger.success(f"🎉 存储桶 [{bucket_name}] 同步完成 ")
        except Exception as e:
            logger.error(f"❌ 存储桶 [{bucket_name}] 同步失败: {str(e)}")

    logger.success("🎉🎉🎉 所有存储桶同步完成！")


if __name__ == "__main__":
    down_main()
