import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import json
import re
from PIL import Image
from io import BytesIO
from loguru import logger
import pymongo
import time
import random

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://max.book118.com/",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}


def check_title(title):
    """
    根据标题判断是否属于大学理科试卷
    eg: 离散数学B卷及答案
    线性代数专升本答案
    线性代数与概率统计和答案
    :param title:
    :return: 1 大学理科试卷, 0 非大学理科试卷, -1 不确定
    """
    stage_keywords = ["大学", "学院", "专升本", "考研"]
    subject_keywords = ["数学", "物理", "化学", "生物", "地理", "信息技术", "计算机", "电子", "通信", "机械", "材料",
                        "化工", "科学", "生化"]
    major_keywords = ["高等数学", "高数", "线性代数", "离散数学", "复变函数", "数学建模", "概率论与数理统计",
                      "高等代数",
                      "分子生物", "应用物理", "电力工程", "电机", "建筑施工", "钻井工程", "结构力学", "力学", "统计学",
                      "方程", "数理"
                              "计算机科学与技术", "软件工程", "信息技术", "操作系统", "数据结构", "计算机组成原理",
                      "云计算技术", "C语言",
                      "计算机基础"]
    type_keywords = ["卷", "试卷", "试题", "测试题", "真题", "课后题", "练习题", "习题", "复习题", "例题", "题集",
                     "题库", "解析", "答案", "作业题", "期末复习"]
    keywords = stage_keywords + subject_keywords + major_keywords + type_keywords
    stage_pattern = '|'.join(stage_keywords)
    subject_pattern = '|'.join(subject_keywords)
    major_pattern = '|'.join(major_keywords)
    type_pattern = '|'.join(type_keywords)
    match = re.search(fr'({stage_pattern}).*?({subject_pattern}).*?({type_pattern})', title)
    if match:
        return 1
    # 直属大学的专业, 可无需阶段关键匹配
    match = re.search(fr'({major_pattern}).*?({type_pattern})', title)
    if match:
        return 1
    exclusion_stage_keywords = ["小学", "小升初", "中学", "初中", "高中", "中考", "高考"]
    exclusion_subject_keywords = ["语文", "英语", "政治", "文史", "哲学", "法学", "经济", "管理", "艺术", "文学",
                                  "外语",
                                  "历史", "中国近现代史纲要", "语言", "考古", "教育", "广播", "播音", "主持", "马克思",
                                  "影视", "美术", "新闻",
                                  "戏曲", "教学设计", "动画", "心理学", "形势与政策", "思想道德与法治", "电子商务"]
    exclusion_type_keywords = ["课件", "教案", "报告", "论文", "说明书", "教学大纲", "合同", "协议书", "范本", "讲义",
                               "简介"]
    exclusion_keywords = exclusion_stage_keywords + exclusion_subject_keywords + exclusion_type_keywords
    # 排除相关关键词
    if any(keyword in title for keyword in exclusion_keywords):
        return 0
    # 指定
    if all(keyword in title for keyword in keywords):
        return 1
    # 不确定
    return -1


# 这里是获取参数的
def get_token(url):
    # 正常请求
    # url = "https://max.book118.com/html/2017/0329/97842486.shtm"
    params = {
        "from": "search",
        "index": "1"
    }
    response = requests.get(url, headers=headers, params=params)
    view_token = re.search(r"view_token: '(.*?)' //预览的token", response.text).group(1)
    aid = re.search(r"aid: (.*?), //解密后的id", response.text).group(1)
    t = re.search(r"senddate: '(.*?)',", response.text).group(1)
    max_page = re.search(r'preview_page: (.*?),', response.text).group(1)
    return view_token, t, aid, max_page


# 延申
def yans(aid, t):
    ys_list = []
    url = "https://api.book118.com//ycl/Recommend/getData"
    params = {
        "aid": aid,
        "t": t,
    }
    # print(params)
    datas = requests.get(url, headers=headers, params=params).json()['a_data']
    # print(datas.text)
    for data in datas:
        title = str(data['title']).split('.')[0]
        # 这里是筛选，如果为1就进行操作
        if check_title(title) == 1:
            # print(a_data)
            url = "https://max.book118.com" + data['url']
            if info_col.count_documents({'url': url}) == 0:
                ys_list.append(1)
                yans_mycol.insert_one({
                    "title": title,
                    "aid": url.split('/')[-1].split('.')[0],
                    "url": url
                })
            else:
                logger.warning('已存在，跳过')
    return len(ys_list)


def get_img(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def img_to_Pdf(image_urls, aid, title):
    # 下载图片并保存到列表中
    images = [None] * len(image_urls)  # 创建一个列表，预先分配空间
    with ThreadPoolExecutor(max_workers=len(image_urls)) as executor:
        # 提交任务并保存Future对象
        future_to_url = {executor.submit(get_img, url): url for url in image_urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                # 获取任务结果
                img = future.result()
                # 找到图片在原始列表中的位置并保存
                for i, u in enumerate(image_urls):
                    if u == url:
                        images[i] = img
                        break
            except Exception as exc:
                logger.error(f'{url} generated an exception: {exc}')
    # 将图片合并成PDF
    if all(img is not None for img in images):  # 确保所有图片都已下载
        os.makedirs(target_dir, exist_ok=True)
        filepath = os.path.join(target_dir, f'{aid}-{title}.pdf')
        images[0].save(filepath, save_all=True, append_images=images[1:])


def get_images(page, aid, view_token):
    img_list = []
    url = "https://openapi.book118.com/getPreview.html"
    params = {
        '': '',
        'project_id': '1',
        'aid': aid,
        'view_token': view_token,
        'page': page,
        'filetype': 'doc',
    }

    response = requests.get(url, headers=headers, params=params)
    # print(response.text)
    datas = json.loads(response.text.replace('jsonpReturn(', '').replace(');', ''))['a_data']
    # print(datas)

    for data in dict(datas).items():
        if data[1] == '':
            time.sleep(random.randint(1, 3))
            return get_images(page=page, aid=aid, view_token=view_token)
        else:
            img_list.append({data[0]: 'https:' + data[1]})
    return img_list


# 这里开始正式采集
def main(url, title):
    """
    先接收url然后调用，调用完再删除
    :return: 不返回了
    """
    # 解析出aid
    aid = url.split('/')[-1].split('.')[0]

    view_token, t, aid_for_img, max_page = get_token(url)
    logger.debug(f"已衍生出:{yans(aid=aid, t=t)}个")

    logger.debug(f"开始采集{title}！")

    logger.debug(f"开始采集{title}的图片！共{max_page}张")

    res_List = []
    with ThreadPoolExecutor(max_workers=int(max_page) // 6) as fp:
        for page in range(1, int(max_page) + 1, 6):
            res = fp.submit(get_images, aid=aid_for_img, page=page, view_token=view_token)
            res_List += res.result()
    sorted_values = [list(d.values())[0] for d in sorted(res_List, key=lambda x: int(next(iter(x))))]

    logger.debug(f"开始转换{title}的图片！")
    img_to_Pdf(sorted_values, title=title, aid=aid_for_img)
    ti_dic = {
        "platform": '原创力文档(max.book118.com)',
        "title": title,  # 文件
        "原文链接": url,
        "有无答案": "有",
        "初始PDF": "图片转pdf",
        "aid": aid
    }
    info_col.insert_one(ti_dic)
    logger.success(str(ti_dic) + "采集完毕！")


def get_main(url, title):
    # 检测一下，如果这个url没出现过就采集
    if info_col.count_documents({'url': url}) == 0:
        main(url=url, title=title)
        # 采集完了就删掉
    else:
        logger.warning(url + "这个采集过了，跳过！")
    yans_mycol.delete_many({'url': url})
    logger.debug(str({'url': url}) + "已经删除！")


if __name__ == '__main__':
    myclient = pymongo.MongoClient(
        'mongodb://root:MuChen111@dds-2vc0414763e7d5241873-pub.mongodb.cn-chengdu.rds.aliyuncs.com:3717,dds-2vc0414763e7d5242801-pub.mongodb.cn-chengdu.rds.aliyuncs.com:3717/admin?replicaSet=mgset-1150459045')
    mydb = myclient["book118db"]
    yans_mycol = mydb["yans_data"]
    info_col = mydb['to_info_col']
    target_dir = r'D:\原创文库'
    main('https://max.book118.com/html/2017/1124/141290409.shtm', '离散数学题库大全及答案')
    while True:
        with ThreadPoolExecutor(10) as f:
            distinct_value = yans_mycol.distinct('url')
            titles = yans_mycol.distinct('title')
            for url, title in zip(distinct_value, titles):
                future = f.submit(get_main, url=url, title=title)
                future.add_done_callback(lambda x: print(x.result()))
