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
    def __init__(self, mongo_host, mongo_port, mongo_db):
        mongoClient = MongoClient(
            mongo_host,
            mongo_port
        )

        db = mongoClient[mongo_db]
        self.collection = db['jobs']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=settings.get('MONGODB_HOST'),
            mongo_port=settings.get('MONGODB_PORT'),
            mongo_db=settings.get('MONGODB_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['jobid'] in self.ids:  
            raise DropItem("Duplicate item found: (id)%s" % item['id'])
        
        for 
            self.collection.update(dict(item))
            logging.log("Lagou Job added to MongoDB", level=log.DEBUG, spider=spider)
        return item