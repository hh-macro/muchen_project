import json

mapping = {
    "cpws_al_case_sort_name": "allx",  # 案例类型
    "filename": "pcmc",  # 文件名
    "cpws_al_no": "code",  # 入库编号
    "cpws_al_sort_name": "ay",  # 案由/罪名
    "cpws_al_slfy_name": "slfy",  # 审理法院
    "cpws_al_zs_date": "cprq",  # 裁判日期
    "cpws_al_ajzh": "ah",  # 案号
    "cpws_al_slcx_name": "slcx",  # 审理程序
    "cpws_al_rk_time": "fbsj",  # 入库时间
    "cpws_al_ts_name": "wslx",  # 文书类型
    "biaodi": "bd",
    "biaodiwu": "bdw",
    "shulifei": "slf",
    "title": "almc",  # 标题
    "cpws_al_keyword": "keyword",  # 关键字
    "cpws_al_jbaq": "slcm",  # 基本案情
    "cpws_al_cply": "byrw",  # 裁判结果/裁判理由
    "cpws_al_cpyz": "cpyd",  # 裁判要旨
    "cpws_al_glsy": "cpws_al_glsy",  # 关联索引
    "laiyuan": "fbjg",
    "cpws_url": "orglist/url",
}


def replace_keys(data, mapping):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = mapping.get(key, key)
            if isinstance(new_key, dict):
                new_dict.update(replace_keys(value, new_key))
            else:
                new_dict[new_key] = replace_keys(value, mapping)
        return new_dict
    elif isinstance(data, list):
        return [replace_keys(item, mapping) for item in data]
    else:
        return data


with open('人民法院案例库/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


transformed_data = [replace_keys(item, mapping) for item in data]
# print(transformed_data)

with open('人民法院案例库/new_data.json', 'w', encoding='utf-8') as new_file:
    json.dump(transformed_data, new_file, ensure_ascii=False, indent=4)

print("数据已转换成功！")
