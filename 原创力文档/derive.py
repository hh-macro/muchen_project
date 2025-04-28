# _*_ coding : UTF-8 _*_
# @Time : 2024/10/28 上午9:26
# @Auther : Tiam
# @File : derive
# @Project : question-crawler
# @Desc : 衍生文档
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

import execjs
import pika
import requests
from bs4 import BeautifulSoup
from loguru import logger
from pymongo import MongoClient
from tenacity import retry, stop_after_attempt, wait_random, TryAgain, stop_after_delay, retry_if_exception_type, retry_if_not_exception_type
import yaml

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
                      "{process.name} | "  # 进程名
                      "{thread.name} | "  # 进程名
                      "<level>{module}</level>.<cyan>{function}</cyan>"  # 模块名.方法名
                      ":<cyan>{line}</cyan> | "  # 行号
                      "<level>{level.icon}{level}</level>: "  # 等级 图标
                      "<level>{message}</level>",  # 日志内容
            "level": 'INFO'
        },
        {
            "sink": "renrendoc_derive.log",  # 日志文件名
            "level": "DEBUG",  # 日志等级
            "rotation": "100 MB",  # 按周滚动
            "retention": "10 days",  # 保留10天
            "enqueue": True,  # 异步写入
            "compression": "zip",  # 压缩格式
            # "serialize": True  # 序列化日志为json格式
        },
    ],
    "extra": {"user": "Tiam"}
}
logger.configure(**config)

cookies = {
    'aa1ecd2d8bf97b72dedb625f320a70bf': 'eyIyMzUwNDI1OTIiOjF9',
    '585ca0f783c538407119f6ece093cd59': '83c538407119f6ec',
    '18389a4a9ad5795744699cff0ba66c15': '11',
    'PHPSESSID': 'a111c5ee6a8b1e1ef14f199166b63d21',
    '6c6de0691ee16338_SearchKeywordCompletion': '1730078144%2C55',
    '6c6de0691ee16338_SearchApiSearchV2': '1730078166%2C60',
    '6c6de0691ee16338_Ajax_getSimilarDocNew': '1730078916%2C1',
    '2da3a13895524d90e149523f875a5eef': '%7Cbd6b8fb-11%7C76243f5-9%7Cae579c9-10%7C',
    '3f453a8f42dc022b10fb40eb6ef27e71': '182811081,123880437,198621435',
    '8aadb593368924b34945502a93eddb5b': 'eyIxOTg2MjE0MzUiOjEsIjEyMzg4MDQzNyI6MSwiMTgyODExMDgxIjoxfQ%3D%3D',
    'PREVIEWHISTORYPAGES': '182811081_1,123880437_1,198621435_4',
    'cfeaf09c40ea17a847ac11252ae43b23': '%7B%22123880437%22%3A%22KYKIQ5o1LSSO%405itAlv%40aFQ%22%7D',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'aa1ecd2d8bf97b72dedb625f320a70bf=eyIyMzUwNDI1OTIiOjF9; 585ca0f783c538407119f6ece093cd59=83c538407119f6ec; 18389a4a9ad5795744699cff0ba66c15=11; PHPSESSID=a111c5ee6a8b1e1ef14f199166b63d21; 6c6de0691ee16338_SearchKeywordCompletion=1730078144%2C55; 6c6de0691ee16338_SearchApiSearchV2=1730078166%2C60; 6c6de0691ee16338_Ajax_getSimilarDocNew=1730078916%2C1; 2da3a13895524d90e149523f875a5eef=%7Cbd6b8fb-11%7C76243f5-9%7Cae579c9-10%7C; 3f453a8f42dc022b10fb40eb6ef27e71=182811081,123880437,198621435; 8aadb593368924b34945502a93eddb5b=eyIxOTg2MjE0MzUiOjEsIjEyMzg4MDQzNyI6MSwiMTgyODExMDgxIjoxfQ%3D%3D; PREVIEWHISTORYPAGES=182811081_1,123880437_1,198621435_4; cfeaf09c40ea17a847ac11252ae43b23=%7B%22123880437%22%3A%22KYKIQ5o1LSSO%405itAlv%40aFQ%22%7D',
    'Pragma': 'no-cache',
    'Referer': 'https://www.renrendoc.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


# with open('大学理科相关专业.yml', 'r', encoding='utf-8') as file:
#     # 使用yaml.load()函数来加载YAML文件内容
#     # 使用yaml.safe_load()函数来避免执行YAML文件中的任意代码
#     yml = yaml.safe_load(file)
#     major_list = yml.get('major')


@retry(stop=(stop_after_attempt(3) | stop_after_delay(15)),
       wait=wait_random(1, 3),
       reraise=True
       )
def request_recommend_docs(doc_id, agg_id) -> list[dict]:
    logger.debug(f'请求推荐文档: {doc_id}, agg_id: {agg_id}')
    response = requests.get(
        f'https://www.renrendoc.com/renrendoc_v1/Ajax/getRecommend/id/{doc_id}/aggId/{agg_id}.html',
        cookies=cookies,
        headers=headers,
    )
    response.raise_for_status()
    json_data = response.json()
    if json_data['code'] != 200:
        raise requests.RequestException(f"get recommend fail with {json_data['code']} code and msg: {json_data.get('msg')}.")
    recommend_docs_html = json_data['a_data']['recommend']
    soup = BeautifulSoup(recommend_docs_html, 'html.parser')
    recommend_docs = []
    for a_tag in soup.find_all("a"):
        # /paper/202099476.html
        if match := re.search(r'/paper/(\w+).html', a_tag.get('href')):
            doc_id = match.group(1)
            title = a_tag.get('title')
            recommend_docs.append({
                'doc_id': doc_id,
                'title': title,
            })
    return recommend_docs


@retry(stop=(stop_after_attempt(3) | stop_after_delay(15)),
       wait=wait_random(1, 3),
       reraise=True
       )
def request_similar_docs(agg_id) -> list[dict]:
    logger.debug(f'请求相似文档: {agg_id}')
    response = requests.get(
        f'https://www.renrendoc.com/renrendoc_v1/ajax/getSimilarDocNew/id/{agg_id}',
        cookies=cookies,
        headers=headers,
    )
    response.raise_for_status()
    json_data = response.json()
    docs = list(map(lambda x: {'doc_id': x['id'], 'title': x['title']}, json_data['a_data']))
    # 第一个文档是自己, 去掉
    return docs[1:]


@retry(stop=(stop_after_attempt(3) | stop_after_delay(15)),
       wait=wait_random(1, 3),
       reraise=True
       )
def request_detail(doc_id):
    response = requests.get(
        f'https://www.renrendoc.com/renrendoc_v1/Detail/data/id/{doc_id}.html',
        cookies=cookies,
        headers=headers,
    )
    response.raise_for_status()
    # var view_params =
    view_params = re.search(r'var\s+view_params\s*=\s*(.*?);', response.text, re.DOTALL)
    if not view_params:
        logger.error(f'view_params not found in response: {response.text}')
        return
    view_params = execjs.eval(view_params.group(1))
    # title, bookId, bookInfo.totalPage
    # 少于5页的文档没有 previewParams
    preview_params = re.search(r'var\s+previewParams\s*=\s*(.*?);', response.text, re.DOTALL)
    if preview_params:
        preview_params = execjs.eval(preview_params.group(1))
    # realFreePage(真实可免费预览页数), total_c(实际文档页数), encrypt(加载预览所需参数)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = []
    for img_tag in soup.select('#page img'):
        cls = img_tag.get('class')
        if 'nolazy' in cls:
            url = f'http:{img_tag.get("src")}'
        elif 'lazy' in cls:
            url = f'http:{img_tag.get("a_data-src")}'
        else:
            logger.warning(f'unknown img tag class: {cls}')
            continue
        # page = img_tag.get('a_data-page')
        image_urls.append(url)
    # detail-article
    detail_article = soup.select_one('.detail-article')
    if detail_article:
        detail_article = detail_article.text.strip()
    return {
        'doc_id': doc_id,
        'title': view_params['title'],
        'book_id': view_params['bookId'],
        'bookInfo': view_params['bookInfo'],
        'image_urls': image_urls,
        'detail_article': detail_article,
        'real_free_page': preview_params['realFreePage'] if preview_params else None,
        'total_page': preview_params['total_c'] if preview_params else None,
        'encrypt': preview_params['encrypt'] if preview_params else None,
    }


@retry(stop=(stop_after_attempt(3) | stop_after_delay(15)),
       wait=wait_random(1, 3),
       reraise=True
       )
def request_doc(doc_id):
    logger.debug(f'请求文档详情: {doc_id}')
    response = requests.get(f'https://www.renrendoc.com/paper/{doc_id}.html', cookies=cookies, headers=headers)
    # 404 Client Error: Not Found for url: https://www.renrendoc.com/paper/327904847.html
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # 1. 获取预览图片地址
    preview_image_urls = []
    for index, img_tag in enumerate(soup.select('#page img')):
        # 非第一页懒加载, 地址在data-src中
        url = f'http:{img_tag.get("a_data-src")}'
        if index == 0:
            url = f'http:{img_tag.get("src")}'
        preview_image_urls.append(url)
    # 2. 获取 agg_id 和 encrypt(可选) !!! 这两个参数只有这个接口返回
    preview_params = re.search(r'var\s+previewParams\s*=\s*(.*?);', response.text, re.DOTALL)
    if preview_params:
        preview_params = execjs.eval(preview_params.group(1))
    detail_params = re.search(r'var\s+detail_params\s*=\s*(.*?);', response.text, re.DOTALL)
    if not detail_params:
        logger.error(f'detail_params not found in response: {response.text}')
        return
    detail_params = execjs.eval(detail_params.group(1))
    agg_id = detail_params['aggID']
    # 3. 文档相关信息  title, bookId, bookInfo.totalPage
    # bug: 标题中可能存在 ; eg: doc_id: 214652518
    view_params = re.search(r'var\s+view_params\s*=\s*(.*?);\n', response.text, re.DOTALL)
    if not view_params:
        logger.error(f'view_params not found in response: {response.text}')
        return
    view_params = execjs.eval(view_params.group(1))
    # 4. 文档简介
    detail_article = soup.select_one('.detail-article')
    if detail_article:
        detail_article = detail_article.text.strip()
    return {
        'doc_id': doc_id,
        'preview_image_urls': preview_image_urls,
        'agg_id': agg_id,  # 用于获取推荐文档和相似文档
        'title': view_params['title'],
        'book_id': view_params['bookId'],
        'bookInfo': view_params['bookInfo'],
        'detail_article': detail_article,  # 文档简介
        'real_free_page': preview_params['realFreePage'] if preview_params else None,
        'total_page': preview_params['total_c'] if preview_params else None,
        # 翻页请求预览图片的参数
        'encrypt': preview_params['encrypt'] if preview_params else None,
    }
    # 相关文档, 使用 agg_id 参数调用 getRecommend 接口获取的才是真相关的文档, 这里html的文档并不相干


def derive_docs(doc_id):
    """
    无限衍生文档
    :param doc_id:
    :return:
    """
    # 1. 获取文档详情
    doc_detail = request_doc(doc_id)
    agg_id = doc_detail['agg_id']
    # 2. 获取相似文档
    similar_docs = request_similar_docs(agg_id)
    # 3. 使用相似文档获取推荐文档, 不能使用当前文档ID, 否则是不相干的
    total_recommend_docs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for doc in similar_docs:
            time.sleep(.1)
            executor.submit(request_recommend_docs, doc['doc_id'], agg_id).add_done_callback(lambda x: total_recommend_docs.extend(x.result()))
    # for doc in similar_docs:
    #     recommend_docs = request_recommend_docs(doc['doc_id'], agg_id)
    #     total_recommend_docs.extend(recommend_docs)
    # 根据doc_id去重,
    recommend_docs = list({doc['doc_id']: doc for doc in total_recommend_docs}.values())

    return {
        'doc_detail': doc_detail,
        'recommend_docs': recommend_docs,
        'similar_docs': similar_docs,
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
    subject_keywords = ["数学", "物理", "化学", "生物", "地理", "信息技术", "计算机", "电子", "通信", "机械", "材料", "化工", "科学", "生化"]
    major_keywords = ["高等数学", "高数", "线性代数", "离散数学", "复变函数", "数学建模", "概率论与数理统计", "高等代数",
                      "分子生物", "应用物理", "电力工程", "电机", "建筑施工", "钻井工程", "结构力学", "力学",
                      "计算机科学与技术", "软件工程", "信息技术", "操作系统", "数据结构", "计算机组成原理", "云计算技术", "C语言", "计算机基础"]
    type_keywords = ["卷", "试卷", "试题", "测试题", "真题", "课后题", "练习题", "习题", "复习题", "例题", "题集", "题库", "解析", "答案", "作业题", "期末复习"]
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
    exclusion_subject_keywords = ["语文", "英语", "政治", "文史", "哲学", "法学", "经济", "管理", "艺术", "文学", "外语",
                                  "历史", "中国近现代史纲要", "语言", "考古", "教育", "广播", "播音", "主持", "马克思", "影视", "美术", "新闻",
                                  "戏曲", "教学设计", "动画", "心理学", "形势与政策", "思想道德与法治", "电子商务"]
    exclusion_type_keywords = ["课件", "教案", "报告", "论文", "说明书", "教学大纲", "合同", "协议书", "范本", "讲义", "简介"]
    exclusion_keywords = exclusion_stage_keywords + exclusion_subject_keywords + exclusion_type_keywords
    # 排除相关关键词
    if any(keyword in title for keyword in exclusion_keywords):
        return 0
    # 指定
    if all(keyword in title for keyword in keywords):
        return 1
    # 不确定
    return -1


def main():
    # mongodb
    client = MongoClient('localhost', 27017)
    # client = MongoClient("mongodb://root:muchenai%402024@dds-2vc035b3cea37e441509-pub.mongodb.cn-chengdu.rds.aliyuncs.com:3717,dds-2vc035b3cea37e442755-pub.mongodb.cn-chengdu.rds.aliyuncs.com:3717/admin?replicaSet=mgset-1150458882")
    db = client['renrendoc']
    # 保存衍生过的文档
    collection_derive = db['doc_derive']
    # 待衍生文档
    collection_stack = db['doc_stack']
    # rabbitmq
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    queue_name = '245332265'
    channel.queue_declare(queue=queue_name, durable=True)  # 声明一个队列, durable=True表示队列持久化
    # root: https://www.renrendoc.com/paper/123880437.html
    # https://www.renrendoc.com/p-9821438.html
    # https://www.renrendoc.com/paper/165721028.html
    doc = {
        'doc_id': queue_name,
        'title': '大学离散数学试题集(非常完整试题)2468',
    }
    # doc = {
    #     'doc_id': '220979977',
    #     'title': '(完整版)大学物理试题库(后附详细答案)',
    # }
    # doc = {
    #     'doc_id': '300312654',
    #     'title': '中南大学2020-2021学年第1学期生物技术《现代分子生物学》考试试卷(附答案)',
    # }
    # doc = {
    #     'doc_id': '157647778',
    #     'title': '大学计算机组成原理期末考试试卷附答案',
    # }
    # channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(doc))
    while True:
        try:
            # 出队
            method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
            if not body:
                logger.success("no more doc_id to derive, it's over! ")
                break
            doc = json.loads(body)
            doc_id = doc['doc_id']
            if collection_derive.find_one({'doc_id': doc_id}):
                logger.debug(f'文档已衍生过, doc_id: {doc_id}')
                continue
            # 检查标题
            if check_title(doc['title']) != 1:
                logger.warning(f'文档不符合需求 title: {doc["title"]} :https://www.renrendoc.com/paper/{doc_id}.html')
                continue
            queue_state = channel.queue_declare(queue=queue_name, passive=True)
            logger.info(f'开始衍生 {doc["title"]}: https://www.renrendoc.com/paper/{doc_id}.html, 剩余待处理: {queue_state.method.message_count}')
            # executor.submit(derive_docs, doc_id).add_done_callback(callback)
            doc_derive = derive_docs(doc_id)
            # detail 入库
            collection_derive.insert_one(doc_derive['doc_detail'])
            all_derive_docs = doc_derive['recommend_docs'] + doc_derive['similar_docs']
            # all_derive_docs = doc_derive['similar_docs']
            # 发布消息
            for doc in all_derive_docs:
                json_doc = json.dumps(doc)
                collection_stack.replace_one({'doc_id': doc['doc_id']}, doc, upsert=True)
                channel.basic_publish(exchange='', routing_key=queue_name, body=json_doc, properties=pika.BasicProperties(
                    delivery_mode=2,  # 消息持久化, 避免重启服务丢失消息
                ))
            logger.success(f"衍生文档完成 doc_id: {doc_id}, title: {doc_derive['doc_detail']['title']}, 衍生文档数量: {len(all_derive_docs)}")
        except KeyboardInterrupt:
            logger.warning('程序被强行终止! KeyboardInterrupt')
            break
    # 释放资源
    client.close()
    connection.close()


if __name__ == '__main__':
    main()
