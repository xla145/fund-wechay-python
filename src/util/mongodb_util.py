# -*- coding: UTF-8 -*-
# mongoDb的工具类

from pymongo import MongoClient


class MongoDbUtil(object):

    def __init__(self) -> None:
        super().__init__()
        host = "localhost"
        port = 27017
        self.client = MongoClient('mongodb://%s:%d/' % (host, port))

    # 获取db
    def get_db(self, database='xula_tool'):
        return self.client[database]






