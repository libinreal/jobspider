# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging

class JobPipeline(object):
    def __init__(self):
        mongoClient = MongoClient(
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']
        )
        db = mongoClient[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.ids = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids:  
            raise DropItem("Duplicate item found: (id)%s" % item['id'])
        else:
            self.collection.insert(dict(item))
            logging.log("Lagou Job added to MongoDB", level=log.DEBUG, spider=spider)
        return item