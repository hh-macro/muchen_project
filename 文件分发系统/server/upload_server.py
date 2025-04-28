import yaml
from minio import Minio
import os
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

# ================= 日志配置 =================
logger.add(
    "../upload.log",
    rotation="10 MB",
    retention="30 days",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    encoding="utf8"  # 指定文件编码为 UTF-8
)

logger.add(
    lambda msg: print(msg, end=""),
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
)


# 从 YAML 文件加载配置
def load_config():
    with open("server-config.yaml", "r", encoding='utf-8') as file:
        return yaml.safe_load(file)


CONFIG = load_config()


def create_minio_client():
    """创建 MinIO 客户端"""
    return Minio(
        CONFIG["minio"]["endpoint"],
        access_key=CONFIG["minio"]["access_key"],
        secret_key=CONFIG["minio"]["secret_key"],
        secure=CONFIG["minio"]["secure"]
    )


class ProgressCallback:
    def __init__(self, object_name, total_size):
        self.object_name = object_name  # 文件名
        self.total_size = total_size  # 文件总大小（字节）
        self.transferred = 0  # 已传输的字节数

    def update(self, transferred_bytes):
        """处理进度更新"""
        self.transferred = transferred_bytes
        percentage = (self.transferred / self.total_size) * 100 if self.total_size > 0 else 0
        logger.debug(
            f"{self.object_name} - "
            f"已上传: {percentage:.1f}% "
            f"({self.transferred / (1024 * 1024):.2f} MB / {self.total_size / (1024 * 1024):.2f} MB)"
        )

    def set_meta(self, *args, **kwargs):
        """兼容 MinIO 内部调用"""
        pass


def upload_file(file_info):
    """带进度显示的文件上传"""
    full_path, object_name = file_info
    try:
        total_size = os.path.getsize(full_path)
        progress_callback = ProgressCallback(object_name, total_size)
        client = create_minio_client()
        client.fput_object(
            CONFIG["bucket"]["name"],
            object_name,
            full_path,
            progress=progress_callback
        )
        logger.success(f"✅ 上传完成: {object_name}")
        return True
    except Exception as e:
        logger.error(f"❌ 上传失败 {object_name}: {str(e)}")
        return False


def list_local_files(local_dir):
    """列出本地目录中的所有文件"""
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, local_dir).replace("\\", "/")
            yield full_path, rel_path


def ensure_bucket_exists(client, bucket_name):
    """确保存储桶存在"""
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logger.info(f"✅ 存储桶 '{bucket_name}' 创建成功")
        else:
            logger.info(f" oxidizable 后验存储桶 '{bucket_name}' 已存在")
    except Exception as e:
        logger.error(f"❌ 创建存储桶时出错: {str(e)}")
        raise


def main():
    """主上传逻辑"""
    logger.info(f"🔄 开始上传本地目录 [{CONFIG['local']['directory']}] 到存储桶 [{CONFIG['bucket']['name']}]")

    # 创建 MinIO 客户端
    client = create_minio_client()
    ensure_bucket_exists(client, CONFIG["bucket"]["name"])

    local_files = list(list_local_files(CONFIG["local"]["directory"]))
    if not local_files:
        logger.warning("⚠️ 本地目录中没有文件可上传")
        return
    logger.info(f"📁 发现 {len(local_files)} 个待上传文件")
    with ThreadPoolExecutor(max_workers=CONFIG["settings"]["max_workers"]) as executor:
        results = executor.map(upload_file, local_files)
    success_count = sum(1 for r in results if r)
    logger.info(
        f"🎉 上传完成！成功: {success_count}/{len(local_files)} | "
        f"目标存储桶: {CONFIG['bucket']['name']}"
    )


if __name__ == "__main__":
    main()