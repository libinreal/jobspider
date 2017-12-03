# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class JobPipeline(object):
	def __init__(self):
		mongoConnection = pymongo.Connection(
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']
        )
        db = mongoConnection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.ids = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids:  
            raise DropItem("Duplicate item found: (id)%s" % item['id'])  
        else: 
        	self.collection.insert(dict(item))
        	log.msg("Lagou Job added to MongoDB",
                level=log.DEBUG, spider=spider)
        return item
