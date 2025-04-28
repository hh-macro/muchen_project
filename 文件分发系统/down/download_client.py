from minio import Minio
import os
from loguru import logger
import yaml
import shutil
from tqdm.auto import tqdm  # 新增进度条库

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


def file_exist(path):
    # CONFIG = load_config()
    # path = CONFIG['local']['local_dir']
    # path = "D:at1/at2/at3"
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"目录不存在已创建: {path}")


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

    client = create_minio_client()

    for bucket_config in buckets:
        client = create_minio_client()  # 再次创建 MinIO 客户端

        bucket_name = bucket_config['name']
        bucket_dir = bucket_config['bucket_dir']
        local_dir = local_dir_template.format(bucket_name=bucket_name, bucket_dir=bucket_dir)  # 动态生成本地目录

        logger.info(f"🔄🔄🔄 启动同步存储桶: {bucket_name} (本地路径: {local_dir})")

        file_exist(CONFIG['local']['local_dir'])  #

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
        if different_items:
            logger.info("以下文件和文件夹名在本地和存储桶中不一致:")
            for item in different_items:
                logger.info(f" - {item}")

        # 删除本地多余的文件和文件夹
        for item in local_set - minio_set:
            local_path = os.path.join(local_dir, item)
            delete_local_item(local_path)

        # 下载存储桶中缺少的文件和文件夹
        for item in minio_set - local_set:
            download_item(client, bucket_name, item, local_dir, bucket_dir)

        logger.success(f"🎉 同步完成! 📂 存储桶: {bucket_name} ✅ 成功同步文件夹: {local_dir}")
        # 清理 MinIO 客户端（可选）
        del client

    logger.success("🎉 所有存储桶同步完成!")


if __name__ == "__main__":
    download_main()

"""
2025-03-03    此代码为同步整文件夹，一但发现版本号不相同，则直接替换整个文件夹

"""
