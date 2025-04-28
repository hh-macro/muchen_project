from minio import Minio
import io

client = Minio(
    "47.99.52.9:9000",
    access_key="admin",
    secret_key="Aa123456.",
    secure=False
)

# 文件夹列表
# file_list = ['exceptions', 'processor', 'protocol', 'static', 'test', 'tools', 'utils']
file_list = ['app', 'data', 'test', 'web', 'app/process', 'app/search', 'app/static','app/utils']

# 根路径
root_path = "dxstj-SQ-main/dxstj-SQ-main"

# 创建每个文件夹
for folder in file_list:
    # 构造完整的路径
    full_path = f"{root_path}/{folder}/"
    # 上传一个空对象来模拟文件夹
    client.put_object("stj", full_path, io.BytesIO(b""), 0)

# file_list = ['exceptions', 'processor', 'protocol', 'static', 'test', 'tools', 'utils']


# client.put_object("test", "text/text/", io.BytesIO(b""), 0)
