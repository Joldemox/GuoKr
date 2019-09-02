# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class GuokrspiderPipeline(object):
    # 其中的spider参数是为了保证是对应爬取数据的爬虫一致，也就是爬取的数据不被混乱
    def process_item(self, item, spider):
        # 此时的item为一个对象，所以需要转换为字典或者以字典为基础的列表
        self.collections.insert(dict(item))
        return item

    def open_spider(self, spider):
        self.client = MongoClient()
        self.collections = self.client['guokr']['gk2']

    def close_spider(self, spider):
        self.client.close()
