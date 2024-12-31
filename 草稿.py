original_dict = {
    "cpws_al_case_sort_name": "刑事",
    "filename": "何某林非法吸收公众存款案",
    "cpws_al_no": "2024-04-1-113-004",
    "cpws_al_sort_name": "非法吸收公众存款罪",
    "cpws_al_slfy_name": "四川省巴中市中级人民法院",
    "cpws_al_zs_date": "2019.06.04",
    "cpws_al_ajzh": "（2019）川19刑终73号",
    "cpws_al_slcx_name": "二审",
    "cpws_al_rk_time": "2024-12-30 11:29:37",
    "cpws_al_ts_name": "（刑三庭）",
    "biaodi": "",
    "biaodiwu": "",
    "shulifei": "",
    "file_content": {
        "title": "何某林非法吸收公众存款案",
        "cpws_al_keyword": [
            "刑事",
            "非法吸收公众存款罪",
            "不特定人员",
            "雇佣关系",
            "情节显著轻微"
        ],
        "cpws_al_jbaq": "...",
        "cpws_al_cply": "...",
        "cpws_al_cpyz": "...",
        "cpws_al_glsy": "...",
    },
    "laiyuan": "人民法院案例库",
    "cpws_url": "https://rmfyalk.court.gov.cn/view/content.html?id=...",
}

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


# Replace keys in original_dict based on data_j2
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


# Apply the transformation
transformed_dict = replace_keys(original_dict, mapping)
print(transformed_dict)
