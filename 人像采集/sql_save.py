import pymysql

# 1. 创建链接对象
connection = pymysql.connect(
    host='127.0.0.1',  # 数据库服务器的地址
    user='root',  # 用户名
    password='654321',  # 用户密码
    database='image',  # 操作的数据库名
    port=3306,  # 端口
    charset='utf8'  # 字符编码
)
cursor = connection.cursor()

sql = "insert into image_data(time_name, url_name) VALUE ('%s', '%s');"
datas = [('173512186463096', 'https://gaoimg.com/?dl=/2024/08/3c739ba50add0a41-1.jpg'),
         ('173512186463096', 'https://gaoimg.com/?dl=/2024/08/3c739ba50add0a41-1.jpg')]
for data in datas:
    execute_sql = sql % data
    cursor.execute(execute_sql)  # 执行插入操作

connection.connect()  # 提交保存
connection.close()
