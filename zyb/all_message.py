import pandas as pd
from pymongo import MongoClient

client = MongoClient(
    'mongodb://root:Aliyun_Mongo_20250218@dds-2vc3c96a7e797ee41197-pub.mongodb.cn-chengdu.rds.aliyuncs.com:3717,dds-2vc3c96a7e797ee42971-pub.mongodb.cn-chengdu.rds.aliyuncs.com:3717/admin?replicaSet=mgset-1150525521')
db = client['作业帮5']
collection = db['log']

target_dates = ["03-12", "03-13", "03-14"]
device_id_list = [
    '015-506826168', '016-625908340', '017-934365485', '004-724254809',
    '019-302008258', '93-256658041', '020-416118280', '95-530461709'
]

def get_device_data(device_id):
    pipeline = [
        {"$addFields": {"date_part": {"$substr": ["$time", 5, 5]}}},
        {"$match": {"date_part": {"$in": target_dates},
                    "s_video_num": {"$exists": True},
                    "device_id": device_id}},
        {"$group": {"_id": {"phone": "$phone", "date": "$date_part"},
                    "total": {"$sum": 1},
                    "valid": {"$sum": {"$cond": [{"$gt": ["$s_video_num", 0]}, 1, 0]}}}},
        {"$project": {"_id": 0,
                      "账号": "$_id.phone",
                      "日期": "$_id.date",
                      "有效率": {"$concat": [{"$toString": "$valid"}, "/", {"$toString": "$total"}]}}},
        {"$sort": {"账号": 1, "日期": 1}}
    ]
    return list(collection.aggregate(pipeline))

all_data = []
for device_id in device_id_list:
    print(f"Processing device_id: {device_id}")
    results = get_device_data(device_id)
    data = pd.DataFrame(results)
    data['设备号'] = device_id
    all_data.append(data)

df = pd.concat(all_data, ignore_index=True)

# 创建透视表
pivot_table = pd.pivot_table(df, values='有效率', index=['设备号', '账号'],
                            columns='日期', aggfunc=lambda x: x)
pivot_table.reset_index(inplace=True)
pivot_table.columns.name = None

# 计算汇总数据
summary_data = {'设备号': '总计', '账号': '总计'}
for date in target_dates:
    total_valid = 0
    total_count = 0
    if date in pivot_table.columns:
        for value in pivot_table[date]:
            if pd.isna(value):
                continue
            try:
                valid, total = map(int, value.split('/'))
                total_valid += valid
                total_count += total
            except:
                pass
    summary_data[date] = f"{total_valid}/{total_count}"

# 创建带汇总的DataFrame
empty_rows = pd.DataFrame([{col: '' for col in pivot_table.columns} for _ in range(2)])
summary_df = pd.DataFrame([summary_data])
final_df = pd.concat([pivot_table, empty_rows, summary_df], ignore_index=True)

# 调整列顺序（保持原始顺序）
final_df = final_df[['设备号', '账号'] + target_dates]

final_df.to_excel('all_devices_message.xlsx', index=False)
print("处理完成，结果已保存到 all_devices_message.xlsx")