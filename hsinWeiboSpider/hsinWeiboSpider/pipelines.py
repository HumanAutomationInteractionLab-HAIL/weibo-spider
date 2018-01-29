# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.contrib.exporter import CsvItemExporter
import pymongo
from scrapy.conf import settings


class HsinweibospiderPipeline(object):
    def process_item(self, item, spider):
        return item


class CsvPipeline(object):
    def __init__(self):
        self.file = open("./collected.csv", 'wb+')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class JsonPipeline(object):
    def __init__(self):
        self.file = open("./collected.json", 'wb')
        self.exporter = JsonItemExporter(
            self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        #return item


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings.get('MONGODB_SERVER'), settings.get('MONGODB_PORT'))
        db = connection[settings.get('MONGODB_DB')]
        self.collection = db[settings.get('MONGODB_COLLECTION')]

    def process_item(self, item, spider):
        if "NickName" in item:
            print("item profile", item)
            profileItem = dict(item)
            self.collection.insert(profileItem)  # 向数据库插入一条记录
        else:
            for j in range(10):
                try:
                    jStr = str(j)
                    newItem = {
                        "Attitudes_Count": item["Attitudes_Count"][jStr],
                        "Comments_Count": item["Comments_Count"][jStr],
                        "Content": item["Content"][jStr],
                        "Created_At": item["Created_At"][jStr],
                        "Source": item["Source"][jStr],
                        "User": item["User"][jStr],
                        "Weibo_Id": item["Weibo_Id"][jStr],
                    }
                    postItem = dict(newItem)  # 把item转化成字典形式

                    self.collection.insert(postItem)  # 向数据库插入一条记录
                except:
                    print("error occurs in Item")
        #return 0  # 会在控制台输出原item数据，可以选择不写