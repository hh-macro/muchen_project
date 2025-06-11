# -- coding: utf-8 --
# @Author: 胡H
# @File: mgPaginator.py
# @Created: 2025/6/6 10:55
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc: mongo 分页查询接口 -> MongoPaginator
from pymongo import MongoClient


class MongoPaginator:
    def __init__(self, db):
        self.db = db

    def paginate(self, collection_name: str, page: int = 1, page_size: int = 10, filter_query: dict = None,
                 sort_by: list = None, projection: dict = None):
        """ 分页查询指定集合
        :param collection_name: 集合名  -> 要查询的 MongoDB 集合名称
        :param page: 当前页码，从1开始   -> 当前请求的页码 | 默认1页
        :param page_size: 每页条数  ->   页显示的数据条数 | 默认10条
        :param filter_query: 查询条件（dict）  ->   查询条件 | 默认为 None
        :param sort_by: 排序条件，如 [("created_at", -1)]  ->  排序条件，按照 created_at 字段倒序（-1 为降序，1 为升序）| 默认为None不排序
        :param projection: 字段投影（如 {"_id": 0, "name": 1}）
        :return: dict 包含数据和分页信息  ->
        """
        if filter_query is None:
            filter_query = {}
        if sort_by is None:
            sort_by = []

        collection = self.db[collection_name]

        skip_count = (page - 1) * page_size
        total = collection.count_documents(filter_query)
        cursor = collection.find(filter_query, projection)
        if sort_by:
            cursor = cursor.sort(sort_by)
        cursor = cursor.skip(skip_count).limit(page_size)
        results = list(cursor)

        return {
            "page": page,  # 当前页码
            "page_size": page_size,  # 每页条数
            "total": total,  # 总共有多少条符合条件的数据
            "total_pages": (total + page_size - 1) // page_size,  # 总共有多少页
            "data": results  # 当前页的数据列表
        }


if __name__ == "__main__":
    client = MongoClient(
        "mongodb://localhost:27017")
    db = client['renrendoc']

    paginator = MongoPaginator(db)

    page = 1
    page_size = 5
    while True:
        message_result = paginator.paginate(
            collection_name="doc_stack1",
            page=page,
            page_size=page_size,
            # filter_query={"status": "active"},
            # sort_by=[("created_at", -1)]
            # projection={"_id": 0, "doc_id": 1, "title": 1}  # 只返回 name 和 created_at 字段，不返回 _id
        )
        data_results = message_result["data"]
        if page >= message_result["total_pages"]:  #
            break
        print(data_results)
        page += 1
