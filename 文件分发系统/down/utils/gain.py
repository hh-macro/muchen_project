from minio import Minio

# 创建 MinIO 客户端
client = Minio(
    "47.99.52.9:9000",
    access_key="admin",
    secret_key="Aa123456.",
    secure=False, 
)

bucket_name = "zyb"
object_name = "zuoyebang-SQ-3/version-3.5.1"

try:
    data = client.get_object(bucket_name, object_name)
    content = data.read().decode("utf-8")
    print(content)
except Exception as e:
    print("Error:", e)