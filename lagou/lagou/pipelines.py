# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from items import JobItem

import json
import logging

class JobPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host = crawler.settings.get('MONGODB_HOST'),
            mongo_port = crawler.settings.get('MONGODB_PORT'),
            mongo_db = crawler.settings.get('MONGODB_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(
            self.mongo_host,
            self.mongo_port
        )

        db = self.client[self.mongo_db]
        self.collection = db['jobs']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            # print 'pipline module , process_item, jobid %s' % item['jobid']

            #update mongodb and if not exists insert
            self.collection.update({'jobid': item['jobid']}, dict(item), True)
            # logging.log(logging.DEBUG, "insert job %s into MongoDB", item['jobid'])

        return item